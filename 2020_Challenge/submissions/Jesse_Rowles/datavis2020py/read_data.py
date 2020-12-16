import pandas as pd
import os
import numpy as np
import datetime as dt

def read_data():
    # This function is called by each individual visualization script to read the data from
    # the csv's and do some processing used by all
    os.chdir('C:/Users/jesse/Documents/Grad_School/Other/Data Visualization Challenge')

    #read in and process raw_data.csv
    mf = 0.041619 #meter tick rate given in raw_data.csv
    raw = pd.read_csv('raw_data.csv',header=3)
    raw.columns = ['time','rec','pulses'] #rename columns
    raw.index = pd.to_datetime(raw['time']) #convert to datetime so logical operators can be used
    raw = raw.drop('time',axis=1) #duplicate time column removed
    raw['vol'] = mf*raw['pulses'] #convert number of pulses to a volume of water
    raw['gpm'] = raw['vol']/(4/60) #convert gallons per 4 seconds to gallons per minute

    #read in and process classified_events.csv
    evn = pd.read_csv('classified_events.csv')
    evn.columns = ['start','end','dur','vol','flow_gpm','peak','mode','label']
    # convert to datetime format
    evn['start'] = pd.to_datetime(evn['start'])
    evn['end'] = pd.to_datetime(evn['end'])

    #assign colors to each type of event so it's consistent among visualizations
    evn['col'] = 'grey'
    typs = np.unique(evn['label'])
    cols = ['red','blue','green','magenta','goldenrod','purple','teal']
    nums = np.arange(0,len(typs))
    for i in range(len(typs)):
        #assigns colors, as well as a number to go with each color
        evn.loc[evn['label']==typs[i],'col'] = cols[i]
        evn.loc[evn['label']==typs[i],'cnum'] = nums[i]

    # label, number, and color associated with each type decoder table made here
    tdc = [typs,nums,cols[0:len(typs)]]
    return raw, evn, mf, tdc
