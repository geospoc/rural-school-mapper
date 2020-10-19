# unc-sch-01
Github Repo for the UNICEF School project


# School Detection using Remotely Sensed Satellite Imagery

Remotely Sensed Imagery can be used for multiple applications and amongst which building and road detection are the key ones.But School detection is one of the complex problems that needs to be addressed given the variety of features they cover.This repository marks the begining of the school detection project in this direction.



# Data Download Mechanism

The data for the schools is input in the form of POI's in the csv file. The csv file contains necessary Latitude and Longitude and accordingly the script loads csv file and downloads the tiles at zoom level 17 from mapbox.


# Maks Generation

Masks for each image downloaded through the mapbox are generated using python utilising **roi-poly** package.
