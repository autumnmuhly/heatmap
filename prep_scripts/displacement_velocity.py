from obspy.core import read 
import os 
import sys

def displacement_velocity(evt):
    # dirc=wd.split('/')[-1]
    dirc = evt
    print(dirc)
    #os.system("mv displacement_sac/*.sac .")
    sac_files='*.sac'
    st=read(sac_files)
    for tr in st:
        #print(tr.id)
        station=tr.stats.station
        network=tr.stats.network
        channel=tr.stats.channel
        #print(station,network,channel)
        new_trace=tr.differentiate(method='gradient')
        new_trace.write(f'{dirc}.{station}.{network}.{channel}.V.sac', format="sac")
    try:
        os.mkdir('displacement_sac')
    except:
        print('already has a displacement dir')
    os.system("mv *D.sac displacement_sac")
