# ---------------------------------------------------------------------
# This script uses Pandas and Matplotlib to generate some simple plots
# of the raw data for the Living Learning Center buildings. It is
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

# Select just one building for a quick demo visualization
# NOTE: This assumes that the data file is in the same directory as this script.
# Change the path here to the location of the file on your hard disk.
df = pd.read_csv('LLC_BLDG_E_OCT-10-4-NOV-13_VisChallenge.csv', header=0, sep=',',
                 index_col=0, parse_dates=True, infer_datetime_format=True, low_memory=False)

# Create the figure and set its size
fig = plt.figure(figsize=(20, 10))

# -----------------
# Cold Water Supply
# -----------------
# Select a day's worth of data
beginDate = '2018-10-12 00:00:00'
endDate = '2018-10-13 00:00:00'
df_sub = df[beginDate:endDate]

# Plot a day of data
ax1 = fig.add_subplot(3, 3, 1)
ax1.plot(df_sub.index, df_sub['coldInFlowRate'], 'o-', label='Cold Supply')

# Set the title, axes labels, legend, etc.
ax1.set_ylabel('Flow Rate (gal/min)')
ax1.set_xlabel('Date')
ax1.grid(True)
ax1.xaxis.set_major_locator(mdates.HourLocator(interval=2))
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
ax1.legend(loc='upper left', shadow=True)
plt.title('One Day of Data')

# Select an hour's worth of data
beginDate = '2018-10-12 08:00:00'
endDate = '2018-10-12 09:00:00'
df_sub = df[beginDate:endDate]

# Plot an hour of data
ax2 = fig.add_subplot(3, 3, 4)
ax2.plot(df_sub.index, df_sub['coldInFlowRate'], 'o-', label='Cold Supply')

# Set the title, axes labels, legend, etc.
ax2.set_ylabel('Flow Rate (gal/min)')
ax2.set_xlabel('Date')
ax2.grid(True)
ax2.xaxis.set_major_locator(mdates.MinuteLocator(interval=10))
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
plt.title('One Hour of Data')

# Select 10 minutes of data
beginDate = '2018-10-12 08:30:00'
endDate = '2018-10-12 08:40:00'
df_sub = df[beginDate:endDate]

# Plot 10 minutes of data
ax3 = fig.add_subplot(3, 3, 7)
ax3.plot(df_sub.index, df_sub['coldInFlowRate'], 'o-', label='Cold Supply')

# Set the title, axes labels, legend, etc.
ax3.set_ylabel('Flow Rate (gal/min)')
ax3.set_xlabel('Date')
ax3.grid(True)
ax3.xaxis.set_major_locator(mdates.MinuteLocator(interval=2))
ax3.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
plt.title('10 Minutes of Data')
# -----------------

# -----------------
# Hot Water Supply
# -----------------
# Select a day's worth of data
beginDate = '2018-10-12 00:00:00'
endDate = '2018-10-13 00:00:00'
df_sub = df[beginDate:endDate]

# Plot a day of data
ax1 = fig.add_subplot(3, 3, 2)
ax1.plot(df_sub.index, df_sub['hotInFlowRate'], 'o-', label='Hot Supply', color='r')

# Set the title, axes labels, legend, etc.
ax1.set_ylabel('Flow Rate (gal/min)')
ax1.set_xlabel('Date')
ax1.grid(True)
ax1.xaxis.set_major_locator(mdates.HourLocator(interval=2))
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
ax1.legend(loc='upper left', shadow=True)
plt.title('One Day of Data')

# Select an hour's worth of data
beginDate = '2018-10-12 08:00:00'
endDate = '2018-10-12 09:00:00'
df_sub = df[beginDate:endDate]

# Plot an hour of data
ax2 = fig.add_subplot(3, 3, 5)
ax2.plot(df_sub.index, df_sub['hotInFlowRate'], 'o-', label='Hot Supply', color='r')

# Set the title, axes labels, legend, etc.
ax2.set_ylabel('Flow Rate (gal/min)')
ax2.set_xlabel('Date')
ax2.grid(True)
ax2.xaxis.set_major_locator(mdates.MinuteLocator(interval=10))
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
plt.title('One Hour of Data')

# Select 10 minutes of data
beginDate = '2018-10-12 08:30:00'
endDate = '2018-10-12 08:40:00'
df_sub = df[beginDate:endDate]

# Plot 10 minutes of data
ax3 = fig.add_subplot(3, 3, 8)
ax3.plot(df_sub.index, df_sub['hotInFlowRate'], 'o-', label='Hot Supply', color='r')

# Set the title, axes labels, legend, etc.
ax3.set_ylabel('Flow Rate (gal/min)')
ax3.set_xlabel('Date')
ax3.grid(True)
ax3.xaxis.set_major_locator(mdates.MinuteLocator(interval=2))
ax3.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
plt.title('10 Minutes of Data')
# -----------------

# -----------------
# Hot Water Return
# -----------------
# Select a day's worth of data
beginDate = '2018-10-12 00:00:00'
endDate = '2018-10-13 00:00:00'
df_sub = df[beginDate:endDate]

# Plot a day of data
ax1 = fig.add_subplot(3, 3, 3)
ax1.plot(df_sub.index, df_sub['hotOutPulseCount'], 'o-', label='Hot Return', color='m')

# Set the title, axes labels, legend, etc.
ax1.set_ylabel('Pulses')
ax1.set_xlabel('Date')
ax1.grid(True)
ax1.xaxis.set_major_locator(mdates.HourLocator(interval=2))
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
ax1.legend(loc='upper left', shadow=True)
plt.title('One Day of Data')

# Select an hour's worth of data
beginDate = '2018-10-12 08:00:00'
endDate = '2018-10-12 09:00:00'
df_sub = df[beginDate:endDate]

# Plot an hour of data
ax2 = fig.add_subplot(3, 3, 6)
ax2.plot(df_sub.index, df_sub['hotOutPulseCount'], 'o-', label='Hot Return', color='m')

# Set the title, axes labels, legend, etc.
ax2.set_ylabel('Pulses')
ax2.set_xlabel('Date')
ax2.grid(True)
ax2.xaxis.set_major_locator(mdates.MinuteLocator(interval=10))
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
plt.title('One Hour of Data')

# Select 10 minutes of data
beginDate = '2018-10-12 08:30:00'
endDate = '2018-10-12 08:40:00'
df_sub = df[beginDate:endDate]

# Plot 10 minutes of data
ax3 = fig.add_subplot(3, 3, 9)
ax3.plot(df_sub.index, df_sub['hotOutPulseCount'], 'o-', label='Hot Return', color='m')

# Set the title, axes labels, legend, etc.
ax3.set_ylabel('Pulses')
ax3.set_xlabel('Date')
ax3.grid(True)
ax3.xaxis.set_major_locator(mdates.MinuteLocator(interval=2))
ax3.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
plt.title('10 Minutes of Data')
# -----------------

# Make sure the plot displays
fig.tight_layout()
plt.show()

print('Done')

