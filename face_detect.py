import cv2
from retinaface import RetinaFace

detector = RetinaFace(quality="normal")
img_path = 'dataset/IU/IU.jpg'
img_bgr = cv2.imread(img_path, cv2.IMREAD_COLOR)
img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
detections = detector.predict(img_rgb)
print(detections)

img_result = detector.draw(img_rgb, detections)
img = cv2.cvtColor(img_result, cv2.COLOR_RGB2BGR)
cv2.imshow("windows", img)
key = cv2.waitKey()
if key == ord("q"):
   print("exit")

cv2.destroyWindow("windows")
