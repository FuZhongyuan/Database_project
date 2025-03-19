from flask import Blueprint, render_template, request, current_app, redirect, url_for, flash, session, g, \
    render_template_string, jsonify
from exts import db, mail
from werkzeug.security import generate_password_hash, check_password_hash
import random
from utils import restful
from forms.user import RegisterForm, LoginForm, EditProfileForm
from models.user import UserModel
from models.post import *
from models.email import EmailCaptchaModel
from decorators import login_required
from werkzeug.datastructures import CombinedMultiDict
from werkzeug.utils import secure_filename
import os
import string
from flask_mail import Message

bp = Blueprint("user", __name__, url_prefix="/user") # 这个页面的URL需要使用/user索引


# @bp.route("/register", methods=['GET', 'POST'])
# def register():
#     if request.method == 'GET':
#         return render_template("front/register.html")
#     else:
#         form = RegisterForm(request.form)
#         if form.validate():
#             email = form.email.data
#             username = form.username.data
#             password = form.password.data
#             user = UserModel(email=email, username=username, password=password)
#             db.session.add(user)
#             db.session.commit()
#             return redirect(url_for("user.login"))
#         else:
#             for message in form.messages:
#                 flash(message)
#             return redirect(url_for("user.register"))


# GET:从服务器上获取数据
# POST：将客户端的数据提交给服务器
@bp.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'GET':
        # 如果是 GET 请求，返回注册页面模板
        # return render_template("register.html")
        return render_template("front/register.html", form=form)
    elif request.method == 'POST':
        # 验证用户提交的邮箱和验证码是否对应且正确
        # #表单验证:flask-wtf: wtforms
        form = RegisterForm(request.form)  # 自动验证
        if form.validate():  # 自动调用RegisterForm类中的验证器
            # 如果表单验证通过，获取表单中用户输入的邮箱、用户名和密码
            email = form.email.data
            username = form.username.data
            password = form.password.data
            # 创建一个新用户对象，并将用户输入的信息存储到数据库中
            user = UserModel(email=email, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            # 注册成功后重定向用户到登录页面
            return redirect(url_for("user.login"))
        else:
            # 如果表单验证不通过，打印表单验证错误信息到控制台，并重定向用户回到注册页面
            print(form.errors)
            # return redirect(url_for("auth.register"))
            return render_template_string('''
        <script>
            alert('请重新输入');
            window.location.href = "{{ url_for('user.register') }}";
        </script>
    ''')


@bp.route("/captcha/email")
def mail_captcha():
    try:
        # /captcha/email/<email>
        # /captcha/email?email=xxx@qq.com
        email = request.args.get("email")  # 得到目标邮件的地址
        # 4/6: 随机数组、宁母、数组和字母的组合
        source = string.digits * 6
        captcha = random.sample(source, 6)
        # print(captcha)
        captcha = "".join(captcha)
        message_body = f"【南开大学校园集市论坛】您的验证码是{captcha}，请勿告诉别人！"
        message = Message(subject="南开大学校园集市论坛验证码", recipients=[email], body=message_body)
        mail.send(message)
        # memcached/redis
        # 用数据库表的方式存储
        email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
        db.session.add(email_captcha)
        db.session.commit()
        # RESTful API->code": 200表示相应正常
        return jsonify({"code": 200, "message": "", "data": None})
    except Exception as e:
        print(e)
        return restful.server_error()


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("front/login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = UserModel.query.filter_by(email=email).first()
            a = user.check_password(password)
            if user and user.check_password(password):
                if not user.is_active:
                    flash("该用户已被禁用！")
                    return redirect(url_for("user.login"))
                session['user_id'] = user.id
                if remember:
                    session.permanent = True
                return redirect("/")
            else:
                flash("邮箱或者密码错误！")
                return redirect(url_for("user.login"))
        else:
            for message in form.messages:
                flash(message)
            return render_template("front/login.html")


# # 如果没有指定methods参数，默认就是get请求
# @bp.route("/login", methods=['GET', 'POST'])
# def login():
#     if request.method == 'GET':
#         return render_template("front/login.html")
#     else:
#         form = LoginForm(request.form)
#         if form.validate():
#             email = form.email.data
#             password = form.password.data
#             user = UserModel.query.filter_by(email=email).first()
#             if not user:
#                 print("邮箱在数据库中不存在")
#                 return redirect(url_for("user.login"))
#             if check_password_hash(user.password, password):
#                 # cookie:一般用来存放登录和授权你的东西
#                 # flask中的session是通过加密以后存放在cookie中的
#                 session['user_id'] = user.id
#                 # 这行代码在登录成功之后会被放在cookie中，在以后访问其他页面的时候会被交给其他页面用来快速登录
#                 return redirect("/")
#             else:
#                 print("密码错误")
#                 return redirect(url_for("user.login"))
#         else:
#             print(form.errors)
#             return

@bp.get('/logout')
def logout():
    session.clear()
    return redirect("/")


@bp.get("/profile/<string:user_id>")
def profile(user_id):
    user = UserModel.query.get(user_id)
    is_mine = False
    if hasattr(g, "user") and g.user.id == user_id:
        is_mine = True
    context = {
        "user": user,
        "is_mine": is_mine
    }
    print(user)
    return render_template("front/profile.html", **context)


@bp.post("/profile/edit")
@login_required
def edit_profile():
    form = EditProfileForm(CombinedMultiDict([request.form, request.files]))
    if form.validate():
        username = form.username.data
        avatar = form.avatar.data
        signature = form.signature.data

        # 如果上传了头像
        if avatar.startswith("http"):
            g.user.avatar = avatar
        elif avatar.startswith("上传头像链接"):
            pass
        elif avatar:
            # 生成安全的文件名
            filename = secure_filename(avatar.filename)
            # 拼接头像存储路径
            avatar_path = os.path.join(current_app.config.get("AVATARS_SAVE_PATH"), filename)
            # 保存文件
            avatar.save(avatar_path)
            # 设置头像的url
            g.user.avatar = url_for("media.media_file", filename=os.path.join("avatars", filename))
        # g.user.avatar = avatar
        g.user.username = username
        g.user.signature = signature
        db.session.commit()
        return redirect(url_for("user.profile", user_id=g.user.id))
    else:
        for message in form.messages:
            flash(message)
        return redirect(url_for("user.profile", user_id=g.user.id))


@bp.route("/mail/test")
def mail_test():
    message = Message(subject="邮箱测试", recipients=["1504411960@qq.com"], body="这是一条测试邮件")
    mail.send(message)
    return "邮件发送成功"


@bp.post('/logoff')
def logoff():
    session_data = dict(session)
    user_id = session['user_id']
    this_user = UserModel.query.filter_by(id=user_id).first()

    try:
        # 查询帖子
        posts = PostModel.query.filter_by(author=this_user).all()  # post返回值为course_id主键查询的帖子
        # print(post.id)
        if posts is None:
            raise Exception('Course not found.')
        # # 删除关联的帖子记录
        # enrollments = PostModel.query.filter_by(board_id=this_user).all()

        for post in posts:
            db.session.delete(post)
            # 删除关联的帖子记录
            enrollments = CommentModel.query.filter_by(post_id=post.id).all()
            for enrollment in enrollments:
                db.session.delete(enrollment)
        committes = CommentModel.query.filter_by(author_id=user_id).all()
        for committe in committes:
            db.session.delete(committe)

        # 删除自己
        db.session.delete(this_user)

        # # 删除模块
        # db.session.delete(board)
        # 提交事务
        db.session.commit()
        session.clear()
        return restful.ok()
    except Exception as e:
        # 出现异常时回滚事务
        db.session.rollback()
        return 'Course withdrawal failed: ' + str(e)

