import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.security import check_password_hash, generate_password_hash

from checkIn.db import get_db
from checkIn.auth import login_required

bp = Blueprint('user', __name__, url_prefix='/user')


@login_required
@bp.route('/', methods=('GET', ))
def index():
    """个人主页"""
    username = g.user['username']
    return render_template('user/homepage.html')
