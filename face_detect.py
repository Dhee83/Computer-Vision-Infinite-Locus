import cv2
import base64
import websocket
import json
from capture import send_frame
from constants import *


video = cv2.VideoCapture(VIDEO_FILE)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

while True:
    ret, frame = video.read()
    if not ret:
        break

    # Reduce frame size by half
    frame = cv2.resize(frame, None, fx=FX, fy=FY)
    if ret and PUBLISH_DATA:
        _, buffer = cv2.imencode('.jpg', frame)
        frame_base64 = base64.b64encode(buffer).decode('utf-8')


    height, width, _ = frame.shape
    roi = frame[int(height/2):height, :]

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(20, 20))

    for (x, y, w, h) in faces:
        cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('Face Detection', frame)

    if cv2.waitKey(1) == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
