# -*- coding: utf-8 -*-
"""
The data_raw class imports the raw data

"""


import pandas as pd

class data_raw:
    def __init__(self, file):
        self.df = self.import_raw(file)
        
    def import_raw(file):
        ''' Imports and prepares the raw data '''
        
        raw_data = pd.read_csv(file,header=3)
        
        # Get the pulse to gallon conversion
        with open(file,'r') as f:
            f.readline()
            f.readline()
            data = f.readline() # Conversion exists on the third line
            
        # Get the numeric value for conversion
        split_data = data.split()
        conversion = float(split_data[2])
        
        raw_data['Vol (gal)'] = raw_data.Pulses*conversion
        
        return raw_data