import os
import argparse
from obspy import UTCDateTime
from datetime import datetime, timezone

def parseArgs():
    parser = argparse.ArgumentParser(description='creates dir, cp files, runs heatmap, and prepares for looper')
    parser.add_argument('-e', '--evtlist', help="list of events", required=True)
    return parser.parse_args()

eventfile="run_these.txt"
def event_list(eventfile):
    event_ID=[]
    with open(eventfile, "r") as infile:
        headerline = infile.readline()
        for line in infile:
            items = line.split()
            date=items[0]
            time=items[1]
            ID=datetime.strptime(f'{date} {time}', "%Y-%m-%d %H:%M:%S")
            ID=UTCDateTime(ID).strftime("%Y%m%d%H%M")
            event_ID.append(ID)
    return event_ID
def run_heatmap(event_ID):
    wd=os.getcwd()
    for evt in event_ID:
        print(evt)
        if os.path.exists(evt):
            os.system('rm -r '+evt)
        os.mkdir(evt)
        os.chdir(evt)
        os.system('cp /home/amuhly/majorarc/All.stations .')
        os.system(f'cp /usc/data/ADEPT/Info/{evt}.event .')
        os.system(f'heatmapcalc -s All.stations -e {evt}.event --minsta 20 --grid 40000 --arrayradius 1.4 -p SKS,SKKKKS')
        os.chdir(wd)
        # os.system(f'cp /home/amuhly/heatmap/prep_scripts/grab_sac.py')
    
args = parseArgs()
eventfile=args.evtlist
evt_list=event_list(eventfile)
run_heatmap(evt_list)
