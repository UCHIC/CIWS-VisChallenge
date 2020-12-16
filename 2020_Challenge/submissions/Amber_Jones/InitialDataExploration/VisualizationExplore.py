
# Import Libraries
#####################
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.sankey import Sankey
import squarify
import seaborn as sns
from pywaffle import Waffle
#####################

# Import Classified/Labeled Event Data
#####################
df_events = pd.read_csv('../Classified_Events.csv', engine='python', header=0, parse_dates=True, infer_datetime_format=True)

#####################
# Treemaps
#####################
# Group data by label
df = df_events.groupby('Label', as_index=False)['Volume(gal)'].sum()
df['Volume(gal)'] = df['Volume(gal)'].astype(int)
# Reorder rows
df = df.reindex([3, 2, 5, 4, 0, 1])
# Concatonate label + volume for plotting
df['label+vol'] = df['Label'] + '\n(' + df['Volume(gal)'].astype(str) + ' gallons)'
# Add columns for daily averages
df['daily'] = (df['Volume(gal)']/14).astype(int)
df['daily_label+vol'] = df['Label'] + '\n(' + df['daily'].astype(str) + ' gallons)'
# Subset for indoor water use
df_indoor = df[(df.Label != 'irrigation') & (df.Label != 'hose')]

# Overall Treemap
#####################
labels = df['label+vol']
sizes = df['Volume(gal)']
colors = [plt.cm.Spectral(i/float(len(labels))) for i in range(len(labels))]

plt.figure(figsize=(12, 8), dpi=80)
squarify.plot(sizes=sizes, label=labels, color=colors, alpha=.8)
plt.title('Overall Water Use')
plt.axis('off')
plt.show()

# Daily Average Treemap
#####################
labels = df['daily_label+vol']
sizes = df['daily']
colors = [plt.cm.Spectral(i/float(len(labels))) for i in range(len(labels))]

plt.figure(figsize=(12, 8), dpi=80)
squarify.plot(sizes=sizes, label=labels, color=colors, alpha=.8)
plt.title('Average Daily Water Use')
plt.axis('off')
plt.show()

# Indoor Treemap
#####################
labels = df_indoor['label+vol']
sizes = df_indoor['Volume(gal)']
colors = [plt.cm.Spectral(i/float(len(labels))) for i in range(len(labels))]

plt.figure(figsize=(12, 8), dpi=80)
squarify.plot(sizes=sizes, label=labels, color=colors, alpha=.8)
plt.title('Indoor Water Use')
plt.axis('off')
plt.show()

# Daily Average Indoor Treemap
#####################
labels = df_indoor['daily_label+vol']
sizes = df_indoor['daily']
colors = [plt.cm.Spectral(i/float(len(labels))) for i in range(len(labels))]

plt.figure(figsize=(12, 8), dpi=80)
squarify.plot(sizes=sizes, label=labels, color=colors, alpha=.8)
plt.title('Average Daily Indoor Water Use')
plt.axis('off')
plt.show()


#####################
# Sankey Plots
#####################
# Organize data as in/out flows
df_flows = df_events.groupby('Label', as_index=False)['Volume(gal)'].sum().sort_values('Volume(gal)', ascending=False)
df_flows['Volume(gal)'] = -df_flows['Volume(gal)'].astype(int)
df_flows = df_flows.append(-df_flows.sum(numeric_only=True), ignore_index=True)
df_flows.iloc[6, 0] = 'Total Volume'
# Daily averages
df_flows['daily'] = (df_flows['Volume(gal)']/14).astype(int)

# Overall Plots
#####################
flows = df_flows['Volume(gal)']
labels = df_flows['Label']
Sankey(head_angle=150, unit='gal', scale=1/24524, offset=0.2,
       flows=flows, labels=labels,
       orientations=[0, -1, 1, -1, -1, -1, 0],
       pathlengths=[0.6, 0.25, 0.25, 0.25, 0.25, 0.25, 0.6]).finish()
plt.title('Flows')
plt.show()

