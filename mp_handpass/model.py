import mediapipe as mp
from mediapipe.tasks import python


def get_hand_keypoints(image):
    base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
    options = python.vision.HandLandmarkerOptions(base_options=base_options,
                                           num_hands=2, min_hand_detection_confidence=0.7)
    detector = python.vision.HandLandmarker.create_from_options(options)
    # Get hand landmarks from the input image.
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
    detection_result = detector.detect(mp_image)
    return detection_result
