from flask import Blueprint, request, render_template, jsonify, current_app, url_for, send_from_directory, g, abort, \
    redirect, flash
from werkzeug.utils import secure_filename
import os
from models.post import PostModel, BoardModel, CommentModel
from exts import csrf, db
from decorators import login_required
from forms.post import PublicPostForm, PublicCommentForm
from utils import restful
from flask_paginate import Pagination
from sqlalchemy import text

bp = Blueprint("front", __name__, url_prefix="")


@bp.route("/")
def index():
    boards = BoardModel.query.filter_by(is_active=True).all()

    # 获取页码参数
    page = request.args.get("page", type=int, default=1)
    # 获取板块参数
    board_id = request.args.get("board_id", type=int, default=0)

    # 当前page下的起始位置
    start = (page - 1) * current_app.config.get("PER_PAGE_COUNT")
    # 当前page下的结束位置
    end = start + current_app.config.get("PER_PAGE_COUNT")

    # 查询对象
    query_obj = PostModel.query.filter_by(is_active=True).order_by(PostModel.create_time.desc())
    # 过滤帖子
    if board_id:
        query_obj = query_obj.filter_by(board_id=board_id)
    # 总共有多少帖子
    total = query_obj.count()

    # 当前page下的帖子列表
    posts = query_obj.slice(start, end)

    # 分页对象
    pagination = Pagination(bs_version=4, page=page, total=total, outer_window=0, inner_window=2, alignment="center")

    context = {
        "posts": posts,
        "boards": boards,
        "pagination": pagination,
        "current_board": board_id
    }
    current_app.logger.info("index页面被请求了")
    return render_template("front/index.html", **context)


@bp.route("/post/public", methods=['GET', 'POST'])
@login_required
def public_post():
    if request.method == 'GET':
        boards = BoardModel.query.all()
        return render_template("front/public_post.html", boards=boards)
    else:
        form = PublicPostForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            # author_id = form.author_id.data
            post = PostModel(title=title, content=content, board_id=board_id, author=g.user, author_id=g.user.id)
            db.session.add(post)
            db.session.commit()
            return restful.ok()
        else:
            message = form.messages[0]
            return restful.params_error(message=message)


@bp.route('/image/<path:filename>')
def uploaded_image(filename):
    path = current_app.config.get("UPLOAD_IMAGE_PATH")
    return send_from_directory(path, filename)