# Daily Sankey Plots
#####################
flows = df_flows['daily']
labels = df_flows['Label']
Sankey(head_angle=150, unit='gal', scale=1/1751, offset=0.2,
       flows=flows, labels=labels,
       orientations=[0, -1, 1, -1, -1, -1, 0],
       pathlengths=[0.6, 0.25, 0.25, 0.25, 0.25, 0.25, 0.6]).finish()
plt.title('Daily flows')
plt.show()

# Indoor Sankey Plots
#####################
df_flows = df_events.groupby('Label', as_index=False)['Volume(gal)'].sum().sort_values('Volume(gal)', ascending=False)
df_indoor_flows = df_flows[(df_flows.Label != 'irrigation') & (df_flows.Label != 'hose')]
df_indoor_flows['Volume(gal)'] = -df_indoor_flows['Volume(gal)'].astype(int)
df_indoor_flows = df_indoor_flows.append(-df_indoor_flows.sum(numeric_only=True), ignore_index=True)
df_indoor_flows.iloc[4, 0] = 'Total \n Volume'
# Daily averages
df_indoor_flows['daily'] = (df_indoor_flows['Volume(gal)']/14).astype(int)

# Indoor Plot
#####################
flows = df_indoor_flows['Volume(gal)']
labels = df_indoor_flows['Label']
Sankey(head_angle=150, unit='gal', scale=1/1839, offset=0.2,
       flows=flows, labels=labels,
       orientations=[0, -1, 1, -1, 0],
       pathlengths=[0.6, 0.25, 0.25, 0.25, 0.6]).finish()
plt.title('Flow diagram')
plt.show()

# Daily Indoor Plot
#####################
flows = df_indoor_flows['daily']
labels = df_indoor_flows['Label']
Sankey(head_angle=150, unit='gal', scale=1/131, offset=0.2,
       flows=flows, labels=labels,
       orientations=[0, -1, 1, -1, 0],
       pathlengths=[0.6, 0.25, 0.25, 0.25, 0.6],
       #color='b'
       ).finish()
plt.title('Daily flows')
plt.show()

fig = plt.figure(figsize=(16, 6), dpi=80)
ax = fig.add_subplot(1, 1, 1, xticks=[], yticks=[],
                     title='Daily flows')
sankey = Sankey(ax=ax, scale=1/131, head_angle=120, unit='gal', shoulder=0.075, margin=0.2, offset=0.15)
sankey.add(flows=flows, labels=labels, orientations=[0, -1, 1, -1, 0],
           pathlengths=[0.25, 0.25, 0.25, 0.25, 1],
           fill = False)  # Arguments to matplotlib.patches.PathPatch
diagrams = sankey.finish()
diagrams[0].texts[-1].set_color('r')
diagrams[0].text.set_fontweight('bold')






#####################
# Marginal Histogram
#####################
# Create Fig and gridspec
fig = plt.figure(figsize=(16, 10), dpi=80)
grid = plt.GridSpec(4, 4, hspace=0.5, wspace=0.2)

# Define the axes
ax_main = fig.add_subplot(grid[:-1, :-1])
ax_right = fig.add_subplot(grid[:-1, -1], xticklabels=[], yticklabels=[])
ax_bottom = fig.add_subplot(grid[-1, 0:-1], xticklabels=[], yticklabels=[])

# Scatterplot on main ax
groups = df_events.groupby('Label')
for name, group in groups:
    ax_main.plot(group['Volume(gal)'], group['Duration(min)'], marker='o', linestyle='', label=name)
ax_main.legend()
#ax_main.scatter('Duration(min)', 'Volume(gal)', c=df_events.Label.astype('category').cat.codes, alpha=.9, data=df_events, cmap="tab10", linewidths=.5)
#ax_main.sns.scatterplot(x="Duration(min)", y="Volume(gal)", data=df_events, hue="Label")

# histogram on the bottom
ax_bottom.hist(df_events['Duration(min)'], 40, histtype='stepfilled', orientation='vertical', color='gray')
ax_bottom.invert_yaxis()

# histogram on the right
ax_right.hist(df_events['Volume(gal)'], 40, histtype='stepfilled', orientation='horizontal', color='gray')

