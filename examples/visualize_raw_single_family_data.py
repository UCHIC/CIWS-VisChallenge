# ---------------------------------------------------------------------
# This script uses Pandas and Matplotlib to generate some simple plots
# of the raw data for the single family residential dataset. It is
# meant to provide a quick visualization so you can get a feel for what
# the raw data look like.
# Author: Jeff Horsburgh
# Last Modified: 2-1-2019
# This script was written for Python 3.7
# ---------------------------------------------------------------------

# Import the necessary Python libraries
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Read the data file
# NOTE: This assumes the data file is in the same folder as this script
# Change the path here to where you located the data file on your hard disk.
df = pd.read_csv('Single-Family_ResidentialWaterUseDataSample.csv', header=12, sep=',',
                 index_col=0, parse_dates=True, infer_datetime_format=True, low_memory=False)

# Create the output figure and set its size
fig = plt.figure(figsize=(10, 10))

# Select a day's worth of data
beginDate = '2018-06-05 00:00:00'
endDate = '2018-06-06 00:00:00'
df_sub = df[beginDate:endDate]

# Plot a day of data
ax1 = fig.add_subplot(3, 1, 1)
ax1.plot(df_sub.index, df_sub['Pulse_Count'], 'o-', label='Pulse Count')

# Set the title, axes labels, legend, etc.
ax1.set_ylabel('Pulses')
ax1.set_xlabel('Date')
ax1.grid(True)
left, right = plt.xlim()
ax1.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=2, maxticks=10, interval_multiples=True))
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
plt.title('One Day of Data')

# Select and plot a couple of hours of data in the afternoon
beginDate = '2018-06-05 17:00:00'
endDate = '2018-06-05 20:00:00'
df_sub = df[beginDate:endDate]
ax2 = fig.add_subplot(3, 1, 2)
ax2.plot(df_sub.index, df_sub['Pulse_Count'], 'o-', label='Pulse Count')

# Set the title, axes labels, legend, etc.
ax2.set_ylabel('Pulses')
ax2.set_xlabel('Date')
ax2.grid(True)
ax2.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=2, maxticks=10, interval_multiples=True))
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
plt.title('Three Hours of Data in the Afternoon')

# Select and plot another two hours of data in the late morning
beginDate = '2018-06-05 10:00:00'
endDate = '2018-06-05 12:00:00'
df_sub = df[beginDate:endDate]
ax3 = fig.add_subplot(3, 1, 3)
ax3.plot(df_sub.index, df_sub['Pulse_Count'], 'o-', label='PulseCount')

# Set the title, axes labels, legend, etc.
ax3.set_ylabel('Pulses')
ax3.set_xlabel('Date')
ax3.grid(True)
ax3.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=2, maxticks=10, interval_multiples=True))
ax3.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
plt.title('Two Hours of Data in the Late Morning')

# Make sure the plot displays
fig.tight_layout()
plt.show()

print('Done')

