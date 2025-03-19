from models.user import PermissionModel, RoleModel, PermissionEnum, UserModel
from models.post import BoardModel, PostModel, CommentModel
from models.email import *
from models.view import UserPost
import click
from exts import db
from faker import Faker
import random
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


# from werkzeug.security import generate_password_hash


def create_permission():
    for permission_name in dir(PermissionEnum):
        if permission_name.startswith("__"):
            continue
        permission = PermissionModel(name=getattr(PermissionEnum, permission_name))
        db.session.add(permission)
    db.session.commit()
    click.echo("权限添加成功！")


def create_role():
    # 稽查员
    inspector = RoleModel(name="稽查", desc="负责审核帖子和评论是否合法合规！")
    inspector.permissions = PermissionModel.query.filter(
        PermissionModel.name.in_([PermissionEnum.POST, PermissionEnum.COMMENT])).all()

    # 运营
    operator = RoleModel(name="运营", desc="负责网站持续正常运营！")
    operator.permissions = PermissionModel.query.filter(PermissionModel.name.in_([
        PermissionEnum.POST,
        PermissionEnum.COMMENT,
        PermissionEnum.BOARD,
        PermissionEnum.FRONT_USER
    ])).all()

    # 管理员
    administrator = RoleModel(name="管理员", desc="负责整个网站所有工作！")
    administrator.permissions = PermissionModel.query.all()

    db.session.add_all([inspector, operator, administrator])
    db.session.commit()
    click.echo("角色添加成功！")


def create_test_user():
    admin_role = RoleModel.query.filter_by(name="管理员").first()
    zhangsan = UserModel(username="张三", email="zhangsan@zlkt.net", password="111111", is_staff=True, role=admin_role)

    operator_role = RoleModel.query.filter_by(name="运营").first()
    lisi = UserModel(username="李四", email="lisi@zlkt.net", password="111111", is_staff=True, role=operator_role)

    inspector_role = RoleModel.query.filter_by(name="稽查").first()
    wangwu = UserModel(username="王五", email="wangwu@zlkt.net", password="111111", is_staff=True, role=inspector_role)

    inspector_role = None
    zhaoliu = UserModel(username="赵六", email="zhaoliu@zlkt.net", password="111111", is_staff=True,
                        role=inspector_role)

    inspector_role = None
    aaaa = UserModel(username="aaaa", email="aaaa@zlkt.net", password="111111", is_staff=False, role=inspector_role)

    inspector_role = None
    bbbb = UserModel(username="bbbb", email="bbbb@zlkt.net", password="111111", is_staff=False, role=inspector_role)

    db.session.add_all([zhangsan, lisi, wangwu, zhaoliu, aaaa, bbbb])
    db.session.commit()
    click.echo("测试用户添加成功！")


@click.option("--username", '-u')
@click.option("--email", '-e')
@click.option("--password", '-p')
def create_admin(username, email, password):
    admin_role = RoleModel.query.filter_by(name="管理员").first()
    admin_user = UserModel(username=username, email=email, password=password, is_staff=True, role=admin_role)
    db.session.add(admin_user)
    db.session.commit()
    click.echo("管理员创建成功！")


def create_board():
    board_names = ['打听求助', '二手限制', '恋爱交友', '兼职招聘', '校园招聘']
    for board_name in board_names:
        board = BoardModel(name=board_name)
        db.session.add(board)
    db.session.commit()
    click.echo("板块添加成功！")


def create_test_post():
    fake = Faker(locale="zh_CN")
    author = UserModel.query.first()
    boards = BoardModel.query.all()
    # post = PostModel(title=title, content=content, board_id=board_id, author=g.user, author_id=g.user.id)
    click.echo("开始生成测试帖子...")
    for x in range(109):
        title = fake.sentence()
        content = fake.paragraph(nb_sentences=10)
        random_index = random.randint(0, 31)
        board_id = boards[random_index].id
        post = PostModel(title=title, content=content, author=author, author_id=author.id,
                         board_id=board_id)
        db.session.add(post)
    db.session.commit()
    click.echo("测试帖子生成成功！")