# Decorations
ax_main.set(title='Duration vs Volume', xlabel='Volume(gal)', ylabel='Duration(min)')
ax_main.title.set_fontsize(20)
for item in ([ax_main.xaxis.label, ax_main.yaxis.label] + ax_main.get_xticklabels() + ax_main.get_yticklabels()):
    item.set_fontsize(14)

xlabels = ax_main.get_xticks().tolist()
ax_main.set_xticklabels(xlabels)
plt.legend()
plt.show()

# Refined Marginal Histogram
#####################
df_sort = df_events.sort_values('Volume(gal)', ascending=False)
# two distinct types of irrigation events
df_sub = df_events[df_events['Volume(gal)'] < 2000]

# Create Fig and gridspec
fig = plt.figure(figsize=(16, 10), dpi=80)
grid = plt.GridSpec(4, 4, hspace=0.5, wspace=0.2)

# Define the axes
ax_main = fig.add_subplot(grid[:-1, :-1])
ax_right = fig.add_subplot(grid[:-1, -1], xticklabels=[], yticklabels=[])
ax_bottom = fig.add_subplot(grid[-1, 0:-1], xticklabels=[], yticklabels=[])

# Scatterplot on main ax
groups = df_sub.groupby('Label')
for name, group in groups:
    ax_main.plot(group['Volume(gal)'], group['Duration(min)'], marker='o', linestyle='', label=name)
ax_main.legend()
#ax_main.scatter('Duration(min)', 'Volume(gal)', c=df_events.Label.astype('category').cat.codes, alpha=.9, data=df_events, cmap="tab10", linewidths=.5)
#ax_main.sns.scatterplot(x="Duration(min)", y="Volume(gal)", data=df_events, hue="Label")

# histogram on the bottom
ax_bottom.hist(df_sub['Duration(min)'], 40, histtype='stepfilled', orientation='vertical', color='gray')
ax_bottom.invert_yaxis()

# histogram on the right
ax_right.hist(df_sub['Volume(gal)'], 40, histtype='stepfilled', orientation='horizontal', color='gray')

# Decorations
ax_main.set(title='Duration vs Volume', xlabel='Volume(gal)', ylabel='Duration(min)')
ax_main.title.set_fontsize(20)
for item in ([ax_main.xaxis.label, ax_main.yaxis.label] + ax_main.get_xticklabels() + ax_main.get_yticklabels()):
    item.set_fontsize(14)

xlabels = ax_main.get_xticks().tolist()
ax_main.set_xticklabels(xlabels)
plt.show()


#####################
# Hourly Aggregation
#####################

df_hourly = df_events[['Volume(gal)', 'Duration(min)', 'Label']].copy()
df_hourly['Hour'] = pd.to_datetime(df_events['StartTime']).dt.hour
df_grouped = df_hourly.groupby(['Label', 'Hour'], as_index=False)['Volume(gal)'].sum()
df_grouped = df_hourly.groupby(['Label', 'Hour'], as_index=False).aggregate({'Volume(gal)': np.sum, 'Duration(min)': np.average})
df_grouped = df_hourly.groupby(['Label', 'Hour'], as_index=False).agg({'Volume(gal)': np.sum, 'Duration(min)': ['mean', 'min', 'max']})
df_grouped.columns = ['Label', 'Hour', 'Volume_tot', 'Duration_mean', 'Duration_min', 'Duration_max']

# Volume
df_pvt = pd.pivot_table(df_grouped, values='Volume_tot', index=['Hour'], columns=['Label'], fill_value=0)
df_pvt = df_pvt[['irrigation', 'hose', 'shower', 'toilet', 'clothwasher', 'faucet']]

Labels = list(df_pvt.columns)
colors = [plt.cm.Spectral(i/float(len(Labels)-1)) for i in range(len(Labels))]
N = len(df_pvt)
bottom = np.zeros(N)
width = 0.5
for elem, color in zip(Labels, colors):
    plt.bar(df_pvt.index, df_pvt[elem], bottom=bottom, color=color, width=width)
    bottom += df_pvt[elem]

