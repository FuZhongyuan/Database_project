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

bp = Blueprint("view", __name__, url_prefix="/view")


@bp.get('/user_comments_view')
def user_comments_view():
    # 执行查询操作，获取view2的数据
    user_id = session.get('user_id')
    query = text('SELECT * FROM user_comments_view WHERE user_id = :user_id')
    result = db.session.execute(query, {'user_id': user_id})
    view2_data = result.fetchall()
    # 渲染admin.html视图，并将查询结果传递给模板
    return render_template('view/user_comments_view.html', view2_data=view2_data)


@bp.route('/user_comments/<int:comment_id>')
def user_comments(comment_id):
    if comment_id is None:
        return redirect(url_for('user.login'))
    query = text('SELECT * FROM user_comments_view WHERE comment_id = :comment_id')
    result = db.session.execute(query, {'comment_id': comment_id})
    comments = result.fetchall()
    return render_template('view/user_comments_details.html', comments=comments)
