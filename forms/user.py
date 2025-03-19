import wtforms  # 导入 wtforms 库
from wtforms import StringField, ValidationError, BooleanField, FileField
from wtforms.validators import Email, EqualTo, Length, InputRequired
from flask_wtf.file import FileAllowed
from exts import cache
from models.user import UserModel
from models.email import EmailCaptchaModel
from .baseform import BaseForm
from exts import db  # 导入数据库扩展对象


class RegisterForm(BaseForm):
    email = StringField(validators=[Email(message="请输入正确格式的邮箱！")])
    captcha = StringField(validators=[Length(min=6, max=6, message="请输入正确格式的验证码！")])
    username = StringField(validators=[Length(min=2, max=20, message="请输入正确长度的用户名！")])
    password = StringField(validators=[Length(min=6, max=20, message="请输入正确长度的密码！")])
    confirm_password = StringField(validators=[EqualTo("password", message="两次密码不一致！")])

    # def validate_email(self, field):
    #     email = field.data
    #     user = UserModel.query.filter_by(email=email).first()
    #     if user:
    #         raise ValidationError(message="邮箱已经存在")

    # 自定义验证方法：检查邮箱是否已经被注册
    def validate_email(self, field):
        """检查邮箱是否已经被注册"""
        email = field.data
        # field.data可以获取用户输入的值
        user = UserModel.query.filter_by(email=email).first()  # 在数据库中查询是否已存在该邮箱
        # filter_by(email=email): 这是一个过滤器，它告诉数据库只选择那些邮箱与指定邮箱相匹配的用户。email是传入的参数，用于与数据库中的邮箱进行比较。
        # first(): 这是查询的一个方法，它告诉数据库只返回满足条件的第一个结果。如果没有符合条件的结果，它会返回 None。
        if user:
            raise wtforms.ValidationError(message="该邮箱已经被注册!")  # 若存在，抛出验证错误

    # def validate_captcha(self, field):
    #     captcha = field.data
    #     email = self.email.data
    #     cache_captcha = cache.get(email)
    #     if not cache_captcha or captcha != cache_captcha:
    #         raise ValidationError(message="验证码错误！")

    # 自定义验证方法：检查验证码是否正确
    def validate_captcha(self, field):
        """检查验证码是否正确"""
        captcha = field.data
        email = self.email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).first()  # 在数据库中查询验证码是否正确
        if not captcha_model:
            raise wtforms.ValidationError(message="邮箱或验证码错误!")  # 若验证码不正确，抛出验证错误
        else:
            # TODO: 可以删除 captcha_model，占用时间，可以写一个脚本定期删除
            db.session.delete(captcha_model)
            db.session.commit()


class LoginForm(BaseForm):
    email = StringField(validators=[Email(message="请输入正确格式的邮箱！")])
    password = StringField(validators=[Length(min=6, max=20, message="请输入正确长度的密码！")])
    remember = BooleanField()


class EditProfileForm(BaseForm):
    username = StringField(validators=[Length(min=2, max=20, message="请输入正确格式的用户名！")])
    avatar_root = FileField(validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], message="文件类型错误！")])
    avatar = StringField(validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], message="文件类型错误！")])
    signature = StringField()

    def validate_signature(self, field):
        signature = field.data
        if signature and len(signature) > 100:
            raise ValidationError(message="签名不能超过100个字符")
