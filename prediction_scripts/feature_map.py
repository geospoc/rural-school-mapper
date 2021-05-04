# -*- coding: utf-8 -*-
"""
Created on Mon May  3 22:34:32 2021

@author: SHUBHAM
"""

import numpy as np
import matplotlib.pyplot as plt
import os
from keras_unet.models import satellite_unet
from keras.callbacks import ModelCheckpoint
from keras.optimizers import Adam, SGD
from keras_unet.metrics import iou, iou_thresholded
from keras import metrics
from keras.preprocessing.image import load_img,img_to_array
from keras.models import Model
import tensorflow as tf



#Define model here
input_shape=(512,512,3)


model = satellite_unet(
    input_shape,
    #use_batch_norm=False,
    num_classes=1,
    #filters=64,
    #dropout=0.2,
    output_activation='sigmoid',
    num_layers=4
)



#Model checkpoints
model_filename=''

callback_checkpoint = ModelCheckpoint(
    model_filename, 
    verbose=1, 
    monitor='val_loss', 
    save_best_only=True,
)






#Compile model here
model.compile(
    #optimizer=Adam(), 
    optimizer=SGD(lr=0.01, momentum=0.99),
    loss='binary_crossentropy',
    #loss=jaccard_distance,
    metrics=[iou, iou_thresholded,metrics.binary_accuracy,metrics.Accuracy()]
)



model_filename='weights.h5'

#Load weights
model.load_weights(model_filename)

#Dictionary of layers
dict_layer = dict([(layer.name, layer) for layer in model.layers])


#Directory for saving feature maps
path='E:\\maps\\'


for i in list(dict_layer.keys()):
    
    layer_name=i
    model_pred = Model(inputs=model.inputs, outputs=dict_layer[layer_name].output)
    image = load_img('IMAGE.PNG')

    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)

    with tf.device('/cpu:0'):
        feature_maps = model_pred.predict(image)
        
    os.mkdir(path+i)
    for index in range( feature_maps.shape[3]):
        plt.imshow(feature_maps[0, :, :, index], cmap='hot')

        plt.savefig(path+i+"\\"+str(index)+'.jpg')
		









