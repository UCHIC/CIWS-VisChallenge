from read_data import read_data
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import numpy as np

#this script creates stacked bar charts for each hour of the day

#read in data, create totals dataframe to keep track of totals by type
raw, evn, mf, tdc = read_data()
evn.index = evn['start']
tots = pd.DataFrame({'col':tdc[2]})
tots.index = tdc[0]
#create bins for hour of day starting at midnight
bins = pd.date_range('2020-07-01', periods=24, freq='1H')
#loop through bins to calculate total in each hour
for i in bins:
    ct = i.strftime('%H:%M') #format as hour:minute for plotting labels
    tots[ct] = 0 #initialize new column in totals dataframe containing totals from hour

    #filter dataframe between hours of interest
    evnbt = evn.between_time(ct, (i+dt.timedelta(minutes=60)).strftime('%H:%M'))
    #sum volume over each type
    totyp = evnbt.groupby('label').sum()['vol']
    tots.loc[totyp.index, ct] = totyp

#plot
labels = bins.strftime('%H:%M')
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
bot = np.zeros(len(bins)) #keeping track of the top of the previous type so that bar charts can be stacked
hands = []
for t in tots.index:
    vals = tots.loc[t,:].values[1:]
    c = evn.loc[evn['label'] == t, 'col'][0]
    ax.bar(labels,vals,bottom=bot,color=c)
    hands.append(t)
    bot = vals + bot #change bot to be top of this type so next type will be on top of it
ax.legend(hands)
ax.set_ylim([0,300])
ax.set_ylabel('Volume Water Used (gal)')
plt.title('Total Volume of Water Used by Type of Use\nIn Each Hour of Day')
plt.xticks(rotation=90)
plt.savefig('Images/Hourly Stacked Bar.png')
plt.show()
