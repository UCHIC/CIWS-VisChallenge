# -----------------------------------------------------------
# This script was written to do some quick pre-processing of
# the full-resolution raw data. It imports the full resolution
# data from the LLC buildings and calculates a single data
# file with total volume of cold, hot, and total water use on
# a daily basis. This is just for convenience to generate a
# smaller summarized file for building subsequent
# visualizations.
# Author: Jeff Horsburgh
# Last Updated: 2-1-2019
# This script was written for Python 3.7
# -----------------------------------------------------------

# Import the necessary Python libraries
import pandas as pd

# To compare across buildings, we need to decide on a consistent
# time period for the analysis. We'll work with one month of
# data from each building.
beginDate = '2018-10-12 00:00:00'
endDate = '2018-11-11 23:59:59'

# The CSV files are large, so read them one at a time and summarize
# them into smaller datasets that will be easier to work with. Start
# with a dictionary that lists the files for the buildings.
# NOTE: This assumes that the data files are located in the same
# folder as this script. Change the file path here if your files are
# stored elsewhere on your computer.
inputFiles = {
    'C': 'LLC_BLDG_C_OCT-10-11-NOV-13_VisChallenge.csv',
    'D': 'LLC_BLDG_D_OCT-10-4-NOV-13_VisChallenge.csv',
    'E': 'LLC_BLDG_E_OCT-10-4-NOV-13_VisChallenge.csv',
    'F': 'LLC_BLDG_F_OCT-10-4-NOV-13_VisChallenge.csv'
}

# Create a new pandas data frame to hold the output
daily_summary = pd.DataFrame()

# Loop through each file in our dictionary and process the raw data
# to daily summaries.
for bldg, file in inputFiles.items():
    # Read the file from disk
    df = pd.read_csv(file, header=0, sep=',', index_col=0,
                     parse_dates=True, infer_datetime_format=True,
                     low_memory=False)

    # Subset the file to a common data window using the begin and end dates
    df_sub = df[beginDate:endDate]

    # Get the number of values in the subset data frame and print it to the
    # console. I did this to check and see if the data are really continuous.
    # Looks like there are some missing time periods in the data.
    print('There are ' + str(len(df_sub)) + ' data points in your subset.')

    # Sum the data for each day within the time period. Add the result as a new
    # series (column) in the output data frame.
    # NOTE: Because the data aren't 100% continuous and there are some missing time steps
    # these summaries will be mostly accurate but there will be some error due to
    # missing data.
    daily_summary['coldVol_' + bldg] = df_sub['coldInFlowRate'].resample('D').sum() / 60
    daily_summary['hotVol_' + bldg] = df_sub['hotInFlowRate'].resample('D').sum() / 60 - \
                                      df_sub['hotOutPulseCount'].resample('D').sum()
    daily_summary['totVol_' + bldg] = daily_summary['coldVol_' + bldg] + daily_summary['hotVol_' + bldg]

# Write the resulting Pandas data frame out to a CSV file that we can then read
# for subsequent analyses
daily_summary.to_csv('daily_total_volume_data.csv')

print('Done!')




