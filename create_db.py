import sqlite3
import io
import os
import numpy as np
import cv2
from retinaface import RetinaFace
import onnxruntime as rt
from sklearn.preprocessing import normalize
from skimage import transform as trans

def adapt_array(arr):
   out = io.BytesIO()
   np.save(out, arr)
   out.seek(0)
   return sqlite3.Binary(out.read())


def convert_array(text):
   out = io.BytesIO(text)
   out.seek(0)
   return np.load(out)


def load_file(file_path):
   file_data = {}
   for person_name in os.listdir(file_path):
      person_file = os.path.join(file_path, person_name)

      total_pictures = []
      for picture in os.listdir(person_file):
         picture_path = os.path.join(person_file, picture)
         total_pictures.append(picture_path)

      file_data[person_name] = total_pictures

   return file_data


def face_detect(img_path):
   detector = RetinaFace(quality="normal")
   img_bgr = cv2.imread(img_path, cv2.IMREAD_COLOR)
   img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
   detections = detector.predict(img_rgb)
   #print(detections)

   img_result = detector.draw(img_rgb, detections)
   img = cv2.cvtColor(img_result, cv2.COLOR_RGB2BGR)
   #cv2.imshow("windows", img)
   #key = cv2.waitKey()
   #if key == ord("q"):
      #print("exit")

   #cv2.destroyWindow("windows")
   return img, detections


def get_embeddings(img_rgb, detections):
   onnx_path = "model/arcfaceresnet100.onnx"

   extractor = rt.InferenceSession(onnx_path)

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
      aligned = cv2.warpAffine(img_rgb, M, (112, 112), borderValue=0)

   t_aligned = np.transpose(aligned, (2, 0, 1))
   inputs = t_aligned.astype(np.float32)
   input_blob = np.expand_dims(inputs, axis=0)

   first_input_name = extractor.get_inputs()[0].name
   first_output_name = extractor.get_outputs()[0].name

   predict = extractor.run([first_output_name], {first_input_name: input_blob})[0]
   final_embedding = normalize(predict).flatten()
   return face_position, face_landmarks, final_embedding



sqlite3.register_adapter(np.ndarray, adapt_array)
sqlite3.register_converter("ARRAY", convert_array)
conn_db = sqlite3.connect('database.db')
if os.path.exists('database.db') == False:
   conn_db.execute("CREATE TABLE face_info \
            (id INT PRIMARY KEY NOT NULL, \
            name TEXT NOT NULL, \
            embedding ARRAY NOT NULL)")

file_path = 'dataset'
if os.path.exists(file_path):
   file_data = load_file(file_path)

   for i, person_name in enumerate(file_data.keys()):
      picture_path = file_data[person_name]
      sum_embeddings = np.zeros([1, 512])
      for j, picture in enumerate(picture_path):
         img_rgb, detections = face_detect(picture)
         position, landmarks, embeddings = get_embeddings(img_rgb, detections)
         sum_embeddings += embeddings

      final_embedding = sum_embeddings / len(picture_path)
      adapt_embedding = adapt_array(final_embedding)

      conn_db.execute("INSERT INTO face_info (id, name, embedding) VALUES (?, ?, ?)",
                      (i, person_name, adapt_embedding))
   conn_db.commit()
   conn_db.close()