# 创建视图
def creat_view():
    db.session.execute('''
            CREATE VIEW User_Comments_View AS
            SELECT u.username AS username,
                   u.id AS user_id,
                   c.id AS comment_id,
                   c.content AS content,
                   c.create_time AS create_time,
                   c.post_id AS post_id
            FROM User u JOIN comment c ON u.id = c.author_id
            # GROUP BY u.id;
        ''')
    db.session.commit()
    click.echo("视图生成成功！")


def creat_trigger():
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
    db.session.execute(create_trigger_query)

    # 提交更改
    db.session.commit()

    print("触发器创建成功！")


# 创建存储过程
def create_update_procedure():
    # cursor = db.cursor()

    # 定义存储过程语句
    procedure_query = """
        CREATE PROCEDURE update_board_name(
        IN original_name VARCHAR(100),
        IN new_name VARCHAR(100),
        IN reason TEXT,
        IN contact VARCHAR(100)
    )
    BEGIN
        -- 检查新名称的长度是否小于3个字符
        IF CHAR_LENGTH(new_name) < 3 THEN
            -- 如果是，则使用SIGNAL语句抛出一个错误
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '新名称长度必须大于2个字符';
        ELSE
            -- 如果新名称长度符合要求，则更新board表
            UPDATE board SET name = new_name WHERE name = original_name;
        END IF;
    END;
    """

    # 执行创建存储过程的SQL语句
    db.session.execute(procedure_query)
    db.session.commit()
    print("修改板块名称存储过程创建成功！")


# 创建存储过程
def create_post_belong_procedure():
    # cursor = db.cursor()

    # 定义存储过程语句
    procedure_query = """
    CREATE PROCEDURE update_post_belong(
        IN original_name VARCHAR(100),
        IN new_name VARCHAR(100),
        IN reason TEXT,
        IN contact VARCHAR(100)
    )
    BEGIN
        -- 声明变量来存储查询结果
        DECLARE original_board_id INT;
        DECLARE new_board_id INT;
        DECLARE original_board_count INT;
        DECLARE new_board_count INT;
    
        -- 查询原始板块的ID
        SELECT id INTO original_board_id FROM board WHERE name = original_name LIMIT 1;
    
        -- 检查原始板块是否存在
        IF original_board_id IS NULL THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '原始板块名称不存在';
        ELSE
            -- 查询新板块的ID
            SELECT id INTO new_board_id FROM board WHERE name = new_name LIMIT 1;
    
            -- 检查新板块是否存在
            IF new_board_id IS NULL THEN
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '新板块名称不存在';
            ELSE
                -- 更新帖子所属板块
                UPDATE post SET board_id = new_board_id WHERE board_id = original_board_id;
            END IF;
        END IF;
    END;
    """

    # 执行创建存储过程的SQL语句
    db.session.execute(procedure_query)
    db.session.commit()
    print("修改帖子板块存储过程创建成功！")


def create_user():
    # 假设的role_id，你需要根据实际情况替换为有效的值
    # role_id = NULL

    # 生成100条SQL插入语句
    sql_statements = []
    for i in range(0, 40):
        # user_id = str(uuid.uuid4())
        username = f'username_{i}'
        password = '123456'
        email = f'user{i}@example.com'
        avatar = f'https://tse3-mm.cn.bing.net/th/id/OIP-C.4wgKhs-PxZzVtDbWY3j2pwAAAA?rs=1&pid=ImgDetMain'  # 请替换为实际的头像URL
        signature = f'signature_{i}'
        # join_time = datetime.now()
        # sql = f"INSERT INTO user (id, username, _password, email, avatar, signature, join_time, is_staff, is_active " \
        #       f"VALUES ('{user_id}', '{username}', '{password}', '{email}', '{avatar}', '{signature}', '{join_time}', FALSE, TRUE);"
        # sql_statements.append(sql)
        # user = UserModel(email=email, username=username, password=password)
        # 输出生成的SQL语句
        # 执行创建普通用户的SQL语句
        # 创建一个新用户对象，并将用户输入的信息存储到数据库中
        user = UserModel(email=email, username=username, password=password, signature=signature, avatar=avatar)
        db.session.add(user)
        db.session.commit()
    print("普通用户创建成功！")


