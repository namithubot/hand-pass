import cv2 as cv
import numpy as np

from gesture_recognizer import get_gesture_name, get_gesture_name_custom
from utils import write_on_image, hash_gesture


def is_landmark_equal(landmarks1, landmarks2):
    if (len(landmarks1) != len(landmarks2)):
        return False
    for l1, l2 in zip(landmarks1, landmarks2):
        for l12, l22 in zip(l1, l2):
            if round(l12.x, 2) != round(l22.x, 2) or round(l12.y, 2) != round(l22.y, 2):
                return False
    return True


image = cv.cvtColor(cv.imread('image.jpg'), cv.COLOR_BGR2RGB)
# image = mp.Image.create_from_file("image.jpg")

password = []
password_unhashed = []
input = []
isRecording = False
isEntering = False
escape_gesture = 'paper'
mode = 'None'
last_gesture = ''

use_mp = True

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    # gray = cv.cvtColor(frame, cv)

    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    if use_mp:
        gesture_name = get_gesture_name(frame)
    else:
        gesture_name = get_gesture_name_custom(frame)

    if gesture_name not in ['unrecognized', 'none', ''] and gesture_name != last_gesture:
        gesture_hash = hash_gesture(gesture_name)
        if isRecording:
            if gesture_name != escape_gesture:
                password.append(gesture_hash)
                password_unhashed.append(gesture_name)
        elif isEntering:
            if len(password) == 0:
                print('success')
                break
            if password[0] == gesture_hash:
                password.pop(0)
        last_gesture = gesture_name

    # STEP 5: Process the classification result. In this case, visualize it.
    annotated_image = cv.cvtColor(write_on_image(frame, mode + ' ' + gesture_name + ':' + ",".join(password_unhashed), 50, 50), cv.COLOR_RGB2BGR)
    # Display the resulting frame
    cv.imshow('frame', annotated_image)
    if cv.waitKey(1) == ord('r'):
        isRecording = True
        isEntering = False
        mode = 'Rec'
        last_gesture = ''
        print("Recorded keypoint")
    elif cv.waitKey(1) == ord('e'):
        isRecording = False
        isEntering = True
        mode = 'Enteringqq'
        last_gesture = ''
        print(password)
    elif cv.waitKey(1) == ord('c') and not isEntering:
        print('clear password')
        password = []
        password_unhashed = []
    elif cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
