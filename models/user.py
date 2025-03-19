from exts import db
from datetime import datetime
from shortuuid import uuid
from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash


class PermissionEnum(Enum):
    BOARD = "板块"
    POST = "帖子"
    COMMENT = "评论"
    FRONT_USER = "前台用户"
    CMS_USER = "后台用户"


class PermissionModel(db.Model):
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name')
        self.id = kwargs.get('id')

    __tablename__ = "permission"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Enum(PermissionEnum), nullable=False, unique=True)


"""
用于实现多对多（Many-to-Many）关系。在这个例子中，role_permission_table是一个关联表，用于描述角色和权限之间的多对多关系。
"""
role_permission_table = db.Table(
    "role_permission_table",
    db.Column("role_id", db.Integer, db.ForeignKey("role.id")),
    db.Column("permission_id", db.Integer, db.ForeignKey("permission.id"))
)


class RoleModel(db.Model):
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name')
        self.id = kwargs.get('id')
        self.desc = kwargs.get('desc')
        self.create_time = kwargs.get('create_time')

    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(200), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    permissions = db.relationship("PermissionModel", secondary=role_permission_table, backref="roles")


class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(100), primary_key=True, default=uuid)
    username = db.Column(db.String(50), nullable=False, unique=True)
    _password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    avatar = db.Column(db.String(500))
    signature = db.Column(db.String(100))
    join_time = db.Column(db.DateTime, default=datetime.now)
    is_staff = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)

    # 外键
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))
    role = db.relationship("RoleModel", backref="users")  # 关系，role可以赋值为RoleModel的实例

    def __init__(self, *args, **kwargs):
        self.username = kwargs.get('username')
        self.email = kwargs.get('email')
        self.avatar = kwargs.get('avatar')
        self.signature = kwargs.get('signature')
        self.join_time = kwargs.get('join_time')
        self.is_staff = kwargs.get('is_staff')
        self.is_active = kwargs.get('is_active')
        self.role_id = kwargs.get('role_id')
        self.id = kwargs.get('id')
        if "password" in kwargs:
            self.password = kwargs.get('password')
            kwargs.pop("password")
        super(UserModel, self).__init__(*args, **kwargs)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        result = check_password_hash(self.password, raw_password)
        return result

    def has_permission(self, permission):
        return permission in [permission.name for permission in self.role.permissions]
