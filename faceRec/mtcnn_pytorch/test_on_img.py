from src import detect_faces, show_bboxes
from PIL import Image

img = Image.open('me.jpg')
bounding_boxes, landmarks = detect_faces(img, min_face_size=10.0)
img2 = show_bboxes(img, bounding_boxes, landmarks)
img2.show()
