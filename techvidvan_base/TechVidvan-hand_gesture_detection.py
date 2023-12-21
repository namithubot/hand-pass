# TechVidvan hand Gesture Recognizer

# import necessary packages

import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
from tensorflow.keras.models import load_model

# initialize mediapipe
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Load the gesture recognizer model
model = load_model('mp_hand_gesture')

# Load class names
f = open('gesture.names', 'r')
classNames = f.read().split('\n')
f.close()
print(classNames)


# Initialize the webcam
cap = cv2.VideoCapture(0)

password = []
last_gesture = ''
recording = False
password_entry = False
escape_gesture = 'stop'
mode = 'None'

while True:
    # Read each frame from the webcam
    _, frame = cap.read()

    x, y, c = frame.shape

    # Flip the frame vertically
    frame = cv2.flip(frame, 1)
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Get hand landmark prediction
    result = hands.process(framergb)

    # print(result)
    
    className = ''

    # post process the result
    if result.multi_hand_landmarks:
        landmarks = []
        for handslms in result.multi_hand_landmarks:
            for lm in handslms.landmark:
                # print(id, lm)
                lmx = int(lm.x * x)
                lmy = int(lm.y * y)

                landmarks.append([lmx, lmy])

            # Drawing landmarks on frames
            mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

            # Predict gesture
            prediction = model.predict([landmarks])
            # print(prediction)
            classID = np.argmax(prediction)
            className = classNames[classID]
    
    if recording:
        if len(password) < 1 or (password[-1] != className and className != escape_gesture):
            password.append(className)
    elif password_entry:
        if len(password) == 0:
            print('success')
            break
        if className != escape_gesture and className != last_gesture and password[0] == className:
            last_geture = password.pop(0)
            print(last_geture)

    # show the prediction on the frame
    cv2.putText(frame, mode + ' : ' + className, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                   1, (0, 0, 255), 2, cv2.LINE_AA)

    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect multiple faces in a captured frame 
    # scaleFactor: Parameter specify how much the 
    # image sizeis reduced at each image scale. 
    # minNeighbors: Parameter specify how many 
    # neighbours each rectangle should have to retain it. 
    # rectangle consists the detect object. 
    # Here the object is the face. 
    face = cascade.detectMultiScale(
        gray_image, scaleFactor=2.0, minNeighbors=4)

    for x, y, w, h in face:

        # draw a border around the detected face.  
        # (here border color = green, and thickness = 3) 
        image = cv2.rectangle(frame, (x, y), (x+w, y+h),
                              (0, 255, 0), 3)

        # blur the face which is in the rectangle 
        image[y:y+h, x:x+w] = cv2.medianBlur(image[y:y+h, x:x+w],
                                             35)

        # Show the final output
    cv2.imshow("Output", frame) 

    if cv2.waitKey(1) == ord('q'):
        break
    elif cv2.waitKey(1) == ord('r'):
        recording = True
        mode = 'Recording'
    elif cv2.waitKey(1) == ord('p'):
        password = list(filter(lambda p: p != '', password))
        print(password)
        recording = False
        password_entry = True
        mode = 'Enter password'

# release the webcam and destroy all active windows
cap.release()

cv2.destroyAllWindows()