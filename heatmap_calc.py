#!/usr/bin/env python

#combine station and gridpoint for heatmap
import os
import math
from math import radians, cos, sin, asin, sqrt, pi
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
min_eq_needed=1


'----------------------------'
#DO NOT CHANGE BELOW HERE
'---------------------------'
radius_of_earth=6378

# Distance range of phase, from TauP
dist = heatmap.phase_dist_range(phase)
if dist is None:
    print(f"Cannot determine phase distance range for {phase}")
    sys.exit(0)
print(f"phase: {phase}  dist: {dist}")

#Get complete grid points and scale to Earth - come up with what is a reasonable number. why 1000? spacing should represent array size

grid_array=heatmap.create_gridpoint(number_points)

#Now lets load in our station data
#need to check for NA or empty ???
station_list=heatmap.read_stations_adept('tests/resources/test_stations_lat.txt')
print('loaded in sta data')
#construst arrays for every gridpoint
radius_point_deg=heatmap.radius_per_gridpoint(number_points)
print(radius_of_earth)

print(f"attemp array form arrays for min {min_station} station in {radius_point_deg} deg")


array_list=heatmap.form_all_array(station_list,grid_array,radius_point_deg,min_station)

print(f"formed {len(array_list)} arrays for min {min_station} station in {radius_point_deg} deg")


if len(array_list) == 0:
    print(f"no arrays pass for radius {radius_point_deg} deg with  min {min_station} stations")
    sys.exit(1)

#Load in our earthquake data
eq_list=heatmap.read_earthquakes_adept('tests/resources/test_earthquakes_lat.txt')

# a list of eq for all arrrays
arrayToeq=[]
#array class that will hold array-eq pairs class in prep for testing distance
for arr in array_list:
    arrayToeq.append(heatmap.ArrayToEqlist(arr))
#evt class that will holds eq-array pairs  
eqToarray=[]
for evt in eq_list:
    eqToarray.append(heatmap.EqtoArrayList(evt))
    
#loop over evts and arrays and check if distance range is met
for arr in arrayToeq:
    for evt in eq_list:
        arr.check_eq(evt,dist,min_station)


#loop over array in array list to decided if enough eq exist to be considered an array
good_arrays=[]
for arr in arrayToeq:
    if arr.eqcount>=min_eq_needed:
        good_arrays.append(arr)

if len(good_arrays) == 0:
    print(f"no arrays pass min eq {min_eq_needed} for radius {radius_point_deg} deg")


mydata={
    "array_list":array_list,
    "grid_array": grid_array,
    "good_arrays": good_arrays,
    "phase": phase,
    "dist": dist,
    "min_sta_per_array": min_station,
    "min_eq_at_array": min_eq_needed,
    "eq_list": eq_list,
    "station_list": station_list,
    "radius_point_deg": radius_point_deg,
    "radius_of_earth": radius_of_earth
}

outfilename = "outfile.json"
with open(outfilename, "w") as outf:
    outf.write(jsonpickle.encode(mydata))
