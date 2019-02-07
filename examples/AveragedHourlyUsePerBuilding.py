
# Created by: Jaxon White
# Date: 11/21/18

# Modified by: Joseph Brewer
# Date: 1/30/19

# Description:  This is a simple script for the purpose of visualizing
# water use within the Living Learning Community at Utah State.
# Specifically, the script describes the average hourly per capita
# water use for each building for which data is available.
#
#___________________________________________


# Imports
import pandas as pd
import matplotlib.pyplot as plt


# Functions
def building_code(bldg):
    """Gets the correct information to build correct csv file name

        Arguments:
            bldg - the building code for the LLC building
        Returns:
            dateID - code for the beginning date within the csv file
            timeID - code for the beginning time within the csv file
    """
    filepath = "/Users/joseph/Desktop/VisTest/"
    if bldg == "C":
        dateID = "OCT-10-11-NOV-13"
    elif bldg == "D":
        dateID = "OCT-10-4-NOV-13"
    elif bldg == "E":
        dateID = "OCT-10-4-NOV-13"
    elif bldg == "F":
        dateID = "OCT-10-4-NOV-13"
    else:
        print('No building with this code...')

    return filepath + "LLC_BLDG_" + bldg + "_" +dateID+ "_VisChallenge.csv"

def Full_df(file):
    """Imports csv file as a data frame based on csv file name

        Arguments:
            file - file pathway for the csv file
        Returns:
            df- data frame for a specific building
    """
    fields = ['Date', 'hotInFlowRate', 'coldInFlowRate']
    df = pd.read_csv(file, header=0, sep=',', index_col=0, parse_dates=True,
                      infer_datetime_format=True, low_memory=True, usecols=fields, error_bad_lines=False)
    return df

def Resample(df_z, kind, time):
    """Resamples the data frame from 1 second resolution to either
            1 Hour or 1 Day resolution

        Arguments:
            df_z - full data frame
            kind - Water type, either hotIn or coldIn
            time - resolution, either 1H or 24H
        Returns:
            df_a - resampled data frame
    """
    df_a = df_z[kind].resample(rule=time, base=0).sum() * (1 / 60)
    return df_a

def Mean_Hour(df_y):
    """Groups by hour and finds the average value

        Arguments:
            df_y - resampled hourly data frame
        Returns:
            df_b - data frame of average value grouped by the hour of the day
    """
    df_b = df_y.groupby(df_y.index.hour).mean()
    return df_b

def Aver_Plot(df, ax, label, color):
    """Creates line plots for a data frame

            Arguments:
                df - data frame for data you want to plot
                ax - which subplot do you want it to plot to
                label - legend label
                color - color of the line

            Returns:
                x - line on the time series plot
    """
    b = df.plot(y=df, kind='line', marker='.', use_index=True, ax=ax, label=label,
                             style='-', color=color)
    return b

def configure_subplot(y1lab, y2lab,xlab, title, pos, ncol, legtitle):
    """Configures a new subplot for a figure.

    Sets default properties including the title of the subplot.

    arguments:
        y1lab - label for the y axis for the top subplot
        y2lab - label for the y axis for the bottom subplot
        xlab - label for the x axes
        title - title of the plot
        pos - position of the legend
        ncol - how many columns within the legend
        legtitle - title for the legend
    returns:
        N/A
    """
    ax.set_ylabel(y1lab)
    ax2.set_ylabel(y2lab)
    ax2.set_xlabel(xlab)
    ax.set_xlabel(xlab)
    ax.set_title(title)
    ax.yaxis.grid(True)
    ax2.yaxis.grid(True)
    ax.legend(loc=pos, shadow=True, ncol=ncol, title=legtitle)
    ax2.legend(loc=pos, shadow=True, ncol=ncol, title=legtitle)
#==========================================================================

# Headers of data frame columns
hotIn = 'hotInFlowRate'         # Renamed the hotInFlowRate column
coldIn = 'coldInFlowRate'       # Renamed the coldInFlowRate column


# Number of residents per building
cpop = 89
dpop = 87
epop = 92
fpop = 94

# Building C data frames
print('Generating dataframe for Building C, please wait...')
file_C = building_code("C")   # Build File path to read building C data
df_C = Full_df(file_C)        # Convert csv to a data frame

