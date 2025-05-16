
from datetime import datetime

from .gridpoint import Station, Location, EQ

def read_stations_adept(filepath):
    """
    Reads ADEPT style stations file. Each line is:
    network station location lat lon elevation depth firstdate lastdate
    """
    sta_list = []
    with open(filepath, "r") as infile:
        headerline = infile.readline() # ignore this one
        for line in infile:
            items = line.split()
            net = items[0]
            sta = items[1]
            loc = items[2]
            lat = float(items[3])
            lon = float(items[4])
            loc = Location(lat, lon)
            elev = float(items[5])
            depth = float(items[6])
            firstdate = datetime.fromisoformat(items[7])
            lastdate = datetime.fromisoformat(items[8])
            sta = Station(f"{net}_{sta}",loc, firstdate, lastdate)
            sta_list.append(sta)
    return sta_list


def read_earthquakes_adept(filepath):
    """
    Reads ADEPT style earthquake file. Each line is:
    eventid datetime name mag magtype lat lon depth np1_strike np1_dip np1_rake
    """
    eq_list = []
    with open(filepath, "r") as infile:
        headerline = infile.readline() # ignore this one
        for line in infile:
            items = line.split()
            eventid = items[0]
            time = datetime.fromisoformat(items[1])
            name = items[2]
            mag = float(items[3])
            magtype = items[4]
            lat = float(items[5])
            lon = float(items[6])
            loc = Location(lat, lon)
            depth = float(items[7])
            strike = float(items[8]) if items[8] != "None" else None
            dip = float(items[9]) if items[9] != "None" else None
            rake = float(items[10]) if items[10] != "None" else None
            eq = EQ(loc, time)
            eq_list.append(eq)
    return eq_list
