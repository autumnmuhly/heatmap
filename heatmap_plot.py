#!/usr/bin/env python

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
from types import SimpleNamespace
import heatmap


infilename = "heatmap.json"
with open(infilename, "r") as inf:
    mydata = jsonpickle.decode(inf.read())
mydata = SimpleNamespace(mydata)


#some formatting things for our colorbar
eq_count=[]
print(eq_count)
for arr in mydata.good_arrays:
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

#for sta in mydata.station_list:
    #station_scatter=ax.scatter(sta.loc.cart.x, sta.loc.cart.y, sta.loc.cart.z, color='tomato', alpha=1, s=50)
print('starting to plot 3D')
#for evt in mydata.eq_list:
    #ax.scatter(evt.loc.cart.x,evt.loc.cart.y,evt.loc.cart.z,color='red',s=100)

ax.scatter(north_pole.cart.x,north_pole.cart.y,north_pole.cart.z,color='yellow',s=100)
ax.scatter(south_pole.cart.x,south_pole.cart.y,south_pole.cart.z, color='yellow',s=100, label='North and South Pole')

for pt in mydata.grid_array:
    ax.scatter(pt.loc.cart[0],pt.loc.cart[1],pt.loc.cart[2],c=0,cmap=cm.cool,norm=norm,alpha=.5,s=2)

for arr in mydata.good_arrays:
    arr_scatter=ax.scatter(arr.array.pt.loc.cart[0],arr.array.pt.loc.cart[1],arr.array.pt.loc.cart[2],c=arr.eqcount,cmap=cm.cool,norm=norm,s=50)


ax.set_box_aspect([mydata.radius_of_earth,mydata.radius_of_earth,mydata.radius_of_earth])
cbar = fig.colorbar(arr_scatter)
cbar.set_label(f'Number of earthquakes in {",".join(mydata.phase)} range at grid point', rotation=90)

#plot on 2D map
print('starting to plot 2D')
plt.figure()
ax = plt.axes(projection=ccrs.PlateCarree())
#ax.coastlines(resolution='10m')
ax.add_feature(cfeature.OCEAN, color='lightskyblue')
ax.add_feature(cfeature.LAND, color="oldlace")
gridlines=ax.gridlines(draw_labels=True, alpha=.80)
#for sta in mydata.station_list:
    #plt.scatter(sta.loc.lon,sta.loc.lat, marker='v', s=30, color='tomato')

#for evt in mydata.eq_list:
    #plt.scatter(evt.loc.lon,evt.loc.lat,marker='o',s=20,color='#ffff84')

for pt in mydata.grid_array:
    plt.scatter(pt.loc.lon,pt.loc.lat, marker='o', s=2, c=0,cmap=cm.cool,norm=norm,alpha=.2)

for arr in mydata.good_arrays:
    arr_scatter=plt.scatter(arr.array.pt.loc.lon,arr.array.pt.loc.lat,marker='o', s=20, c=arr.eqcount,cmap=cm.cool, norm=norm,transform=ccrs.PlateCarree())
 #need to edit plotting a little bit to plot the values. plotting all grid points seperate from those with value
cbar=fig.colorbar(arr_scatter)
cbar.set_label(f'Number of earthquakes in {",".join(mydata.phase)} range at grid point', rotation=90)
plt.show()
