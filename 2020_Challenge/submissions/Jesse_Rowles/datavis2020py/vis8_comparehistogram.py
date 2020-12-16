from read_data import read_data
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import numpy as np

#this script creates histogram of the home of interest for each type of water use
# on top of histograms of (made-up) data of nearby homes

raw, evn, mf, tdc = read_data()
evn.index = evn['start']

dates = evn['start'].map(lambda t: t.date()).unique()
#this time the totals dataframe is set up differently with each half-day being
# the index rather than the type in other scripts here.
tots = pd.DataFrame(index=pd.DatetimeIndex(pd.date_range(min(dates),max(dates),\
                     freq='12H')),columns=tdc[0])
othertots = tots.copy()


for i in tots.index: #gets totals for each day
    evnbt = evn.loc[(evn['start']>=i) & (evn['start'] < (i+dt.timedelta(hours=12))),:]
    for j in tots.columns:
        tots.loc[i,j] = evnbt.loc[evnbt['label']==j,'vol'].sum()
        #randomly scale data from home by some value most likely less than 1 for comparison
        othertots.loc[i,j] = evnbt.loc[evnbt['label']==j,'vol'].sum() * np.random.normal(loc=0.7,scale=0.2)

#remove totals
tots = tots.drop('irrigation',axis = 1)
othertots = othertots.drop('irrigation',axis = 1)

tots['Total'] = tots.sum(axis=1)
othertots['Total'] = othertots.sum(axis=1)

#plot two histograms on top of each other
datlabs = [i.strftime('%b-%d') for i in dates]
for c in tots.columns:
    if c != 'Total':
        col = np.array(tdc[2])[tdc[0] == c][0]
    else:
        col = 'teal' #teal for totals
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    offset = max(tots[c])*0.03
    bins = np.linspace(0, max(max(othertots[c]), max(tots[c])+offset), 10)
    plt.hist(tots[c],color=col,alpha=0.9,\
             edgecolor=col,linewidth=4,bins=bins) #plot home in color
    plt.hist(othertots[c],color='grey',alpha=0.5,\
             edgecolor='black',linewidth=4,bins=bins-offset) #plot nearby homes in gray
    plt.xlabel('Volume of Water Used (gal)')
    plt.ylabel('Number of Days')
    plt.title('Histogram of Total Water Used in Each Day: ' + c.capitalize() +'\nCompared to Nearby Homes')
    plt.legend(['Your Home','Nearby Homes'])
    plt.savefig('Images/Histogram Compare ' +c+'.png')
    plt.show()
