from obspy.core.event import read_events
from obspy.core.utcdatetime import UTCDateTime
cat = read_events('events_6.xml')
print(cat)
for evt in cat:
    event=evt.origins[0]
    evtid=event.resource_id
    lat=event.latitude
    lon=event.longitude
    time=UTCDateTime(event.time).strftime("%Y-%m-%dT%H:%M:%S")
    name=UTCDateTime(event.time).strftime("%Y%m%dT%H%M%S")
    depth=event.depth
    np1_strike=0
    np1_dip=0
    np1_rake=0
    magnitudes=evt.magnitudes
    magnitudes=evt.magnitudes[0]
    mag=magnitudes.mag
    magtype=magnitudes.magnitude_type
    #print(evtid, time, mag, magtype, lat, lon, depth, np1_strike, np1_dip, np1_rake)
    #name datetime mag magtype lat lon depth np1_strike np1_dip np1_rake eq_id url dir rtz_stacount rtz_filecount zne_stacount zne_filecoun
    file=open("evt_info.txt",'a+')
    text=(f'{name} {time} {mag} {magtype} {lat} {lon} {depth} {np1_strike} {np1_dip} {np1_rake}\n')
    file.writelines(text)
    file.close()
