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
    max_dis=180
    dist=(0,180)
elif phase == 'SKKS':
    min_dis=85
    max_dis=170
elif phase =='S3KS':
    min_dis=110
    max_dis=175
elif phase =='S4KS':
    min_dis=130
    max_dis=175
else:
    print('add phase to list')

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
station_name=df[1].to_list()
#need to check for NA or empty ???

station_list=[]
for i in range(len(station_lat)):
    sta=heatmap.Station(station_name,heatmap.Location(station_lat[i],station_lon[i]),station_start[i],station_end[i])
    station_list.append(sta)

#construst arrays for every gridpoint
area_per_point=(4*pi*radius_of_earth*radius_of_earth)/number_points
radius_point_km=sqrt(area_per_point/pi)
radius_point_deg=radius_point_km/111

#form arrays
min_station=1
array_list=heatmap.form_all_array(station_list,grid_array,radius_point_deg,min_station)


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

#loop over evts and arrays and check. delete arrays where eq count is below the min eq needed or color the dots by amount of earthquakes 
for arr in array_list:
    for evt in eq_list:
        arr.check_eq(evt,dist)

print(array_list[0].eqcount)

#loop over array in array list. if they have more than min number then add then to good_array
min_eq_needed=1
good_arrays=[]
for arr in array_list:
    if arr.eqcount>min_eq_needed:
        good_arrays.append(arr)


area_per_point=(4*pi*radius_of_earth*radius_of_earth)/number_points
radius_point_km=sqrt(area_per_point/pi)
radius_point_deg=radius_point_km/111
eq_yes=dict()
station_yes=dict()
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
                     count_array=0
                     if pt_sta<=radius_point_deg:
                          if sta.start<evt.time<sta.stop:
                               count_array+=1
                     station_yes[pt]=count_array
    eq_yes[pt]=count

print("*****")
print(len(good_arrays))


#refernce points
north_pole=heatmap.Location(90,0)
south_pole=heatmap.Location(-90,0)

#Plot on sphere of earth
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
norm=plt.Normalize(0,max_value)



for sta in station_list:
    station_scatter=ax.scatter(sta.loc.cart.x, sta.loc.cart.y, sta.loc.cart.z, color='tomato', alpha=1, s=50)

#ax.scatter(x_com, y_com, z_com, color='green', s=2)

for evt in eq_list:
    ax.scatter(evt.loc.cart.x,evt.loc.cart.y,evt.loc.cart.z,color='red',s=100)

ax.scatter(north_pole.cart.x,north_pole.cart.y,north_pole.cart.z,color='yellow',s=100)
ax.scatter(south_pole.cart.x,south_pole.cart.y,south_pole.cart.z, color='yellow',s=100, label='North and South Pole')

#for pt in grid_array:
    #pt_scatter=ax.scatter(pt.loc.cart[0],pt.loc.cart[1],pt.loc.cart[2],c=station_yes[pt],cmap=cm.cool,norm=norm,s=2)

for arr in good_arrays:
    pt_scatter=ax.scatter(arr.pt.loc.cart[0],arr.pt.loc.cart[1],arr.pt.loc.cart[2],c=arr.eqcount,cmap=cm.cool,norm=norm,s=50)


ax.set_box_aspect([radius_of_earth,radius_of_earth,radius_of_earth])
cbar = fig.colorbar(station_scatter)
cbar.set_label('Number of stations in SKS range at grid point', rotation=90)

#plot on 2D map 
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

for arr in good_arrays:
    pt_scatter=plt.scatter(arr.pt.loc.lon,arr.pt.loc.lat,marker='o', s=20, c=arr.eqcount,cmap=cm.cool, norm=norm,transform=ccrs.PlateCarree())
    
#for pt in grid_array:
    #pt_scatter=plt.scatter(pt.loc.lon,pt.loc.lat, marker='o', s=2, c=station_yes[pt],cmap=cm.cool, norm=norm,transform=ccrs.PlateCarree())
cbar=fig.colorbar(pt_scatter)
cbar.set_label('Number of stations in SKS range at grid point', rotation=90)
plt.show()
