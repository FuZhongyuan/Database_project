from MySQLdb import IntegrityError
from flask import Blueprint, g, redirect, render_template, request, flash, url_for
from flask_wtf import csrf

from models.user import PermissionEnum
from models.user import UserModel, RoleModel
from models.post import PostModel, CommentModel, BoardModel
from forms.cms import AddStaffForm, EditStaffForm, EditBoardForm, PublicBoardNameForm
from exts import db
from decorators import permission_required
from utils import restful

bp = Blueprint("cms", __name__, url_prefix="/cms")


@bp.before_request
def cms_before_request():
    if not hasattr(g, "user") or g.user.is_staff == False:
        return redirect("/")


@bp.context_processor
def cms_context_processor():
    return {"PermissionEnum": PermissionEnum}


@bp.get("")
def index():
    return render_template("cms/index.html")


@bp.get("/staff/list")
@permission_required(PermissionEnum.CMS_USER)
def staff_list():
    users = UserModel.query.filter_by(is_staff=True).all()
    return render_template("cms/staff_list.html", users=users)


@bp.route("/staff/add", methods=['GET', 'POST'])
@permission_required(PermissionEnum.CMS_USER)
def add_staff():
    if request.method == "GET":
        roles = RoleModel.query.all()
        return render_template("cms/add_staff.html", roles=roles)
    else:
        form = AddStaffForm(request.form)
        if form.validate():
            email = form.email.data
            role_id = form.role.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                flash("没有此用户！")
                return redirect(url_for("cms.add_staff"))
            user.is_staff = True
            user.role = RoleModel.query.get(role_id)
            db.session.commit()
            return redirect(url_for("cms.add_staff"))
            # """跳转没实现"""
            # return redirect(url_for("cms.staff_list"))


@bp.route("/board/add_board", methods=['GET', 'POST'])
@permission_required(PermissionEnum.CMS_USER)
def add_board():
    #  TODO:要新建板块
    if request.method == "GET":
        # roles = RoleModel.query.all()
        return render_template("cms/edit_board.html")
    else:
        # 处理表单提交的数据
        # category_name = request.form['category_name']
        # 这里可以根据表单提交的数据执行相应的操作，比如保存到数据库中
        form = PublicBoardNameForm(request.form)
        if form.validate():
            BoardName = form.BoardName.data
            curr_board = BoardModel.query.filter_by(name=BoardName).first()
            if curr_board:
                flash('不能输入同一个板块名', 'error')
                print("不能输入同一个板块名")
                return redirect(url_for('cms.add_board'))
            board = BoardModel(name=BoardName)
            db.session.add(board)
            db.session.commit()
            boards = BoardModel.query.all()
            return redirect(url_for('cms.add_board'))
            # return render_template("cms/boards.html", boards=boards)
            # return redirect(url_for("cms.board_list"))  # 假设 '/board_list' 是 'cms.board_list' 的 URL
        # return redirect(url_for('cms.board_list'))
        # return redirect(url_for('cms.board_list'))
        """跳转没实现"""
        # return redirect(url_for("cms.board_list"))  # 假设 '/board_list' 是 'cms.board_list' 的 URL


@bp.get("/boards")
@permission_required(PermissionEnum.BOARD)
def board_list():
    boards = BoardModel.query.all()
    return render_template("cms/boards.html", boards=boards)


@bp.route("/staff/update", methods=['POST'])
@permission_required(PermissionEnum.CMS_USER)
def update_staff():
    pass


@bp.route("/staff/edit/<string:user_id>", methods=['GET', 'POST'])
@permission_required(PermissionEnum.CMS_USER)
def edit_staff(user_id):
    user = UserModel.query.get(user_id)
    if request.method == 'GET':
        roles = RoleModel.query.all()
        return render_template("cms/edit_staff.html", this_user_id=user_id, user=user, roles=roles)
    else:
        form = EditStaffForm(request.form)
        if form.validate():
            is_staff = form.is_staff.data
            role_id = form.role.data

            user.is_staff = is_staff
            if user.role.id != role_id:
                user.role = RoleModel.query.get(role_id)
            db.session.commit()
            return redirect(url_for("cms.edit_staff", user_id=user_id))
        else:
            for message in form.messages:
                flash(message)
            return redirect(url_for("cms.edit_staff", user_id=user_id))


