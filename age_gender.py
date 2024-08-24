import cv2
import math
# from capture import send_frame

# Load pre-trained models
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
gender_net = cv2.dnn.readNetFromCaffe('detection_models/gender_net_definitions/deploy.prototxt', 'detection_models/models/gender_net.caffemodel')
age_net = cv2.dnn.readNetFromCaffe('detection_models/age_net_definitions/deploy.prototxt', 'detection_models/models/age_net.caffemodel')

# Define age and gender classes
# age_list = ['(0-2)','(3-4)', '(4-6)', '(8-12)', '(15-20)', '(22-27)', '(29-34)', '(36-43)', '(48-53)', '(60-100)']
age_list = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(33-37)', '(38-43)', '(48-53)', '(60-100)']
gender_list = ['Male', 'Female']

# Open webcam
video_capture = cv2.VideoCapture(0)

while True:
    # Read frame from webcam
    ret, frame = video_capture.read()

    # Convert frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=1, minSize=(15, 15))

    for (x, y, w, h) in faces:
        # Extract face region of interest (ROI)
        face_roi = frame[y:y + h, x:x + w]

        # Preprocess face ROI for gender classification
        face_blob = cv2.dnn.blobFromImage(face_roi, 1.0, (227, 227), (78.4263377603, 87.7689143744, 114.895847746), swapRB=False)

        # Gender prediction
        gender_net.setInput(face_blob)
        gender_preds = gender_net.forward()
        gender = gender_list[gender_preds[0].argmax()]

        # Preprocess face ROI for age estimation
        # face_blob = cv2.dnn.blobFromImage(face_roi, 1.0, (227, 227), (78.4263377603, 87.7689143744, 114.895847746), swapRB=False)
        face_blob = cv2.dnn.blobFromImage(face_roi, 1.0, (227, 227), (78.4163377603, 87.7589143744, 114.835847746), swapRB=False)

        # Age prediction
        age_net.setInput(face_blob)
        age_preds = age_net.forward()
        age = age_list[age_preds[0].argmax()]

        # Draw rectangle around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display gender and age information
        label = f'{gender}, {age}'
        cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Display the resulting frame

        cv2.imshow('Video', frame)


    # Exit loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# asyncio.get_event_loop().run_until_complete(process_frames())

# Release the video capture object and close windows
video_capture.release()
cv2.destroyAllWindows()


# # import cv2
# # import math
# # import asyncio
# # import websockets

# # # Load pre-trained models
# # face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
# # gender_net = cv2.dnn.readNetFromCaffe('detection_models/gender_net_definitions/deploy.prototxt', 'detection_models/models/gender_net.caffemodel')
# # age_net = cv2.dnn.readNetFromCaffe('detection_models/age_net_definitions/deploy.prototxt', 'detection_models/models/age_net.caffemodel')

# # # Define age and gender classes
# # age_list = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(33-37)', '(38-43)', '(48-53)', '(60-100)']
# # gender_list = ['Male', 'Female']


# # # Open webcam
# # video_capture = cv2.VideoCapture(0)


# # async def send_frame(frame):
# #     async with websockets.connect("ws://localhost:8000/ws/data/") as websocket:
# #         # Encode frame to JPEG format
# #         _, buffer = cv2.imencode('.jpg', frame)
# #         frame_bytes = buffer.tobytes()

# #         # Send frame bytes to the WebSocket server
# #         await websocket.send(frame_bytes)


# # async def process_frames():
# #     while True:
# #         # Read frame from webcam
# #         ret, frame = video_capture.read()

# #         # Convert frame to grayscale for face detection
# #         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# #         # Detect faces in the frame
# #         faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

# #         for (x, y, w, h) in faces:
# #             # Extract face region of interest (ROI)
# #             face_roi = frame[y:y + h, x:x + w]

# #             # Preprocess face ROI for gender classification
# #             face_blob = cv2.dnn.blobFromImage(face_roi, 1.0, (227, 227), (78.4263377603, 87.7689143744, 114.895847746), swapRB=False)

# #             # Gender prediction
# #             gender_net.setInput(face_blob)
# #             gender_preds = gender_net.forward()
# #             gender = gender_list[gender_preds[0].argmax()]

# #             # Preprocess face ROI for age estimation
# #             face_blob = cv2.dnn.blobFromImage(face_roi, 1.0, (227, 227), (78.4263377603, 87.7689143744, 114.895847746), swapRB=False)

# #             # Age prediction
# #             age_net.setInput(face_blob)
# #             age_preds = age_net.forward()
# #             age = age_list[age_preds[0].argmax()]

# #             # Draw rectangle around the face
# #             cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

# #             # Display gender and age information
# #             label = f'{gender}, {age}'
# #             cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

# #         # Send frame with text overlay to WebSocket
# #         await send_frame(frame)

# #         # Display the resulting frame
# #         cv2.imshow('Video', frame)

# #         # Exit loop if 'q' is pressed
# #         if cv2.waitKey(1) & 0xFF == ord('q'):
# #             break


# # # Run the processing loop asynchronously
# # asyncio.get_event_loop().run_until_complete(process_frames())

# # # Release the video capture object and close windows
# # video_capture.release()
# # cv2.destroyAllWindows()


# import cv2
# import math

# # Load pre-trained models
# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
# # face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
# gender_net = cv2.dnn.readNetFromCaffe('detection_models/gender_net_definitions/deploy.prototxt', 'detection_models/models/gender_net.caffemodel')
# age_net = cv2.dnn.readNetFromCaffe('detection_models/age_net_definitions/deploy.prototxt', 'detection_models/models/age_net.caffemodel')

# # Define age and gender classes
# age_list = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
# gender_list = ['Male', 'Female']

# # Open webcam
# video_capture = cv2.VideoCapture(0)

# while True:
#     # Read frame from webcam
#     ret, frame = video_capture.read()

#     # Convert frame to grayscale for face detection
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     # Detect faces in the frame
#     faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

#     for (x, y, w, h) in faces:
#         # Extract face region of interest (ROI)
#         face_roi = frame[y:y + h, x:x + w]

#         # Preprocess face ROI for gender classification
#         face_blob = cv2.dnn.blobFromImage(face_roi, 1.0, (227, 227), (78.4263377603, 87.7689143744, 114.895847746), swapRB=False)

#         # Gender prediction
#         gender_net.setInput(face_blob)
#         gender_preds = gender_net.forward()
#         gender = gender_list[gender_preds[0].argmax()]

#         # Preprocess face ROI for age estimation
#         face_blob = cv2.dnn.blobFromImage(face_roi, 1.0, (227, 227), (78.4263377603, 87.7689143744, 114.895847746), swapRB=False)

#         # Age prediction
#         age_net.setInput(face_blob)
#         age_preds = age_net.forward()
#         age = age_list[age_preds[0].argmax()]

#         # Draw rectangle around the face
#         cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

#         # Display gender and age information
#         label = f'{gender}, {age}'
#         cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

#     # Display the resulting frame
#     cv2.imshow('Video', frame)

#     # Exit loop if 'q' is pressed
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release the video capture object and close windows
# video_capture.release()
# cv2.destroyAllWindows()



