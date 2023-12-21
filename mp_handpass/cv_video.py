import cv2 as cv
import numpy as np

from model import get_hand_keypoints
from utils import draw_landmarks_on_image


def is_landmark_equal(landmarks1, landmarks2):
    if (len(landmarks1) != len(landmarks2)):
        return False
    for l1, l2 in zip(landmarks1, landmarks2):
        for l12, l22 in zip(l1, l2):
            if round(l12.x, 3) - round(l22.x, 3) > 0.1 or round(l12.y, 3) - round(l22.y, 3) > 0.1:
                print(l12.x)
                print(l22.x)
                print(l22.y)
                print(l12.y)
                return False
    return True


image = cv.cvtColor(cv.imread('image.jpg'), cv.COLOR_BGR2RGB)
# image = mp.Image.create_from_file("image.jpg")

keypoints_test = get_hand_keypoints(image)

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
    keypoints = get_hand_keypoints(frame)
    print(keypoints.hand_landmarks)

    # STEP 5: Process the classification result. In this case, visualize it.
    annotated_image = cv.cvtColor(draw_landmarks_on_image(frame, keypoints, is_landmark_equal(keypoints_test.hand_landmarks, keypoints.hand_landmarks)), cv.COLOR_RGB2BGR)
    # Display the resulting frame
    cv.imshow('frame', annotated_image)
    if cv.waitKey(1) == ord('r'):
        print("Recorded keypoint")
        keypoints_test = keypoints
    elif cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