plt.ylabel('Volume (gal)')
plt.xlabel('Hour of Day')
plt.title('Total Hourly Water Use')
plt.xticks(df_pvt.index)
plt.legend(Labels)
plt.show()

# Without Irrigation
df_drop = df_pvt.drop(columns=['irrigation', 'hose'], index=[0, 3, 4, 5, 6])
Labels = list(df_drop.columns)
colors = [plt.cm.Spectral(i/float(len(Labels)-1)) for i in range(len(Labels))]
N = len(df_drop)
bottom = np.zeros(N)
width = 0.5
for elem, color in zip(Labels, colors):
    plt.bar(df_drop.index, df_drop[elem], bottom=bottom, color=color, width=width)
    bottom += df_drop[elem]

plt.ylabel('Volume (gal)')
plt.xlabel('Hour of Day')
plt.title('Total Hourly Water Use')
plt.xticks(df_drop.index)
plt.legend(Labels)
plt.show()

#Side by Side
bottom = np.zeros(N)
wide = 0
for elem, color in zip(Labels, colors):
    plt.bar(df_drop.index + wide, df_drop[elem], bottom=bottom, color=color, width=0.15)
    wide += 0.15

plt.ylabel('Volume (gal)')
plt.xlabel('Hour of Day')
plt.title('Total Hourly Water Use')
plt.xticks(df_drop.index)
plt.legend(Labels)
plt.show()

#Only Shower
plt.bar(df_drop.index, df_drop['shower'], width=1, edgecolor='white', color='#2d7f5e')
plt.ylabel('Volume (gal)')
plt.xlabel('Hour of Day')
plt.title('Hourly Shower Volume')
plt.xticks(df_drop.index)
plt.show()

#Shower Duration
df_pvt_duration = pd.pivot_table(df_grouped, values='Duration_mean', index=['Hour'], columns=['Label'], fill_value=0)
df_pvt_duration = df_pvt_duration[['irrigation', 'hose', 'shower', 'toilet', 'clothwasher', 'faucet']]
df_drop_duration = df_pvt_duration.drop(columns=['irrigation', 'hose'], index=[0, 3, 4, 5, 6])

df_pvt_duration = pd.pivot_table(df_grouped, values='Duration_max', index=['Hour'], columns=['Label'], fill_value=0)
df_pvt_duration = df_pvt_duration[['irrigation', 'hose', 'shower', 'toilet', 'clothwasher', 'faucet']]
df_drop_duration = df_pvt_duration.drop(columns=['irrigation', 'hose'], index=[0, 3, 4, 5, 6])

plt.bar(df_drop_duration.index, df_drop_duration['shower'], width=1, edgecolor='white', color='#2d7f5e')
plt.ylabel('Duration (min)')
plt.xlabel('Hour of Day')
plt.title('Hourly Shower Duration')
plt.xticks(df_drop.index)
plt.show()


# use box plots? lines of ranges? violin plots?

#####################
# Grouped Violin Plot
#####################
df_indoor_events = df_events[(df_events.Label != 'irrigation') & (df_events.Label != 'hose')]

sns.violinplot(x="Label", y="Volume(gal)", data=df_indoor_events, palette="Pastel1")
sns.violinplot(x="Label", y="Duration(min)", data=df_indoor_events, palette="Pastel1")
sns.plt.show()

# Shower Hourly Violin Plot
df_hourly_shower = df_hourly[(df_events.Label == 'shower')]
sns.violinplot(x="Hour", y="Duration(min)", data=df_hourly_shower, palette="Pastel1", cut =0)
sns.boxplot(x="Hour", y="Duration(min)", data=df_hourly_shower, palette="Pastel1")


#####################

# Shower
df_events['Flowrate(gpm)'][df_events['Label'] == 'shower'].mean()
# 1.758 gpm

df_events['Volume(gal)'][df_events['Label'] == 'shower'].sum()/14
# 589 gal
# 42 gal

df_events['Duration(min)'][df_events['Label'] == 'shower'].sum()
# 313 minutes
# 22.4 minutes

