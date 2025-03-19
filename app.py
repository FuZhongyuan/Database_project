import click
from flask import Flask
from exts import db, mail, cache, csrf, avatars
import config
from flask_migrate import Migrate
from blueprints.cms import bp as cms_bp
from blueprints.front import bp as front_bp
from blueprints.user import bp as user_bp
from blueprints.media import bp as media_bp
from blueprints.view import bp as view_bp
import commands
from bbs_celery import make_celery
import hooks
import filters
import logging
from models.post import *
from models.email import *
from models.user import *
import logging

app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)
db.init_app(app)
mail.init_app(app)
cache.init_app(app)
avatars.init_app(app)

# 设置日志级别
app.logger.setLevel(logging.INFO)

# CSRF保护
csrf.init_app(app)

migrate = Migrate(app, db)

# 注册蓝图
app.register_blueprint(cms_bp)
app.register_blueprint(front_bp)
app.register_blueprint(user_bp)
app.register_blueprint(media_bp)
app.register_blueprint(view_bp)

"""
这三行代码实现了数据库的创建和动态迁移
详见https://blog.csdn.net/weixin_44951273/article/details/98895759
"""

"""
用户发出请求后,先用一个对象存储用户的user_id，然后再去执行视图函数
flask db init:只需要执行一次
flask db migrate:将orm模型生成迁移脚本
flask db upgrade:将迁移脚本映射到数据库中
手动删除目录后可以再次执行，数据库中也要清空表格
"""

# 添加命令
app.cli.command("create-permission")(commands.create_permission)  # flask create-permission
app.cli.command("create-role")(commands.create_role)  # flask create-role
app.cli.command("create-test-front")(commands.create_test_user)
app.cli.command("create-board")(commands.create_board)
app.cli.command("create-test-post")(commands.create_test_post)  # 生成测试帖子
app.cli.command("create-admin")(commands.create_admin)  # flask create-admin -u admin -e 11111@qq.com -p 123456
"""
一共有两种创建表的方法，一种是调用python封装的函数add函数，还有一种就是直接运行sql语句
"""
app.cli.command("create-view")(commands.creat_view)
app.cli.command("create-trigger")(commands.creat_trigger)
app.cli.command("create-update-procedure")(commands.create_update_procedure)  # 创建存储过程
app.cli.command("create-post_belong-procedure")(commands.create_post_belong_procedure)  # 创建存储过程
app.cli.command("create-user")(commands.create_user)
app.cli.command("sql-create-user")(commands.sql_create_user)  # 直接使用sql语句也能插入，但是注意修改邮箱的值
app.cli.command("create-comment")(commands.create_comment)  # 插入随机评论
app.cli.command("create_update_boardID_procedure")(commands.create_update_boardID_procedure)

"""
create_admin参数有：
"--username", '-u'
"--email", '-e'
"--password", '-p'
"""

# 构建celery
celery = make_celery(app)

# 添加钩子函数
app.before_request(hooks.bbs_before_request)
app.errorhandler(401)(hooks.bbs_401_error)
app.errorhandler(404)(hooks.bbs_404_error)
app.errorhandler(500)(hooks.bbs_500_error)

# 添加模板过滤器
app.template_filter("email_hash")(filters.email_hash)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 在第一次运行时创建数据库表

    # app.debug = True
    # handler = logging.FileHandler('flask.log', encoding='UTF-8')
    # handler.setLevel(logging.DEBUG)  # 设置日志记录最低级别为DEBUG，低于DEBUG级别的日志记录会被忽略，不设置setLevel()则默认为NOTSET级别。
    # logging_format = logging.Formatter(
    #     '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    # handler.setFormatter(logging_format)
    # app.logger.addHandler(handler)
    app.run()
