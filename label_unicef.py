# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 16:54:58 2020

@author: SHUBHAM
"""

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