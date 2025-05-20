from .mesh_setup import latlon_cartesian,cart_latlon
from .distaz import DistAz

def is_ok_eq_sta(evt,sta,distRange):
    "Takes in an eq and checks if sta/pt is existed at time of event and if the stations are within range"
    min_dist=distRange[0]
    max_dist=distRange[1]
    if sta.start<evt.time<sta.stop:
        dist=DistAz(evt.loc.lat,evt.loc.lon,sta.loc.lat,sta.loc.lon)
        gc=dist.delta
        if min_dist<gc<max_dist:
            #print(f'this eq and sta are okay {evt},{sta}')
            return True
        #else:
            #print("not ok distance eq_sta")
    #else:
        #print(f'not ok time eq_sta {sta.start} {evt.time} {sta.stop}')
    return False

class Array:
    def __init__(self,pt,radius,sta_list):
        "an array has a grid point, a radius, and a list of stations in it"
        self.pt=pt
        self.radius=radius
        self.sta_list=sta_list 
        self.eqcount=0
        self.stacde=[]
    def check_eq(self,evt,distRange):
        "checks if any events are within range from array, if so count 1 for that array"
        min=distRange[0]
        max=distRange[1]
        dist=DistAz(self.pt.loc.lat,self.pt.loc.lon,evt.loc.lat,evt.loc.lon)
        if dist.delta>min and dist.delta<max:
            for sta in self.sta_list:
                if is_ok_eq_sta(evt,sta,distRange) == True:
                    self.eqcount +=1
                #else:
                    #print(f"not ok sta {evt} {sta}")
        #else:
            #print(f"not ok gp {self.pt}")

def form_array(sta_list,pt,radius):    
    sta_array_list=[]
    for sta in sta_list:
        dist=DistAz(pt.loc.lat,pt.loc.lon,sta.loc.lat,sta.loc.lon)
        pt_sta=dist.delta
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

