
from multiprocessing import Pool
import functools
import os

from .mesh_setup import latlon_cartesian,cart_latlon
from .distaz import DistAz

def is_ok_eq_sta(evt,sta,distRange):
    "Takes in an eq and checks if sta/pt is existed at time of event and if the stations are within range"
    min_dist=distRange[0]
    max_dist=distRange[1]
    #print(sta.name, sta.start,evt.time, sta.stop)
    if sta.start<=evt.time and (sta.stop=='None' or evt.time<=sta.stop):
        #print('weve add the above to list')
        #print(sta.name, sta.stop)
        dist=DistAz(evt.loc.lat,evt.loc.lon,sta.loc.lat,sta.loc.lon)
        gc=abs(dist.delta)
        if min_dist<gc<max_dist:
            #print(f'this eq and sta are okay {evt},{sta}')
            return True
        #else:
            #print("not ok distance eq_sta")
    #else:
        #print(f'not ok time eq_sta {sta.start} {evt.time} {sta.stop}')
    return False

def is_array_gp_okay(arr,spacing):
    x=0
    y=0
    z=0
    for sta in arr.sta_list:
        cart=latlon_cartesian(sta.loc.lat,sta.loc.lon)
        #print(cart.x,cart.y,cart.z)
        x+=cart.x
        y+=cart.y
        z+=cart.z
    num=len(arr.sta_list)
    cm_latlon=cart_latlon(x/num,y/num,z/num)
    diff=DistAz(arr.pt.loc.lat,arr.pt.loc.lon,cm_latlon[0],cm_latlon[1])
    if diff.delta>=(spacing/2):
        return False
    return True


class EqtoArrayList:
    "a list of arrays for all the earthquakes"
    def __init__(self,evt):
        self.evt=evt 
        self.array_list=[]
    def check_array(self,arr,distRange,minSta):
        "checks if any arrays are within range from earthquake, if so add array to the array list"
        min=distRange[0]
        max=distRange[1]
        dist=DistAz(arr.pt.loc.lat,arr.pt.loc.lon,self.evt.loc.lat,self.evt.loc.lon)
        distance=abs(dist.delta)
        count=0
        if distance>min and distance<max:
            self.truth_count=0
            for sta in self.sta_list:
                if is_ok_eq_sta(self,sta,distRange) == True:
                    self.truth_count+=1
                    if self.truth_count >= minSta:
                        self.array_lists.append(arr)
                        if os.path.exists('grid_pts.txt'):
                            os.remove('grid_pts.txt')
                        count+=1
                        file=open("grid_pts.txt",'a+')
                        text=(f'gridpoint {count} {arr.pt.loc.lat} {arr.pt.loc.lon}\n')
                        file.writelines(text)
                        file.close()
                        break

class ArrayToEqlist:
    "a list of eq for all arrrays"
    def __init__(self,array):
        self.array=array
        self.eqlists=[]
        self.eqcount=len(self.eqlists)
    def check_eq(self,evt,distRange,minSta):
        "checks if any events are within range from array, if so count 1 for that array and add event to eqlist"
        min=distRange[0]
        max=distRange[1]
        dist=DistAz(self.array.pt.loc.lat,self.array.pt.loc.lon,evt.loc.lat,evt.loc.lon)
        distance=abs(dist.delta)
        if distance>min and distance<max:
            self.truth_count=0
            for sta in self.array.sta_list:
                if is_ok_eq_sta(evt,sta,distRange) == True:
                    self.truth_count+=1
                    if self.truth_count >= minSta:
                        self.eqcount +=1 #is now adding one to the grid point if all stations meet the criteria
                        self.eqlists.append(evt)
                        break

class EqArrayPair:
    "the earthquake distance pairs"
    def __init__(self):
        self.self=self
        

class DepthVolume:
    "holds the pairs that goes through our point of interest"
    def __init__(self,pt,depthrange,radius):
        self.pt=pt
        self.radius=radius
        
        
