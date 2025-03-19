from exts import db
from datetime import datetime


class EmailCaptchaModel(db.Model):
    def __init__(self, *args, **kwargs):
        self.id = kwargs.get("id")  # 从 kwargs 中获取 id 参数
        self.email = kwargs.get("email")  # 从 kwargs 中获取 email 参数
        self.captcha = kwargs.get("captcha")
        self.used = kwargs.get("used")

    __tablename__ = "email_captcha"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    captcha = db.Column(db.String(100), nullable=False)
    used = db.Column(db.Boolean, default=False)  # 使用后就将验证码删掉
