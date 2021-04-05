# -*- coding: utf-8 -*-
"""
Script for conversion of linestring geojsons to polygons
This script keeps polygons having an area of minimum 500 sq.m. only and rest are discarded.
@author: SHUBHAM
"""

import os
import geopandas as gpd
from shapely.geometry import mapping,Polygon
import glob
import re



#This function converts linestrings to polygons
def line_to_poly(shps):
    gdf = gpd.read_file(shps) 
    geom = [x for x in gdf.geometry]
    coords = mapping(geom[0])['coordinates']
    mm=[]
    for cs in coords:
        
        lats = [i[1] for i in cs ]
        lons = [i[0] for i in cs ]
        if (len(lats) and len(lons)) >2:
            polyg = Polygon(zip(lons, lats))
            mm.append(polyg)
        
    return gpd.GeoDataFrame(crs=gdf.crs, geometry=mm)

#Target directory where geojsons will be stored
tar='D:\\Final_ahmednagar_polygons\\'

gjsons = sorted(glob.glob('D:\\Final_Geojsons_Ahmednagar\*'), key=lambda x:float(re.findall("(\d+)",x)[0]))
c=0
for gj in gjsons:
    
    poly=line_to_poly(gj)
    post = poly.copy()
    post= post.to_crs({'init': 'epsg:3857'})
    post["area"] = post['geometry'].area

    result_df=post[post["area"]>500]
    if len(result_df)>0:
        result_df.to_crs({'init': 'epsg:4326'}).to_file(tar+os.path.split(gj)[1].split('.')[0]+'.geojson', driver='GeoJSON')
        print('Geojson Created no. {}'.format(c))
    
    else:
        print("Geojson Not created no. {}".format(c))
        
    c+=1
    
    
    

