#Plots 
from math import sin, sqrt, pi
import math
import numpy as np
import matplotlib.pyplot as plt

def radius_per_gridpoint(number_points, radius_of_earth=6371):
    """
    evenly divide area of sphere to get radius per gridpoint, approximate
    """
    area_per_point=(4*pi*radius_of_earth*radius_of_earth)/number_points
    radius_point_km=sqrt(area_per_point/pi)
    deg_per_km = 360/(2*pi*radius_of_earth)
    radius_point_deg=radius_point_km * deg_per_km
    print(f'number of points {number_points} radius {radius_point_deg}')
    return radius_point_deg

points=np.arange(500,10000,500)
degrees=[]
for pt in points:
    degrees.append(radius_per_gridpoint(pt))
degrees=np.array(degrees)
print(type(points))
print(type(degrees))
plt.plot(degrees,points, c='#35063e')
plt.scatter(degrees,points, c='#35063e')
plt.yticks(np.arange(0,10000,1000))
plt.xlabel('Degrees')
plt.ylabel('Number of Points')
plt.title('Grid Spacing')
plt.show()
