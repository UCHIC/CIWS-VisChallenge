# -*- coding: utf-8 -*-
"""
The data_classified class imports the classified data and processes it to get 
the desired statistics.

The outputs of the 'get' functions are generally able to be used with the 
plot_ideals function in the data_processing.py file.

"""

import pandas as pd
import matplotlib.pyplot as plt
import water_params as param

class data_classified:
    def __init__(self, file):
        self.df = self.import_classified(file)
        self.indoor_df = self.get_indoor()
        self.outdoor_df = self.get_outdoor()
        
        self.data_start = self.df['DateTimeStart'].min()
        self.data_end = self.df['DateTimeStart'].max()
        days = (self.data_end - self.data_start).days
        seconds = (self.data_end - self.data_start).seconds
        self.data_duration = days + seconds/param.sec_day
        
        # Ideal values
        self.ideal_toilet_gpf = param.ideal_toilet_gpf
        self.moderate_toilet_gpf = param.moderate_toilet_gpf
        self.ideal_faucet_gpm = param.ideal_faucet_gpm
        self.ideal_shower_gpm = param.ideal_shower_gpm
        self.ideal_shower_duration = param.ideal_shower_duration
        
        self.cost_gal = param.cost_gal
    
    def import_classified(self, file):
        """
        Reads in the classified data from a csv file and does some minor 
        formatting to get the data in a position that it can be used
        
        Args:
            file: Filepath to the classified data csv
        
        Returns:
            pandas dataframe of all the classified events
        
        """
        
        class_data = pd.read_csv(file)
        
        # Convert the dates to a datetime representation
        class_data['DateTimeStart'] = pd.to_datetime(class_data['StartTime'])
        class_data['DateTimeEnd'] = pd.to_datetime(class_data['EndTime'])
        class_data['Day'] = class_data['DateTimeStart'].dt.day_name()
        
        # Get the start and end times of each event as a decimal in the form hour.part_of_hour
        minutes = class_data['DateTimeStart'].dt.minute/60.0
        seconds = class_data['DateTimeStart'].dt.second/3600.0
        class_data['Hour_Start'] = class_data['DateTimeStart'].dt.hour + minutes + seconds
        
        minutes = class_data['DateTimeEnd'].dt.minute/60.0
        seconds = class_data['DateTimeEnd'].dt.second/3600.0
        class_data['Hour_End'] = class_data['DateTimeEnd'].dt.hour + minutes + seconds
        
        # Format the measurements with a space between the description and unit
        values = class_data.columns
        for val in values:
            split_val = val.split('(')
            if len(split_val) > 1:
                split_val[1] = '(' + split_val[1]
                combined_val = " ".join(split_val)
                class_data = class_data.rename(columns={val:combined_val})
        
        # Change "closhwasher spelling
        class_data = class_data.replace({"clothwasher":"clothes washer"})
        
        # Capitalize the labesl
        labels = class_data.Label.unique()
        for lab in labels:
            class_data = class_data.replace({lab:lab.title()})
        
        return(class_data)
        
    def get_indoor(self):
        ''' 
        Gets all the events that deal with indoor usage 
        
        Returns:
            pandas dataframe of all events determined to be indoor events
        '''
        
        df = self.df;
        indoor_labels = ['Faucet','Toilet','Clothes Washer','Shower']
        indoor_df = df.loc[df.Label.isin(indoor_labels)]
        return(indoor_df)
        
    def get_outdoor(self):
        ''' 
        Gets all the events that deal with outdoor usage
        
        Returns:
            pandas dataframe of all events determined to be outdoor events
        '''
        
        df = self.df
        outdoor_labels = ['Hose','Irrigation']
        outdoor_labels = df.loc[df.Label.isin(outdoor_labels)]
        return(outdoor_labels)
        
    def total_cost(self, cost_gal):
        """
        Calculates an estimate of the total water cost over a month
        If data exists for more or less than a month, the data is averaged to
        represent a single month assuming param.days_month is the number of 
        days in a month
        
        Args:
            cost_gal: Cost per gallon of water
        
        Returns:
            Dictionary where keys are the category labels and entries are how 
            much was spent on that category
        
        """
        cost_dict = {}
        for name, group in self.df.groupby('Label'):
            total_vol = group.sum()['Volume (gal)']
            
            days = (group.DateTimeStart.max() - group.DateTimeStart.min()).days
            seconds = (group.DateTimeStart.max() - group.DateTimeStart.min()).seconds
            days = days + seconds/param.sec_day
            
            vol_day = total_vol/days
            vol_month = vol_day*param.days_month
            
            cost_dict[name] = vol_month*cost_gal
            
            
        return cost_dict
        
        
    def irrigation_times(self):
        """
        Determines the earliest and latest times that irrigation occurs.
        A boxplot graph is used to get the max and min times that irrigation 
        happens while rejecting any outliers.
        
        The max time is the highest end time for irrigation in the upper whisker
        The min time is the lowest start time for irrigation in the lower whisker
        
        
        Returns:
            Dictionary containing the calculated min start and max end irrigation times
            This can be passed to plot_water_times in data_processing.py to plot
        
        """
        # Get all irrigation events
        irr_df = self.outdoor_df.groupby('Label').get_group('Irrigation').copy()
        #irr_df['Day'] = irr_df['DateTimeStart'].apply(lambda x: x.timetuple().tm_yday)
        
        start_times = irr_df['Hour_Start']
        end_times = irr_df['Hour_End']
        
        # Use boxplot to get the highest/lowest values that aren't outliers
        B = plt.boxplot(start_times)
        min_start = B['whiskers'][0].get_ydata()[1] # Min of bottom whisker
        B = plt.boxplot(end_times)
        max_end = B['whiskers'][1].get_ydata()[1] # Max of upper whisker
        
        results = {}
        results['StartTime'] = min_start
        results['EndTime'] = max_end
        results['IdealStart'] = param.ideal_start # Per lawnDoctor, earliest water time is 4 AM
        results['IdealEnd'] = param.ideal_end # Per LawnDoctor, latest water time is 9 AM
        
        return(results)
        
        
    def get_irrigation_gpm(self, actual_acre):
        ''' 
        Calculate water used as irrigation per month and compares that to an ideal value based on acrage
        Also calculates how much land you could water with current consumption
        Assumes .623 gal/sqft/week (set in water_params)
        All results are scaled to represent a single month
        
        Args:
            actual_acre: Actual acerage of the plot under consideration
                
        Returns:
            Dictionary showing the actual and ideal amounts of water used for irrigation
            Additionally, shows the actual acerage as well as the acerage that could be irrigated
            using the current amount of water
            
            Can be used with plot_ideals in data_processing.py
                
        
        '''        
            
        sqft2acre = 1/43560.0
        acre2sqft = 1/sqft2acre
        
        # Get irrigation events and total volume used on irrigation
        irr_df = self.outdoor_df.groupby('Label').get_group('Irrigation')
        total_gal = irr_df.sum()['Volume (gal)']
        
        # Determine how long data exists for
        n_days = (irr_df.DateTimeStart.max() - irr_df.DateTimeStart.min()).days
        n_seconds = (irr_df.DateTimeStart.max() - irr_df.DateTimeStart.min()).seconds
        n_time = n_days + n_seconds/param.sec_day
        
        # Calculate the possible acerage based off current irrigation usage
        equiv_sqft = total_gal*param.days_week/(param.gal_sqft*n_time) # (gal/days)*(7 days/1 week)*(sqft * week/ .623 gal)
        equiv_acre = equiv_sqft*sqft2acre
        
        # Calculate the ideal amount of irrigation water
        actual_sqft = actual_acre * acre2sqft
        ideal_usage = actual_sqft * param.gal_sqft * n_time / param.days_week # sqft * (.623 gal/ week*sqft)*days*(1 week/7 days)
        
        # Calculate monthly usage
        month_usage = total_gal*param.days_month/n_time # Gallons/month
        ideal_month_usage = ideal_usage*param.days_month/n_time # Gallons/month
        
        # Calculate potential savings
        gal_saved_month = month_usage - ideal_month_usage
        dollar_saved = gal_saved_month*self.cost_gal
        
        results = {}
        results['Name'] = 'Irrigation Usage'
        results['Units'] = 'Gallons per Month'
        results['Actual Usage (gal)'] = month_usage
        results['Ideal Usage (gal)'] = ideal_month_usage
        results['Potential Savings ($)'] = dollar_saved
        results['Potential Savings (gal)'] = gal_saved_month
        results['Plot Area (acre)'] = actual_acre
        results['Possible Area (acre)'] = equiv_acre

        return results
    
    def get_shower_gpm(self):
        """
        Calculates the average shower flowrate and compares it to the ideal
        Reduces all flowrates above the ideal to calculate an ideal usage scenario
        
        Returns:
            Dictionary with the average and ideal shower flowrates as well as 
            possible savings
            Can be used with plot_ideals in data_processing.py
        
        """
        
        
        shower_df = self.df.groupby('Label').get_group('Shower').copy()
        mean_gpm = shower_df['Flowrate (gpm)'].mean()
        
        (dollar_saved_month, gal_saved_month) = self.calc_flow_savings(shower_df, self.ideal_shower_gpm)
        
        results = {}
        results['Name'] = 'Shower Flowrate'
        results['Units'] = 'Gallons per Minute'
        results['Actual Flowrate (gpm)'] = mean_gpm
        results['Ideal Flowrate (gpm)'] = self.ideal_shower_gpm
        results['Potential Savings ($)'] = dollar_saved_month
        results['Potential Savings (gal)'] = gal_saved_month
        
        return(results)
        
    def get_shower_time(self):
        """
        Calculates the average shower duration and compares it to the ideal
        Reduces all durations above the ideal to calculate an ideal usage scenario
        
        Returns:
            Dictionary with the average and ideal shower durations as well as 
            possible savings
            Can be used with plot_ideals in data_processing.py
        
        """
        shower_df = self.df.groupby('Label').get_group('Shower').copy()
        mean_gpm = shower_df['Duration (min)'].mean()
        
        (dollar_saved_month, gal_saved_month) = self.calc_time_savings(shower_df, self.ideal_shower_duration)
        
        results = {}
        results['Name'] = 'Shower Duration'
        results['Units'] = 'Minutes'
        results['Actual Duration (min)'] = mean_gpm
        results['Ideal Duration (min)'] = self.ideal_shower_duration
        results['Potential Savings ($)'] = dollar_saved_month
        results['Potential Savings (gal)'] = gal_saved_month
        
        return(results)
        
    def get_faucet_gpm(self):
        """
        Calculates the average faucet flowrate and compares it to the ideal
        Reduces all flowrates above the ideal to calculate an ideal usage scenario
        
        Returns:
            Dictionary with the average and ideal faucet flowrates as well as 
            possible savings
            Can be used with plot_ideals in data_processing.py
        
        """
        
        
        faucet_df = self.df.groupby('Label').get_group('Faucet').copy()
        mean_gpm = faucet_df['Flowrate (gpm)'].mean()
        
        (dollar_saved_month, gal_saved_month) = self.calc_flow_savings(faucet_df, self.ideal_faucet_gpm )
        
        
        results = {}
        results['Name'] = 'Faucet Flowrate'
        results['Units'] = 'Gallons per Minute'
        results['Actual Flowrate (gpm)'] = mean_gpm
        results['Ideal Flowrate (gpm)'] = self.ideal_faucet_gpm 
        results['Potential Savings ($)'] = dollar_saved_month
        results['Potential Savings (gal)'] = gal_saved_month
        
        return(results)
        
    def get_toilet_gpf(self):
        """
        Calculates the average toilet gallons per flush and compares it to the ideal
        Reduces all usage above the ideal to calculate an ideal usage scenario
        
        Returns:
            Dictionary with the average and ideal toilet gallon/flush as well as 
            possible savings
            Can be used with plot_ideals in data_processing.py
        
        """
        
        toilet_df = self.df.groupby('Label').get_group('Toilet').copy()
        mean_gal = toilet_df['Volume (gal)'].mean()
        
        (dollar_saved_month, gal_saved_month) = self.calc_vol_savings(toilet_df, self.ideal_toilet_gpf)
        
        results = {}
        results['Name'] = 'Toilet'
        results['Units'] = 'Gallons per Flush'
        results['Actual Usage (gal/flush)'] = mean_gal
        results['Ideal Usage (gal/flush)'] = self.ideal_toilet_gpf
        results['Typical Usage (gal/flush)'] = self.moderate_toilet_gpf
        results['Potential Savings ($)'] = dollar_saved_month
        results['Potential Savings (gal)'] = gal_saved_month
        
        return(results)
        
    def calc_vol_savings(self, df, ideal_vol):
        ''' 
        Calculates the savings over month if volume for each event which is over
        the idea volume is capped at the ideal volume
        
        Args:
            df: pandas dataframe containing all desired events
            ideal_vol: Ideal volume for each event (gallon)
            
        Returns:
            The dollar amount saved each month if volume is capped
            The gallon amount saved each month if volume is capped
        '''
        
        df['IdealVolume'] = df['Volume (gal)']
        df.loc[df['IdealVolume'] > ideal_vol, 'IdealVolume'] = ideal_vol
        ideal_gal = df['IdealVolume'].sum()
        actual_gal = df['Volume (gal)'].sum()
        diff_gal = actual_gal - ideal_gal
        dollar_saved = diff_gal*self.cost_gal
        dollar_saved_month = dollar_saved*param.days_month/self.data_duration
        diff_gal_month = diff_gal*param.days_month/self.data_duration
        
        return(dollar_saved_month, diff_gal_month)
        
    def calc_flow_savings(self, df, ideal_flow):
        ''' 
        Calculates the savings over month if flow for each event which is over
        the idea flow is capped at the ideal flow
        
        Args:
            df: pandas dataframe containing all desired events
            ideal_flow: Ideal flow rate for each event (gallon/minute)
            
        Returns:
            The dollar amount saved each month if flowrate is capped
            The gallon amount saved each month if flowrate is capped
        '''
        
        df['IdealFlow'] = df['Flowrate (gpm)']
        df.loc[df['IdealFlow'] > ideal_flow, 'IdealFlow'] = ideal_flow
        df['IdealVol'] = df['IdealFlow']*df['Duration (min)']
        ideal_gal = df['IdealVol'].sum()
        actual_gal = df['Volume (gal)'].sum()
        diff_gal = actual_gal - ideal_gal
        dollar_saved = diff_gal*self.cost_gal
        dollar_saved_month = dollar_saved*param.days_month/self.data_duration
        diff_gal_month = diff_gal*param.days_month/self.data_duration
        
        return(dollar_saved_month, diff_gal_month)
        
    def calc_time_savings(self, df, max_time):
        ''' 
        Calculates the savings over month if duration for each event which is over
        the idea time is capped at the ideal duration
        
        Args:
            df: pandas dataframe containing all desired events
            max_time: Ideal duration for each event (minuts)
            
        Returns:
            The dollar amount saved each month if duration is capped
            The gallon amount saved each month if duration is capped
        '''
        
        df['IdealDuration'] = df['Duration (min)']
        df.loc[df['IdealDuration'] > max_time, 'IdealDuration'] = max_time
        df['IdealVol'] = df['Flowrate (gpm)']*df['IdealDuration']
        ideal_gal = df['IdealVol'].sum()
        actual_gal = df['Volume (gal)'].sum()
        diff_gal = actual_gal - ideal_gal
        dollar_saved = diff_gal*self.cost_gal
        dollar_saved_month = dollar_saved*param.days_month/self.data_duration
        diff_gal_month = diff_gal*param.days_month/self.data_duration
        
        return(dollar_saved_month, diff_gal_month)
        
        
    def calc_dt_savings(self, df, dt):
        ''' 
        Calculates the savings over month if duration for each event is reduced 
        by the specified time
        
        If the duration for an event is below the specified time, it is not affected
        
        Args:
            df: pandas dataframe containing all desired events
            dt: Time to reduce each duration by (minutes)
            
        Returns:
            The dollar amount saved each month if duration is reduced
            The gallon amount saved each month if duration is reduced
        '''
        
        df['IdealDuration'] = df['Duration (min)'] - dt
        df.loc[df['IdealDuration'] < 0, 'IdealDuration'] = 0
        df['IdealVol'] = df['Flowrate (gpm)']*df['IdealDuration']
        ideal_gal = df['IdealVol'].sum()
        actual_gal = df['Volume (gal)'].sum()
        diff_gal = actual_gal - ideal_gal
        dollar_saved = diff_gal*self.cost_gal
        dollar_saved_month = dollar_saved*param.days_month/self.data_duration
        diff_gal_month = diff_gal*param.days_month/self.data_duration
        
        return(dollar_saved_month, diff_gal_month)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        