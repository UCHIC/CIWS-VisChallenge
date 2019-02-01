# ---------------------------------------------------------------
# Visualize the LLC data that have been summed to daily total volumes.
# The plot generates total water use for each day by building.
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

# Read the CSV file with the total daily water use data
# NOTE: Assumes the data file is in the same directory as this script. If not
# modify the path here.
df = pd.read_csv('daily_total_volume_data.csv', header=0, sep=',', index_col=0,
                 parse_dates=True, infer_datetime_format=True, low_memory=False)

# Create the figure - it will have four subplots - and set its size
fig = plt.figure(figsize=(20, 10))

# Plot the total daily water use for each building
ax1 = fig.add_subplot(2, 2, 1)
ax1.plot(df.index, df['totVol_C'], 'o-', label='Bldg. C')
ax1.plot(df.index, df['totVol_D'], 'o-', label='Bldg. D')
ax1.plot(df.index, df['totVol_E'], 'o-', label='Bldg. E')
ax1.plot(df.index, df['totVol_F'], 'o-', label='Bldg. F')

# Set the title, axes labels, legend, etc.
plt.ylim(500, 3750)
ax1.set_ylabel('Water Use (gal)')
ax1.set_xlabel('Date')
ax1.grid(True)
plt.title('Total Daily Water Use by Building')
legend = ax1.legend(loc='upper right', shadow=True)

# Plot box plots for total daily water use by building
ax2 = fig.add_subplot(2, 2, 3)
boxPlotData = [df['totVol_C'], df['totVol_D'], df['totVol_E'], df['totVol_F']]
ax2.boxplot(boxPlotData, labels=['C', 'D', 'E', 'F'])
ax2.set_ylabel('Total Daily Water Use (gal)')
ax2.set_xlabel('Building')

# Plot per capita daily water use for each building
ax3 = fig.add_subplot(2, 2, 2)
ax3.plot(df.index, df['totVol_C'] / 89, 'o-', label='Bldg. C')
ax3.plot(df.index, df['totVol_D'] / 87, 'o-', label='Bldg. D')
ax3.plot(df.index, df['totVol_E'] / 92, 'o-', label='Bldg. E')
ax3.plot(df.index, df['totVol_F'] / 94, 'o-', label='Bldg. F')

# Set the title, axes labels, legend, etc.
plt.ylim(5, 40)
ax3.set_ylabel('Per Capita Water Use (gal)')
ax3.set_xlabel('Date')
ax3.grid(True)
plt.title('Per Capita Daily Water Use by Building')
legend = ax3.legend(loc='upper right', shadow=True)

# Plot box plots for per capita daily water use by building
ax4 = fig.add_subplot(2, 2, 4)
boxPlotData = [df['totVol_C'] / 89, df['totVol_D'] / 87,
               df['totVol_E'] / 92, df['totVol_F'] / 94]
ax4.boxplot(boxPlotData, labels=['C', 'D', 'E', 'F'])
ax4.set_ylabel('Per Capita Daily Water Use (gal)')
ax4.set_xlabel('Building')

# Make sure the plot displays
fig.tight_layout()
plt.show()

print('Done!')

