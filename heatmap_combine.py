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
station_list=heatmap.read_stations_adept('test_stations_lat.txt')
print('loaded in sta data')
#construst arrays for every gridpoint
area_per_point=(4*pi*radius_of_earth*radius_of_earth)/number_points
radius_point_km=sqrt(area_per_point/pi)
radius_point_deg=radius_point_km/111
print(radius_of_earth)
#form arrays
print(datetime.datetime.now())
min_station=1
array_list=heatmap.form_all_array(station_list,grid_array,radius_point_deg,min_station)
print(datetime.datetime.now())
#now we want to load in our earthquake data
eq_list=heatmap.read_earthquakes_adept('test_earthquakes.txt')
print('loaded in eq data')

#loop over evts and arrays and check if distance range is met 
print('starting arr-evt calculation')
for arr in array_list:
    for evt in eq_list:
        arr.check_eq(evt,dist)
print('finished arr-evt calculation')


#loop over array in array list to decided if enough stations exist to be considered an array
min_eq_needed=1
good_arrays=[]
for arr in array_list:
    print(arr.eqcount)
    if arr.eqcount>=min_eq_needed:
        good_arrays.append(arr)

if len(good_arrays) == 0:
    print(f"no arrays pass min eq {min_eq_needed} for radius {radius_point_deg} deg")

#some formatting things for our colorbar
eq_count=[0,1]
for arr in good_arrays:
    eq_count.append(arr.eqcount)
#need to put something here in case eq_count is empty
if len(eq_count)<1:
    print('there are no eq within range. change eq list')
    sys.exit()
max_value=max(eq_count)

print(eq_count)
#refernce points
north_pole=heatmap.Location(90,0)
south_pole=heatmap.Location(-90,0)

#Plot on sphere of earth
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
norm=plt.Normalize(0,max_value)

#for sta in station_list:
    #station_scatter=ax.scatter(sta.loc.cart.x, sta.loc.cart.y, sta.loc.cart.z, color='tomato', alpha=1, s=50)
print('starting to plot 3D')
for evt in eq_list:
    ax.scatter(evt.loc.cart.x,evt.loc.cart.y,evt.loc.cart.z,color='red',s=100)

ax.scatter(north_pole.cart.x,north_pole.cart.y,north_pole.cart.z,color='yellow',s=100)
ax.scatter(south_pole.cart.x,south_pole.cart.y,south_pole.cart.z, color='yellow',s=100, label='North and South Pole')

for pt in grid_array:
    ax.scatter(pt.loc.cart[0],pt.loc.cart[1],pt.loc.cart[2],c=arr.eqcount,cmap=cm.cool,norm=norm,alpha=.5,s=2)

for arr in good_arrays:
    arr_scatter=ax.scatter(arr.pt.loc.cart[0],arr.pt.loc.cart[1],arr.pt.loc.cart[2],c=arr.eqcount,cmap=cm.cool,norm=norm,s=50)


ax.set_box_aspect([radius_of_earth,radius_of_earth,radius_of_earth])
cbar = fig.colorbar(arr_scatter)
cbar.set_label('Number of earthquakes in SKS range at grid point', rotation=90)

#plot on 2D map 
print('starting to plot 2D')
plt.figure()
ax = plt.axes(projection=ccrs.PlateCarree())
#ax.coastlines(resolution='10m')
ax.add_feature(cfeature.OCEAN, color='lightskyblue')
ax.add_feature(cfeature.LAND, color="oldlace")
gridlines=ax.gridlines(draw_labels=True, alpha=.80)
for sta in station_list:    
    plt.scatter(sta.loc.lon,sta.loc.lat, marker='v', s=10, color='tomato')
    
for evt in eq_list:
    plt.scatter(evt.loc.lon,evt.loc.lat,marker='o',s=20,color='#06470c')

for pt in grid_array:
    plt.scatter(pt.loc.lon,pt.loc.lat, marker='o', s=2, c='blue', alpha=.5)

for arr in good_arrays:
    arr_scatter=plt.scatter(arr.pt.loc.lon,arr.pt.loc.lat,marker='o', s=20, c=arr.eqcount,cmap=cm.cool, norm=norm,transform=ccrs.PlateCarree())
 #need to edit plotting a little bit to plot the values. plotting all grid points seperate from those with value   
cbar=fig.colorbar(arr_scatter)
cbar.set_label('Number of earthquakes in SKS range at grid point', rotation=90)
plt.show()
