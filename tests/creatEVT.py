#Create a station list using obspy FDSN for stations that existed during the frame of reference, and certain magnitude
#eventid datetime name mag magtype lat lon depth np1_strike np1_dip np1_rake
import obspy
from obspy.clients.fdsn import Client
from obspy.core.utcdatetime import UTCDateTime
import os
if os.path.exists('sta_info.txt'):
    os.remove('sta_info.txt')
client = Client("IRIS")
starttime = UTCDateTime("2001-01-01")
endtime = UTCDateTime("2002-01-02")
min_mag=5.9
min_depth=70
cat=client.get_events(starttime=starttime, endtime=endtime,minmagnitude=min_mag,mindepth=min_depth)
print(cat)