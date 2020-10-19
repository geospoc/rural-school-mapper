# Objective
Detection of Zilla Parishad(ZP) School(s) from Satellite basemap imagery under the Guidence of UNICEF Data Science Team (https://www.unicef.org/innovation/innovation-fund-geospoc-geospatial)

# Licence
GNU AGPLv3 https://choosealicense.com/licenses/agpl-3.0/

# School Detection using Remotely Sensed Satellite Imagery

Remotely Sensed Imagery can be used for multiple applications and amongst which building and road detection are the key ones.But School detection is one of the complex problems that needs to be addressed given the variety of features they cover.This repository marks the begining of the school detection project in this direction.



# Data Download Mechanism

The data for the schools is input in the form of POI's in the csv file. The csv file contains necessary Latitude and Longitude and accordingly the script loads csv file and downloads the tiles at zoom level 17 from mapbox.


# Mask Generation

Masks for each image downloaded through the mapbox are generated using python utilising **roi-poly** package.


# Model Training

The model training and prediction phase utilises the satellite unet model implemented through **keras-unet** package.The script utilises the following packages :


* keras
* keras-unet
* scikit-image
* PIL
* matplotlib

The script is tested with keras 2.3.1 with tensorflow 1.15.2 