@bp.route("/staff/edit1/<string:user_id>", methods=['POST'])
@permission_required(PermissionEnum.CMS_USER)
def edit_staff1(user_id):
    # user = UserModel.query.get(user_id)
    # form = EditStaffForm(request.form)
    # if form.validate():
    #     is_staff = form.is_staff.data
    #     role_id = form.role.data
    #
    #     user.is_staff = is_staff
    #     if user.role.id != role_id:
    #         user.role = RoleModel.query.get(role_id)
    #     db.session.commit()
    #     return redirect(url_for("cms.edit_staff", user_id=user_id))
    # else:
    #     for message in form.messages:
    #         flash(message)
    #     return redirect(url_for("cms.edit_staff", user_id=user_id))

    role_id = request.form.get("role_id", type=int)
    my_user = request.form.get("user_id", type=int)
    if role_id == None:
        return restful.params_error(message="请传入role_id参数！")
    user = UserModel.query.filter_by(id=user_id).first()

    if user is None:
        return restful.params_error(message="未找到对应的用户！")

    user.role_id = role_id
    db.session.commit()
    return restful.ok()


@bp.route("/staff/edit2/<string:user_id>", methods=['POST'])
@permission_required(PermissionEnum.CMS_USER)
def edit_staff2(user_id):
    is_staff = request.form.get("isstaff", type=int)
    my_user = request.form.get("user_id", type=int)
    if is_staff == None:
        return restful.params_error(message="请传入role_id参数！")
    user = UserModel.query.filter_by(id=user_id).first()

    if user is None:
        return restful.params_error(message="未找到对应的用户！")

    user.is_staff = is_staff
    user.role_id = None
    db.session.commit()
    return restful.ok()


@bp.route("/staff/add_role", methods=['POST'])
@permission_required(PermissionEnum.CMS_USER)
def add_role():
    inputEmail = request.form.get("inputEmail")
    role_id = request.form.get("role_id", type=int)
    if inputEmail == None:
        return restful.params_error(message="请传入inputEmail参数！")
    user = UserModel.query.filter_by(email=inputEmail).first()

    if user is None:
        return restful.params_error(message="未找到对应的用户！")

    user.role_id = role_id
    user.is_staff = 1
    db.session.commit()
    return restful.ok()


@bp.route("/users")
@permission_required(PermissionEnum.FRONT_USER)
def user_list():
    users = UserModel.query.filter_by(is_staff=False).all()  # 不显示员工
    return render_template("cms/users.html", users=users)


@bp.post("/users/active/<string:user_id>")
@permission_required(PermissionEnum.FRONT_USER)
def active_user(user_id):
    is_active = request.form.get("is_active", type=int)
    if is_active == None:
        return restful.params_error(message="请传入is_active参数！")
    user = UserModel.query.get(user_id)
    user.is_active = bool(is_active)
    db.session.commit()
    return restful.ok()


@bp.get('/posts')
@permission_required(PermissionEnum.POST)
def post_list():
    posts = PostModel.query.all()
    return render_template("cms/posts.html", posts=posts)


@bp.post('/posts/active/<int:post_id>')
@permission_required(PermissionEnum.POST)
def active_post(post_id):
    is_active = request.form.get("is_active", type=int)
    if is_active == None:
        return restful.params_error(message="请传入is_active参数！")
    post = PostModel.query.get(post_id)
    post.is_active = bool(is_active)
    db.session.commit()
    return restful.ok()


@bp.get('/comments')
@permission_required(PermissionEnum.COMMENT)
def comment_list():
    comments = CommentModel.query.all()
    return render_template("cms/comments.html", comments=comments)


@bp.post('/comments/active/<int:comment_id>')
@permission_required(PermissionEnum.COMMENT)
def active_comment(comment_id):
    is_active = request.form.get("is_active", type=int)
    if is_active == None:
        return restful.params_error(message="请传入is_active参数！")
    comment = CommentModel.query.get(comment_id)
    comment.is_active = bool(is_active)
    db.session.commit()
    return restful.ok()


