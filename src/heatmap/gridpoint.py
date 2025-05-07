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

class Station:
    def __init__(self,loc,start,stop):
        "station takes a location, start time, and end time"
        self.loc=loc
        self.start=start
        self.stop=stop
        
class EQ:
    def __init__(self,loc,event_time):
        self.loc=loc
        self.time=event_time
