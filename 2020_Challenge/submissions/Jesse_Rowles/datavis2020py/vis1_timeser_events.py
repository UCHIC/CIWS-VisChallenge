from read_data import read_data
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.patches as ptc
import matplotlib.dates as mdt
import datetime as dt
import numpy as np
import math

#This visualization shows time series of raw volume recorded in each time step
# as well as a color coded rectangle to show the time and duration of each event

raw, evn, mf, tdc = read_data()

# gets unique list of each date in the dataset
dates = evn['start'].map(lambda t: t.date()).unique()

#all 15 days are a lot to put on one plot so, do 'daysper' per plot
daysper = 3
n=1

# Option to toggle collapsing colored events to one line or keep separate
collapse = 1 #0 to show on different y values, 1 to show on same y

for d in range(len(dates)):
    #initialize dataframe to keep track of totals in each type for showing in legend
    tots = pd.DataFrame(index=tdc[0], columns=['vol'])
    tots['vol'] = 0 #create volume column

    #only creat figure on first of 'daysper' days
    pnum = math.fmod(d, daysper)+1
    if pnum == 1:
        fig = plt.figure(figsize=[16, 16])
    ax = fig.add_subplot(daysper,1,pnum)
    dtstr = dates[d].strftime('%b-%d-%Y') #reformat date for labeling plots
    dmn = dt.datetime.combine(dates[d], dt.time())
    td = dmn
    tm = dmn + dt.timedelta(days=1)
    print(dtstr)
    ax.set_ylabel(dtstr + '\nFlow Rate Water Used (gal/min)')

    #filter raw dataset to day of interest based on 'start' index
    dayraw = raw[(raw.index >= td) & (raw.index < tm)]
    dayevn = evn[(evn['start'] >= td) & (evn['start'] < tm)].reset_index()
    #plot raw volume of day
    pts = ax.plot(dayraw.index,dayraw.gpm,'-',color='black',alpha=1,label = 'Flow Rate Water Used (gal/min)')
    ax2 = ax.twinx()
    for i in range(0,len(dayevn.index)):
        #loop through each event in the day and plot it as a colored rectangle
        l = dayevn.loc[i,'label']
        v = dayevn.loc[i,'vol']
        tots.loc[l,'vol'] = tots.loc[l,'vol'] + v
        s = mdt.date2num(dayevn.loc[i,'start'])
        e = mdt.date2num(dayevn.loc[i,'end'])
        if collapse == 0:
            y = dayevn.loc[i,'cnum']
        else:
            y = 0
        r = ptc.Rectangle((s,y),e-s,1,color=dayevn.loc[i,'col'],alpha=0.4)
        ax2.add_patch(r)

    #format date on x axis for readability
    fmt = mdt.DateFormatter('%H:%M')
    ax.xaxis.set_major_formatter(fmt)

    #label second y axis based on if collapsed or not
    if collapse == 0:
        ax2.set_ylim([0,6])
        ax2.set_yticks(np.arange(0.5,7,1))
        ax2.set_yticklabels(tdc[0])
    else:
        ax2.set_ylim([0,1])
        ax2.axes.get_yaxis().set_visible(False)

    #add values of total volume of water used in each type to legend (plus percentages)
    tots = tots.append(pd.DataFrame({'vol':sum(tots['vol'])},index=['sum']))
    tots['prop'] = (tots['vol']/tots.loc['sum','vol'])*100
    leg=pts
    for t in tots.index: #this loop builds each legend entry individually and manually
        if not t == 'sum':
            lab = t+': ' + str(round(tots.loc[t,'prop'],1)) + '% (' + \
                str(round(tots.loc[t, 'vol'], 1)) + ' gal)'
            c = np.unique(evn.loc[evn['label']==t,'col'])[0]
            hdl = ptc.Patch(color = c, label = lab)
            leg.append(hdl)
    lgd = ax2.legend(handles = leg,title = 'Daily Totals',bbox_to_anchor=(1.1,1))
    ax.set_xlim([td,tm])

    #save figure and show
    if pnum == daysper:
        plt.savefig('Images/Time Series ' + str(n) +'.png',bbox_extra_artists=(lgd,), bbox_inches='tight')
        n = n + 1
plt.draw()
plt.show()