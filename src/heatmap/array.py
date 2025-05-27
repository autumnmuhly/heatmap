from .mesh_setup import latlon_cartesian,cart_latlon
from .distaz import DistAz

def is_ok_eq_sta(evt,sta,distRange):
    "Takes in an eq and checks if sta/pt is existed at time of event and if the stations are within range"
    min_dist=distRange[0]
    max_dist=distRange[1]
    if sta.start<evt.time<sta.stop:
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

class EqtoArrayList:
    "a list of arrays for all the earthquakes"
    def __init__(self,evt):
        self.evt=evt 
        self.array_list=[]
    def check_array(self,arr,distRange,minSta):
        "checks if any arrays are within range from earthquake, if so add array to the array list"
        min=distRange[0]
        max=distRange[1]
        dist=DistAz(arr.pt.loc.lat,arr.pt.loc.lon,self.EQ.loc.lat,self.EQ.loc.lon)
        distance=abs(dist.delta)
        if distance>min and distance<max:
            self.truth_count=0
            for sta in self.sta_list:
                if is_ok_eq_sta(self,sta,distRange) == True:
                    self.truth_count+=1
                    if self.truth_count >= minSta:
                        self.array_lists.append(arr)
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
    def __init__(self,pt,radius,sta_list):
        "an array has a grid point, a radius, and a list of stations in it"
        self.pt=pt
        self.radius=radius
        self.sta_list=sta_list 
        self.eqcount=0
        self.stacode=[]
def form_array(sta_list,pt,radius):    
    sta_array_list=[]
    for sta in sta_list:
        dist=DistAz(pt.loc.lat,pt.loc.lon,sta.loc.lat,sta.loc.lon)
        pt_sta=abs(dist.delta)
        if pt_sta<=radius:
            sta_array_list.append(sta)
            #print(f'adding this station {sta.name} to gpt located {pt.loc.lat}')
    return Array(pt,radius,sta_array_list)

def form_all_array(sta_list,grid_array,radius,minSta):
    array_list=[]
    for pt in grid_array:
        array=form_array(sta_list,pt,radius) 
        if len(array.sta_list)>= minSta:
            array_list.append(array)
    return array_list

# create a class of earthquake array pairs for each earthquake
