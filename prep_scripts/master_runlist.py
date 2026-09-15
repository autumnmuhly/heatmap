import os
import argparse
from obspy import UTCDateTime
from datetime import datetime, timezone
from displacement_velocity import displacement_velocity
import subprocess

def parseArgs():
    parser = argparse.ArgumentParser(description='creates dir, cp files, runs heatmap, and prepares for looper')
    parser.add_argument('-e', '--evtlist', help="list of events", required=True)
    return parser.parse_args()

def format_eventfile(eventfile):
    "Formats the event list to be in a readable format to make directories"
    events=[]
    with open (eventfile, "r") as infile:
        #headerline = infile.readline()
        for line in infile:
            items = line.split()
            date_and_time=items[2]
            print(date_and_time)
            events.append(date_and_time)
    with open('eq_list','w') as file1:
        for evt in events:
            text=(f'{evt}\n')
            file1.writelines(text)
    return events


def event_list(eventfile):
    event_ID=[]
    with open(eventfile, "r") as infile:
        #mheaderline = infile.readline()
        for line in infile:
            # print(line)
            event_ID.append(line.strip())
            # items = line.split()
            # #ID=items[0]
            # date=items[0]
            # time=items[1]
            # ID=datetime.strptime(f'{date} {time}', "%Y-%m-%d %H:%M:%S")
            # ID=UTCDateTime(ID).strftime("%Y%m%d%H%M")
            # event_ID.append(ID)
    return event_ID

def run_heatmap(event_ID):
    wd=os.getcwd()
    for evt in event_ID:
        print(evt)
        try: 
            os.mkdir(evt)
            os.chdir(evt)
            # print(os.getcwd)
            subprocess.run(['cp', '/home/amuhly/majorarc/All.stations', '.'])
            subprocess.run(['cp', f'/usc/data/ADEPT/Info/{evt}.event', '.'])
            #os.chdir(wd)
            os.system('cp /home/amuhly/majorarc/All.stations .')
            os.system(f'cp /usc/data/ADEPT/Info/{evt}.event .')
            # For yellowstone
            #os.system(f'heatmapcalc -s All.stations -e {evt}.event --minsta 20 --grid 40000 --arrayradius 1.4 -p SKS,SKKKKS --region -98 -83 33 41')
            os.system(f'heatmapcalc -s All.stations -e {evt}.event --minsta 20 --grid 40000 --arrayradius 1.0 -p SKKKKS')
            os.system(f'prepvespa')
            os.system(f'python3 /home/amuhly/heatmap/prep_scripts/grabsac.py -e {evt}')
            os.system("mv new_sta_list station_list_total")
            displacement_velocity(evt)
        except:
            print(f'directory already exists {evt}')
        os.chdir(wd)



args = parseArgs()
eventfile=args.evtlist
evt_list=event_list(eventfile)
# try:
#     evt_list=event_list(eventfile)
# except:
#     print('first we need to change the format')
#     evt_list=format_eventfile(eventfile)
#     eventfile='eq_list'
run_heatmap(evt_list)

