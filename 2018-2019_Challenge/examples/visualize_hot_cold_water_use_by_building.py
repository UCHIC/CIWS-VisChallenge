# ----------------------------------------------------------------
# Visualize the percentage of hot and cold water use for each LLC
# building. This script uses the daily total volume data as input.
# Author: Jeff Horsburgh
# Last Modified: 2-1-2019
# NOTE: This script assumes that the "calculate_daily_total_volumes.py"
# script has already been run to generate the "daily_total_volume_data.CSV"
# file.
# This script was written for Python 3.7
# ----------------------------------------------------------------

# Import the necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the CSV file with the daily total volume data
# NOTE: Assumes that the data file is in the same folder as this script.
# If not, set the path to data file here.
df = pd.read_csv('daily_total_volume_data.csv', header=0, sep=',', index_col=0,
                 parse_dates=True, infer_datetime_format=True, low_memory=False)

# Aggregate the data frame by summing the columns
sums = df.aggregate('sum')

buildings = ['C', 'D', 'E', 'F']
x = np.arange(4)

# Create the figure and set its size
fig = plt.figure(figsize=(10, 10))

# Create the pie charts.
# Slices are ordered and plotted counter-clockwise:
for i in x:
    ax = fig.add_subplot(2, 2, i + 1)
    sizes = [sums['coldVol_' + buildings[i]] / sums['totVol_' + buildings[i]],
             sums['hotVol_' + buildings[i]] / sums['totVol_' + buildings[i]]]
    ax.pie(sizes, labels=['Cold', 'Hot'], autopct='%1.1f%%',
           startangle=90, colors=['c', 'r'])
    ax.set_title('Building ' + buildings[i])
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Set the main figure title
fig.suptitle('Cold Versus Hot Water Use by Building', fontsize=16)

# Make sure the plot displays
plt.show()

print('Done!')

