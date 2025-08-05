#grab sacfiles from a local or remote directory
import os
import jsonpickle
from types import SimpleNamespace
from obspy import UTCDateTime
import obspy
from obspy.clients.fdsn import Client
import statistics

class SacStream:
    def __init__(self, stanm, network):
        "Sac files have a sta name, min and max amp"
        self.stanm = stanm
        self.network=network
        self.depmin = [] #for later if we need it ?
        self.depmax = [] #for later if we need it ?

def readStaFile(stafile):
    sta_list = []
    #check for station duplicates using awk 
    command=f"awk -F, '!seen[$1>$2 ? $1 FS $2 : $2 FS $1]++' {stafile} > temp_sta"
    os.system(command)
    rm_command=f"mv -f temp_sta {stafile}"
    os.system(rm_command)
    #extract sta info from file
    with open('station_list_total', "r") as infile:
        headerline = infile.readline() # ignore this one
        for line in infile:
            items = line.split()
            sta_list.append(SacStream(items[0],items [1]))
    return sta_list

def check_sacfiles(stafile):
    """
    Removes sac files with bad amplitude value.
    takes in a station list txt file
    """
    #extract station info from file
    sta_list=readStaFile(stafile)
    
    #get min and max amplitudes for sac files
    for sta in sta_list:
            #change directories
            os.chdir(f"sac")
            stream=obspy.read(f'*.{sta.stanm}.{sta.network}*R.D.sac',debug_headers=True) #ending of .sac file is adept specific
            min=stream[0].stats.sac.depmin
            max=stream[0].stats.sac.depmax
            if min == 0 or min == "nan" or max == 0 or max == "nan":
                print(f'needs to be deleted {sta.stanm}')
                station=sta.stanm
                network=sta.network
                os.chdir(f"../")
                command=f"awk -v network='{network}' -v station='{station}' '$1 != station && $2 != network' {stafile} > output.txt"
                os.system(command)
                move_cmmd=f"mv -f output.txt {stafile}"
                os.system(move_cmmd)
            else:
                break
    os.chdir("../")
    return sta_list


def grab_sacfiles(checked_list,evt_name):
    for sacfile in checked_list:
        #print(f"cp /usc/data/ADEPT/{evt_name}/*{sacfile.stanm}.{sacfile.network}*R.D.sac .")
        #os.system('pwd')
        print(f"cp sac/{evt_name}.{sacfile.stanm}.{sacfile.network}*R.D.sac .")
        os.system(f"cp sac/{evt_name}.{sacfile.stanm}.{sacfile.network}*R.D.sac .")
        #os.system(f"cp /usc/data/ADEPT/{evt_name}/*{checked_list[i][0]}.{checked_list[i][1]}*R.D.sac .")
    return


infilename = "heatmap.json"
with open(infilename, "r") as inf:
    mydata = jsonpickle.decode(inf.read())
    mydata = SimpleNamespace(mydata)


#get event date 
for arr in mydata.good_arrays:
    for evt in arr.eqlists:
        eq_name=UTCDateTime(evt.time).strftime("%Y%m%d%H%M")
        #delete sta that dont have data
        #check to make sure station count is still good)


#cd to diretory with sac files 
#get rid of bad sac files
check_stalist=check_sacfiles('station_list_total')
grab_sacfiles(check_stalist,eq_name)


#check to make sure station count is still good???










    
# st = obspy.read('*.sac', debug_headers=True)
# sacfiles=[]
# for sacfile in st:   
#     sacfiles.append(SacStream(sacfile.stats.sac.kstnm.strip(),sacfile.stats.sac.depmin,sacfile.stats.sac.depmax))
    # stanm=sacfile.stats.sac.kstnm.strip()+''
    # time_beg=sacfile.stats.sac.b
    # time_end=sacfile.stats.sac.e
    # depmin.append(sacfile.stats.sac.depmin)
    # depmax=sacfile.stats.sac.depmax
    # file=open("STA_AMP_LIST.txt",'a+')
    # text=(f'{cnt} {stanm} {depmin} {depmax}\n')
    # file.writelines(text)
    # file.close()             
# mins=[]
# for str in sacfiles:
#     mins.append(str.depmin)
# med_min=statistics.median(mins)
# print(med_min)

# bad_sta=[]
# for str in sacfiles:
#     if str.depmin == 0 or str.depmin == "nan" or str.depmax == 0 or str.depmax == "nan":
#         print(f'{str.stanm} {str.depmin} {str.depmax}')
#     else: 
#         bad_sta.append(str.stanm)