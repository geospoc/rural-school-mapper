#!/usr/bin/env python
# coding: utf-8




import pandas as pd
import mercantile
import requests
import shutil

#Create an output folder to store images
# Read POI's from Excel file containing Fields 'Latitude' and 'Longitude'
poi=pd.read_excel("/POI's.xlsx")

for index,df in poi.iterrows():
    
    lat_long=[df['Latitude'],df['Longitude']]
    delta = 0.0005
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
            
            r = requests.get('https://api.mapbox.com/v4/mapbox.satellite/'+str(z)+'/'+str(x)+'/'+str(y)+'@2x.png?access_token=MAPBOX_ACCESS_TOKEN', stream=True)
            if r.status_code == 200:
                #Put path of output folder
                with open('U:\\output\\' +str(index)+'.'+str(lat_long[1]) + '.' + str(lat_long[0]) + '.png', 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)


