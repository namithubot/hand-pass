import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


def get_hand_keypoints(image):
    # STEP 2: Create an HandLandmarker object.
    base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
    options = vision.HandLandmarkerOptions(base_options=base_options,
                                           num_hands=2)
    detector = vision.HandLandmarker.create_from_options(options)
    # STEP 4: Detect hand landmarks from the input image.
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
    detection_result = detector.detect(mp_image)
    return detection_result
