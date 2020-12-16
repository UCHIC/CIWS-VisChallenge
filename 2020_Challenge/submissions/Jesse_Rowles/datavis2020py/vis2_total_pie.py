from read_data import read_data
import matplotlib.pyplot as plt
import pandas as pd

#this script creates pie charts of all types of water use as well as all without irrigation


raw, evn, mf, tdc = read_data()
#initialize data frame containing totals of each type
tots = pd.DataFrame({'col':tdc[2],'vol':0})
tots.index = tdc[0]

#calculate sums of each type and store in 'tots' dataframe
for i in tots.index:
    tots.loc[i,'vol'] = evn.loc[evn['label']==i,'vol'].sum()

# add sum row for all types and all types without irrigation
tots = tots.append(pd.DataFrame({'vol':sum(tots['vol'])},index=['sum']))
tots = tots.append(pd.DataFrame({'vol':sum(tots.loc[(tots.index != 'sum') & (tots.index != 'irrigation'), 'vol'])},index=['sum_noir']))
tots['prop_all'] = (tots['vol']/tots.loc['sum','vol'])*100 #calculate proportion of all types
tots['prop_noir'] = (tots['vol']/tots.loc['sum_noir','vol'])*100 #calculate proportion of all types without irrigation

#create pie chart for all types of water use
laball = tots.index[(tots.index != 'sum') & (tots.index != 'sum_noir')] #labels for pie chart
#create variable containing size of each pie slice
szeall = list((tots.loc[laball,'vol']*100).astype('int'))
clrall = tots.loc[(tots.index != 'sum') & (tots.index != 'sum_noir'),'col'] #colors for pie chart
#plot and save
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
p=ax.pie(szeall,labels=laball, startangle=0,autopct='%1.1f%%',colors=clrall,pctdistance = 1.13,labeldistance=1.28)
[p[0][i].set_alpha(0.5) for i in range(len(p[0]))]
plt.title('Proportion of Cumulative Water Used by Type (Volume)')
plt.savefig('Images/Pie Water Use By Type.png')
plt.show()

#create pie chart for all types of water use without irrigation
labnir = tots.index[(tots.index != 'sum') & (tots.index != 'sum_noir') & (tots.index != 'irrigation')] #pie chart labels
szenir = list((tots.loc[labnir,'vol']*100).astype('int')) #percent for each slice
clrnir = tots.loc[(tots.index != 'sum') & (tots.index != 'sum_noir') & (tots.index != 'irrigation'),'col']# pie chart colors
#plot and save
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
p=ax.pie(szenir,labels=labnir, startangle=0,autopct='%1.1f%%',colors=clrnir,labeldistance=1.1)
[p[0][i].set_alpha(0.5) for i in range(len(p[0]))]
plt.title('Proportion of Cumulative Water Used by Type Without Irrigation (Volume)')
plt.savefig('Images/Pie Water Use No Irr.png')
plt.show()
