# -*- coding: utf-8 -*-
#@author: SHUBHAM
#This script is covered under GNU AGPL License.
#This script utilises kerasunet package for training school data.
#It utilises Tensorflow 1.15.2.
# For appropriate training utilise adequate hyperparameters.

# Importing necessary libraries
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import sys
from PIL import Image
from keras_unet.utils import plot_imgs
from sklearn.model_selection import train_test_split
from keras_unet.utils import get_augmented
from keras_unet.utils import plot_imgs
from keras_unet.models import satellite_unet
from keras.callbacks import EarlyStopping,ModelCheckpoint
from keras.optimizers import Adam, SGD
from keras_unet.metrics import iou, iou_thresholded
from keras_unet.losses import jaccard_distance



# Each mapbox image fed to the Unet is a 512x512 3-channel(RGB image)
#The masks are one channel binary images having area of interest

# Binary masks containing area of Interest and images
masks = sorted(glob.glob("/filepath/*.jpg"))
imgs = sorted(glob.glob("filepath/*.png"))


# Generating numpy arrays
images_list = []
masks_list = []
for image, mask in zip(imgs,masks):
    
    images_list.append(np.array(Image.open(image)))
    im = Image.open(mask)
    masks_list.append(np.array(im))

images_np = np.asarray(images_list)
masks_np = np.asarray(masks_list)


# Verifying one to one correspondence between masks and images
mask1=[os.path.split(i)[1].split('.')[0] for i in masks]
imgur=[os.path.split(i)[1].split('.')[0] for i in imgs]

print(images_np.shape, masks_np.shape)
print(mask1==imgur)


#Plot Images
plot_imgs(org_imgs=images_np, mask_imgs=masks_np, nm_img_to_plot=10, figsize=6)

print(images_np.max(), masks_np.max())


# Rescaling image intensity values 

x = np.asarray(images_np, dtype=np.float32)/255
y = np.asarray(masks_np, dtype=np.float32)/255 


# Reshaping the masks

y = y.reshape(y.shape[0], y.shape[1], y.shape[2], 1)
print(x.shape, y.shape)



#Splitting Training and Testing data
x_train, x_val, y_train, y_val = train_test_split(x, y, test_size=0.2, random_state=0)

print("x_train: ", x_train.shape)
print("y_train: ", y_train.shape)
print("x_val: ", x_val.shape)
print("y_val: ", y_val.shape) 



#Perform Data Augmentation to make appropriate changes to data
#performing various operations such as rotation,flip etc.

train_gen = get_augmented(
    x_train, y_train, batch_size=16,
    data_gen_args = dict(
        rotation_range=15.,
        width_shift_range=0.05,
        height_shift_range=0.05,
        shear_range=50,
        zoom_range=0.2,
        horizontal_flip=True,
        vertical_flip=True,
        fill_mode='constant'
    )) 

#Plot images with mask overlays 
batch = next(train_gen)
xx, yy = batch
print(xx.shape, yy.shape)
plot_imgs(org_imgs=xx, mask_imgs=yy, nm_img_to_plot=5, figsize=6)


# Importing Satellite Unet model from the keras_unet package

input_shape = x_train[0].shape

model = satellite_unet(
    input_shape,
    num_classes=1,
    output_activation='sigmoid',
    num_layers=4
)



#Creating Checkpoint
model_filename = '/model.h5'
callback_checkpoint =ModelCheckpoint(
    model_filename, 
    verbose=1, 
    monitor='val_loss', 
    save_best_only=True,
)



#Compiling the model with appropriate optimizer

model.compile(
    
    optimizer=SGD(lr=0.01, momentum=0.99),
    loss='binary_crossentropy',
    metrics=[iou, iou_thresholded]
)



#Early Stopping criterion upto mentioned epochs
earlystopper = EarlyStopping(patience=3, verbose=1)


#Training model for 10 epochs with earlystopping criterion
history = model.fit_generator(
    train_gen,
    steps_per_epoch=30,
    epochs=10,
    
    validation_data=(x_val, y_val),
    callbacks=[earlystopper,callback_checkpoint]
)




#Predictions
model.load_weights(model_filename)
y_pred = model.predict(x_val)


#Plot Predicted Images
plot_imgs(org_imgs=x_val, mask_imgs=y_val, pred_imgs=y_pred, nm_img_to_plot=5)


