from read_data import read_data
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import numpy as np

# creates stacked bar plots by type of event for proportion of day's use

plot_text = 0 #toggles turning on or off total volume text on bars

raw, evn, mf, tdc = read_data()
#create totals dataframe to keep track of total by type
tots = pd.DataFrame({'col':tdc[2],'vol':0})
tots.index = tdc[0]

#get total amount used
for i in tots.index:
    tots.loc[i,'vol'] = evn.loc[evn['label']==i,'vol'].sum()

#get total amount used by type for each day
dates = evn['start'].map(lambda t: t.date()).unique()
for i in dates:
    ct = i.strftime('%b-%d')
    tots[ct] = 0
    evnbt = evn.loc[(evn['start']>=i) & (evn['start'] < (i+dt.timedelta(days=1))),:]
    totyp = evnbt.groupby('label').sum()['vol']
    tots.loc[totyp.index, ct] = totyp

tc = tots['col']
tots = tots.drop('col',axis=1)
tnoir = tots.copy().drop('irrigation')

tots.loc['sum'] = tots.sum()
tnoir.loc['sum'] = tnoir.sum()
#calculate proportions of each type used on each day
tpro = (tots.divide(tots.loc['sum'].values))*100
tnip = (tnoir.divide(tnoir.loc['sum'].values))*100

labels = pd.DatetimeIndex(dates).strftime('%a %b-%d')

#with irrigation
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
bot = np.zeros(len(dates))
hands = []
for t in tpro.index:
    vals = tpro.loc[t, :].values[1:]
    if t != 'sum':
        c = (evn.loc[evn['label'] == t, 'col']).iloc[0]
        ax.bar(labels,vals,bottom=bot,color=c)
        bot = vals + bot
        hands.append(t)
lgd = ax.legend(hands, bbox_to_anchor = [1.1,1])
ax.set_ylabel('Proportion of Water Use Type (%)')
plt.title('Proportion of Water Used by Type of Use\nIn Each Day')
plt.xticks(rotation=90)
plt.savefig('Images/Daily Proportion Stacked Bar.png',bbox_extra_artists=(lgd,), bbox_inches='tight')
plt.show()

#no irrigation with option to add numbers
if plot_text == 1:
    fig = plt.figure(figsize=[9,7])
else:
    fig = plt.figure()
ax = fig.add_subplot(1,1,1)
bot = np.zeros(len(dates))
hands = []
for t in tnip.index:
    vals = tnip.loc[t, :].values[1:]
    if t != 'sum':

        c = (evn.loc[evn['label'] == t, 'col']).iloc[0]
        ax.bar(labels,vals,bottom=bot,color=c)
        hands.append(t)
        col = 'white'
    else:
        col = 'black'

    bot = vals + bot
    if plot_text == 1:
        textvals = np.nan_to_num(tnoir.loc[t, :].values[1:])
        vals = np.nan_to_num(vals)
        tt = [str(int(i)) for i in textvals]
        for j in range(len(vals)):
            if int(tt[j]) != 0: #add text of total volume used to each type on day
                plt.text(labels[j], bot[j] - vals[j], tt[j], ha='center', color=col, fontweight='bold')
lgd = ax.legend(hands, bbox_to_anchor = [1.1,1])
ax.set_ylabel('Proportion of Water Use Type (%)')
plt.title('Proportion of Water Used by Type of Use\nIn Each Day, Without Irrigation')
plt.xticks(rotation=90)
plt.savefig('Images/Daily Proportion Stacked Bar No Ir.png' ,bbox_extra_artists=(lgd,), bbox_inches='tight')
plt.show()