# 这个实现的是删除板块
@bp.post('/board/delete/<int:board_id>')
@permission_required(PermissionEnum.CMS_USER)
def withdraw_board(board_id):
    try:
        # 查询模块
        board = BoardModel.query.filter_by(id=board_id).first()  # post返回值为course_id主键查询的帖子
        if board is None:
            raise Exception('Course not found.')
        # 删除关联的帖子记录
        enrollments = PostModel.query.filter_by(board_id=board_id).all()

        for enrollment in enrollments:
            # 删除相关的评论
            comments = CommentModel.query.filter_by(post_id=enrollment.id).all()
            for comment in comments:
                db.session.delete(comment)
            db.session.delete(enrollment)

        # 删除模块
        db.session.delete(board)
        # 提交事务
        db.session.commit()
        return restful.ok()
    except Exception as e:
        # 出现异常时回滚事务
        db.session.rollback()
        return 'Course withdrawal failed: ' + str(e)


# @bp.post('/board/delete/<int:board_id>')
# @permission_required(PermissionEnum.CMS_USER)
# def withdraw_board(board_id):
#     try:
#         with db.session.begin():
#             # 查询模块
#             board = BoardModel.query.filter_by(id=board_id).first()
#             if board is None:
#                 raise Exception('Board not found.')
#
#             # 删除关联的帖子记录
#             PostModel.query.filter_by(board_id=board_id).delete()
#
#             # 删除模块
#             db.session.delete(board)
#
#             return restful.ok()
#
#     except IntegrityError as e:
#         db.session.rollback()
#         return 'Course withdrawal failed: ' + str(e)
#     except Exception as e:
#         db.session.rollback()
#         return 'Course withdrawal failed: ' + str(e)


# @bp.post('/board/delete/<int:board_id>')
# @permission_required(PermissionEnum.CMS_USER)
# def withdraw_course(board_id):
#     try:
#         my_board_id = request.form.get("board_id", type=int)
#         # 开启事务
#         db.session.begin()
#
#         # 查询帖子
#         post = PostModel.query.get(my_board_id)  # post返回值为course_id主键查询的帖子
#         if post is None:
#             raise Exception('Post not found.')
#
#         # 删除关联的评论记录
#         CommentModel.query.filter_by(post_id=my_board_id).delete()
#
#         # 删除帖子
#         db.session.delete(post)
#
#         # 提交事务
#         db.session.commit()
#
#         return restful.ok()
#     except Exception as e:
#         # 出现异常时回滚事务
#         db.session.rollback()
#         return 'Post deletion failed: ' + str(e)


@bp.post("/boards/edit")
@permission_required(PermissionEnum.BOARD)
def edit_board():
    form = EditBoardForm(request.form)
    if form.validate():
        board_id = form.board_id.data
        name = form.name.data
        board = BoardModel.query.get(board_id)
        board.name = name
        db.session.commit()
        return restful.ok()
    else:
        return restful.params_error(form.messages[0])


@bp.route("/post/change/<int:post_id>", methods=['GET', 'POST'])
@permission_required(PermissionEnum.CMS_USER)
def post_change(post_id):
    post = PostModel.query.get(post_id)
    board = BoardModel.query.get(post.board_id)
    if request.method == 'GET':
        boardModels = BoardModel.query.all()
        return render_template("cms/change_post.html", post=post, board=board, board_name=board.name)
    else:
        return render_template("cms/change_post.html", post=post, board=board, board_name=board.name)


# 这个函数调用存储过程更改板块的名字
@bp.route("/post/change_post_belong", methods=['GET', 'POST'])
@permission_required(PermissionEnum.CMS_USER)
def change_post_belong():
    try:
        original_name = request.form['original_board_name']
        new_name = request.form['new_name']
        reason = request.form.get('reason')
        contact = request.form.get('contact')

        # 调用存储过程来更新板块名称
        # 定义一个SQL调用语句，用于执行一个名为`update_board_name`的存储过程
        # 这个存储过程预计接受四个参数：原始名称(original_name)，新名称(new_name)，更改原因(reason)以及联系方式(contact)
        update_procedure = "CALL update_post_belong(:original_name, :new_name, :reason, :contact)"

        # 使用Flask-SQLAlchemy的db.session.execute()方法来执行上述定义的存储过程
        # 这个方法接受一个SQL语句和一个参数字典
        # 在这个字典中，关键字参数与存储过程中的参数相对应
        db.session.execute(
            update_procedure,  # 执行的SQL调用语句
            {
                'original_name': original_name,  # 存储过程的第一个参数，原始名称
                'new_name': new_name,  # 存储过程的第二个参数，新名称
                'reason': reason,  # 存储过程的第三个参数，更改原因
                'contact': contact  # 存储过程的第四个参数，联系方式
            }
        )

        # 调用db.session.commit()来提交当前会话中的所有更改到数据库
        # 这是必须的步骤，以确保存储过程的执行结果被正式保存到数据库中
        db.session.commit()

        postModels = PostModel.query.all()
        return render_template("cms/posts.html", posts=postModels)
    except Exception as e:
        # 出现异常时回滚事务
        db.session.rollback()
        flash('新板块名称不存在', 'error')
        print('Course withdrawal failed: ' + str(e))
        postModels = PostModel.query.all()
        return render_template("cms/posts.html", posts=postModels)


