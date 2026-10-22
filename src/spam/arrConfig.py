from .gridpoint import Location
import numpy as np
from scipy.spatial.distance import cdist, euclidean


class Center:
    "Center has a location (lat,lon and cart (x,y,z))"
    def __init__(self,lat,lon):
        self.lat=lat
        self.lon=lon

def calcArthCenter(array):
    lat=[]
    lon=[]
    cnt=0
    lat_add=0
    lon_add=0
    for sta in array.good_sta_list:
        lat.append(sta.loc.lat)
        lat_add+=sta.loc.lat
        lon.append(sta.loc.lon)
        lon_add+=sta.loc.lon
        cnt+=1
    avglat=lat_add/cnt
    avglon=lon_add/cnt
    array.center=Center(avglat,avglon)
    # print('have assigned a value to array.array2quake.center')
    # print(array.center)
    # arr.center.lat=avglat
    # arr.center.lon=avglon
    return

def calcGeomedian(array,array_center,eps=1e-5):
    "Geometric median is the point that minimizes the sum of distances to the sample points."
    "also known as the spatial median.https://stackoverflow.com/questions/30299267/geometric-median-of-multidimensional-points"
    station_loc = []
    for sta in array.good_sta_list:
        station_loc.append((sta.loc.lon,sta.loc.lat))
    y = (array_center.lon,array_center.lat)
    X = np.array(station_loc)
    xiterations = 0
    while True:
        D = cdist(X, [y])
        nonzeros = (D != 0)[:, 0]

        Dinv = 1 / D[nonzeros]
        Dinvs = np.sum(Dinv)
        W = Dinv / Dinvs
        T = np.sum(W * X[nonzeros], 0)

        num_zeros = len(X) - np.sum(nonzeros)
        xiterations+=1
        if xiterations > 100000:
            print("Did not converge")
            return None
        if num_zeros == 0:
            y1 = T
        elif num_zeros == len(X):
            return y
        else:
            R = (T - y) * Dinvs
            r = np.linalg.norm(R)
            rinv = 0 if r == 0 else num_zeros/r
            y1 = max(0, 1-rinv)*T + min(1, rinv)*y
        if euclidean(y, y1) < eps:
            lat = float(y1[1])
            lon = float(y1[0])
            array.geoCenter = Center(lat,lon)
            return y1
            # print(y1)
            # print(type(y1))
            # print(len(y1))
            # return y1
        y = y1


