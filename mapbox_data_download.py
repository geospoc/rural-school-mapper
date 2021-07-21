# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 13:31:13 2021

@author: SHUBHAM
"""

#!/usr/bin/env python
# coding: utf-8
#@author: SHUBHAM SHARMA
#This code is covered under GNU AGPL license
#This script downloads the mapbox tiles as per the Points of interest(POI's)
#stored in Excel file(.xlsx).
#The mapbox access token for the account is requored to access the raster API

import os
import pandas as pd
import mercantile
import requests
import shutil
#from dotenv import load_dotenv

#load_dotenv('/home/runner/work/rural-school-mapper/rural-school-mapper/.env')
#Create an output folder to store images
# Read POI's from Excel file containing Fields 'Latitude' and 'Longitude'
def mapbox_download(poi,MAT):
    
    #poi=pd.read_excel("/POI's.xlsx")
    #path to store images
    print(poi.shape)
    outpath=os.getenv("DATA")
    stat_list=[]
    
    for index,df in poi.iterrows():
        
        lat_long=[df['Latitude'],df['Longitude']]
        delta = 0                 #0.0005 for downloading as it will give all the tiles related to the specified lat-lon
        top_left = [lat_long[0]+delta, lat_long[1]-delta]
        bottom_right = [lat_long[0]-delta, lat_long[1]+delta]
        z = 17 # Zoom level
        
        #Finding tiles 
        top_left_tiles = mercantile.tile(top_left[1],top_left[0],z)
        bottom_right_tiles = mercantile.tile(bottom_right[1],bottom_right[0],z)
        
        x_tile_range = [top_left_tiles.x,bottom_right_tiles.x]
        y_tile_range = [top_left_tiles.y,bottom_right_tiles.y]
        print(x_tile_range)
        print(y_tile_range)
       
        
        for i,x in enumerate(range(x_tile_range[0],x_tile_range[1]+1)):
            for j,y in enumerate(range(y_tile_range[0],y_tile_range[1]+1)):
                print(x,y)
                
                r = requests.get('https://api.mapbox.com/v4/mapbox.satellite/'+str(z)+'/'+str(x)+'/'+str(y)+'@2x.png?access_token='+MAT, stream=True)
                if r.status_code == 200:
                    #Put path of output folder
                    with open(outpath +str(index)+'.'+str(lat_long[1]) + '.' + str(lat_long[0]) + '.png', 'wb') as f:
                        r.raw.decode_content = True
                        shutil.copyfileobj(r.raw, f)
        
                        stat_list.append(r.status_code)   
    print(stat_list)             
    return stat_list    
        

def test_download():
    test=pd.read_csv(os.getenv("DATA")+'mapbox_test.csv')
    #print("CSV:  ",os.getenv("DATA")+'mapbox_test.csv')
    #access token
    MAT=os.getenv("MAT")
    assert mapbox_download(test,MAT)==[200]*test.shape[0]
    
    
    



#MAPBOX_ACCESS_TOKEN 