(df_events['Duration(min)'][df_events['Label'] == 'shower']*1.5).sum()/14
# 470.7 gal
# 33.6 gal

df_events['Duration(min)'][df_events['Label'] == 'shower'].mean()
#9.5

# new dataframe
df_shower = df_events[df_events['Label'] =='shower']
df_shower['Duration(min)'].sum()
# 313.8 min
df_shower['Volume(gal)'].sum()
# 589.3 gal

# 589.3/313.8 = 1.88 gpm

# 313.8*1.5 = 470.7 gal/14 = 33.6 gal/day
# saving 8.5 gal/day

df_shower['ShortShowerDuration'] = np.where(df_shower['Duration(min)'] >= 10, 10, df_shower['Duration(min)'])
df_shower['ShortShowerDuration'].sum()
# 261.7 min * 1.88 gpm = 492 gallons/14 = 35.1 gal/day
# saving 7 gal/day

#261.7 min * 1.5 gpm = 392 gallons/14 = 28 gal/day
# saving 14 gal/day

plt.hist(df_shower['Duration(min)'])



# $23.25 for 10,000 gallons of water.
# 75 cents per 1,000 gallons if residents use anywhere from 10,001 to 50,000 gallons.
# 1.50 per 1,000 gallons for all usage over 50,000 gallons

df['monthly'] = df['daily'] * 30

# 27154 gallons/acre 0.28*2/3 acres = 5069 gal is 1 inch of water
# 27154 * 0.28 * 2/3 * 30/7 = 21723 gallons/month

47340 * 7/30 * 3/2 * 1/0.28 *1/27154
# currently using 2.18 inches/week

# 27154 gallons/acre 0.28*2/3*0.5 acres = 2534.5 gal is 1 inch of water
# 27154 * 0.28 * 2/3 * 30/7 * 0.5 = 10862 gallons/month



Labels = ['Indoor', 'Sprinklers']
Scenario = ['Current Irrigation Schedule', 'Reduce Lawn by Half', 'Reduce Irrigation by Half', 'Reduce Lawn and Irrigation']
Indoor = [5160, 5160, 5160, 5160]
Sprinklers = [47430, 23715, 21723, 10862]

pricing = pd.DataFrame({'Scenario':Scenario, 'Indoor':Indoor, 'Sprinklers':Sprinklers})
pricing['Total'] = pricing['Indoor'] + pricing['Sprinklers']
pricing['FirstTier'] = np.where(pricing['Total'] >= 50000, 40000, pricing['Total']-10000)
pricing['SecondTier'] = np.where(pricing['Total'] >= 50000, pricing['Total']-50000, 0)
pricing['FirstTierCost'] = pricing['FirstTier']*0.75/1000
pricing['SecondTierCost'] = pricing['SecondTier']*1.5/1000
pricing['TotalCost'] = pricing['FirstTierCost'] + pricing['SecondTierCost'] + 23.25

colors = [plt.cm.Spectral(i/float(len(Labels)-1)) for i in range(len(Labels))]
width = 0.5
p1 = plt.bar(Scenario, Indoor, bottom=0, color=colors[0], width=width)
p2 = plt.bar(Scenario, Sprinklers, bottom=Indoor, color=colors[1], width=width)
p3 = plt.axhline(y=10000, linewidth=1.5, linestyle='--', color='k')
plt.text(x=4.5, y=10500, s='Flat Rate Tier', fontweight='bold', color='k')
p4 = plt.axhline(y=50000, linewidth=1.5, linestyle='--', color='k')
plt.text(x=4.5, y=50500, s='Irrigation Tier', fontweight='bold', color='gray')
for i, rows in pricing.iterrows():
    plt.annotate('{:,}'.format(rows['Total']) + ' gal', xy=(i, rows['Total']+1000), rotation=0, color='k', ha='center', va='center', alpha =0.7, fontsize=9)
    plt.annotate('${:,.2f}'.format(rows['TotalCost']), xy=(i, 13000), rotation=0, color='k', ha='center', va='center', fontsize=9, bbox=dict(boxstyle='square', fc='white'))
