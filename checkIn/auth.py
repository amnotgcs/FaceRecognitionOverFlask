import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.security import check_password_hash, generate_password_hash

from checkIn.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.before_app_request
def load_logged_in_user():
    """请求时鉴权"""
    user_id = session.get('user_id')

    if not user_id:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM users WHERE id = ?', (user_id, )
        ).fetchone()


@bp.route('/register', methods=('GET', 'POST'))
def register():
    """注册新用户"""
    if request.method == 'POST':
        username = request.form['inputUsername']
        password = request.form['inputPassword']
        email = request.form['inputEmail']
        motto = request.form['inputMotto']
        db = get_db()
        error = None

        if not username:
            error = '必须提供用户名'
        elif not password:
            error = '必须提供密码'

        if not error:
            try:
                db.execute(
                    'INSERT INTO users (username, password, email, motto) VALUES (?, ?, ?, ?)',
                    (username, generate_password_hash(password), email, motto)
                )
                db.commit()
            except db.IntegrityError:
                error = f'用户 {username} 已经被注册了！'
            else:
                return redirect(url_for('auth.login'))
        flash(error)
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    """用户登录"""
    if request.method == 'POST':
        username = request.form['inputUsername']
        password = request.form['inputPassword']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM users WHERE username = ?', (username, )
        ).fetchone()

        if not user:
            error = '用户名不存在！'
        elif not check_password_hash(user['password'], password):
            error = '用户名与密码不匹配！！'

        if not error:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('user.index'))

        flash(error)
    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    """用户注销"""
    session.clear()
    return redirect(url_for('auth.login'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not g.user:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


@bp.route('/')
def index():
    return 'hello ' + g.user['username']

