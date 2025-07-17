#autumn muhly June 13,2025
#obspy version to get station information for a list of .sac files. Requires you to be in directory with the .sac files. return sra_info.txt file in the proper format for TALOOPER
#network station location lat lon elevation depth firstdate lastdate
import obspy
from obspy.clients.fdsn import Client
import os
from obspy import UTCDateTime

if os.path.exists('sta_info.txt'):
    os.remove('sta_info.txt')
st = obspy.read('*.sac', debug_headers=True)
client=Client('IRIS')
for sacfile in st:
    stanm=sacfile.stats.sac.kstnm.strip()+''
    stala=format(sacfile.stats.sac.stla,'.4f')
    stalo=format(sacfile.stats.sac.stlo,'.4f')
    stael=0
    stadp=0
    netwrk=sacfile.stats.sac.knetwk
    inventory=client.get_stations(network=netwrk,station=stanm,level='station')
    station=inventory[0][0]
    start=UTCDateTime(station.start_date).strftime("%Y-%m-%dT%H:%M:%S")
    end=station.end_date
    if end is not None:
        end=UTCDateTime(station.end_date).strftime("%Y-%m-%dT%H:%M:%S")
    location=00
    file=open("sta_info.txt",'a+')
    text=(f'{netwrk[:2]} {stanm} {location} {stala} {stalo} {stael} {stadp} {start} {end}\n')
    file.writelines(text)
    file.close()
print('Run create_evt.py if you dont have event list. If you have event list you are ready to heatmap')
