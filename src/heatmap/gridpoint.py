from .mesh_setup import latlon_cartesian,cart_latlon
from .distaz import DistAz

class Location:
    def __init__(self,lat,lon,cart=None):
        "Location is made up of a lat, lon and cartesian coordinates"
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
        "cartesian coordinates (x,y,z)"
        self.cart=cart
        self.x,self.y,self.z= cart

class Gridpoint:
    def __init__(self,cart):
        "grid point takes in a cartesian touple but also has a lat and lon"
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
        'earthquakes have a location and a time'
        self.loc=loc
        self.time=event_time
    def __str__(self):
        return f"{self.time} {self.loc}"




#Could also create a catalog of earthquakes by idk year for example and counts the arrays 