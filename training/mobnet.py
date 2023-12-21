import os
import pickle
import tensorflow as tf
from keras.src.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D

data_dir = "data"

augment = ImageDataGenerator(
    rotation_range=30,
    zoom_range=0.25,
    width_shift_range=0.10,
    height_shift_range=0.10,
    shear_range=0.10,
    horizontal_flip=True,
    fill_mode="nearest",
    validation_split=0.2
)

train_ds = augment.flow_from_directory(
    directory=data_dir,
    classes=os.listdir('data'),
    subset='training'
)
# tf.keras.utils.image_dataset_from_directory(
#     data_dir,
#     validation_split=0.2,
#     class_names=,
#     subset="training",
#     seed=123)


val_ds = augment.flow_from_directory(
    directory=data_dir,
    classes=os.listdir('data'),
    subset='validation'
)
    
# tf.keras.utils.image_dataset_from_directory(
#     data_dir,
#     validation_split=0.2,
#     class_names=os.listdir('data'),
#     subset="validation",
#     seed=123))

class_indices = {v: k for k, v in train_ds.class_indices.items()}

# AUTOTUNE = tf.data.AUTOTUNE
# train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)
# val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)

vgg_16 = tf.keras.applications.MobileNetV3Small(include_top=False, weights='imagenet')

vgg_16.trainable = False

# Adding our own custom head
# Start by taking the output feature maps from the model
x = vgg_16.output

# Convert to a single-dimensional vector by Global Average Pooling. 
# We could also use Flatten()(x) GAP is more effective reduces params and controls overfitting.
x = GlobalAveragePooling2D()(x)

# x = Dense(2500, activation='relu')(x)
# 
# # Dropout 40% of the activations, helps reduces overfitting
# x = Dropout(0.40)(x)
# 
# x = Dense(1300, activation='relu')(x)
# 
# # Dropout 40% of the activations, helps reduces overfitting
# x = Dropout(0.40)(x)


x = Dense(712, activation='relu')(x)

# Dropout 40% of the activations, helps reduces overfitting
x = Dropout(0.40)(x)

# 
# x = Dense(128,activation='relu', use_bias=False)(x)
# x = Dense(64,activation='relu', use_bias=False)(x)
# x = Dense(32,activation='relu', use_bias=False)(x)

# The fianl layer will contain 7 output units (no of units = no of classes) with softmax function.
preds = Dense(20,activation='softmax')(x)

# Construct the full model
model = Model(inputs=vgg_16.input, outputs=preds)

model.compile(optimizer='Adam', loss='categorical_crossentropy',metrics=['accuracy'])

history = model.fit(train_ds, epochs=10, validation_data=(val_ds))

model.save('res_gesture.keras')

f = open('labels.pickle', "wb")
f.write(pickle.dumps(class_indices))
f.close()

import cv2

image = cv2.imread("data/smile/opencv_frame_31.jpg")

# Expand the dimensions of the image to 4
image_expand = tf.expand_dims(image, axis=0)

prediction = model.predict(image_expand)
print(prediction)
predicted_class_idx = tf.argmax(prediction[0])
predicted_class = class_indices[predicted_class_idx.numpy()]

print(f"Predicted class: {predicted_class}")
