from exts import db
from datetime import datetime
from sqlalchemy import text


# 板块模型
class BoardModel(db.Model):
    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.create_time = kwargs.get('create_time')
        self.is_active = kwargs.get('is_active')

    __tablename__ = 'board'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    is_active = db.Column(db.Boolean, default=True)


# 帖子模型
class PostModel(db.Model):
    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.title = kwargs.get('title')
        self.content = kwargs.get('content')
        self.create_time = kwargs.get('create_time')
        self.read_count = kwargs.get('read_count')
        self.is_active = kwargs.get('is_active')
        self.board_id = kwargs.get('board_id')
        self.author_id = kwargs.get('author_id')

    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    read_count = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    board_id = db.Column(db.Integer, db.ForeignKey("board.id"))
    author_id = db.Column(db.String(100), db.ForeignKey("user.id"), nullable=False)

    board = db.relationship("BoardModel", backref="posts")
    author = db.relationship("UserModel", backref='posts')



# 评论模型
class CommentModel(db.Model):
    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.content = kwargs.get('content')
        self.create_time = kwargs.get('create_time')
        self.post_id = kwargs.get('post_id')
        self.author_id = kwargs.get('author_id')
        self.is_active = kwargs.get('is_active')

    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    author_id = db.Column(db.String(100), db.ForeignKey("user.id"), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    post = db.relationship("PostModel", backref=db.backref('comments', order_by=create_time.desc(), lazy="dynamic"))
    author = db.relationship("UserModel", backref='comments')
