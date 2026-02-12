from pierce import taup_pierce
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import jsonpickle
from heatmap import Gridpoint,Station,EQ,Location
from heatmap import EqtoArrayList
from types import SimpleNamespace
import sys
import math
from heatmap import PiercePoint
import pyproj

model='prem'
infilename = "heatmap.json"

with open(infilename, "r") as inf:
    mydata = jsonpickle.decode(inf.read())
mydata = SimpleNamespace(mydata)

good_arrays=mydata.good_arrays
eq_list=mydata.eq_list
pp={}

depth_of_interest=2889.0

part_of_ray='lastleg'

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
print('printing whats in piercepoints')
for arr in good_arrays:
    print(arr.piercepoints)


ax = plt.axes(projection=ccrs.PlateCarree())

ax.add_feature(cfeature.OCEAN, color='lightskyblue')
ax.add_feature(cfeature.LAND, color="oldlace")
for evt in eq_list:
    evtid=evt.time.strftime('%m%d%Y%H%M%S')
    print(evtid)
    ax.scatter(evt.loc.lon,evt.loc.lat,marker='o',s=9, color="#021c50",alpha=.30,transform=ccrs.PlateCarree())
    for arr in good_arrays:
        ax.scatter(arr.array.pt.loc.lon,arr.array.pt.loc.lat,marker='v',s=13, c='none',edgecolors='blue',alpha=.20,transform=ccrs.PlateCarree())
        print(arr.piercepoints)
        ax.scatter(arr.piercepoints[evtid].lon,arr.piercepoints[evtid].lat,marker='o',s=13, c='none',edgecolors='red',alpha=.20,transform=ccrs.PlateCarree())
        g = pyproj.Geod(ellps='WGS84')
        (az12, az21, dist) = g.inv(arr.array.pt.loc.lon,arr.array.pt.loc.lat, evt.loc.lon,evt.loc.lat)
        lonlats = g.npts(arr.array.pt.loc.lon,arr.array.pt.loc.lat, evt.loc.lon,evt.loc.lat,1 + int(dist / 1000))
        lons, lats = zip(*lonlats)
        ax.plot(lons, lats, color='red', linewidth=0.5, transform=ccrs.Geodetic(), alpha=0.5)

plt.title('Distribution of PiercePoints')
plt.tight_layout()
ax.set_extent([-180, 180, -90, 90], crs=ccrs.PlateCarree())
#plt.show()
plt.savefig('piercepoints.png', dpi=900, bbox_inches='tight', pad_inches=0.1)




























# plt.figure()
# ax = plt.axes(projection=ccrs.PlateCarree())
# ax.add_feature(cfeature.OCEAN, color='lightskyblue')
# ax.add_feature(cfeature.LAND, color="oldlace")
# ax.scatter(major_pt.lon,major_pt.lat,marker='o',s=20,color='#960056')
# ax.scatter(minor_pt.lon,minor_pt.lat,marker='o',s=20,color='#601ef9')
# for sta in basestations:
#     print(f'this is in base station {sta.lon} {sta.lat}')
#     ax.scatter(sta.lon,sta.lat,marker='o',s=20,color='red')
# ax.set_extent([-180, 180, -90, 90], crs=ccrs.PlateCarree())
# plt.title(f'{event_ID}')
# plt.savefig('piercepoints.png', dpi=700, bbox_inches='tight', pad_inches=0.1)