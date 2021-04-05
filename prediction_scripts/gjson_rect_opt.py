# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 16:13:16 2021

Script for optimisng rectangular envelopes around polygons.
Only those rectangles are retained which have length less than 200 m.

@author: SHUBHAM
"""

import os
import glob
import re
from shapely.geometry import LineString


import geopandas as gpd

#Target directory to store final geojsons
tar='D:\\test\\'


#Directory having original polygon geojsons
orig=sorted(glob.glob('D:\\Final_ahmednagar_polygons\\*'), key=lambda x:float(re.findall("(\d+)",x)[0]))
c=0

for file in orig:
    break
    
    rd=gpd.read_file(file)
    dfr=rd.copy()
    
    dfr['geometry']=dfr['geometry'].envelope
    
    dfrproj= dfr.to_crs({'init': 'epsg:3857'})
    dfr['length']=None
    
    for index,row in dfrproj.iterrows():
        
        btup=row['geometry'].bounds
        dfr.loc[index,'length']=LineString([(btup[0],btup[3]),(btup[2],btup[3])]).length

    del dfrproj
    result_df=dfr[dfr["length"]<200]
    result_df=result_df.drop(columns=['length'])
      
    if len(result_df)!=0:
        result_df.to_file(tar+os.path.split(file)[1].split('.')[0]+'.geojson',driver='GeoJSON') 
    else:
        print("Empty File no. {}".format(c))
    
    print("File no.{} processed".format(c))
    c+=1
    
    
   
    
