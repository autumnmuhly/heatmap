import numpy as np
import math
from distaz import DistAz
from math import radians, cos, sin, asin, sqrt, pi
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 

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

#Get complete grid points and scale to Earth - come up with what is a reasonable number. why 1000? spacing should represent array size
number_points=1000
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

def latlon_cartesian(lat,lon):
    R=6378
    lat=np.radians(lat)
    lon=np.radians(lon)
    x = R*np.cos(lat)*np.cos(lon)
    y = R*np.cos(lat)*np.sin(lon)
    z = R*np.sin(lat)
    return x,y,z

# running a test case of lat lon  to cartesian then back to lat lon to see if the calculations are correct 
hawaii=(19.90,-155.67)
x_hawaii,y_hawaii,z_hawaii=latlon_cartesian(hawaii[0],hawaii[1])
new_hawaii=cart_latlon(x_hawaii,y_hawaii,z_hawaii)

# i have verfied these work for a variety of points just hawaii is listed above but i did it for north and south poles and fliped thelat long.
gridpoints_lat=[]
gridpoints_lon=[]
for i in range(len(x_com)):
    gridpoints_geodetic=cart_latlon(x_com[i],y_com[i],z_com[i])
    gridpoints_lat.append(gridpoints_geodetic[0])
    gridpoints_lon.append(gridpoints_geodetic[1])




class Gridpoint:
    def __init__(self,lat,lon,x_cart,y_cart,z_cart):
        self.lat=lat
        self.lon=lon
        self.x_cart=x_cart
        self.y_cart=y_cart
        self.z_cart=z_cart
        self.phaseCount = {}
    def distToSta(self, sta):
        return DistAz(self.lat,self.lon,sta.lat,sta.lon)



fib_grid=Gridpoint(gridpoints_lat,gridpoints_lon,x_com,y_com,z_com)

# different distance
def dist3d(x1,y1,z1,x2,y2,z2):
    x_diff=(x2-x1)**2
    y_diff=(y2-y1)**2
    z_diff=(z2-z1)**2
    distance=sqrt(x_diff+y_diff+z_diff)
    return distance


#look at distances between points 
distance_first=10000
distance_second=10000
distance_third=10000
distance_fourth=10000
distance_fifth=10000
distance_sixth=1000
for i in range(len(fib_grid.x_cart)):
    #distance=DistAz(fib_grid.lat[40],fib_grid.lon[40],fib_grid.lat[i],fib_grid.lat[i])
    distance=dist3d(fib_grid.x_cart[9],fib_grid.y_cart[9],fib_grid.z_cart[9],fib_grid.x_cart[i],fib_grid.y_cart[i],fib_grid.z_cart[i])
    #print(distance)
    distance=abs(distance)
    #print(distance)
    if distance < distance_first:
        if distance !=0:
            first_neighbor=[fib_grid.x_cart[i],fib_grid.y_cart[i],fib_grid.z_cart[i]]
            distance_first=distance
    elif distance<distance_second :
        #second_neighbor=[fib_grid.x_cart[i],fib_grid.y_cart[i],fib_grid.z_cart[i]]
        distance_second=distance
    elif distance<distance_third :
        #third_neighbor=[fib_grid.x_cart[i],fib_grid.y_cart[i],fib_grid.z_cart[i]]
        distance_third=distance
    elif distance<distance_fourth :
        #fourth_neighbor=[fib_grid.x_cart[i],fib_grid.y_cart[i],fib_grid.z_cart[i]]
        distance_fourth=distance
    elif distance<distance_fifth :
        #fifth_neighbor=[fib_grid.x_cart[i],fib_grid.y_cart[i],fib_grid.z_cart[i]]
        distance_fifth=distance


def find_neighbors(how_many):
    #trying to do neighbor search but with a list that we are comparing 
    neighbors=np.ones((len(fib_grid.x_cart),2)).tolist()
    neighbors[0][0]=100000
    neighbors = []
    #print(neighbors)
    for i in range(len(fib_grid.x_cart)):
        distance=dist3d(fib_grid.x_cart[9],fib_grid.y_cart[9],fib_grid.z_cart[9],fib_grid.x_cart[i],fib_grid.y_cart[i],fib_grid.z_cart[i])
        #print(f' this is the distance {distance}')
        if distance != 0:
            #print('possible')
            found = False
            closest=(distance,i)
            for j in range(min(how_many, len(neighbors))):
                if distance<neighbors[j][0]:
                    neighbors.insert(j,closest)
                    found = True
                    break
            if not found and len(neighbors) < how_many:
                neighbors.append(closest)
        neighbors = neighbors[:how_many]
    return neighbors

HOW_MANY=5
neighbors = find_neighbors(HOW_MANY)
print(neighbors)
    




fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x_com, y_com, z_com, color='green', s=2)
#ax.scatter(first_neighbor[0],first_neighbor[1],first_neighbor[2], color='pink',s=100)
for i in range(HOW_MANY):
    index=neighbors[i][1]
    ax.scatter(x_com[index],y_com[index],z_com[index],color='pink',s=100)
#ax.scatter(second_neighbor[0],second_neighbor[1],second_neighbor[2], color='pink',s=100)
#ax.scatter(third_neighbor[0],third_neighbor[1],third_neighbor[2], color='pink',s=100)
#ax.scatter(fourth_neighbor[0],fourth_neighbor[1],fourth_neighbor[2], color='pink',s=100)
#ax.scatter(fifth_neighbor[0],fifth_neighbor[1],fifth_neighbor[2], color='pink',s=100)
ax.scatter(fib_grid.x_cart[9], fib_grid.y_cart[9], fib_grid.z_cart[9], color='yellow', s=100)
ax.set_box_aspect([radius_of_earth,radius_of_earth,radius_of_earth])
ax.legend()
plt.show()
