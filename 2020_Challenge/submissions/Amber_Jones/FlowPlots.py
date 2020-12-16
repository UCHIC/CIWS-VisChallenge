##########################################
# Daily Flow Plots
##########################################
# Created by: Amber Jones
# Date: 3 Dec 2020
# This script plots flow diagrams (Sankey plots) for the in/out of water flows on a daily basis.
# The script imports labeled event data, groups according to labels, divides into daily averages, and classifies as indoor/outdoor.
# Flow plots are made for overall water use and indoor. Indoor is created separately because of variation in scale.

# Import Libraries
#####################
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.sankey import Sankey
#####################

# Import Classified/Labeled Event Data
#####################
df_events = pd.read_csv('Classified_Events.csv', engine='python', header=0, parse_dates=True, infer_datetime_format=True)

# Organize data as in/out flows
#####################
# Aggregate all events by use
df_flows = df_events.groupby('Label', as_index=False)['Volume(gal)'].sum().sort_values('Volume(gal)', ascending=False)
# Daily averages
df_flows['daily'] = (df_flows['Volume(gal)']/14).astype(int)
# Class indoor/outdoor
df_in_out_flows = pd.DataFrame({'Label': ('Indoor', 'Outdoor', 'Total'),
                                'Daily Volume': (-df_flows['daily'][(df_flows.Label != 'irrigation') & (df_flows.Label != 'hose')].sum(),
                                                 -df_flows['daily'][(df_flows.Label == 'irrigation') | (df_flows.Label == 'hose')].sum(),
                                                 df_flows['daily'].sum()
                                                 )})

# Organize indoor use as in/out flows
#####################
df_indoor_flows = df_flows[(df_flows.Label != 'irrigation') & (df_flows.Label != 'hose')]
df_indoor_flows['daily'] = -df_indoor_flows['daily'].astype(int)
df_indoor_flows = df_indoor_flows.append(-df_indoor_flows.sum(numeric_only=True), ignore_index=True)
df_indoor_flows.iloc[4, 0] = 'Indoor'

# Daily Flow Plots
#####################
# plots 2 subplots: one for overall split between outdoor and indoor, another for indoor uses.

# Overall
# input data
flows = df_in_out_flows['Daily Volume']
labels = df_in_out_flows['Label']
color = '#346888'
# plotting
fig = plt.figure(figsize=(8, 10))
fig.subplots_adjust(hspace=0.05, wspace=0.05)
ax = fig.add_subplot(2, 1, 1)
ax.axis('off')
in_out_flows = Sankey(ax=ax, head_angle=120, unit=' gal', scale=1/1751, offset=0.25, margin=0.2, shoulder=0.1,)
in_out_flows.add(flows=flows, labels=labels, orientations=[-1, 0, 0], pathlengths=[0.25, 1, 1.5],
                 trunklength=0.5, facecolor=color, linewidth=1, patchlabel='Total Daily Water Use')
diagrams = in_out_flows.finish()
plt.title('Daily Water Use', fontsize=16)

# Indoor
# input data
flows = df_indoor_flows['daily']
labels = df_indoor_flows['Label']
color = '#94bed9'
# plotting
ax = fig.add_subplot(2, 1, 2)
ax.axis('off')
indoor_flows = Sankey(ax=ax, head_angle=120, unit=' gal', scale=1/130, offset=0.3, margin=0.2, shoulder=0.1,)
indoor_flows.add(flows=flows, labels=labels, orientations=[0, -1, 1, -1, 1], pathlengths=[0.5, 0.25, 0.25, 0.25, 0.9],
                 trunklength=1.5, facecolor=color, linewidth=1, patchlabel='Indoor Daily Water Use')
diagrams = indoor_flows.finish()
plt.show()

# to save
plt.savefig('Images/flowplots.png', bbox_inches='tight')

##########################################
