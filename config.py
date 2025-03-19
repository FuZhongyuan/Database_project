from datetime import timedelta
import os


class BaseConfig:
    # 用于 Flask 应用程序的安全密钥。
    SECRET_KEY = "fzy"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 定义了 Flask 会话的持久化生命周期。timedelta(days=7) 表示会话将在用户浏览器中持续 7 天。
    # 这意味着如果用户在 7 天内没有与网站交互，他们的会话将过期。
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # 设置了用户上传图片的存储路径。
    UPLOAD_IMAGE_PATH = os.path.join(os.path.dirname(__file__), "media")

    # 用于分页功能，文章列表中，每次只加载一定数量的项目。
    PER_PAGE_COUNT = 10


class DevelopmentConfig(BaseConfig):
    # MySQL所在的主机名
    HOSTNAME = "localhost"
    # MySOL监听的端口号，默认3306
    PORT = 3306
    # 连MySQL的用户名，读者用自己设置的
    USERNAME = "root"
    # 连接MySQL的密码，用自己mysql的
    PASSWORD = "A20040903fzy"
    # MySQL上创建的数据库名称
    DATABASE = "hospital"
    # 生成密钥
    SECRET_KEY = "fzy"

    # mysql+mysqldb://root:A20040903fzy@localhost:3306/hospital?charset=utf8mb4
    DB_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
    SQLALCHEMY_DATABASE_URI = DB_URI

    # 邮箱配置信息
    MAIL_SERVER = "smtp.163.com"
    MAIL_USE_SSL = True
    MAIL_PORT = 465
    MAIL_USERNAME = "allenfzy2022@163.com"
    MAIL_PASSWORD = "HRAXTNTVGVDFMGVK"
    MAIL_DEFAULT_SENDER = "allenfzy2022@163.com"
    SECRET_KE = "fafadgrawewga"
    # 缓存配置
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "127.0.0.1"
    CACHE_REDIS_PORT = 6379

    # Celery配置
    # 格式：redis://:password@hostname:port/db_number
    CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
    CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"

    # 定义了一个路径，用于保存用户上传的头像图片。
    AVATARS_SAVE_PATH = os.path.join(BaseConfig.UPLOAD_IMAGE_PATH, "avatars")

    # 用于配置Flask - WTF扩展的CSRF（跨站请求伪造）保护功能，目前测试阶段暂时先关闭
    WTF_CSRF_ENABLED = False


class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://[测试服务器MySQL用户名]:[测试服务器MySQL密码]@[测试服务器MySQL域名]:[测试服务器MySQL端口号]/pythonbbs?charset=utf8mb4"


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://[生产环境服务器MySQL用户名]:[生产环境服务器MySQL密码]@[生产环境服务器MySQL域名]:[生产环境服务器MySQL端口号]/pythonbbs?charset=utf8mb4"
