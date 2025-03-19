from exts import db
from datetime import datetime
from datetime import datetime
from sqlalchemy import text
from exts import db
from datetime import datetime
from shortuuid import uuid
from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash

# 创建数据库视图
class UserPost(db.Model):
    __tablename__ = 'user_post_view'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    post_count = db.Column(db.Integer)


