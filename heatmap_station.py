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

print('made it to the grid')
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
print('made it station ')


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


#each station will get a point if an earthquake occurs in the right distance, in the right time frame
#eq_yes=[0]*(len(station_lat))
eq_yes=dict()
max_value=0
for sta in station_list:
    count=0
    for evt in eq_list:
        #Check if earthquake and station existed at the same 
        if sta.start<evt.time<sta.stop:
            dist=heatmap.DistAz(evt.loc.lat,evt.loc.lon,sta.loc.lat,sta.loc.lat)
            gc=dist.delta
            print(f'gcarc distance betwen {sta} and {evt} is {gc}')
            if min_dis<gc<max_dis:
                count+=1
                print('we added one')
    eq_yes[sta]=count
    max_value=max(count,max_value)

#refernce points
north_pole=heatmap.Location(90,0)
south_pole=heatmap.Location(-90,0)

#Plot on sphere of earth
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
norm=plt.Normalize(0,max_value)

for sta in station_list:
    print(eq_yes[sta])
    station_scatter=ax.scatter(sta.loc.cart.x, sta.loc.cart.y, sta.loc.cart.z, c=eq_yes[sta], cmap = cm.cool, norm=norm, alpha=1, s=50)
cbar = fig.colorbar(station_scatter)
cbar.set_label('Number of earthquakes in SKS range', rotation=90)
#ax.scatter(x_com, y_com, z_com, color='green', s=2)

for evt in eq_list:
    ax.scatter(evt.loc.cart.x,evt.loc.cart.y,evt.loc.cart.z,color='red',s=100)

ax.scatter(north_pole.cart.x,north_pole.cart.y,north_pole.cart.z,color='yellow',s=100)
ax.scatter(south_pole.cart.x,south_pole.cart.y,south_pole.cart.z, color='yellow',s=100, label='North and South Pole')

for pt in grid_array:
    ax.scatter(pt.loc.cart[0],pt.loc.cart[1],pt.loc.cart[2],color='blue',s=2)
ax.set_box_aspect([radius_of_earth,radius_of_earth,radius_of_earth])

#plot on 2D map 
plt.figure()
ax = plt.axes(projection=ccrs.PlateCarree())
#ax.coastlines(resolution='10m')
ax.add_feature(cfeature.OCEAN, color='lightskyblue')
ax.add_feature(cfeature.LAND, color="oldlace")
#ax.add_feature(cfeature.LAKES, facecolor='lightblue')
#ax.add_feature(cfeature.STATES, linestyle=':', edgecolor='black', linewidth=0.5)
#ax.set_extent([-85.5, -80.5, 37, 41], crs=ccrs.PlateCarree())
gridlines=ax.gridlines(draw_labels=True, alpha=.80)
for sta in station_list:    
    station_scatter=plt.scatter(sta.loc.lon,sta.loc.lat, marker='v', s=50, c=eq_yes[sta],cmap=cm.cool, transform=ccrs.PlateCarree())
cbar = fig.colorbar(station_scatter)
cbar.set_label('Number of earthquakes in SKS range', rotation=90)
for evt in eq_list:
    plt.scatter(evt.loc.lon,evt.loc.lat,marker='o',s=50,color='#06470c')
for pt in grid_array:
    plt.scatter(pt.loc.lon,pt.loc.lat,marker='o',s=2,color='blue')

#plt.show()


#find distance betweent two grid points 
#find the area of the sphere
area_per_point=(4*pi*radius_of_earth*radius_of_earth)/number_points
print(f'each grid point represents about {area_per_point}km on the Earth')
#raidus of the circle on the earth isnt flat but is okay when points are large in number 
radius_point=sqrt(area_per_point/pi)
print(f'The radius of each grid point {radius_point}km')

#Calculate distance between points 





