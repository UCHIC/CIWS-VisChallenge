"""
Andres Duque
"""


import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scipy
from sklearn.decomposition import PCA
import pandas as pd
from matplotlib.patches import Rectangle, Circle
import matplotlib as mpl
import matplotlib.colors as clr

cmap = matplotlib.cm.get_cmap('Set2')

def summarize_df(df, feature):
    ''' 
    This function summarizes the dataframe by one of the features (feature)
    by each of the uses, by day and hour   
    '''
    # Get all the possible uses
    uses = np.unique(df.Label)
    # Find the accumulated volume consumption for all the uses
    df_use = pd.DataFrame(0, index=np.arange(len(df)), columns = uses)
    
    for i in range(df.shape[0]):
        use = df.Label[i]
        df_use.loc[i, use] = df[feature].loc[i]
    df_use['Dates'] = df['EndTime']
    df_use['Days']  = df_use['Dates'].str.partition(" ")[0].str.partition("-")[2]
    df_use['Hours'] = df_use['Dates'].str.partition(" ")[2].str.partition(":")[0]
    df_use['Hours_float'] = df_use['Hours'].astype(np.float)
    
    days = np.unique(df_use['Days'])
    # Compute the accumulated use by each day
    Accumulated_days_use = pd.DataFrame(0, index=np.arange(len(days)), 
                                                  columns = uses)
    
    for i in range(Accumulated_days_use.shape[0]):
        dayuse = df_use[df_use['Days'] == days[i]][uses]  
        Accumulated_days_use.loc[i] = dayuse.sum()
    
    Accumulated_days_use.plot(subplots=True)  
    Accumulated_days_use['Total'] = Accumulated_days_use.sum(axis= 1)
    Accumulated_days_use['Days'] = days
    
    
    Accumulated = df_use[uses].cumsum()
    Accumulated['Total'] = Accumulated.sum(axis= 1)
    Accumulated['Dates'] = df_use['Dates']
    Accumulated['Days']  = df_use['Days']
    
    Accumulated_hours = pd.DataFrame(0, index=np.arange(24), 
                                                  columns = uses)
    for i in range(24):
        houruse = df_use[df_use['Hours_float'] == i][uses]  
        Accumulated_hours.loc[i] = houruse.sum()
    
    
    Accumulated_hours['Total'] = Accumulated_hours.sum(axis= 1)
    Accumulated_hours['Hours'] = np.arange(0,24)

    return df_use, Accumulated, Accumulated_days_use, Accumulated_hours


# df_use, Accumulated, Accumulated_days = summarize_df(df, 'Volume(gal)')

def day_hour_use(df_use, use, colorm):
    '''This function plots the combined days and hours 
    in a colormap plot'''
    cmap = clr.LinearSegmentedColormap.from_list('custom blue',
                                     ['#ffffff',colorm],
                                     N=256)
    days = np.unique(df_use['Days'])
    df_day_hour = pd.DataFrame(0, index=np.arange(0,24), 
                                                  columns = days)
    for i in days:
        for j in range(24):
            houruse = df_use[(df_use['Days'] == i) & (df_use['Hours_float'] == j)][use]  
            df_day_hour.loc[j, i] = houruse.sum()
    fig = plt.figure()
    plt.matshow(df_day_hour, cmap = cmap)
    plt.xticks(range(len(days)), days, fontsize = 5, rotation = 90)
    plt.yticks(range(24), range(24), fontsize = 10)
    plt.xlabel('Days')
    plt.ylabel('Hours')
    plt.title('Volume consumption by day and hour {}'.format(use))
    plt.colorbar(shrink = 0.5)

def plot_daily_use(Accumulated_days, uses):  
    '''This function plots the daily consumption
    by each of the (uses) input in the argument'''
    colors = plt.cm.Set2(range(len(uses))) 
    fig, ax = plt.subplots(len(uses),1, figsize = (20,20))
    days = Accumulated_days['Days']
    # plot color map to identify days and hours of use
    for k in range(len(uses)):
        cmap = clr.LinearSegmentedColormap.from_list('custom blue',
                                             ['#ffffff',colors[k]],
                                             N=256)

        ax[k].matshow(np.array(Accumulated_days[uses[k]]).reshape(1,-1), cmap = cmap)
        ax[k].set_xticks(range(len(days)))
        ax[k].set_xticklabels(days, fontsize=18)
        ax[k].set_yticks([])
        ax[k].xaxis.set_ticks_position('bottom')
    # Extract the major use by day
    
        for (i, j), z in np.ndenumerate(np.array(Accumulated_days[uses[k]]).reshape(1,-1)):
            ax[k].text(j, i, '{:0.1f}'.format(z), ha='center', va='center',
                       fontsize=20)
        
        ax[k].set_title("Daily use {} (Volume(gal))".format(uses[k]), fontsize=30)


    
        
