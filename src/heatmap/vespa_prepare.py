#!/usr/bin/env python
#run this file after heatmapcalc to get files needed to run beamforming script
import sys
import os
import jsonpickle
from types import SimpleNamespace

def prepare_vespa():
    infilename = "heatmap.json"
    with open(infilename, "r") as inf:
        mydata = jsonpickle.decode(inf.read())
    mydata = SimpleNamespace(mydata)
    if os.path.exists('grid_pts.txt'):
        os.remove('grid_pts.txt')
    if os.path.exists('station_list_total'):
        os.remove('station_list_total')
    if os.path.exists('base_stations'):
        os.remove('base_stations')
    with open("base_stations_test",'w') as file1, open("grid_pts_test.txt",'w') as file2, open('station_list_total','w') as file3:
        count_array=0
        sta_list_total=[]
        for arr in mydata.good_arrays:
            count_array+=1
            #create base station list
            bs_text={f'{arr.array.basestation.netwrk} {arr.array.basestation.name} {format(arr.array.basestation.loc.lat,'.4f')} {format(arr.array.basestation.loc.lon,'.4f')}\n'}
            file1.writelines(bs_text)
            #create gridpoint list
            lat_array=format(arr.array.pt.loc.lat,'.4f')
            lon_array=format(arr.array.pt.loc.lon,'.4f')
            gp_text=(f'{count_array} {lat_array} {lon_array}\n')
            file2.writelines(gp_text)
            #create station list
            for sta in arr.array.sta_list:
                sta_list_total.append(sta)
                text=(f'{sta.netwrk} {sta.name} {0.0} {sta.loc.lat} {sta.loc.lon} {0.0} {0.0} {sta.start} {sta.stop}\n')
                file3.writelines(text)
    return 

def main():
    prepare_vespa()

if __name__ == '__main__':
    sys.exit(main())