class Array:
    def __init__(self,pt,radius, station_distances, basestation=None):
        "an array has a grid point, a radius, a list of stations in it, and a base station"
        self.pt=pt
        self.radius=radius
        self.sta_list=list(station_distances) 
        self.eqcount=0
        self.sta_array_list=[]
        self.basestation=basestation
        self.station_distances=station_distances
def form_array(sta_list,pt,radius):
    sta_array_list=[]
    sta_distance=[]
    sta_dist = {}
    min_dist=361
    basestation=None
    for sta in sta_list:
        dist=DistAz(pt.loc.lat,pt.loc.lon,sta.loc.lat,sta.loc.lon)
        pt_sta=abs(dist.delta)
        if pt_sta<=radius:
            #print(sta.name, pt.loc)
            sta_array_list.append(sta)
            sta_dist[sta] = pt_sta
            if pt_sta<min_dist:
                basestation=sta
                min_dist=pt_sta
            #print(f'adding this station {sta.name} to gpt located {pt.loc.lat}')
    return Array(pt,radius,sta_dist, basestation)


def inner_form_array(sta_list, radius, pt):
    return form_array(sta_list,pt,radius)

def form_all_array(sta_list,grid_array,radius,minSta):
    array_list=[]
    partial_form_array = functools.partial(inner_form_array, sta_list, radius)

    with Pool(processes=(os.process_cpu_count()-1)) as pool:
        array_list = pool.map(partial_form_array, grid_array)

    return [a for a in array_list if len(a.sta_list)>=minSta]

class EqGridAssignment:
    def __init__(self,gridpoint,earthquake):
        self.gridpoint=gridpoint
        self.eqList=earthquake

def form_eq(evt_list,pt,radius):
    "each earthquake is assigned to a gridpoint"
    #print(pt)
    eq_pt_list=[]
    for evt in evt_list:
        dist=DistAz(pt.loc.lat,pt.loc.lon,evt.loc.lat,evt.loc.lon)
        pt_evt=abs(dist.delta)
        if pt_evt<=radius:
            eq_pt_list.append(evt)
    return EqGridAssignment(pt,radius,eq_pt_list)

def form_all_eq_grid(evt_list,grid_array,radius):
    evt_pt_list=[]
    for pt in grid_array:
        evt_pt_list.append(form_eq(evt_list,pt,radius))
    return evt_pt_list
# create a class of earthquake array pairs for each earthquake

def items_in_dist(locList,point,minRadius,maxRadius):
    """""
    locList-list of things that have location 
    point- central location (a grid point)
    radius - distance radius around point
    """""
    good_locs = []
    for locItem in locList:
        dist = DistAz(locItem.loc.lat,locItem.loc.lon, point.loc.lat,point.loc.lon)
        dist=abs(dist.delta)
        if minRadius <= dist <= maxRadius:
            good_locs.append(locItem)
    return good_locs

class DistGrouping:
    "Has a "
    def __init__(self, itemList, center_point ):
        self.itemList=itemList
        self.centerpoint=center_point

def group_items_by_dist(loc_list, point_list, minRadius, maxRadius, minSuccessful):
    """
    loc_list- list of things that have a location 
    point_list- list of grid points
    minRadius/maxRadius- min/max radius that the distance betweent the loc and point must satisfy 
    minSuccessful-can be 0, how many of them in that range to be considered good
    Return a touple where the 0th index is the point and the foundlist are the pairs for that point
    """
    good_lists = []
    for point in point_list:
        found_list = items_in_dist(loc_list, point, minRadius, maxRadius)
        if (len(found_list) >= minSuccessful) & (len(found_list) != 0):
            #good_lists.append(DistGrouping(found_list, point) )
            good_lists.append( (point, found_list) )
    return good_lists

#where all the thins have a .time attribute
#sta.time=[start,end]
#evt.time=[origintime,origintime]
#grid_point.time=None

#def time_overlaps(timerangea,timerangeb):
    #where timeable is a point in time 
    #if timerangea or timerangeb is None:
        #return True
    #if timerangea.max<timerangeb.min || timerangea.min> timerangeb.max:
     #       return False
    #return True