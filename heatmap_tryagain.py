#autumnmuhly

import os
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib import cm
from math import radians, cos, sin, asin, sqrt, pi
from mpl_toolkits.mplot3d import Axes3D
import cartopy.crs as ccrs
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
    min_dis=10
    max_dis=40


#Get complete grid points and scale to Earth - come up with what is a reasonable number. why 1000? spacing should represent array size

grid_array=heatmap.create_gridpoint(number_points)

print('made it to the grid')
#Now lets load in our station data  
os.chdir('/Users/autumnmuhly/Work/outercore/programs/SmKS/eventdir/adept/info') #gonna have to change this to be current working directory 
df = pd.read_csv('All_stations.txt', sep=" ", header=None)
df = df.iloc[1:]  #Have to get rid of first row cause its a second header 

station_lat=df[3].astype(float).to_numpy()
station_lon=df[4].astype(float).to_numpy()


station_start=pd.to_datetime(df[7])
station_end=pd.to_datetime(df[8])
#need to check for NA or empty ???


station=heatmap.Station(heatmap.Location(station_lat,station_lon),station_start,station_end)
print('made it to the station ')
print(station.loc.cart.x[3])
print(station.start[3])

#now we want to go through our list of earthquakes and if our phase of interest doesn't exist there we want to get rid of that station 
os.chdir('/Users/autumnmuhly/Work/outercore/programs/SmKS/scriptsdir/heatmap_scripts') #gonna have to change this to be current working directory 
events = pd.read_csv('test_earthquakes.txt', sep=" ", header=None)
events= events.iloc[1:]  #Have to get rid of first row cause its a second header 

events_lat=events[5].astype(float).to_numpy()
events_lon=events[6].astype(float).to_numpy()

event_time=pd.to_datetime(events[1])

eq=heatmap.EQ(heatmap.Location(events_lat,events_lon),event_time)


#each station will get a point if an earthquake occurs in the right distance, in the right time frame
eq_yes=[0]*(len(station_lat))
for j in range(len(station_lat)):
    for i in range (len(event_time)):
        #Check if earthquake and station existed at the same 
        ev_time=event_time.iloc[i]
        test_start=station_start.iloc[j]
        test_end=station_end.iloc[j]
        if test_start<ev_time<test_end:
            dist=DistAz(events_lat[i],events_lon[i],station_lat[j],station_lon[j])
            gc=dist.delta
            if min_dis<gc<max_dis:
                eq_yes[j]+=1
        
#np.savetxt('eq_yes',eq_yes)



#if there are stations (lat and longs) with earthquakes then we can calculate the station density 


#Convert station lat/lon to cartesian


x_stations,y_stations,z_stations=heatmap.latlon_cartesian(station_lat,station_lon)


#Testing our conversions with trying to plot hawaii, north/south pole and some other stuff
north_pole=heatmap.Location(90,0)
south_pole=(-90,0)
hawaii=(19.90,-155.67)
#convert sac lat/lon to cartesian 

x_south,y_south,z_south=latlon_cartesian(south_pole[0],south_pole[1])
x_hawaii,y_hawaii,z_hawaii=latlon_cartesian(hawaii[0],hawaii[1])
x_eq,y_eq,z_eq=latlon_cartesian(events_lat,events_lon)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
station_scatter=ax.scatter(x_stations, y_stations, z_stations, c=eq_yes, cmap = cm.cool, alpha=1, s=2, label="Stations")
cbar = fig.colorbar(station_scatter)
cbar.set_label('Number of earhquakes in SKS range', rotation=90)
#ax.scatter(x_com, y_com, z_com, color='green', s=2)
ax.scatter(x_eq,y_eq,z_eq,color='red',s=100)
ax.scatter(north_pole.cart.x,north_pole.cart.y,north_pole.cart.z,color='yellow',s=100)
ax.scatter(x_south,y_south,z_south, color='yellow',s=100, label='North and South Pole')
ax.scatter(x_hawaii,y_hawaii,z_hawaii,color='yellow',s=100,label='Hawaii')
ax.set_box_aspect([radius_of_earth,radius_of_earth,radius_of_earth])
ax.legend()
plt.show()



#Now I actually want to put values in each grid point and color those based on grid points and not station plots
eq_yes=[0]*(len(station_lat))
for j in range(len(station_lat)):
    for i in range (len(event_time)):
        #Check if earthquake and station existed at the same 
        ev_time=event_time.iloc[i]
        test_start=station_start.iloc[j]
        test_end=station_end.iloc[j]
        if test_start<ev_time<test_end:
            dist=DistAz(events_lat[i],events_lon[i],station_lat[j],station_lon[j])
            gc=dist.delta
            if min_dis<gc<max_dis:
                eq_yes[j]+=1
                

#Convert cartesian to lat and long to find distances using DistAz?
def distance_between_cartesian(p1_x,p1_y,p1_z,p2_x,p2_y,p2_z):
    dist=sqrt((p2_x-p1_x)**2+(p2_y-p1_y)**2+(p2_z-p1_z)**2)

#find distance betweent two grid points 
#find the area of the sphere
area_per_point=(4*pi*radius_of_earth*radius_of_earth)/number_points
print(f'each grid point represents about {area_per_point}km on the Earth')
#raidus of the circle on the earth isnt flat but is okay when points are large in number 
radius_point=sqrt(area_per_point/pi)
print(f'The radius of each grid point {radius_point}km')

#Calculate distance between points 






