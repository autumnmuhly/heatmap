#test case for earthquake and array calculator
#these are the files to read in since im going to start messing with things
import heatmap
import pytest
from math import radians, cos, sin, asin, sqrt, pi
from .load_resource import test_stations_lat, test_earthquakes

def test_eq_arr(test_stations_lat, test_earthquakes):
    number_points=1000
    radius_of_earth=6378
    dist=(10,20)
    station_list=test_stations_lat
    eq_list=test_earthquakes
    grid_array=heatmap.create_gridpoint(number_points)
    area_per_point=(4*pi*radius_of_earth*radius_of_earth)/number_points
    radius_point_km=sqrt(area_per_point/pi)
    radius_point_deg=radius_point_km/111
    min_station=1
    array_list=heatmap.form_all_array(station_list,grid_array,2,min_station)
    for arr in array_list:
        for evt in eq_list:
            arr.check_eq(evt,dist)
    min_eq_needed=1
    good_arrays=[]
    for arr in array_list:
        if arr.eqcount>min_eq_needed:
            good_arrays.append(arr)
    eq_count=[]
    for arr in good_arrays:
        eq_count.append(arr.eqcount)
    max_value=max(eq_count)
    assert max_value<=len(eq_count)
    assert eq_count[0]==2, eq_count[1]==2  # if set up with 1000 points, and dist = (10,20)
    return print('everything looks good :)')
