#Create a station list using obspy FDSN for stations that existed during the frame of reference, and certain magnitude
import obspy
from obspy.clients.fdsn import Client
from obspy.core.utcdatetime import UTCDateTime
import os

client=Client("IRIS")
starttime=UTCDateTime("2001-01-01")
endtime=UTCDateTime("2001-01-02")
inventory=client.get_stations(starttime=starttime, endtime=endtime)

for network_list in inventory:
    network=network_list.code
    for station in network_list:
        sta=station.code
        stala=format(station.latitude,'.4f')
        stalo=format(station.longitude,'.4f')
        stael=station.elevation
        stadp=0.0
        location=0.0
        start=UTCDateTime(station.start_date).strftime("%Y-%m-%dT%H:%M:%S")
        end=UTCDateTime(station.end_date).strftime("%Y-%m-%dT%H:%M:%S")
        file=open("sta_info.txt",'a+')
        text=(f'{network} {sta} {location} {stala} {stalo} {stael} {stadp} {start} {end}\n')
        file.writelines(text)
        file.close()