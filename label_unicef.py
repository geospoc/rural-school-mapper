# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 14:14:39 2021

@author: SHUBHAM
"""

# -*- coding: utf-8 -*-
#@author: SHUBHAM SHARMA
# This script is covered under GNU AGPL License.
#This script deals with labelling mapbox tiles 
#For the purpose of labelling each file needs to be open separately and labelled
#The script requires RoiPoly package in order to label the images
#Utilise the script to label each image via CLI(command Line interface)
#On CLI, the user should use command :
#python label_unicef.py


from PIL import Image
import matplotlib.pyplot as plt
from roipoly import RoiPoly
import numpy as np
import os

#Give a path of Input png's



def label(dpath,mpath):
    

    x=Image.open(dpath)
    
    im=np.array(x)
    im=im[:,:,0]
    plt.imshow(im)
    my_roi = RoiPoly(color='r')
    
    mask = my_roi.get_mask(im)
    f_img=Image.fromarray(mask)

    #Output path of mask
    

    # Save mask to the path
    f_img.save(mpath+dpath.split('/')[-1].split('.')[0]+".jpg")
    
    #return 1

def test():
    #path where image is stored in .png format-dpath
    #path where mask is going to be stored
    
    dpath=" "
    mpath=" "
    label(dpath,mpath)
    assert os.path.exists(mpath+dpath.split('/')[-1].split('.')[0]+".jpg")



