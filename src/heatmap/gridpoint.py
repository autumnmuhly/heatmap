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