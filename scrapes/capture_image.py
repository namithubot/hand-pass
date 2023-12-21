import cv2 as cv
import time
import os

cap = cv.VideoCapture(0)
img_counter = 0
gesture_name = "kuch_bhi"

os.mkdir(gesture_name)

while True:
    time.sleep(0.6)
    ret, frame = cap.read()

    img_name = "{}/opencv_frame_{}.jpg".format(gesture_name, img_counter)
    cv.imwrite(img_name, frame, [int(cv.IMWRITE_JPEG_QUALITY), 100])
    print("{} written!".format(img_name))
    img_counter += 1
    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q') or img_counter == 103:
        break