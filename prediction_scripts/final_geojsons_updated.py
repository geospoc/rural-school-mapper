# -*- coding: utf-8 -*-
"""
Script for conversion of mapbox predictions to geojsons.

@author: SHUBHAM

"""

import math
import rasterio
import glob
import re
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import find_contours
from PIL import Image
from shapely.geometry import mapping,Polygon,MultiLineString,LineString
from shapely import wkt
import fiona
from fiona.crs import from_epsg
import time
import shapely

#The input folder contains the predictions in the form of .npy files.
#Further, the naming of each .npy file should be in the form of "id_mapboxtileX_mapboxtileY.npy".
#For Example "0_92788_58757.npy", here 0 is the id, 92788 is the mapbox_x_tile_no. and 58757 is the mapbox_y_tile_no.
#It is very important that the tiles should be numbered in that manner,otherwise the georeferencing will be wrong or not possible.
masks = sorted(glob.glob('D:\\thresholded_masks\\*'), key=lambda x:float(re.findall("(\d+)",x)[0]))

z=17
n = 2**z
no_pred=[]
ctr=0
for ma in masks:
    #print(ma)
    t1=time.time()
    xtile=int(ma.split('\\')[-1].split('.npy')[0].split('.')[-2])
    ytile=int(ma.split('\\')[-1].split('.npy')[0].split('.')[-1])
    
    lon_deg = ((xtile / n)*360.0) - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - (2 * (ytile / n)))))
    lat_deg = lat_rad * (180.0 / math.pi)

    tx=rasterio.transform.from_origin(lon_deg,lat_deg,5.323955725076732e-06 ,5.323955725076732e-06)
    
    image=np.load(ma)
    out=find_contours(image,0.5)
    if not out :
        no_pred.append(ma)
        continue
    else:
        
        cs=[]
        fig, ax = plt.subplots()
        for contour in out:  
            cs.append(ax.plot(contour[:, 1], contour[:, 0], linewidth=2))
        
        plt.close()
        poly=[]
        for i in cs:
            
            x=i[0].get_xdata()
            y=i[0].get_ydata()
            aa=rasterio.transform.xy(tx,y,x)
            poly.append(LineString([(i[0], i[1]) for i in zip(aa[0],aa[1])]))
    
            
        list_polygons =  [wkt.loads(p.wkt) for p in poly]
    
        mult=shapely.geometry.MultiLineString(list_polygons)
    
    
        
        crs = from_epsg(4326)
    
        schema = {
            'geometry': 'MultiLineString',
            'properties': {'id': 'int','Name':'str'},
            
        }
        
        
        
        # Write a new Shapefile
        with fiona.open('D:\\Final_Geojsons_building_thresh\\'+ma.split('\\')[-1].split('.npy')[0].split('.')[0][:-1]+'.geojson', 'w', 'GeoJSON', schema,crs=crs) as c:
            ## If there are multiple geometries, put the "for" loop here
            #for ls in list_polygons:
                
            c.write({
                'geometry': mapping(mult),
                'properties': {'id': 1,'Name':'Detected School'},
            })

    t2=time.time()
    print("\nTime taken for {} th geojson : {} minutes".format(ctr,(t2-t1)/60))    
    ctr+=1