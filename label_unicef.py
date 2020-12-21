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

#Give a path of Input png's
dpath="/Input/input.png"

x=Image.open(dpath)

im=np.array(x)
im=im[:,:,0]
plt.imshow(im)
my_roi = RoiPoly(color='r')

mask = my_roi.get_mask(im)
f_img=Image.fromarray(mask)

#Output path of mask
path="/mask/"

# Save mask to the path
f_img.save(path+dpath.split('/')[2].split('.')[0]+".jpg")