@bp.route("/boards/change_name/<int:board_id>", methods=['GET', 'POST'])
@permission_required(PermissionEnum.CMS_USER)
def board_change(board_id):
    board = BoardModel.query.get(board_id)
    if request.method == 'GET':
        boardModels = BoardModel.query.all()
        return render_template("cms/change_boards_name.html", board_id=board_id, board=board, board_name=board.name)
    else:
        return render_template("cms/change_boards_name.html", board_id=board_id, board=board, board_name=board.name)


# 这个函数调用存储过程更改板块的名字
@bp.route("/boards/change_board_name", methods=['GET', 'POST'])
@permission_required(PermissionEnum.CMS_USER)
def change_board_name():
    try:
        new_id = request.form.get("new_board_id")
        original_id = request.form.get("origin_board_id")
        original_name = request.form['original_name']
        new_name = request.form['new_name']
        reason = request.form.get('reason')
        contact = request.form.get('contact')

        # 调用存储过程来更新板块名称
        # 定义一个SQL调用语句，用于执行一个名为`update_board_name`的存储过程
        # 这个存储过程预计接受四个参数：原始名称(original_name)，新名称(new_name)，更改原因(reason)以及联系方式(contact)
        update_procedure = "CALL update_board_name(:original_name, :new_name, :reason, :contact)"

        # 使用Flask-SQLAlchemy的db.session.execute()方法来执行上述定义的存储过程
        # 这个方法接受一个SQL语句和一个参数字典
        # 在这个字典中，关键字参数与存储过程中的参数相对应
        db.session.execute(
            update_procedure,  # 执行的SQL调用语句
            {
                'original_name': original_name,  # 存储过程的第一个参数，原始名称
                'new_name': new_name,  # 存储过程的第二个参数，新名称
                'reason': reason,  # 存储过程的第三个参数，更改原因
                'contact': contact  # 存储过程的第四个参数，联系方式
            }
        )

        # 存储过程调用语句
        update_procedure = "CALL update_board_id(:original_id, :new_id, :reason, :contact)"

        # 执行存储过程的参数字典
        params = {
            'original_id': original_id,  # 存储过程的第一个参数，原始板块ID
            'new_id': new_id,  # 存储过程的第二个参数，新板块ID
            'reason': reason,  # 存储过程的第三个参数，更改原因
            'contact': contact  # 存储过程的第四个参数，联系方式
        }

        # 使用Flask-SQLAlchemy的db.session.execute()方法来执行存储过程
        db.session.execute(
            update_procedure,  # 执行的SQL调用语句
            params  # 参数字典
        )

        # 调用db.session.commit()来提交当前会话中的所有更改到数据库
        # 这是必须的步骤，以确保存储过程的执行结果被正式保存到数据库中
        db.session.commit()

        boardModels = BoardModel.query.all()
        return render_template("cms/boards.html", boards=boardModels)
    except Exception as e:
        # 出现异常时回滚事务
        db.session.rollback()
        flash('新名称长度必须大于2个字符，而且ID值必须在0到9999之间，且新板块ID不能与其他板块ID冲突', 'error')
        print('Course withdrawal failed: ' + str(e))
        boardModels = BoardModel.query.all()
        return render_template("cms/boards.html", boards=boardModels)


@bp.delete("/boards/active/<int:board_id>")
@permission_required(PermissionEnum.BOARD)
def active_board(board_id):
    try:
        is_active = request.form.get("is_active", int)
        if is_active == None:
            return restful.params_error("请传入is_active参数！")
        board = BoardModel.query.get(board_id)
        board.is_active = bool(is_active)
        db.session.commit()
        return restful.ok()
    except Exception as e:
        # 出现异常时回滚事务
        db.session.rollback()
        return 'Course withdrawal failed: ' + str(e)
