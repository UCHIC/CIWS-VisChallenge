from read_data import read_data
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.patches as ptc
import matplotlib.dates as mdt
from shapely.geometry.polygon import Polygon as pgn
import datetime as dt
import numpy as np
import math

#show reduction in water used when certain improvements are implemented

raw, evn, mf, tdc = read_data()

# create totals dataframe for totals over period of record
tots = pd.DataFrame(index = tdc[0])
tots.index = tdc[0]
evn['vol'] = evn['flow_gpm']*evn['dur']
tots['Original'] = evn.groupby('label').sum()['vol']

#thresholds
slim = 10 # minutes to limit showers to
flim = 1.5 # flow rate shower limit
tlim = 1.3 # limit of gallons per toilet flush
plim = 0.75 # proportion of current faucet flow rate new ones could give

#limit showers to 10 minutes
evnsd = evn.copy()
#find every shower event greater than ten minutes and cap it at 10 minutes
evnsd.loc[(evnsd['dur']>slim) & (evnsd['label']=='shower'),'dur'] = slim
#recalculate volume used based on average flow provided
evnsd['vol'] = evnsd['flow_gpm']*evnsd['dur']
slimttl = 'Shower Duration Max ' + str(slim) + ' Min'
#recalculate sums of each type
tots[slimttl] = evnsd.groupby('label').sum()['vol']



#replace showerheads with 1.5 gpm flow
evnfl = evn.copy()
#cap shower head flow rate to 1.5 gpm by setting all events higher than 1.5 to 1.5
evnfl.loc[(evnfl['flow_gpm']>flim) & (evnfl['label']=='shower'),'flow_gpm'] = flim
#recalulate volume based on new flow rates
evnfl['vol'] = evnfl['flow_gpm']*evnfl['dur']
flimttl = 'Shower Flow ' + str(flim) + ' gpm'
#recalulate totals
tots[flimttl] = evnfl.groupby('label').sum()['vol']

#low water-use toilet
evnvl = evn.copy()
# cap toilet flush volume by given tlim (1.3 gallons per flush)
evnvl.loc[(evnvl['vol']>tlim) & (evnvl['label']=='toilet'),'vol'] = tlim
tlimttl = str(tlim) + ' Gallons Per Toilet Flush'
#recalculate volumes by type
tots[tlimttl] = evnvl.groupby('label').sum()['vol']

#plim factor on faucets
evnfp = evn.copy()
#scale faucet use by 75% based on average calculation
evnfp.loc[(evnfp['label']=='faucet'),'flow_gpm'] = evnfp.loc[(evnfp['label']=='faucet'),'flow_gpm'] * plim
evnfp['vol'] = evnfp['flow_gpm']*evnfp['dur']
plimttl = str(int(plim*100)) + '% Faucet Flow Rate'
#recalculate totals
tots[plimttl] = evnfp.groupby('label').sum()['vol']

#implement all changes
evnall = evn.copy()
evnall.loc[(evnall['dur']>slim) & (evnall['label']=='shower'),'dur'] = slim #shower duration
evnall.loc[(evnall['flow_gpm']>flim) & (evnall['label']=='shower'),'flow_gpm'] = flim #shower flow
#faucet flow
evnall.loc[(evnall['label']=='faucet'),'flow_gpm'] = evnall.loc[(evnall['label']=='faucet'),'flow_gpm'] * plim
#have to recalculate volume first since the toilet change affects volume directly which
# is what's being summed
evnall['vol'] = evnall['flow_gpm']*evnall['dur']
evnall.loc[(evnall['vol']>tlim) & (evnall['label']=='toilet'),'vol'] = tlim #toilet volume limit
tots['All Changes'] = evnall.groupby('label').sum()['vol']

#remove irrigation since it makes it impossible to read
tots = tots.drop('irrigation')

label = []
tots.loc['sum'] = tots.sum(axis=0)

#format labels to create new line for each word for readability
for l in tots.columns:
    sp = [p for p, ltr in enumerate(l) if ltr == ' ']
    lab = l
    if len(sp) > 0:
        for s in sp:
            lab = lab[0:s] + '\n' + lab[s+1:]
    label.append(lab)

#plot and save
fig = plt.figure(figsize=[7,7])
ax = fig.add_subplot(1,1,1)
bot = np.zeros(len(tots.columns))
hands = []
labels = []
for t in tots.index:
    vals = tots.loc[t, :].values
    for v in range(len(vals)):
        #gray out bars that haven't changed from original
        if (vals[v] == vals[0]) and (v > 0):
            alph = 0.45
        else: #if changed or in original dataset, make full alpha (bold)
            alph = 1
        #add bold
        if t != 'sum':
            c = evn.loc[evn['label'] == t, 'col'].values[0]
            bh = ax.bar(label[v],vals[v],bottom=bot[v],color=c,alpha=alph)
        if v == 0:
            hands.append(bh)

    if t != 'sum': #creates text to add of volume used to each use
        labels.append(t)
        col = 'white'
    else:
        col = 'black'
    bot = vals + bot #keep track of top of previous type plotted to stack bars
    tv = np.append(vals[0],vals[1:]-vals[0])
    tt = [str(int(i)) for i in tv]
    for j in range(len(vals)): #plots total volume used text on top of each bar
        plt.text(label[j],bot[j]-vals[j],tt[j],ha='center',color=col,fontweight='bold')
lgd = ax.legend(labels=labels,handles=hands,bbox_to_anchor = [1.1,1]) # add legend
ax.set_ylabel('Volume Water Used (gal)')
plt.plot([0.5,0.5],[0,max(tots.loc['sum',:])+100],'k--',linewidth=3)
plt.title('Difference in Total Volume of Water Used With Improvements (gal)')
plt.savefig('Images/Improvements Stacked Bar Diff.png',bbox_extra_artists=(lgd,), bbox_inches='tight')
plt.show()


#plot figure same as above, only with difference from original numbers plotted on the bars
fig = plt.figure(figsize=[7,7])
ax = fig.add_subplot(1,1,1)
bot = np.zeros(len(tots.columns))
hands = []
labels = []

for t in tots.index:
    vals = tots.loc[t, :].values
    for v in range(len(vals)):
        if (vals[v] == vals[0]) and (v > 0): #gray out unchanged bars
            alph = 0.5
        else: #bold original or changed bars
            alph = 1

        if t != 'sum': #add bars
            c = evn.loc[evn['label'] == t, 'col'].values[0]
            bh = ax.bar(label[v],vals[v],bottom=bot[v],color=c,alpha=alph)
        if v == 0:
            hands.append(bh)

    if t != 'sum': #set color of text to be plotted
        labels.append(t)
        col = 'white'
    else:
        col = 'black'
    bot = vals + bot
    tt = [str(int(i)) for i in vals]
    for j in range(len(vals)): #add text of change from original volume used
        plt.text(label[j],bot[j]-vals[j],tt[j],ha='center',color=col,fontweight='bold')
lgd = ax.legend(labels=labels,handles=hands,bbox_to_anchor = [1.1,1])

ax.set_ylabel('Volume Water Used (gal)')
plt.title('Total Volume of Water Used With Improvements (gal)')
plt.savefig('Images/Improvements Stacked Bar.png',bbox_extra_artists=(lgd,), bbox_inches='tight')
plt.show()

