import base64
import json
from io import BytesIO

from PIL import Image
from flask import (
    Blueprint, render_template, request, jsonify
)

from checkIn.auth import login_required
from faceRec.Learner import face_learner
from faceRec.config import get_config
from faceRec.mtcnn import MTCNN
from faceRec.utils import prepare_facebank, load_facebank

bp = Blueprint('face', __name__, url_prefix='/face')


@login_required
@bp.route('/', methods=('GET', 'POST'))
def index():
    """人脸识别页面"""
    return render_template('face/signin.html')


@bp.route('/receiveImage/', methods=["POST"])
def receive_image():
    if request.method == "POST":

        conf = get_config(False)
        mtcnn = MTCNN()

        learner = face_learner(conf, True)
        learner.threshold = 1.54
        learner.load_state(conf, 'cpu_final.pth', True, True)
        learner.model.eval()

        prepare_facebank(conf, learner.model, mtcnn, False)
        targets, names = load_facebank(conf)
        data = request.data.decode('utf-8')
        image = base64.b64decode(json.loads(data).get('imgData'))
        image = Image.open(BytesIO(image))
        r, g, b, a = image.split()
        image = Image.merge("RGB", (r, g, b))

        rec_result = {
            'msg': 'ok',
        }
        try:
            bboxes, faces = mtcnn.align_multi(image, conf.face_limit, conf.min_face_size)
            results, score = learner.infer(conf, faces, targets, tta=False)
            rec_result['name'] = names[results[0] + 1]
            rec_result['rec_score'] = f'{score[0] * 100 : .2f}%'
        except Exception as e:
            pass
        return jsonify(rec_result)
