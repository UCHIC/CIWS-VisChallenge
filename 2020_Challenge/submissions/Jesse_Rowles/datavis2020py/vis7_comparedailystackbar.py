from read_data import read_data
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import numpy as np

#this script creates a new dataset based on given dataset to compare
# the home given to the new dataset, intended to be fake data representative
# of other nearby homes

raw, evn, mf, tdc = read_data()
evn.index = evn['start']

#initialize totals dataset
tots = pd.DataFrame({'col':tdc[2]})
tots.index = tdc[0]
#initialize totals dataset containing 'nearby' homes
othertots = tots.copy()

#loop through dates to calculate totals
dates = evn['start'].map(lambda t: t.date()).unique()
for i in dates:
    ct = i.strftime('%b-%d')
    tots[ct] = 0

    evnbt = evn.loc[(evn['start']>=i) & (evn['start'] < (i+dt.timedelta(days=1))),:]
    totyp = evnbt.groupby('label').sum()['vol']
    tots.loc[totyp.index, ct] = totyp

    #make up nearby homes data by multiplying homes data by some value likely less than 1
    othertots[ct] = 0
    for t in totyp.index:
        newval = 0
        while newval <= 0:
            newval = totyp.loc[t]*np.random.normal(loc=0.7,scale=0.2)
        othertots.loc[t, ct] = newval

#get rid of irrigation
tots = tots.drop('irrigation')
othertots = othertots.drop('irrigation')

#plot stacked bar charts for both types next to each other
labels = pd.DatetimeIndex(dates).strftime('%a %b %d')
fig = plt.figure(figsize = [13,6])
ax = fig.add_subplot(1,1,1)
bot = np.zeros(len(dates))
obot = np.zeros(len(dates))
hands = []
labs = []
x = np.arange(0,len(labels))
xs = 0.15
tots.loc['sum'] = tots.sum()
othertots.loc['sum'] = othertots.sum()
for t in tots.index:
    vals = tots.loc[t,:].values[1:]
    ovals = othertots.loc[t,:].values[1:]
    if t != 'sum': #plot each type of water use individually
        c = evn.loc[evn['label'] == t, 'col'][0]
        eh = 'none'
        ea = eh
    else: #only plot outlines on total height of bar
        c = 'none'
        eh = 'deepskyblue' #outline color for home of interest
        ea = 'yellowgreen' #outline color for all other homes
        bot = 0
        obot = 0
    h2 = ax.bar(x + (xs+0.02), ovals, bottom=obot, color=c, edgecolor=ea, width=xs * 2, linewidth=2)
    h1 = ax.bar(x-(xs+0.02),vals,bottom=bot,color=c,edgecolor=eh,label=t, width = xs*2,linewidth=2)

    #keep track for legend
    if t != 'sum':
        hands.append(h1)
        labs.append(t)
    else:
        hands.extend([h1,h2])
        labs.extend(['Building of Interest','Median of Nearby Buildings'])

    obot = ovals + obot
    bot = vals + bot

ax.set_xticks(x)
ax.set_xticklabels(labels)
lgd = ax.legend(labels=labs,handles=hands, bbox_to_anchor = [1.05,0.7])
# ax.set_ylim([0,300])
ax.set_ylabel('Volume Water Used (gal)')
plt.title('Total Volume of Water Used by Type of Use\nCompared Between Building of Interest and Nearby Homes')
plt.xticks(rotation=90)
plt.savefig('Images/Daily Stacked Bar Compare.png',bbox_extra_artists=(lgd,), bbox_inches='tight')
plt.show()
