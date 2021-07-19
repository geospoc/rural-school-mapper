# Objective
Detection of Zilla Parishad(ZP) School(s) from Satellite basemap imagery under the Guidence of UNICEF Data Science Team (https://www.unicef.org/innovation/innovation-fund-geospoc-geospatial)

# Licence
GNU AGPLv3 https://choosealicense.com/licenses/agpl-3.0/
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
<[![Coverage Status](https://coveralls.io/repos/github/geospoc/unc-sch-01/badge.svg?branch=master)](https://coveralls.io/github/geospoc/unc-sch-01?branch=master)>
[![Coverage Status](https://coveralls.io/repos/github/geospoc/rural-school-mapper/badge.svg?branch=master)](https://coveralls.io/github/geospoc/rural-school-mapper?branch=master)
# School Detection using Remotely Sensed(RS) Satellite Imagery

RS Imagery can be used for multiple applications amongst which building and road detection are common. But School detection is one of the complex problems that needs to be addressed given the variety of features they cover. This repository marks the begining of the school detection project in this direction.



# Satellite Data Download Mechanism

The data for the schools is input in the form of POI's in the csv file. The user has to input the csv file for downloading mapbox  data at specific Latitude & Longitude for training data.The csv file contains necessary Latitude and Longitude and accordingly the script loads csv file and downloads the tiles at zoom level 17 from Mapbox.


# Mask Generation

Mask for each image(tile) is obtained using **roi-poly** package in Python.The data path inside the directory needs to be changed inside **label_unicef.py** file as **dpath** and target directory where mask is stored as **mpath** then the image will be plotted on the window and user can label out the area for school.


# Model Training

The model training and prediction phase utilises the satellite unet model implemented through **keras-unet** package.The script utilises the following packages :

* keras
* keras-unet
* scikit-image
* PIL
* matplotlib

The script is tested with keras 2.3.1 with tensorflow 1.15.2. 
For inference,the weights are available inside the weights directory.
