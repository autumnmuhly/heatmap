#!/usr/bin/env python

#combine station and gridpoint for heatmap
import os
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib import cm
from math import radians, cos, sin, asin, sqrt, pi
from mpl_toolkits.mplot3d import Axes3D
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import datetime
import sys
import jsonpickle
import heatmap

#THIS IS WHERE YOU CAN DECIDED WHICH PHASES YOU ARE INTERESTED IN
phase='SKS'
#DIRECTORIRES

#Mesh parameters
number_points=1000

# min stations within gridpoint radius to pass
min_station=1

# min eq per array to pass
min_eq_needed=0


'----------------------------'
#DO NOT CHANGE BELOW HERE
'---------------------------'
radius_of_earth=6378


#List of phases- Will add more
if phase == 'SKS':
    dist=(0,30)
elif phase == 'SKKS':
    dist=(85,170)
elif phase =='S3KS':
    dist=(110,175)
elif phase =='S4KS':
    dist=(130,175)
else:
    print('add phase to list')

#Get complete grid points and scale to Earth - come up with what is a reasonable number. why 1000? spacing should represent array size

grid_array=heatmap.create_gridpoint(number_points)

#Now lets load in our station data
#need to check for NA or empty ???
station_list=heatmap.read_stations_adept('tests/resources/test_stations_lat.txt')
print('loaded in sta data')
#construst arrays for every gridpoint
radius_point_deg=heatmap.radius_per_gridpoint(number_points)
print(radius_of_earth)


min_station=1
print(f"attemp array form arrays for min {min_station} station in {radius_point_deg} deg")


array_list=heatmap.form_all_array(station_list,grid_array,radius_point_deg,min_station)

print(f"formed {len(array_list)} arrays for min {min_station} station in {radius_point_deg} deg")


if len(array_list) == 0:
    print(f"no arrays pass for radius {radius_point_deg} deg with  min {min_station} stations")
    sys.exit(1)


#form arrays


print(datetime.datetime.now())
array_list=heatmap.form_all_array(station_list,grid_array,radius_point_deg,min_station)
print(datetime.datetime.now())
#now we want to load in our earthquake data
eq_list=heatmap.read_earthquakes_adept('tests/resources/test_earthquakes.txt')
print('loaded in eq data')

#loop over evts and arrays and check if distance range is met
print('starting arr-evt calculation')
for arr in array_list:
    for evt in eq_list:
        arr.check_eq(evt,dist)
print('finished arr-evt calculation')


#loop over array in array list to decided if enough stations exist to be considered an array
good_arrays=[]
for arr in array_list:
    if arr.eqcount>=min_eq_needed:
        good_arrays.append(arr)

if len(good_arrays) == 0:
    print(f"no arrays pass min eq {min_eq_needed} for radius {radius_point_deg} deg")


mydata={
    "grid_array": grid_array,
    "good_arrays": good_arrays,
    "phase": phase,
    "dist": dist,
    "min_sta_per_array": min_station,
    "min_eq_at_array": min_eq_needed,
    "eq_list": eq_list,
    "station_list": station_list,
    "radius_of_earth": radius_of_earth
}

outfilename = "outfile.json"
with open(outfilename, "w") as outf:
    outf.write(jsonpickle.encode(mydata))
