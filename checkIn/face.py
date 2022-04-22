import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.security import check_password_hash, generate_password_hash

from checkIn.db import get_db
from checkIn.auth import login_required

bp = Blueprint('face', __name__, url_prefix='/face')


@login_required
@bp.route('/', methods=('GET', 'POST'))
def index():
    """人脸识别页面"""
    return render_template('face/signin.html')
