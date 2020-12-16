# -*- coding: utf-8 -*-
"""
This file contains functions for data visualization.

In general, these functions only visualize data that has already been computed
by other functions

Many options about the plot apperances can be set in plotting_params.py
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from icon_plot import icon_plot
import plotting_params as param 

def plot_pie(df, savefile):
    """
    Plot a pie chart showing water usage.
    
    Args:
        df: Pandas dataframe that contains classified events
        savefile: Location to save plot
        
    """
    
    df_vol_sum = df.groupby('Label').sum()['Volume (gal)']

    fig, ax = plt.subplots(figsize=(6,5))
    patches, texts = ax.pie(df_vol_sum,startangle=90)
    plt.legend(patches, df_vol_sum.index, loc="lower left",fontsize=param.text_fontsize)
    fig.suptitle('Water Usage',fontsize=param.title_fontsize)
    fig.tight_layout()
    
    filename = "{}/pie_chart.png".format(savefile).replace(" ","")
    fig.savefig(filename,format='png')


def plot_means(df):
    """
    Plots the mean value for each labeled event
    
    Args:
        df: Pandas dataframe that contains classified events
    
    """
    try:
        mean_values = df.groupby('Label').mean()
    except KeyError:
        print('Column \'Label\' does not exist.')
        print('Is this the classified data?')
        
    all_keys = mean_values.keys()
    
    for key in all_keys:
        fig, ax = plt.subplots()
        mean_values[key].plot.bar(ax=ax)
        ax.set_xlabel('Source')
        ax.set_ylabel(key)
        plt.tight_layout()
        
def generate_icon_plots(indoor_df, save_path):
    """
    Given a classified dataframe of events, this will generate a plot showing
    the average volume of water used for each event with each gallon represented
    as a gallon jug.
    Images will be saved to the specified location
    
    Args:
        indoor_df: Classified pandas dataframe of indoor events. Technically,
        outdoor events (e.g. irrigation) could be used too but will not scale 
        well at all for the visualization
        save_path: Location to save the images
    
    """
    
    for name, group in indoor_df.groupby('Label'):
        
        # Get the visualization
        mean = group.mean()['Volume (gal)']
        (fig, ax) = icon_plot(mean)
        
        # Use the label as the description but if the label is long and has
        # spaces then separate it onto separate lines to conserve space
        fig.text(.75, .06,name.replace(" ","\n"),fontsize=param.title_fontsize, transform=fig.dpi_scale_trans)
        
        # Include the amount in gallons at the top
        amnt_str = "{:.2f} Gal".format(mean)
        fig.suptitle(amnt_str,fontsize=param.title_fontsize,x=.55)
        
        # Save file
        filename = "{}/{}_icon.png".format(save_path,name).replace(" ","")
        fig.savefig(filename,format='png')
        
def plot_water_times(results_dict, save_path):
    ''' 
    Plots the actual and ideal times to water the lawn
    The results_dict should have the fields 'StartTime','EndTime','IdealStart', and 'IdealEnd' 
    with the times as hours and parts of hours 
        
    Args:
        results_dict: Dictionary that has the specified keys
        save_path: Where to save the images
    '''
    
    
    # Have to finagle the xaxis a little so it looks ok with dates
    # The date in here is just a dummy date and doesn't matter
    times = pd.date_range('2020-10-06', periods=1, freq='H')
    
    # Xaxis is in days since epoch so convert everything to that scale
    start_time = mdates.date2num(times[0]) + results_dict['StartTime']/24.0
    duration = (results_dict['EndTime'] - results_dict['StartTime'])/24.0
    start_time_ideal = mdates.date2num(times[0]) + results_dict['IdealStart'] /24.0
    duration_ideal = (results_dict['IdealEnd'] - results_dict['IdealStart'])/24.0
    
    # If the latest time that watering occurs is before the cutoff time, declare
    # water usage as excellent.
    # If watering extends beyond this time, needs improvement
    if start_time + duration <= start_time_ideal + duration_ideal:
        text_msg = 'Usage is\nExcellent'
        actual_color = param.sucsess_color
    else:
        text_msg = 'Water Earlier\nTo Save Water' 
        actual_color = param.fail_color
    
    #Location where the bars will be
    bar_height = .1
    actual_y = .66 - bar_height/2.0
    ideal_y = .33 - bar_height/2.0
    plot_height = 1.0
    
    fig, ax = plt.subplots(figsize=(8,3))

    # Plot the ideal and actual watering times on horizontal bar plot
    ax.broken_barh([(start_time, duration)],(actual_y, bar_height), facecolors=actual_color)
    ax.broken_barh([(start_time_ideal, duration_ideal)],(ideal_y,bar_height), facecolors=param.ideal_color)
    
    # Add veritcal lines to easily see where the ideal watering times are
    ax.plot(( start_time_ideal, start_time_ideal), (0,plot_height), color=param.ideal_color, alpha=.4)
    ax.plot(( start_time_ideal+duration_ideal, start_time_ideal+duration_ideal), (0,plot_height), color=param.ideal_color, alpha=.4)
    
    # Set Y axis labels and ticks
    ax.set_yticks([ideal_y+bar_height/2.0, actual_y+bar_height/2.0])
    ax.set_yticklabels(['Ideal Times to Water', 'When You Water'])
    ax.set_ylim((0,plot_height))
    
    # Set X axis with the hour of the day
    ax.set_xlim(mdates.date2num(times[0]),mdates.date2num(times[0]) + 1)
    ax.xaxis.set_major_locator(mdates.HourLocator(byhour=range(0,25,2) ))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%I %p') )
    ax.tick_params(axis='x', rotation=70)
    ax.tick_params(axis='x', labelsize=param.text_fontsize )
    ax.tick_params(axis='y', labelsize=param.text_fontsize )
    
    # Add message about their water usage (good, poor)
    ax.text( start_time_ideal + duration_ideal + .3 , plot_height/4, text_msg,fontsize=param.text_fontsize,color=actual_color)
    
    # Add title
    fig.suptitle('Irrigation Times',fontsize=param.title_fontsize)
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    # Save image
    filename = "{}/water_times.png".format(save_path).replace(" ","")
    fig.savefig(filename,format='png')
    
def plot_ideals(results, save_path):
    """
    Plot the ideal and actual usage statistics. Also, note how much water could
    be saved by reducing usage to the ideal (if applicable).
    
    Args:
        results: Dictionary with 'Name', 'Ideal', 'Actual','Savings' and 'Units' categories
        save_path: Path to save images. Image name comes from the 'Name' field
    
    """
    
    values = np.empty(2)
    label = ['Actual','Ideal']
    
    # Parse through the dictionary looking for the relevant files
    # Looks for keywords (e.g. "Ideal") but the key can be a longer string
    for key in results.keys():
        if key == 'Name':
            continue
        if 'Ideal' in key:
            values[1] = results[key]
            label[1] = 'Ideal'
        if 'Actual' in key:
            values[0] = results[key]
            label[0] = 'Actual'
        if 'Savings' in key and '$' in key:
            savings_dollar = results[key]
            savings_unit = 'Dollars'
        if 'Savings' in key and 'gal' in key:
            savings_gallon = results[key]
            savings_unit = 'gal'
        if 'Units' in key:
            units = results[key]
            
            
    # Determine if the actual usage is above or below ideal usage
    if values[1] >= values[0]:
        actual_color = param.sucsess_color
        text_msg = 'Usage is\nExcellent'
        x_pos = .75
    else:
        actual_color = param.fail_color
        #text_msg = 'Potential Savings:\n ${:.2f} per Month'.format(savings)
        text_msg = '{:.2f} gallons\nWasted per Month'.format(savings_gallon)
        x_pos = .52
        

    # Plot the ideal and actual as barplots
    fig, ax = plt.subplots(figsize=(3.5,4))
    idx = [1]
    width = .5
    ax.bar(idx[0] - width/2, values[0], width, color=actual_color)
    ax.bar(idx[0] + width/2, values[1], width, color=param.ideal_color)
    
    # Set Y axis, accounting for the text that will be added
    max_val = max(values)
    ax.set_ylabel(units, fontsize=param.text_fontsize)
    ax.set_ylim(0, max_val*1.5)
    ax.tick_params(axis='y', labelsize=param.text_fontsize )
    
    # Set the X axis
    ax.set_xticks([idx[0] - width/2, idx[0] + width/2])
    ax.set_xticklabels(label, fontsize=param.text_fontsize)
    ax.tick_params(axis='x', rotation=70)
    ax.tick_params(axis='x', labelsize=param.text_fontsize )
    
    # Add message about water usgae
    ax.text(x_pos, max_val*1.2,text_msg,fontsize=param.text_fontsize,color=actual_color)
    
    # Add title and clean up graph
    fig.suptitle(results['Name'],fontsize=param.title_fontsize)
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    # Save figure
    filename = "{}/{}.png".format(save_path,results['Name']).replace(" ","")
    fig.savefig(filename,format='png')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