def plot_hour_use(Accumulated_hours, uses):
    '''This function plots the hourly agregatted consumption
    by each of the (uses) input in the argument'''
    colors = plt.cm.Set2(range(len(uses))) 
    fig, ax = plt.subplots(len(uses),1, figsize = (30,20))
    hours = Accumulated_hours['Hours']
    # plot color map to identify days and hours of use
    for k in range(len(uses)):
        cmap = clr.LinearSegmentedColormap.from_list('custom blue',
                                             ['#ffffff',colors[k]],
                                             N=256)

        ax[k].matshow(np.array(Accumulated_hours[uses[k]]).reshape(1,-1), cmap = cmap)
        ax[k].set_xticks(range(len(hours)))
        ax[k].set_xticklabels(hours, fontsize=18)
        ax[k].set_yticks([])
        ax[k].xaxis.set_ticks_position('bottom')
    # Extract the major use by day
    
        for (i, j), z in np.ndenumerate(np.array(Accumulated_hours[uses[k]]).reshape(1,-1)):
            ax[k].text(j, i, '{:0.1f}'.format(z), ha='center', va='center',
                       fontsize=20)
        
        ax[k].set_title("Hourly use {} (Volume(gal))".format(uses[k]), fontsize=30)        
        

def plot_accumulated_use(Accumulated, uses):
    days = Accumulated['Days']
    fig, ax = plt.subplots(figsize = (10,10))
    colors = plt.cm.Set2(range(len(uses))) 
    uses_sum = uses[uses != 'Total']
    end = Accumulated[uses_sum].iloc[-1] 
    for k in range(len(uses)):
        ax.plot(Accumulated[uses[k]], label = uses[k], color = colors[k])
        if uses[k] == 'Total':
            ax.annotate('Percentage = {:.2%}'
                     .format(1),
                fontsize=9,
                fontweight='bold',
                xy=(len(days), Accumulated[uses[k]].iloc[-1]),  
                xycoords='data',
                xytext=(-150, -30),      
                textcoords='offset points',
                arrowprops=dict(arrowstyle="->"),
                bbox=dict(boxstyle="round4, pad=0.1", fc="red", ec="red",
                          alpha =0.2, lw=1))   
        else:
                ax.annotate('Percentage = {:.2%}'
                 .format(Accumulated[uses[k]].iloc[-1]/end.sum()),
            fontsize=9,
            fontweight='bold',
            xy=(len(days), Accumulated[uses[k]].iloc[-1]),  
            xycoords='data',
            xytext=(100, 0),      
            textcoords='offset points',
            arrowprops=dict(arrowstyle="->"),
            bbox=dict(boxstyle="round4, pad=0.1", fc="red",alpha =0.2, ec="red", lw=1))   
           
    ax.legend()
    ax.set_xticks(np.arange(0,len(days),100))
    ax.set_xticklabels(days.iloc[np.arange(0,len(days),100)])
    ax.set_xlabel('Days', fontsize = 15)
    ax.set_ylabel('Accumulated consumption Volume(gal)', fontsize = 15)
    ax.set_title('Consumption progression over time', fontsize = 20)
    
def plot_feature_use(df, use, q, colorm, feature):
    data = np.array(df[feature][df['Label'] == use])
    dates = df['StartTime'][df['Label'] == use]
    Qv = np.quantile(data, q)
    indices = np.where(data > Qv)[0]
    fig, ax = plt.subplots(figsize = (20,10))
    ax.plot(data, color = colorm)
    for k in indices: 
        ax.annotate('Date = {}'
             .format(dates.iloc[k]),
        fontsize=9,
        fontweight='bold',
        xy=(k, data[k]),  
        xycoords='data',
        xytext=(0, 10),      
        textcoords='offset points',
        arrowprops=dict(arrowstyle="->"),
        bbox=dict(boxstyle="round4, pad=0.1", fc="red", ec="red",
                  alpha =0.2, lw=1))   
    
    ax.set_ylim(0,)
    ax.set_ylabel('Volume(gal)', fontsize = 15)
    ax.set_xlabel('Number of each time it is used', fontsize = 15)
    # ax.set_xticks(np.arange(0,len(data),20))
    # ax.set_xticklabels(dates.iloc[np.arange(0,len(data),20)])
    ax.set_title("Total uses of {}, {} with the observaitons above the {} percentile annotated by date".format(use, feature, q*100),
                 fontsize = 20)