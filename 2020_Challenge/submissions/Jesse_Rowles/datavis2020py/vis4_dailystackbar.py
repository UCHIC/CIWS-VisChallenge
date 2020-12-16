from read_data import read_data
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import numpy as np

# Thie script creates stacked bar charts for each day on record of
# different types of water use events

raw, evn, mf, tdc = read_data()
evn.index = evn['start']

# initialize data frame to include totals for each day
tots = pd.DataFrame({'col':tdc[2]})
tots.index = tdc[0]

#get total volume of water use type for each day and store in 'tots'
dates = evn['start'].map(lambda t: t.date()).unique()
for i in dates:
    ct = i.strftime('%b-%d')
    tots[ct] = 0
    #filter by day of interest
    evnbt = evn.loc[(evn['start']>=i) & (evn['start'] < (i+dt.timedelta(days=1))),:]
    totyp = evnbt.groupby('label').sum()['vol'] #sum for each type
    tots.loc[totyp.index, ct] = totyp

#remove irrigation since it makes it impossible to read plots
tots = tots.drop('irrigation')
labels = pd.DatetimeIndex(dates).strftime('%a %b %d') #show day of week and date
#plot and save
fig = plt.figure(figsize = [7,7])
ax = fig.add_subplot(1,1,1)
bot = np.zeros(len(dates))
hands = []
for t in tots.index:
    vals = tots.loc[t,:].values[1:]
    c = evn.loc[evn['label'] == t, 'col'][0]
    ax.bar(labels,vals,bottom=bot,color=c)
    hands.append(t)
    bot = vals + bot
lgd = ax.legend(hands, bbox_to_anchor = [1.05,0.7])
# ax.set_ylim([0,300])
ax.set_ylabel('Volume Water Used (gal)')
plt.title('Total Volume of Water Used by Type of Use\nIn Each Day')
plt.xticks(rotation=90)
plt.savefig('Images/Daily Stacked Bar.png',bbox_extra_artists=(lgd,), bbox_inches='tight')
plt.show()
