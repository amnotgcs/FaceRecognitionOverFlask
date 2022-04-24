from flask import (
    Blueprint, g, render_template
)

from checkIn.auth import login_required

bp = Blueprint('user', __name__, url_prefix='/user')


@login_required
@bp.route('/', methods=('GET', ))
def index():
    """个人主页"""
    username = g.user['username']
    return render_template('user/homepage.html')
