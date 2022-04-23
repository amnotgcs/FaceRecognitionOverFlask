from time import sleep

from PIL import Image

from .Learner import face_learner
from .config import get_config
from .mtcnn import MTCNN
from .utils import load_facebank, prepare_facebank

from json import dump


def do_rec():
    """开始人脸识别"""
    conf = get_config(False)

    mtcnn = MTCNN()
    print('mtcnn loaded')

    learner = face_learner(conf, True)
    learner.threshold = 1.54
    learner.load_state(conf, 'cpu_final.pth', True, True)
    learner.model.eval()
    print('learner loaded')

    targets, names = prepare_facebank(conf, learner.model, mtcnn, False)
    print('facebank updated')
    targets, names = load_facebank(conf)
    print('facebank loaded')

    while True:
        try:
            sleep(0.05)
            fp = open(r'checkIn\static\upload\face.jpg', 'rb')
            image = Image.open(fp)
            r, g, b, a = image.split()
            image = Image.merge("RGB", (r, g, b))
            bboxes, faces = mtcnn.align_multi(image, conf.face_limit, conf.min_face_size)
            bboxes = bboxes[:, :-1]  # shape:[10,4],only keep 10 highest possibiity faces
            bboxes = bboxes.astype(int)
            bboxes = bboxes + [-1, -1, 1, 1]  # personal choice
            results, score = learner.infer(conf, faces, targets, tta=False)
            rec_result = {
                'msg': 'ok',
                'name': names[results[0] + 1],
                'rec_score': f'{score[0] * 100 : .2f}%',
            }
            fp.close()
            with open('face_rec_result.txt', 'wt', encoding='UTF-8') as file:
                dump(rec_result, file)
        except Exception as e:
            rec_result = {
                'msg': 'failed',
                'name': 'NULL',
                'rec_score': '0%',
            }
        finally:
            with open('face_rec_result.txt', 'wt', encoding='UTF-8') as file:
                dump(rec_result, file)

