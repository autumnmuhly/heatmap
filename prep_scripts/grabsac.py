#grab sacfiles from a local or remote repository
import os
import jsonpickle
from types import SimpleNamespace
from obspy import UTCDateTime

infilename = "heatmap.json"
with open(infilename, "r") as inf:
    mydata = jsonpickle.decode(inf.read())
    mydata = SimpleNamespace(mydata)

#check for station duplicates using awk 
os.system("awk -F, '!seen[$1>$2 ? $1 FS $2 : $2 FS $1]++' station_list_total | awk  '{print $0}' > temp_sta")
os.system("mv -f temp_sta station_list_total")
for arr in mydata.good_arrays:
    for evt in arr.eqlists:
        evt_name=UTCDateTime(evt.time).strftime("%Y%m%d%H%M")
        print(evt_name)

sta_list = []

with open('station_list_total', "r") as infile:
    headerline = infile.readline() # ignore this one
    for line in infile:
        items = line.split()
        sta_list.append([items[0],items [1]])

for i in range(len(sta_list)):
        print(f"cp /usc/data/ADEPT/{evt_name}/*{sta_list[i][0]}.{sta_list[i][1]}*R.D.sac .")
        os.system(f"cp /usc/data/ADEPT/{evt_name}/*{sta_list[i][0]}.{sta_list[i][1]}*R.D.sac .")