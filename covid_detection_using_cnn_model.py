# -*- coding: utf-8 -*-
"""Covid detection using CNN model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kUIi7xy5PLyCq5H_leIxdk-oJTSpuKzj

Importing libraries for the model
"""

from google.colab import drive
drive.mount('/content/drive')

import numpy as np 
import pandas as pd
import PIL
from imageio import imread
from skimage.transform import resize

import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential,Model
from tensorflow.keras.layers import Dense, GRU, Flatten, TimeDistributed, Flatten, BatchNormalization, Activation,Dropout
from tensorflow.keras.layers import Conv3D, MaxPooling3D,Conv2D, MaxPooling2D, LSTM, GRU  
from tensorflow.keras import optimizers

import os
import matplotlib.pyplot as plt

import pathlib
covid_dir=pathlib.Path('/content/drive/MyDrive/archive(3)/COVID')
noncovid_dir=pathlib.Path('/content/drive/MyDrive/archive(3)/non-COVID')

count_covid=len(list(covid_dir.glob('*.png')))
count_noncovid=len(list(noncovid_dir.glob('*.png')))
print(count_covid)
print(count_noncovid)

pip install split-folders

import splitfolders
splitfolders.ratio('/content/drive/MyDrive/archive(3)',output='/content/drive/MyDrive/Colab Notebooks/split',seed=1337,ratio=(.7,.2,.1),group_prefix=None, move=False)

dir_test=pathlib.Path('/content/drive/MyDrive/Colab Notebooks/split/test')
dir_train=pathlib.Path('/content/drive/MyDrive/Colab Notebooks/split/train')
dir_val=pathlib.Path('/content/drive/MyDrive/Colab Notebooks/split/val')

covid=list(dir_test.glob('COVID/*'))
PIL.Image.open(str(covid[0]))

image=PIL.Image.open(str(covid[0]))
print(image.size)

from google.colab.patches import cv2_imshow
import cv2
image1=cv2.imread(str(covid[0]))
cv2_imshow(image1)

def data_generator(data_source,img_height, img_width, btc_size):    
    return tf.keras.utils.image_dataset_from_directory(
        data_source,
        validation_split=None,
        subset=None,
        seed=123,
        color_mode='grayscale',
        image_size=(img_height, img_width),
        batch_size=btc_size,
        crop_to_aspect_ratio=True,
        shuffle=True
    )

batch_size=32
image_height=256
image_width=256
train_ds=data_generator(dir_train,image_height,image_width,batch_size)

test_ds=data_generator(dir_test,image_height,image_width,batch_size)
val_ds=data_generator(dir_val,image_height,image_width,batch_size)

print(train_ds.class_names)

batch_size=32
img_height = 256
img_width = 256
num_epochs = 30

model = Sequential([
  layers.Rescaling(1./255, input_shape=(img_height, img_width, 1)),
  layers.Conv2D(16, 3, padding='same', activation='relu'),
  layers.BatchNormalization(),
  layers.MaxPooling2D(),
  layers.Conv2D(32, 3, padding='same', activation='relu'),
  layers.BatchNormalization(),
  layers.MaxPooling2D(),
  layers.Conv2D(64, 3, padding='same', activation='relu'),
  layers.BatchNormalization(),
  layers.MaxPooling2D(),
  layers.Dropout(0.2),
  layers.Flatten(),
  layers.Dense(128, activation='relu'),
  layers.Dense(2)
])

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
               metrics=['accuracy'])

model.summary()

from keras.callbacks import ModelCheckpoint

filepath="/content/drive/MyDrive/Colab Notebooks/saved_models/weights_improvement-{epoch:05d}-{loss:.5f}-{accuracy:.5f}-{val_loss:.5f}-{val_accuracy:.5f}.h5"

checkpoint = ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=True, save_weights_only=False, mode='auto')

from tensorflow.keras.callbacks import ReduceLROnPlateau
LR = ReduceLROnPlateau(monitor='val_loss', factor=0.01, patience=5, cooldown=4, verbose=1,mode='auto',min_delta=0.0001)

callbacks_list=[checkpoint,LR]



history = model.fit(train_ds, epochs=num_epochs, verbose=1, 
                    callbacks=callbacks_list, validation_data=val_ds, 
                    class_weight=None, initial_epoch=0)

acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']

    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs_range = range(num_epochs)

    plt.figure(figsize=(8, 8))
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, acc, label='Training Accuracy')
    plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')

    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    plt.show()

