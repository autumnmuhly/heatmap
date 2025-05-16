from .mesh_setup import latlon_cartesian,cart_latlon
from .distaz import DistAz

class Location:
    def __init__(self,lat,lon,cart=None):
        self.lat=lat
        self.lon=lon
        self._cart=cart
    @property
    def cart(self):
        if self._cart is None:
            self._cart=latlon_cartesian(self.lat,self.lon)
        return self._cart 
    def distTo(self, loc):
        return DistAz(self.lat,self.lon,loc.lat,loc.lon)
    def __str__(self):
        return f"{self.lat},{self.lon}"

class Cartesian:
    def __init__(self,cart):
        "will maybe hold the cartesian grid points"
        self.cart=cart
        self.x,self.y,self.z= cart
        

class Gridpoint:
    def __init__(self,cart):
        "grid point takes in a cartesian touple"
        com=Cartesian(cart)
        lat,lon=cart_latlon(com.x,com.y,com.z)
        self.loc=Location(lat,lon,cart)
        self.phaseCount = {}
    def distToSta(self, sta):
        return self.loc.distTo(sta.loc)
    def __str__(self):
        return f"gp {self.loc}"

class Station:
    def __init__(self,name,loc,start,stop):
        "station takes a location, start time, and end time"
        self.name=name
        self.loc=loc
        self.start=start
        self.stop=stop
    def __str__(self):
        return f"{self.name} {self.loc}"

class EQ:
    def __init__(self,loc,event_time):
        self.loc=loc
        self.time=event_time
    def __str__(self):
        return f"{self.time} {self.loc}"

class Pts_In_Range:
    def __init__(self,loc):
        "points in a range is an updated class with the cartiesan coord of the pts within eq range"
        self.loc=loc


def is_ok_eq_sta(evt,sta,distRange):
    "Takes in an eq and checks if sta/pt is existed at time of event and if the stations are within range"
    min_dist=distRange[0]
    max_dist=distRange[1]
    if sta.start<evt.time<sta.stop:
        dist=DistAz(evt.loc.lat,evt.loc.lon,sta.loc.lat,sta.loc.lon)
        gc=dist.delta
        if min_dist<gc<max_dist:
            return True
        else:
            print("not ok distance eq_sta")
    else:
        print(f'not ok time eq_sta {sta.start} {evt.time} {sta.stop}')
    return False

class Array:
    def __init__(self,pt,radius,sta_list):
        "an array has a grid point, a radius, and a list of stations in it"
        self.pt=pt
        self.radius=radius
        self.sta_list=sta_list 
        self.eqcount=0
    def check_eq(self,evt,distRange):
        "checks if any events are within range from array, if so count 1 for that array"
        min=distRange[0]
        max=distRange[1]
        dist=DistAz(self.pt.loc.lat,self.pt.loc.lon,evt.loc.lat,evt.loc.lon)
        if dist.delta>min and dist.delta<max:
            for sta in self.sta_list:
                if is_ok_eq_sta(evt,sta,distRange) == True:
                    self.eqcount +=1
                else:
                    print(f"not ok sta {evt} {sta}")
        else:
            print(f"not ok gp {self.pt}")

def form_array(sta_list,pt,radius):    
    sta_array_list=[]
    for sta in sta_list:
        dist=DistAz(pt.loc.lat,pt.loc.lon,sta.loc.lat,sta.loc.lon)
        pt_sta=dist.delta
        if pt_sta<=radius:
            sta_array_list.append(sta)
            print(f'adding this station {sta.name} to gpt located {pt.loc.lat}')
    return Array(pt,radius,sta_array_list)

def form_all_array(sta_list,grid_array,radius,minSta):
    array_list=[]
    for pt in grid_array:
        array=form_array(sta_list,pt,radius) 
        if len(array.sta_list)>= minSta:
            array_list.append(array)
    return array_list



#Could also create a catalog of earthquakes by idk year for example and counts the arrays 