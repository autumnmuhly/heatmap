#tests for the array quality 
import heatmap #import DistAz,Gridpoint,Station,Array,form_all_array,ArrayToEqlist,EqtoArrayList,EqGridAssignment,form_eq,group_items_by_dist,items_in_dist
import pytest
import jsonpickle
from types import SimpleNamespace

infilename = "heatmap.json"
with open(infilename, "r") as inf:
    mydata = jsonpickle.decode(inf.read())
mydata = SimpleNamespace(mydata)

array_list=mydata.array_list
good_arrays=mydata.good_arrays
eq_list=mydata.eq_list
for arr in good_arrays:
    array=arr.array
    stations=[]
    for sta in array.sta_list:
        stations.append(sta.name)
print(f'array at {array.pt} has these stations {stations}')