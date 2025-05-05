import numpy as np
import math
from distaz import DistAz
from math import radians, cos, sin, asin, sqrt, pi
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 
from heatmap_classes import Gridpoint
from mesh_setup import fibonacci_sphere
from mesh_setup import find_neighbors

number_points=2000
radius_of_earth=6378 
points=(fibonacci_sphere(number_points))*radius_of_earth

def appendSpherical_np(xyz):
    ptsnew=np.hstack((xyz, np.zeros(xyz.shape)))
    xy=xyz[:,0]**2+xyz[:,1]**2
    ptsnew[:,3]=np.sqrt(xy+xyz[:,2]**2)
    ptsnew[:,4]=np.arctan2(np.sqrt(xy),xyz[:,2])
    ptsnew[:,5]=np.arctan2(xyz[:,1],xyz[:,0])
    return ptsnew

spherical_complete=appendSpherical_np(points)
rho_sph_com=spherical_complete[:,3]
theta_sph_com=spherical_complete[:,4]
phi_sph_com=spherical_complete[:,5]


#Convert complete grid from spherical to cartesian 
x_com=rho_sph_com*np.sin(theta_sph_com)*np.cos(phi_sph_com)
y_com=rho_sph_com*np.sin(theta_sph_com)*np.sin(phi_sph_com)
z_com=rho_sph_com*np.cos(theta_sph_com)

def cart_latlon(x, y, z):
    A=6378
    # calculate longitude, in radians
    longitude = (math.atan2(y, x))
    # calculate latitude, in radians
    xy_hypot = math.hypot(x, y)
    latitude = math.atan(z / xy_hypot)
    latitude=latitude*180/pi
    longitude=longitude*180/pi
    return latitude,longitude 

# Converting our cartesian gridpoints to lat lon 
gridpoints_lat=[]
gridpoints_lon=[]
for i in range(len(x_com)):
    gridpoints_geodetic=cart_latlon(x_com[i],y_com[i],z_com[i])
    gridpoints_lat.append(gridpoints_geodetic[0])
    gridpoints_lon.append(gridpoints_geodetic[1])

#This line loads in gridpoins as a class :)
fib_grid=Gridpoint(gridpoints_lat,gridpoints_lon,x_com,y_com,z_com)

HOW_MANY=5
reference=100
neighbors = find_neighbors(HOW_MANY,reference,fib_grid)

#I want to find the average grid spacing between the points
spacing=[]
for i in range(number_points):
    neighbor_test=find_neighbors(HOW_MANY,i,fib_grid)
    close=neighbor_test[0][0]
    spacing.append(close)
min_spacing=min(spacing)
max_spacing=max(spacing)
print(f'this is the min {min_spacing} and this is the max {max_spacing}, diff is {max_spacing-min_spacing}')