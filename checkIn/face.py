import base64
import json

from flask import (
    Blueprint, render_template, request, Response
)

from checkIn.auth import login_required
from faceRec.fv_on_Img import do_rec

bp = Blueprint('face', __name__, url_prefix='/face')


@login_required
@bp.route('/', methods=('GET', 'POST'))
def index():
    """人脸识别页面"""
    # do_rec()
    return render_template('face/signin.html')


# 图片接收
@bp.route('/receiveImage/', methods=["POST"])
def receive_image():
    if request.method == "POST":
        data = request.data.decode('utf-8')
        img_base64 = json.loads(data).get('imgData')
        img = base64.b64decode(json.loads(data).get('imgData'))
        with open(r'checkIn\static\upload\face.jpg', 'wb') as file:
            file.write(img)

    return Response('upload')
