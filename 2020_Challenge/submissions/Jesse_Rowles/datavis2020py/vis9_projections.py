from read_data import read_data
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.patches as ptc
import matplotlib.dates as mdt
import datetime as dt
import numpy as np
import math

#This visualization takes the first week of the data and projects forward to a monthly scale.
# Then, it compares the monthly scale to previous months of that home, as well as
# nearby homes statistics
plot_text = 1
raw, evn, mf, tdc = read_data()
dates = evn['start'].map(lambda t: t.date()).unique()

#create a list of the dates in the first week of the data
wk1dts = dates[dates <= min(dates) + dt.timedelta(weeks=1)]

#create totals dataframe to keep track of total by type in home of interest,
#past months at home, nearby buildings, and past months of nearby buildings
tots = pd.DataFrame({'col':tdc[2]})
tots.index = tdc[0]
wk1ind = np.in1d(evn['start'].map(lambda t: t.date()), wk1dts)

#loop through each type, get first week of data, multiply by 4 to project to month
# also multiply by some random numbers to make up data for previous months and nearby homes
for i in tots.index:
    tots.loc[i,'Current Projected Month Your Home'] = (evn.loc[evn['label']==i,'vol'].sum())*4
    tots.loc[i,'Min Previous Your Home'] = (evn.loc[evn['label']==i,'vol'].sum())*4*np.random.normal(loc=0.5,scale=0.2)
    tots.loc[i, 'Avg Previous Your Home'] = (evn.loc[evn['label'] == i, 'vol'].sum()) * 4 *np.random.normal(loc=0.8,scale=0.2)
    tots.loc[i, 'Max Previous Your Home'] = (evn.loc[evn['label'] == i, 'vol'].sum()) * 4 *np.random.normal(loc=1.2,scale=0.2)

    tots.loc[i, 'Current Projected Nearby Homes'] = (evn.loc[evn['label'] == i, 'vol'].sum()) * 4 * np.random.normal(loc=0.7,
                                                                                                        scale=0.2)
    tots.loc[i, 'Min Previous Nearby Homes'] = (evn.loc[evn['label'] == i, 'vol'].sum()) * 4 * np.random.normal(loc=0.4,
                                                                                                        scale=0.2)
    tots.loc[i, 'Avg Previous Nearby Homes'] = (evn.loc[evn['label'] == i, 'vol'].sum()) * 4 * np.random.normal(loc=0.7,
                                                                                                        scale=0.2)
    tots.loc[i, 'Max Previous Nearby Homes'] = (evn.loc[evn['label'] == i, 'vol'].sum()) * 4 * np.random.normal(loc=1.1,
                                                                                                        scale=0.2)

tots = tots.drop('irrigation') #remove irrigation since it's hard to analyze data
tots.loc['sum'] = tots.sum() # calculate sums for each dataset of home and nearby homes
label = []

#format labels to create new line for each word for readability
for l in tots.columns:
    if l != 'col':
        sp = [p for p, ltr in enumerate(l) if ltr == ' ']
        lab = l
        if len(sp) > 0:
            for s in sp:
                lab = lab[0:s] + '\n' + lab[s+1:]
        label.append(lab)

# set up bottom values for stacked bar
bot = np.zeros(len(tots.columns)-1)

fig = plt.figure(figsize = [13,6])
ax = fig.add_subplot(1,1,1)

#set x values to separate current month trend from previous month trends from nearby home trends
x = np.arange(0,len(label))
x[1:] = x[1:] + 1
x[np.in1d(label,[i for i in label if 'Nearby' in i])] = x[np.in1d(label,[i for i in label if 'Nearby' in i])]+1

hands = []
labs = []

#plot stacked bar for each type
for t in tots.index:
    vals = tots.loc[t,:].values[1:]
    if t != 'sum': #plot each type of water use individually
        c = tots.loc[tots.index == t,'col'].get_values()[0] #type color
        col = 'white' #text color
        eh = 'black' #edge color
        h1 = ax.bar(x,vals,bottom=bot,color=c,edgecolor=eh,label=t) #plot type bar

    #keep track of handles and labels for legend
        hands.append(h1)
        labs.append(t)
    else:
        col = 'black' #text color


    bot = vals + bot #update bottom value so next bars will be on top of previous
    if plot_text == 1: #add volume numbers to bar
        textvals = np.nan_to_num(tots.loc[t, :].values[1:])
        vals = np.nan_to_num(vals)
        tt = [str(int(i)) for i in textvals] #turn values into rounded string
        for j in range(len(vals)):
            if int(tt[j]) != 0:  # add text of total volume used to each type on projected month
                plt.text(x[j], bot[j] - vals[j], tt[j], ha='center', color=col, fontweight='bold')

#add dashed line from current month projections to others
plt.plot(np.array([min(x), max(x)+1]),np.repeat(tots.loc['sum','Current Projected Month Your Home'],2),'k--',linewidth=2)
ax.set_xticks(x)
ax.set_xticklabels(label)
lgd = ax.legend(labels=labs,handles=hands, bbox_to_anchor = [1.05,0.7])
ax.set_ylabel('Volume Water Used (gal)')
plt.title('Total Volume of Water Used in First Week Projected to Month by Type of Use\nCompared Between Building of Interest and Nearby Homes Trends')
plt.savefig('Images/Total Month Projected Stacked Bar Compare.png',bbox_extra_artists=(lgd,), bbox_inches='tight')
plt.show()
