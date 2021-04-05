# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 17:06:47 2021

@author: SHUBHAM
"""

import os
import glob
import re
import boto3
import tensorflow as tf
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from skimage.filters import threshold_otsu
from keras_unet.models import satellite_unet
from keras.callbacks import ModelCheckpoint
from keras.optimizers import Adam, SGD
from keras_unet.metrics import iou, iou_thresholded
from keras_unet.losses import jaccard_distance
from keras import metrics


#Directory where input mapbox tiles are stored in the form id_mapboxtileX_mapboxtileY
#for example 0_.92788.58757.png
ll=glob.glob('mapbox_ahmednagar/*')


files = sorted(ll, key=lambda x:float(re.findall("(\d+)",x)[0]))
#print(files)


#Define model

input_shape = (512,512,3)

model = satellite_unet(
    input_shape,
    #use_batch_norm=False,
    num_classes=1
    ,
    #filters=64,
    #dropout=0.2,
    output_activation='sigmoid',
    num_layers=4
)


#Callbacks
model_filename ='/New_tuned_weights_ker_chen_mepochs.h5'
callback_checkpoint = ModelCheckpoint(
    model_filename, 
    verbose=1, 
    monitor='val_loss', 
    save_best_only=True,
)



#Compile the model
model.compile(
    #optimizer=Adam(), 
    optimizer=SGD(lr=0.01, momentum=0.99),
    loss='binary_crossentropy',
    #loss=jaccard_distance,
    metrics=[iou, iou_thresholded,metrics.binary_accuracy,metrics.Accuracy()]
)


model.load_weights(model_filename)

#Directory which will contain thresholded masks
os.mkdir('/threshold_masks')




s3 = boto3.resource('s3')
no_pred=[]
tar='threshold_masks/'

#The results will get stored in an s3 bucket having directory called thresholded masks.
for image in files:
    print(image)
    #break
    imgs_list = []
    imgs_list.append(np.array(Image.open(image)))#.convert('L')),(256,256)))#.resize((512,512))))
    #print(imgs_list[0].shape)
    x_val = np.asarray(imgs_list)
    
    y_pred = model.predict(x_val)
    #print(y_pred.shape)
    try:
        thresh=threshold_otsu(y_pred[0,:,:,0])
    except ValueError :
        print("No prediction here")
        pass
    
    binary=y_pred[0,:,:,0]>thresh
    binary=binary*1
    np.save(tar+image.split('/')[-1].split('.png')[0]+'.npy',binary.astype('int8'))
    s3.meta.client.upload_file(tar+image.split('/')[-1].split('.png')[0]+'.npy', 'bucket_name', 'single_class_thresh_masks/'+image.split('/')[-1].split('.png')[0]+'.npy')
    os.remove(tar+image.split('/')[-1].split('.png')[0]+'.npy')
    

