#combine station and gridpoint for heatmap
import os
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib import cm
from math import radians, cos, sin, asin, sqrt, pi
from mpl_toolkits.mplot3d import Axes3D
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from datetime import date
import heatmap

#THIS IS WHERE YOU CAN DECIDED WHICH PHASES YOU ARE INTERESTED IN 
phase='SKS'
#DIRECTORIRES 

#Mesh parameters
number_points=1000

'----------------------------'
#DO NOT CHANGE BELOW HERE
'---------------------------'
radius_of_earth=6378


#List of phases- Will add more 
if phase == 'SKS':
    min_dis=0
    max_dis=65


#Get complete grid points and scale to Earth - come up with what is a reasonable number. why 1000? spacing should represent array size

grid_array=heatmap.create_gridpoint(number_points)

#Now lets load in our station data  
os.chdir('/Users/autumnmuhly/Work/outercore/programs/SmKS/scriptsdir/heatmap_scripts') #gonna have to change this to be current working directory 
df = pd.read_csv('test_stations.txt', sep=" ", header=None)
df = df.iloc[1:]  #Have to get rid of first row cause its a second header 
station_lat=df[3].astype(float).to_numpy()
station_lon=df[4].astype(float).to_numpy()
station_start=pd.to_datetime(df[7]).to_list()
station_end=pd.to_datetime(df[8]).to_list()
#need to check for NA or empty ???

station_list=[]
for i in range(len(station_lat)):
    sta=heatmap.Station(heatmap.Location(station_lat[i],station_lon[i]),station_start[i],station_end[i])
    station_list.append(sta)


#now we want to go through our list of earthquakes and if our phase of interest doesn't exist there we want to get rid of that station 
os.chdir('/Users/autumnmuhly/Work/outercore/programs/SmKS/scriptsdir/heatmap_scripts') #gonna have to change this to be current working directory 
events = pd.read_csv('test_earthquakes.txt', sep=" ", header=None)
events= events.iloc[1:]  #Have to get rid of first row cause its a second header 
events_lat=events[5].astype(float).to_numpy()
events_lon=events[6].astype(float).to_numpy()
event_time=pd.to_datetime(events[1]).to_numpy()

eq_list=[]
for i in range(len(events_lat)):
    eq=heatmap.EQ(heatmap.Location(events_lat[i],events_lon[i]),event_time[i])
    eq_list.append(eq)

area_per_point=(4*pi*radius_of_earth*radius_of_earth)/number_points
radius_point_km=sqrt(area_per_point/pi)
radius_point_deg=radius_point_km/111
eq_yes=dict()
array_yes=dict()
max_value=0
for pt in grid_array:
    count=0
    for evt in eq_list:
            dist=heatmap.DistAz(evt.loc.lat,evt.loc.lon,pt.loc.lat,pt.loc.lon)
            gc=dist.delta
            if min_dis<gc<max_dis:
                count+=1
                for sta in station_list:
                     dis_pt_sta=heatmap.DistAz(pt.loc.lat,pt.loc.lon,sta.loc.lat,sta.loc.lon)
                     pt_sta=dis_pt_sta.delta
                     if pt_sta<=radius_point_deg:
                          print(" potiental subarray. need to check if station was alive during quake")
                          if sta.start<evt.time<sta.stop:
                               print('station was alive') #need to check somewhere how many other stations were alive
                          else:
                               print('station was not alive')
    eq_yes[pt]=count
    max_value=max(count,max_value)

        