@bp.post("/upload/image")
@csrf.exempt
@login_required
def upload_image():
    f = request.files.get('image')
    extension = f.filename.split('.')[-1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return jsonify({
            "errno": 400,
            "data": []
        })
    filename = secure_filename(f.filename)
    f.save(os.path.join(current_app.config.get("UPLOAD_IMAGE_PATH"), filename))
    url = url_for('front.uploaded_image', filename=filename)
    return jsonify({
        "errno": 0,
        "data": [{
            "url": url,
            "alt": "",
            "href": ""
        }]
    })


@bp.get("/post/detail/<int:post_id>")
def post_detail(post_id):
    post = PostModel.query.get(post_id)
    if not post.is_active:
        return abort(404)
    post.read_count += 1
    db.session.commit()
    return render_template("front/post_detail.html", post=post)


# @bp.post("/post/<int:post_id>/comment")
# @login_required
# def public_comment(post_id):
#     form = PublicCommentForm(request.form)
#     if form.validate():
#         content = form.content.data
#         comment = CommentModel(content=content, post_id=post_id, author=g.user, author_id=g.user.id)
#         db.session.add(comment)
#         db.session.commit()
#     else:
#         for message in form.messages:
#             flash(message)
#
#     return redirect(url_for("front.post_detail", post_id=post_id))


def check_comment_length(func):
    def wrapper(comment):
        if len(comment) < 2 or len(comment) > 200:
            raise ValueError("评论长度必须在2到200个字符之间")
        return func(comment)

    return wrapper



def create_trigger():
    # 检查触发器是否已经存在
    trigger_query = "SHOW TRIGGERS LIKE 'before_insert_comment'"
    # with db.engine.connect() as connection:
    result = db.session.execute(text(trigger_query))
    result = db.session.execute("SHOW TRIGGERS LIKE 'before_insert_comment'")
    existing_trigger = result.fetchone()

    # 如果触发器不存在，则创建触发器
    if not existing_trigger:
        # 创建触发器的 SQL 语句
        create_trigger_query = '''
            CREATE TRIGGER before_insert_comment
            BEFORE INSERT ON comment
            FOR EACH ROW
            BEGIN
                DECLARE comment_length INT;
                SET comment_length = CHAR_LENGTH(NEW.content);

                IF comment_length < 2 OR comment_length > 200 THEN
                    SIGNAL SQLSTATE '45000'
                    SET MESSAGE_TEXT = '评论长度必须在2到200个字符之间';
                END IF;
            END;
        '''

        # 执行创建触发器的 SQL 语句
        # with db.engine.connect() as connection:
        db.session.execute(text(create_trigger_query))

        print("触发器创建成功！")
    else:
        print("触发器已经存在，无需重复创建。")

@login_required
@bp.post("/post/<int:post_id>/comment")
def public_comment(post_id):
    try:
        form = PublicCommentForm(request.form)
        # if form.validate():
        content = form.content.data
        new_comment = CommentModel(content=content, post_id=post_id, author=g.user, author_id=g.user.id)
        db.session.add(new_comment)
        # 在评论添加到数据库之前创建触发器
        # create_trigger()
        db.session.commit()
        print("评论已添加：", post_id)
        flash("评论已添加")
        return redirect(url_for("front.post_detail", post_id=post_id))
    except Exception as e:
        print("添加评论失败：", e)
        flash("添加评论失败，请输入2-200字符")
        return redirect(url_for("front.post_detail", post_id=post_id))

# @bp.post("/post/<int:post_id>/comment")
# @login_required
# def public_comment(post_id):
#     form = PublicCommentForm(request.form)
#     if form.validate():
#         content = form.content.data
#         comment = CommentModel(content=content, post_id=post_id, author=g.user, author_id=g.user.id)
#         db.session.add(comment)
#         db.session.commit()
#     else:
#         for message in form.messages:
#             flash(message)
#
#     return redirect(url_for("front.post_detail", post_id=post_id))


@bp.route("/search")
def search():
    # /search?q=flask
    # /search/<q>
    # post，request.form
    q = request.args.get("q")
    # posts = PostModel.query.filter(PostModel.title.contains(q)).all()
    boards = BoardModel.query.filter_by(is_active=True).all()

    # 获取页码参数
    page = request.args.get("page", type=int, default=1)
    # 获取板块参数
    board_id = request.args.get("board_id", type=int, default=0)

    # 当前page下的起始位置
    start = (page - 1) * current_app.config.get("PER_PAGE_COUNT")
    # 当前page下的结束位置
    end = start + current_app.config.get("PER_PAGE_COUNT")

    # 查询对象
    # query_obj = PostModel.query.filter_by(is_active=True).order_by(PostModel.create_time.desc())
    posts = PostModel.query.filter(PostModel.title.contains(q)).order_by(PostModel.create_time.desc())
    # 过滤帖子
    if board_id:
        # posts = posts.filter_by(board_id=board_id)
        posts = posts.filter_by(board_id=board_id)
    # 总共有多少帖子
    total = posts.count()

    # 当前page下的帖子列表
    posts = posts.slice(start, end)

    # 分页对象
    pagination = Pagination(bs_version=4, page=page, total=total, outer_window=0, inner_window=2, alignment="center")

    context = {
        "posts": posts,
        "boards": boards,
        "pagination": pagination,
        "current_board": board_id
    }
    current_app.logger.info("index页面被请求了")
    return render_template("front/index.html", **context)


@bp.get("/laws")
def laws():
    return render_template("front/laws.html")

# @bp.get('/user_comments_view')
# def user_comments_view():
#     # 执行查询操作，获取view2的数据
#     query = text('SELECT * FROM user_comments_view')
#     result = db.session.execute(query)
#     view2_data = result.fetchall()
#     # 渲染admin.html视图，并将查询结果传递给模板
#     return render_template('view/user_comments_view.html', view2_data=view2_data)
