import cv2
from utils import draw_landmarks_on_image
from model import get_hand_keypoints
import mediapipe as mp

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)
image = cv2.cvtColor(cv2.imread('tup.jpg'), cv2.COLOR_BGR2RGB)
#image = mp.Image.create_from_file("image.jpg")

keypoints = get_hand_keypoints(image)
print(keypoints)

# STEP 5: Process the classification result. In this case, visualize it.
annotated_image = cv2.cvtColor(draw_landmarks_on_image(image, keypoints), cv2.COLOR_RGB2BGR)
cv2.imshow('found image', annotated_image)

cv2.waitKey(0) 