plt.annotate('Flat Rate\n$23.25', xy=(3.35, 5000), xytext=(3.425, 5000), annotation_clip=False, rotation=0,
            fontsize=9, ha='left', va='center',
            bbox=dict(boxstyle='square', fc='white'),
            arrowprops=dict(arrowstyle='-[, widthB=2.4, lengthB=0.9', lw=1))
plt.annotate(' $0.75/\n1000gal', xy=(3.35, 30000), xytext=(3.425, 30000), annotation_clip=False, rotation=0,
            fontsize=9, ha='left', va='center',
            bbox=dict(boxstyle='square', fc='white'),
            arrowprops=dict(arrowstyle='-[, widthB=10.35, lengthB=0.9', lw=1))
plt.annotate(' $1.50/\n1000gal', xy=(3.35, 52600), xytext=(3.425, 52600), annotation_clip=False, rotation=0,
            fontsize=9, ha='left', va='center',
            bbox=dict(boxstyle='square', fc='white'),
            arrowprops=dict(arrowstyle='-[, widthB=1.2, lengthB=0.9', lw=1))
plt.ylabel('Volume (gal)')
plt.title('Irrigation Season Monthly Water Use and Cost')
plt.legend((p1, p2), Labels, loc='upper center', ncol=2)
plt.show()


for i, rows in df.iterrows():
    plt.annotate(rows["a"], xy=(i, rows["a"]), rotation=0, color="C0")
    plt.annotate(rows["b"], xy=(i+0.1, rows["b"]), color="lightblue", rotation=+20, ha="left")
    plt.annotate(rows["t"], xy=(i-0.1, rows["t"]), color="purple", rotation=-20, ha="right")



import matplotlib.pyplot as plt
from matplotlib import gridspec

savings_labels = ['Shorter Showers', 'Ultra Low Flow', 'Shorter and Low Flow']
savings = [round(current_daily_vol - short_dur_vol),
           round(current_daily_vol - low_flow_vol),
           round(current_daily_vol - both_vol)]
text = ['Shorter Showers save\n' + str(savings[0]) +' gallons/day',
          'Low Flows save\n' + str(savings[1]) +' gallons/day',
          'Both save\n' + str(savings[2]) +' gallons/day']
colors = ['#25556e', '#457891', '#659cb5']
ncol = max(savings)
nrow = len(savings)

fig, ax = plt.subplots(nrows=rows, ncols=ncol, figsize=(ncol, nrow))
fig.subplots_adjust(hspace=0.00, wspace=0.00)
gs = gridspec.GridSpec(nrow, ncol,
         wspace=0.0, hspace=0.0,
         top=1.-0.5/(nrow+1), bottom=0.5/(nrow+1),
         left=0.5/(ncol+1), right=1-0.5/(ncol+1))
for i, axi in enumerate(ax.flat):
    axi.axis('off')
    # i runs from 0 to (nrows * ncols-1)
    # axi is equivalent with ax[rowid][colid]
    if (i <savings[0]) or (i>= ncol and i <(ncol+savings[1])) or (i>= ncol*2 and i <(ncol*2+savings[2])):
        img = plt.imread('Images/milkjug.png')
        axi.imshow(img, alpha=0.95, extent=[0, 550, 0, 550])
ax[0][0].annotate(text[0], xy=(0, 275), xytext=(0, 275), annotation_clip=False, rotation=0,
            fontsize=11, ha='right', va='center', fontname='Arial Narrow', color=colors[0], fontweight='bold',
            horizontalalignment='right', verticalalignment='top',
            )
ax[1][0].annotate(text[1], xy=(0, 275), xytext=(0, 275), annotation_clip=False, rotation=0,
            fontsize=11, ha='right', va='center', fontname='Arial Narrow', color=colors[1], fontweight='bold',
            horizontalalignment='right', verticalalignment='top',
            )
ax[2][0].annotate(text[2], xy=(0, 275), xytext=(0, 275), annotation_clip=False, rotation=0,
            fontsize=11, ha='right', va='center', fontname='Arial Narrow', color=colors[2], fontweight='bold',
            horizontalalignment='right', verticalalignment='top',
            )
plt.show()

