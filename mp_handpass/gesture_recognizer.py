# Imports neccessary modules.
import pickle
import tensorflow as tf

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import os

from tensorflow import keras


class_indices = pickle.loads(open('../training/labels.pickle', "rb").read())
model = keras.models.load_model("../training/res_gesture.keras")

# Get most probable gesture
def get_gesture_name(image):
	model_path = os.path.abspath("hand_pass.task")
	recognizer = vision.GestureRecognizer.create_from_model_path(model_path)

	# Load the input image.
	mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)

	# Run gesture recognition.
	recognition_result = recognizer.recognize(mp_image)

	top_gesture = 'unrecognized'
	print(recognition_result.gestures)
	# Display the most likely gesture.
	if len(recognition_result.gestures) > 0 and len(recognition_result.gestures[0]) > 0 and recognition_result.gestures[0][0].score > 0.75:
		top_gesture = recognition_result.gestures[0][0].category_name
	return top_gesture


# Get most probable gesture
def get_gesture_name_custom(image):
	image_expand = tf.expand_dims(image, axis=0)
	prediction = model.predict(image_expand)
	predicted_class_idx = tf.argmax(prediction[0])
	predicted_class = class_indices[predicted_class_idx.numpy()]
	print(predicted_class)
	return predicted_class