def sql_create_user():
    # 假设的role_id，你需要根据实际情况替换为有效的值
    # role_id = NULL

    # 生成100条SQL插入语句
    sql_statements = []
    for i in range(40, 45):
        user_id = str(uuid.uuid4())
        username = f'username_{i}'
        hash_password = generate_password_hash('123456')
        email = f'user{i}@example.com'
        avatar = f'https://tse3-mm.cn.bing.net/th/id/OIP-C.4wgKhs-PxZzVtDbWY3j2pwAAAA?rs=1&pid=ImgDetMain'  # 请替换为实际的头像URL
        signature = f'signature_{i}'
        join_time = datetime.now()
        sql = f"INSERT INTO user (id, username, _password, email, avatar, signature, join_time, is_staff, is_active, role_id)" \
              f"VALUES ('{user_id}', '{username}', '{hash_password}', '{email}', '{avatar}', '{signature}', '{join_time}', 0, 1, NULL);"
        db.session.execute(sql)
        db.session.commit()

    print("使用sql创建普通用户创建成功！")


def create_comment():
    fake = Faker(locale="zh_CN")
    author = UserModel.query.first()  # 确保UserModel中有query方法
    posts = PostModel.query.all()  # 假设你想要在所有文章上添加评论
    click.echo("开始生成测试评论...")
    for x in range(300):
        title = fake.sentence()
        content = fake.paragraph(nb_sentences=10)
        random_index = random.randint(0, len(posts) - 1)  # 确保随机索引不会超出posts列表的范围
        post = posts[random_index]  # 获取一个随机的文章对象
        comment = CommentModel(content=content, post_id=post.id, author_id=author.id, is_active=True)
        db.session.add(comment)
    db.session.commit()
    click.echo("测试评论生成成功！")


# 创建存储过程
def create_update_boardID_procedure():
    # cursor = db.cursor()

    # 定义存储过程语句
    procedure_query = """
    CREATE PROCEDURE update_board_id(
        IN original_id VARCHAR(4),
        IN new_id VARCHAR(4),
        IN reason VARCHAR(200),
        IN contact VARCHAR(100)
    )
    BEGIN
        -- 声明变量来存储查询结果
        DECLARE new_board_id INT;
        -- 查询原始板块的ID
        SELECT id INTO new_board_id FROM board WHERE id = new_id LIMIT 1;
        -- 检查原始板块是否存在
        IF new_board_id IS NOT NULL THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '原始板块ID已经存在';
    
        -- 检查原始板块ID和新板块ID是否为非负整数且长度不超过4位
        ELSEIF NOT (original_id REGEXP '^[0-9]{1,4}$' AND original_id NOT LIKE '-%'
            AND new_id REGEXP '^[0-9]{1,4}$' AND new_id NOT LIKE '-%') THEN
            -- 如果不在范围内，则抛出错误
            SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = '板块ID必须是0到9999之间的整数';
        ELSE
            -- 开始事务
            # START TRANSACTION;
            
            -- 更新帖子表中的板块ID
            set foreign_key_checks =0;
            UPDATE post SET board_id = new_id WHERE board_id = original_id;
            
            -- 更新板块表中的板块ID
            UPDATE board SET id = new_id WHERE id = original_id;
            set foreign_key_checks =1;
            
            
            -- 提交事务
            # COMMIT;
        END IF;
    END;
    """

    # 执行创建存储过程的SQL语句
    db.session.execute(procedure_query)
    db.session.commit()
    print("修改板块ID存储过程创建成功！")
