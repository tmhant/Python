import cv2
from retinaface import RetinaFace
import numpy as np
from skimage import transform as trans

src = np.array([
    [30.2946, 51.6963],
    [65.5318, 51.5014],
    [48.0252, 71.7366],
    [33.5493, 92.3655],
    [62.7299, 92.2041]], dtype=np.float32)

for i, face_info in enumerate(detections):
    face_position = [face_info['x1'], face_info['y1'],
                     face_info['x2'], face_info['y2']]
    face_landmarks = [face_info['left_eye'], face_info['right_eye'], face_info['nose'], face_info['left_lip'],
                      face_info['right_lip']]

    dst = np.array(face_landmarks, dtype=np.float32).reshape(5, 2)
    tform = trans.SimilarityTransform()
    tform.estimate(dst, src)
    M = tform.params[0:2, :]
    aligned = cv2.warpAffine(imgRGB, M, (112, 112), borderValue=0)
