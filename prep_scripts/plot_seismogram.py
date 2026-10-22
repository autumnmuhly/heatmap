from obspy.core import read
from obspy.taup import TauPyModel
import matplotlib.pyplot as plt
from datetime import datetime, timezone
import matplotlib.dates as mdates
import numpy as np
import matplotlib.ticker as ticker

class Arrival:
    def __init__(self,phase,time,rayparam):
        'earthquakes have a location and a time'
        self.phase=phase
        self.time=time
        self.rayparm=rayparam
    def __str__(self):
        return f"{self.time} {self.loc}"


# comp='Z'

# st=read(f'*{comp}.sac')
st = read('201502271345.CI.WHF.BHR.V.sac')

# evtdep=20
# dist=117

# min_freq=0.04
# max_freq=.125
# poles=2

# model = TauPyModel(model="prem")
# arrivals = model.get_travel_times(evtdep, dist,phase_list=["SKS", "SKKS","pPPPP","PPPPP"])
# dt = st[0].stats.starttime
# print(dt)
# print(dt.type)
# t1 = dt + 1480
# t2 = dt + 1580
# print(arrivals)

# times = np.arange(np.datetime64('2001-01-02'),
#                   np.datetime64('2002-02-03'), np.timedelta64(75, 'm'))


fig, ax = plt.subplots(figsize=(11,8.5))
ax=fig.axes[0]

start=st[0].stats.starttime
# time_1 = start+1600
# time_2 = start+2500
newtrace=st[0].trim(start+1600,start+1700)
# t1 = mdates.date2num(np.datetime64('2025-12-31T05:50:30'))
# # t2 = mdates.date2num(np.datetime64('2025-12-31T05:53:00'))
# t2 = mdates.date2num(np.datetime64('2025-12-31T05:53:03'))
# #colors={'HHR':'black','HHT':'red'}
for trace in st:
    #trace.filter('bandpass', freqmin=min_freq, freqmax=max_freq, corners=poles, zerophase=True)
    #trace.filter("bandpass", freqmin=1.0, freqmax=20.0, corners=4, zerophase=True)
    times=trace.times("matplotlib")
    # print(times)
    ax.plot_date(times, trace.data, '-', 
                 label=trace.stats.channel)
    #ax.set_aspect(aspect=0.2) 
    # ax.set_xlim(t1,t2)
    # ax.yaxis.set_major_locator(ticker.MultipleLocator(100))
    # ax.yaxis.set_minor_locator(ticker.MultipleLocator(10))
    # ax.tick_params(axis='y', which='minor',
    #            length=3,      # small tick size
    #            labelleft=False)
    # ax.tick_params(axis='y', which='major', length=7)
    # ax.xaxis.set_major_locator(mdates.SecondLocator(interval=10))
    # ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    # ax.xaxis.set_minor_locator(mdates.SecondLocator(interval=1))
    # ax.tick_params(axis='x', which='minor',
    #            length=3,
    #            labelbottom=False)
    # ax.tick_params(axis='x', which='major', length=7, labelrotation=300)
    # ax.set_xlabel('Time (HH:MM:SS)')
    # ax.set_ylabel('Amplitude (mm)')



# #fig=vel_tr_BO2B.plot(starttime=dt+1350, endtime=dt+1500,show=False,handle=True)
# #fig=vel_tr_BO2B.plot(starttime=dt+1350, endtime=dt+1500,show=False,handle=True)
# # ax=fig.axes[0]

# # for arr in arrivals:
# #     arrival_time=dt+arr.time
# #     if (dt+1350)<arrival_time<(dt+1500):
# #         ax.axvline(arrival_time.matplotlib_date, color="purple", linestyle="--")
# #         ax.text(arrival_time.matplotlib_date, ax.get_ylim()[1]*0.9,
# #                 arr.name, color="purple", rotation=90, va="top")

# plt.title(f'EQ1: Seismogram 2')
plt.savefig('plotting_fullseismogram.png',bbox_inches='tight')
# plt.show()
# fig.savefig(f"ENAM_{channel}_velo_{min_freq}_{max_freq}_{poles}.png", dpi=800, bbox_inches="tight")


# #Do for displacement
# dis_tr_BO2B=tr_BO2B.integrate(method='cumtrapz')
# fig=dis_tr_BO2B.plot(starttime=dt+1350, endtime=dt+1500,show=False,handle=True)
# ax=fig.axes[0]

# for arr in arrivals:
#     arrival_time=dt+arr.time
#     if (dt+1350)<arrival_time<(dt+1500):
#         ax.axvline(arrival_time.matplotlib_date, color="purple", linestyle="--")
#         ax.text(arrival_time.matplotlib_date, ax.get_ylim()[1]*0.9,
#                 arr.name, color="purple", rotation=90, va="top")
        
# plt.title(f'Displacement Bandpass {min_freq} {max_freq} {poles}')
# #plt.show()
# fig.savefig(f"ENAM_ECHS_{comp}displace_{min_freq}_{max_freq}_{poles}.png", dpi=800, bbox_inches="tight")

# # #Do for acceleration 

# # acc_tr_BO2B=tr_BO2B.differentiate(method='gradient')
# # fig=acc_tr_BO2B.plot(starttime=dt+1350, endtime=dt+1500,show=False,handle=True)
# # ax=fig.axes[0]

# # for arr in arrivals:
# #     arrival_time=dt+arr.time
# #     if (dt+1350)<arrival_time<(dt+1500):
# #         ax.axvline(arrival_time.matplotlib_date, color="purple", linestyle="--")
# #         ax.text(arrival_time.matplotlib_date, ax.get_ylim()[1]*0.9,
# #                 arr.name, color="purple", rotation=90, va="top")
        
# # plt.title(f'Acceleration Bandpass {min_freq} {max_freq} {poles}')
# # #plt.show()
# # fig.savefig(f"ENAM_BO5B_accel_{min_freq}_{max_freq}_{poles}.png", dpi=800, bbox_inches="tight")
