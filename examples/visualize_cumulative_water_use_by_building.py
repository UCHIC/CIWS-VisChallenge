# ---------------------------------------------------------------
# Visualize the cumulative water use for each LLC building
# This script uses the daily total volume data as input
# Author: Jeff Horsburgh
# Last Modified: 2-1-2019
# NOTE: This script assumes that the "calculate_daily_total_volumes.py"
# script has already been run to generate the "daily_total_volume_data.CSV"
# file.
# This script was written for Python 3.7
# ---------------------------------------------------------------

# Import the necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the CSV file with the daily total volume data
# NOTE: Assumes the data file is located in the same directory as this
# script. If not, change the path here.
df = pd.read_csv('daily_total_volume_data.csv', header=0, sep=',', index_col=0,
                 parse_dates=True, infer_datetime_format=True, low_memory=False)

# Calculate some new Pandas series that have the cumulative daily volumes
cumVolC = df['totVol_C'].cumsum()
cumVolD = df['totVol_D'].cumsum()
cumVolE = df['totVol_E'].cumsum()
cumVolF = df['totVol_F'].cumsum()

# Get the overall and per capita total volume used within each
# building for the whole period
totalVolumes = [cumVolC[-1], cumVolD[-1],
                cumVolE[-1], cumVolF[-1]]
perCapitaVolumes = [cumVolC[-1] / 89, cumVolD[-1] / 87,
                    cumVolE[-1] / 92, cumVolF[-1] / 94]

# Create the list of colors to use in the plots
colors = ['r', 'b', 'g', 'c']

# Create the plot and set its size
fig = plt.figure(figsize=(20, 10))

# Plot the total cumulative volume data series
ax1 = fig.add_subplot(2, 2, 1)
ax1.plot(cumVolC.index, cumVolC, 'o-', label='Bldg. C', color=colors[0])
ax1.plot(cumVolD.index, cumVolD, 'o-', label='Bldg. D', color=colors[1])
ax1.plot(cumVolE.index, cumVolE, 'o-', label='Bldg. E', color=colors[2])
ax1.plot(cumVolF.index, cumVolF, 'o-', label='Bldg. F', color=colors[3])

# Set the title, axes labels, legend, etc.
ax1.set_ylabel('Cumulative Water Use (gal)')
ax1.set_xlabel('Date')
ax1.grid(True)
plt.title('Total Cumulative Water Use by Building')
legend = ax1.legend(loc='upper left', shadow=True)

# Plot the bar plot with total water use by building
ax2 = fig.add_subplot(2, 2, 3)
x = np.arange(4)
barlist = ax2.bar(x, totalVolumes)
# Set the colors of the bars, xtick labels and axes labels
for i in x:
    barlist[i - 1].set_color(colors[i - 1])
plt.xticks(x, ('C', 'D', 'E', 'F'))
ax2.set_ylabel('Overall Total Water Use (gal)')
ax2.set_xlabel('Building')

# Plot the total per capita cumulative volume data series
ax1 = fig.add_subplot(2, 2, 2)
ax1.plot(cumVolC.index, cumVolC / 89, 'o-', label='Bldg. C', color=colors[0])
ax1.plot(cumVolD.index, cumVolD / 87, 'o-', label='Bldg. D', color=colors[1])
ax1.plot(cumVolE.index, cumVolE / 92, 'o-', label='Bldg. E', color=colors[2])
ax1.plot(cumVolF.index, cumVolF / 94, 'o-', label='Bldg. F', color=colors[3])

# Set the title, axes labels, legend, etc.
ax1.set_ylabel('Cumulative Water Use (gal)')
ax1.set_xlabel('Date')
ax1.grid(True)
plt.title('Per Capita Cumulative Water Use by Building')
legend = ax1.legend(loc='upper left', shadow=True)

# Plot the bar plot with per capita water use by building
ax2 = fig.add_subplot(2, 2, 4)
x = np.arange(4)
barlist = ax2.bar(x, perCapitaVolumes)
# Set the colors of the bars, xtick labels and axes labels
for i in x:
    barlist[i - 1].set_color(colors[i - 1])
plt.xticks(x, ('C', 'D', 'E', 'F'))
ax2.set_ylabel('Per Capita Total Water Use (gal)')
ax2.set_xlabel('Building')

# Make sure the plot displays
fig.tight_layout()
plt.show()

print('Done!')