# Group by Hourly data frames Hot In
C_hourlyVolhotIn = Resample(df_C, hotIn, '1H')      # Resampled for 1 Hour
C_hourlyperhotin = C_hourlyVolhotIn / cpop
C_HourlyAvghotInVolper = Mean_Hour(C_hourlyperhotin)

# Groupby Hourly data frames Cold in
C_hourlyVolcoldIn = Resample(df_C, coldIn, '1H')    # Same as above
C_hourlypercoldin = C_hourlyVolcoldIn / cpop
C_HourlyAvgcoldInVolper = Mean_Hour(C_hourlypercoldin)
print('Building C dataframe complete.')


# Building D data frames
print('Generating dataframe for Building D, please wait...')
file_D = building_code("D")
df_D = Full_df(file_D)

# groupby hourly data frames hot in
D_hourlyVolhotIn = Resample(df_D, hotIn, '1H')
D_hourlyperhotin = D_hourlyVolhotIn / dpop
D_HourlyAvghotInVolper = Mean_Hour(D_hourlyperhotin)

# Groupby Hourly data frames Cold in
D_hourlyVolcoldIn = Resample(df_D, coldIn, '1H')
D_hourlypercoldin = D_hourlyVolcoldIn / dpop
D_HourlyAvgcoldInVolper = Mean_Hour(D_hourlypercoldin)


print('Building D dataframe complete.')


# Building E data frames
print('Generating dataframe for Building E, please wait...')
file_E = building_code("E")
df_E = Full_df(file_E)

#Groupby hourly data frames hot in
E_hourlyVolhotIn = Resample(df_E, hotIn, '1H')
E_hourlyperhotin = E_hourlyVolhotIn / epop
E_HourlyAvghotInVolper = Mean_Hour(E_hourlyperhotin)

# Groupby Hourly data frames Cold in
E_hourlyVolcoldIn = Resample(df_E, coldIn, '1H')
E_hourlypercoldin = E_hourlyVolcoldIn / epop
E_HourlyAvgcoldInVolper = Mean_Hour(E_hourlypercoldin)

print('Building E dataframe complete.')


# Building F data frames
print('Generating dataframe for Building F, please wait...')
file_F = building_code("F")
df_F = Full_df(file_F)

# Groupby hourly data frames hot in
F_hourlyVolhotIn = Resample(df_F, hotIn, '1H')
F_hourlyperhotin = F_hourlyVolhotIn / fpop
F_HourlyAvghotInVolper = Mean_Hour(F_hourlyperhotin)

# Groupby Hourly data frames Cold in
F_hourlyVolcoldIn = Resample(df_F, coldIn, '1H')
F_hourlypercoldin = F_hourlyVolcoldIn / fpop
F_HourlyAvgcoldInVolper = Mean_Hour(F_hourlypercoldin)

print('Building F dataframe complete.')
# ======================================================================================================



print('Generating plots, please wait...')


# Hourly average volume per resident use hot vs. cold plot for all buildings
fig4 = plt.figure(figsize=(12, 8))  # figsize=(width, height)
ax = fig4.add_subplot(2, 1, 1)                               # Upper plot
Aver_Plot(C_HourlyAvghotInVolper, ax, 'C', 'blue')
Aver_Plot(D_HourlyAvghotInVolper, ax, 'D', 'red')
Aver_Plot(E_HourlyAvghotInVolper, ax, 'E', 'green')
Aver_Plot(F_HourlyAvghotInVolper, ax, 'F', 'black')
ax.set_xlim(-0.5, 23.5)
xmarks = range(0, 24, 2)
plt.xticks(xmarks)

ax2 = fig4.add_subplot(2, 1, 2)                              # Lower plot
Aver_Plot(C_HourlyAvgcoldInVolper, ax2, 'C', 'blue')
Aver_Plot(D_HourlyAvgcoldInVolper, ax2, 'D', 'red')
Aver_Plot(E_HourlyAvgcoldInVolper, ax2, 'E', 'green')
Aver_Plot(F_HourlyAvgcoldInVolper, ax2, 'F', 'black')
ax2.set_xlim(-0.5, 23.5)
plt.xticks(xmarks)
configure_subplot('Average Hourly Hot Water\n Volume Use per Person (gal)',
                  'Average Hourly Cold Water\n Volume Use per Person (gal)',
                  'Hour of the Day',
                  'Building Comparision of per Person Average Hourly Use', 'lower right', 4, 'Building')
fig4.tight_layout()
plt.show()



print('\n\ndone')



