import numpy as np
import math
from .distaz import DistAz
from math import radians, cos, sin, asin, sqrt, pi

class Cartesian:
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z

def fibonacci_sphere(number_points):
    #https://stackoverflow.com/questions/9600801/evenly-distributing-n-points-on-a-sphere
    points = []
    
    phi = math.pi * (math.sqrt(5.) - 1.)  # golden angle in radians

    for i in range(number_points):
        y = 1 - (i / float(number_points - 1)) * 2  # y goes from 1 to -1
        radius = math.sqrt(1 - y * y)  # radius at y

        theta = phi * i  # golden angle increment

        x = math.cos(theta) * radius
        z = math.sin(theta) * radius

        points.append((x, y, z))

    return np.array(points)


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

def latlon_cartesian(lat,lon):
    R=6378
    lat=np.radians(lat)
    lon=np.radians(lon)
    x = R*np.cos(lat)*np.cos(lon)
    y = R*np.cos(lat)*np.sin(lon)
    z = R*np.sin(lat)
    return Cartesian(x,y,z)

class Neighbors:
    def __init__(self,pt,distances,list_neighbors):
        self.pt=pt #refernce point
        self.list_neighbors=list_neighbors #list of grid points that its neighbors
        self.distances=distances #list of distances to the neighbors

#This function will find the nearest neighbors for any 3D grid 
def find_neighbors(how_many,reference,grid):
    #trying to do neighbor search but with a list that we are comparing 
    neighbors = []
    fib_grid=grid
    #print(neighbors)
    for pt in fib_grid: 
        distance=DistAz(reference.loc.lat,reference.loc.lon,pt.loc.lat,pt.loc.lon)
        distance=distance.delta
        if distance != 0:
            found = False
            closest=(distance,pt)
            for j in range(min(how_many, len(neighbors))):
                if distance<neighbors[j][0]:
                    neighbors.insert(j,closest)
                    found = True
                    break
            if not found and len(neighbors) < how_many:
                neighbors.append(closest)
        neighbors = neighbors[:how_many]
    return neighbors

def radius_per_gridpoint(number_points, radius_of_earth=6371):
    """
    evenly divide area of sphere to get radius per gridpoint, approximate
    """
    area_per_point=(4*pi*radius_of_earth*radius_of_earth)/number_points
    radius_point_km=sqrt(area_per_point/pi)
    deg_per_km = 360/(2*pi*radius_of_earth)
    radius_point_deg=radius_point_km * deg_per_km
    return radius_point_deg
