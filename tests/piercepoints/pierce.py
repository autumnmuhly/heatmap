import json
import sys
import subprocess
from heatmap import latlon_cartesian,cart_latlon
import numpy as np

def getTauPAsJson(cmd):
    """
    Gets results for a TauP command via json. The --json parameter is
    automatically appended to the command.
    """
    splitCmd = cmd.split(" ")
    splitCmd.append("--json")
    result = subprocess.run(splitCmd, capture_output=True)
    result.check_returncode() # will raise CalledProcessError if not ok
    return json.loads(result.stdout)

def taup_pierce(event,station, phase, model):
    """
    Calculates pierce points for a given event and station
    Parameters:
    """
    evdp=event.depth
    evlat=event.loc.lat
    evlon=event.loc.lon
    if isinstance(phase, list):
        ph = ",".join(phase)
    else:
        ph = phase

    #print(f'this is mode')
    #print(f'taup pierce --evdepth {evdp} --event {evlat} {evlon} --model {model} --phase {ph} --station {station.loc.lat} {station.loc.lon} ')
    cmd_pierce=f"taup pierce --evdepth {evdp} --event {evlat} {evlon} --model {model} --phase {ph} --station {station.loc.lat} {station.loc.lon}"
    taupjson = getTauPAsJson(cmd_pierce)
    return taupjson

def get_piercepoints(eventlist,array_list,depth,):
    for eq in eq_list:
        for arr in good_arrays:
            #print(f'this is what is in eq and arr {eq.loc} {arr.array.pt.loc} ')
            pierce_info=taup_pierce(eq,arr.array.pt, mydata.phase,model)
            #print(pierce_info)
            for ar in pierce_info['arrivals']:      #loops through this twice. first one is minor
                if ar['phase'] == "SKKS":
                    a = ar
                    #print(a)
                    if part_of_ray == "lastleg":
                        time=10
                        #print(f'this is time {time}')
                        for p in a["pierce"]:
                            pt=p
                            #print(f'this is pt {pt}')
                            if abs(pt[1] - depth_of_interest) < 10:
                                #print(pt[2])
                                if pt[2]>time:
                                    #print(f'updating time {time}')
                                    time=pt[2]
                                    arr.piercepoints[eq.time.strftime('%m%d%Y%H%M%S')]=PiercePoint(pt[2],pt[3],pt[4])
    return

def create_plane(p1,p2,p3):
    "creates a plane from 3 points. plane is defined by normal vector"
    first=latlon_cartesian(p1[0],p1[1],0)
    second=latlon_cartesian(p2[0],p2[1],0)
    third=latlon_cartesian(p3[0],p3[1],0)

    x=[]
    x.append(first.x)
    x.append(second.x)
    x.append(third.x)
    y=[]
    y.append(first.y)
    y.append(second.y)
    y.append(third.y)
    
    u = [second.x-first.x, second.y-first.y, second.z-first.z]
    v = [third.x-first.x, third.y-first.y, third.z-first.z]
    u=np.array(u)
    v=np.array(v)
    u_cross_v =np.cross(u,v)
    point = np.array([first.x,first.y,first.z])
    normal = np.array(u_cross_v)
    d = -point.dot(normal)
    #print('plane equation:\n{:1.4f}x + {:1.4f}y + {:1.4f}z + {:1.4f} = 0'.format(normal[0], normal[1], normal[2], d))
    return normal,d,point

def pts2planes(lat1,lat2,lon1,lon2):
    "Takes in range of lat and lon and returns back planes that match the box"
    list_planes=[]
    pl1_third_pt=lat1+lat2/2
    pt_plane1=[(lat1,lon1),(lat2,lon1),(pl1_third_pt,lon1)]
    plane1=create_plane(pt_plane1[0],pt_plane1[1],pt_plane1[2])
    list_planes.append(plane1)
    return list_planes
    

class Ray:
    def __init__(self,lat,lon,depth,cart=None):
        "Location is made up of a lat, lon and cartesian coordinates"
        self.lat=lat
        self.lon=lon
        self._cart=cart
    @property
    def cart(self):
        if self._cart is None:
            self._cart=latlon_cartesian(self.lat,self.lon)
        return self._cart
    def __str__(self):
        return f"{self.lat},{self.lon}"