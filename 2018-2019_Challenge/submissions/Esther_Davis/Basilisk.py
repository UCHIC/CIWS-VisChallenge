# -*- coding: utf-8 -*-
"""
Initially created on Sat Jan 26 20:26:44 2019

@author: Esther Davis
For the Cyberinfrasructure for Intelligent Water Supply Data Visualization Challenge (household residential)
at https://github.com/UCHIC/CIWS-VisChallenge


The Basilisk class reads an input csv file of Intelligent Water Supply Data
Basilisk creates two lists --> timestamps & pulses 
    where the item at index n of one list coorisponds with index n of the other list
    
The timestamp list utilize a datetime object, 
    which allows for various time-related manipulations
    
Basilisk has 3 types of functions:
    1-Filtering
    2-Totaling
    3-Averaging
(each described in more detail below)
    
Each function's output follows the patern: [[time],[water]]

"""

from datetime import datetime 
from datetime import timedelta
import csv
import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy

debug = False

class Basilisk(): #residential
    '''
    Initialization
        Reads the CSV file and translates it to the a useable format
    '''

    def __init__(self, csv_file): #have option for csv file or prepared data set?'''
        #csv_file is a string, the path to the csv 
        print('Loading Data (this might take a moment)')
        if debug: print('Initializing...')
        self.timestamps = []
        self.pulses = []
        self.read_csv(csv_file) #fills self.timestamps & self.pulses
        
        if debug: print('data initialized')
      
    def read_csv(self, csv_file):
        csv_data = csv.reader(open(csv_file), delimiter = ',')
        line_count = 0 #just counting the rows
        
        for row in csv_data:
            if line_count > 0:# and line_count < 300000: #use second condition when testing (less boot up time)
                datetime_obj = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S') #create a datetime object out of the data
                self.timestamps.append(datetime_obj)
                pulse = int(row[1])
                self.pulses.append(pulse)
                #the index for the datestamp corresponds with index for its sources
                if debug and line_count % 100000 == 0: 
                    print(datetime_obj)
            line_count +=1 #counting which row we're on
            
    def set_new_data(self, data):
        #data must be of the format [[timestamp],[water]]
        try: 
            #A simple, but not foolproof, method of checking that data is compatible
            test = data[0][0].weekday()
            test = test + data[1][0]
            
            self.timestamps = deepcopy(data[0])
            self.pulses = deepcopy(data[1])
            
        except: print('Error: not a valid data set. Must be of format [[datetime object],[number]]')
        
    '''
    Filtering Functions
    
        Filtering functions return a new set of times/water pulses
        They do NOT change the self.timestamps or self.pulses
            unless you call the set_new_data() function
            
        The timeframe() function restricts the trims data to the times specified
            if the given stop/start time is not given, it iterates increasing
            subtraction/addition until finding a reasonably close date
            
        The filter_weekday() function throws out data from any weekday not listed
            It follows the datetime standard weekday format (ie Mon = 0, Tue = 1, etc.)
   
    '''      
    
    
    def timeframe(self, start, stop, time_format = '%Y-%m-%d %H:%M:%S', data = None):  
    #trims the data to a specified timeframe
        #start & stop arguments = string, following a datetime formatting standard
        #time_format is a specified datetime standard format
        #data follows [[timestamp],[pulse]] format
        
        #determine what data set your working with
        if data == None:
            time = deepcopy(self.timestamps)
            water = deepcopy(self.pulses)          
        else:
            time = data[0]
            water = data[1]
        adjusted = False
            
        if debug: 
            print ('data times:', time[0], '-', time[-1])
            print('searching:', start, '-', stop)
        
        #create a datetime object for start & stop 
        error = 0
        start_ind = None
        start_datetime = datetime.strptime(start, time_format)
        while start_ind == None:
            #find occurance of specified time
            if start_datetime in time:
                start_ind = time.index(start_datetime) 
                #ends loop
            #if the start time isn't found, add increasinly larger amounts of time until finding it
            else:
                start_datetime = start_datetime + timedelta(seconds=1) #add a second
                if debug: print('start time ?',start_datetime)    
                if error >= 7 and error < 30:
                    adjusted = True
                    if error % 5 == 0:
                        start_datetime = start_datetime + timedelta(minutes=1) #add a min 
                        if debug: print('subtracted min')
                elif error >= 30:
                    if error % 5 == 0:
                        start_datetime = start_datetime + timedelta(hours=1) #add a hour     
                elif error > 70:
                    if error % 20 == 0:
                        start_datetime = start_datetime + timedelta(days=1) #add a day
                error +=1
                
            if error > 1000:
                #so that it doesn't search forever for a time that is completely out of range
                start_ind = 0
                print('Error: Start time not found. Set to first avaiable time')
        
        #same process for stop time          
        error = 0
        stop_ind = None
        stop_datetime = datetime.strptime(stop, time_format)
        while stop_ind == None:
            if debug: print('stop time?',stop_datetime)
            #find occurance of specified time
            if stop_datetime in time:
                stop_ind = time.index(stop_datetime) 
                #ends loop
                
            #if the stop time isn't found, sibtract increasinly larger amounts of time until finding it
            else:
                stop_datetime = stop_datetime - timedelta(seconds=1) #subtract a second
                    
                if error >= 7 and error < 30:
                    adjusted = True
                    if error % 5 == 0:
                        stop_datetime = stop_datetime - timedelta(minutes=1) #subtract a min 
                        if debug: print('subtracted min')
                elif error >= 30:
                    if error % 5 == 0:
                        stop_datetime = stop_datetime - timedelta(hours=1) #subtract a hour     
                if error > 70:
                    if error % 20 == 0:
                        stop_datetime = stop_datetime - timedelta(days=1) #subtract a day
                error +=1
                
            if error > 1000:
                #so that it doesn't search forever for a time that is completely out of range
                stop_ind = -1
                print('Error: stop time not found. Set to last avaiable time')
            
        time = time[start_ind:stop_ind]
        water = water[start_ind:stop_ind]
        #warn user of changes
        if adjusted: print ('Error: Exact timeframe not found. Set to', time[0], '-', time [-1])
        return [time, water]
    
    
    def filter_weekday(self, weekdays_to_keep, data = None):
    #specify certain weekdays to look at
        #weekdays_to_keep is a list of numbers corrisponding with the weekdays (0 = Monday, 1 = Tuesday, etc.)
        if data == None:
            data = [self.timestamps, self.pulses]
        new_data = [[],[]]
            
        for time in range(len(data[0])):
            #pull the weekday number from datetime obj
            weekday = data[0][time].weekday() 
             
            if weekday in weekdays_to_keep:
                new_data[0].append(data[0][time])
                new_data[1].append(data[1][time])
        
        return new_data
    
    '''
    Totaling Functions
    
        The total_by_unit() function condenses all the water pulses to the size of a given unit of time
            ex: total_by_unit('hour') returns a list of total water pulses for each hour slot in the data set
        
        The average_by_unit() functions averages water usage for designated time slots
            NOTE: averaging functions replace the timestamps with integers
            ex: average_by_weekday() returns average water usage on Mondays, Tuesdays, etc.
            
        The pulse_to_gallon conversion function returns a list with gallons replacing pulses
            NOTE: use this function very last to avoid calculation errors.
    '''
    
    def pulse_to_gallon(self, data = None):
        #a simple conversion from pulses to gallons
        #use this AFTER filtering/averaging/totaling to avoid calculation error
        
        if data == None:
            data = [self.timestamps, self.pulses]
            
        for i in range(len(data[1])):
            data[1][i] = data[1][i] * .0087
            # 1 "pulse" = a volume of 0.0087 gallons 
       
        return data
            
    
   
    def total_by_unit(self, unit_time = 'date', data = None):
        
        if debug: print('Totaling by', unit_time)
        if data == None: 
            data = [self.timestamps, self.pulses]
        water = []
        days = []
        day_count = -1
        prev_day = None
        for i in range(len(data[0])):
            
            if unit_time == 'date' or unit_time == 'day':
                day = data[0][i].date() #snips the day from the timestamp
            elif unit_time == 'hr' or unit_time == 'hour':
                day = data[0][i].hour #snips hour
            elif unit_time == 'min' or unit_time == 'minute':
                day = data[0][i].minute #snips minute

            if day != prev_day:
                day_count += 1 #ie move onto next day
                water.append(0)
                prev_day = day
                days.append(data[0][i])
                #if debug: print(unit_time, day_count,'(', day, 'th)')
                
            pulse = data[1][i]
            water[day_count] += pulse
            
        return [days, water]
    
    
    '''
    Averaging Functions
    
        The average_by_unit() functions averages water usage for designated time slots
            NOTE: averaging functions replace the timestamps with integers
            Though it currently only averages by minute-stamps and hour-stamps,
                is function can be expanded to include more timeslots
        
        The average_by_weekday() returns average water usage on Mondays, Tuesdays, etc.
        
    '''
    
    
    def average_by_weekday(self, data = None): 
        #adds up all the pulses for Mondays, Tuesdays, etc. then averages 
        if data == None:
            data = [self.timestamps, self.pulses]
        
        water = [0,0,0,0,0,0,0]
        prev_day = None
        weekday_count = [0,0,0,0,0,0,0]
        #weekdays match an index - Monday = 0, Sunday = 6
        for i in range(len(data[0])):
            if data[0][i].date() != prev_day: #see if the day changed
                weekday = data[0][i].weekday() #see what day of the week it is now
                if debug: print('weekday', weekday)
                prev_day = data[0][i].date() #reassign the 'previous day'
                weekday_count[weekday] += 1 #count another Mon/Tue/Wed/etc.
            water[weekday] += data[1][i] #count the pulses per weekday
        
        #average out everything
        for i in range(7):
            water[i] = water[i]/weekday_count[i]
        #['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']#
        days_list = [0,1,2,3,4,5,6]
            
        return [days_list, water]

    
    def average_by_hour(self, data = None):
        #uses similar code to average_by_weekday
        if data == None: #defaults to using own data
            data = [self.timestamps, self.pulses]
           
        water = [] #to keep track of water usage in 24 slots coresponding to hours
        for i in range(24):
            water.append(0)
        hour_count = [] #for averaging calculation later
        for i in range(24):
            hour_count.append(0)
        prev_hour = None
        
        for i in range(len(data[0])):
            clock_hour = data[0][i].hour #see what hour it is now
            if clock_hour != prev_hour: #see if the hour changed
                prev_hour = data[0][i].hour 
                hour_count[clock_hour] += 1 
            water[clock_hour] += data[1][i]
            
        #average out everything
        for i in range(24):
            water[i] = water[i]/hour_count[i]
                
        hour_list = []
        the_hour = 0
        for i in range(24):
            hour_list.append(the_hour)
            the_hour +=1
        
        return [hour_list, water]
    

    
    def average_by_unit(self, unit = 'hr', data = None):
        #this is mostly a template for expanding into other units that an
            #analyzer many want to 'average'
        #interestingly, averaging by the minute stamp does a show a pattern
        if data == None: #defaults to using own data
            data = [self.timestamps, self.pulses]
        
        if unit == 'hr' or unit == 'hour':
            slots = 24
        if unit == 'min' or unit == 'minute':
            slots = 60
        
        water = [] #to keep track of water usage in 24 slots coresponding to hours
        for i in range(slots):
            water.append(0)
        hour_count = [] #for averaging calculation later
        for i in range(slots):
            hour_count.append(0)
            
        prev_hour = None
        
        for i in range(len(data[0])):
            if unit == 'hr' or unit == 'hour':
                clock_hour = data[0][i].hour #see what hour it is now
            if unit == 'min' or unit == 'minute':
                clock_hour = data[0][i].minute
            
            if clock_hour != prev_hour: #see if the hour changed
                if unit == 'hr' or unit == 'hour':
                    prev_hour = data[0][i].hour 
                if unit == 'min' or unit == 'minute':
                    prev_hour = data[0][i].minute
                
                hour_count[clock_hour] += 1 
            water[clock_hour] += data[1][i]
            
        #average out everything
        for i in range(slots):
            water[i] = water[i]/hour_count[i]
                
        hour_list = []
        the_hour = 0
        for i in range(slots):
            hour_list.append(the_hour)
            the_hour +=1
        
        return [hour_list, water]
    
    '''
    Visualization Functions
    '''        
    
    def basic_plot(self, data_set, title = 'Household Water Usage', y_axis = 'Water Use', x_axis = 'Time'):
        #for just one data set
        plt.plot(data_set[0], data_set[1])
        plt.title((title))
        plt.ylabel(y_axis)
        plt.xlabel(x_axis)
        plt.show()
        
    def multidata_plot(self, data_list, colors =['b','g','r','c','m','y','k'], legend_list = None, title = 'Household Water Usage', y_axis = 'Water Use', x_axis = 'Time'):
        #data list is of the form [ [[time],[water]], [[time],[water]], ... , [[time],[water]] ]
        #simplifies plotting
        for i in range(len(data_list)):
            plt.plot(data_list[i][0], data_list[i][1], colors[i])
        if legend_list != None:
            plt.legend((legend_list))
        plt.title((title))
        plt.ylabel(y_axis)
        plt.xlabel(x_axis)
        plt.show()    
     
    
def sample_analysis():
    #baskilisk? 
    Magikarp = Basilisk('test1.txt') #initiate class, read csv file
    
    print('\n\n')
    welcome = 'Basilisk makes use of datetime timestamps to visualize residential water usage through various averaging and filtering functions.'
    print(welcome)
    
    print('\n\n')
    explanation = 'For example, it can graph average water usage  throughout the day.'
    print(explanation)
    
    #task 1 - show average hourly water use
    data = Magikarp.average_by_hour()
    data = Magikarp.pulse_to_gallon(data) #convert to gallons
    #print(data)
    plt.plot(data[0], data[1])
    plt.title(('Average Hourly Household Water Usage'))
    plt.ylabel('Average Water Use (gallons)')
    plt.xlabel('Time')
    plt.show()
    
    print('\n\n')
    explanation = 'Using the same method, it can also compare water use on the weekend to weekdays.'
    print(explanation)
    
    
    #task 2 - compare average hourly weekend use to weekday use
    weekend = Magikarp.filter_weekday([6,5])
    weekday = Magikarp.filter_weekday([0,1,2,3,4])
    #average_by_hour replaces timestamps with a integer, so you have to do it last
    weekend = Magikarp.average_by_hour(weekend) 
    weekday = Magikarp.average_by_hour(weekday)
    weekend = Magikarp.pulse_to_gallon(weekend) #convert to gallons
    weekday = Magikarp.pulse_to_gallon(weekday)
    
    plt.plot(weekend[0], weekend[1], 'r')
    plt.plot(weekday[0], weekday[1], 'b')
    plt.title('Average Hourly Water Usage')
    plt.legend(('Weekend', 'Weekday'))
    plt.ylabel('Average Water Use (gallons)')
    plt.xlabel('Time')
    plt.show()
    
    
    print('\n\n')
    explanation = 'Want more detail? Graph average waterusage for each individual day of the week.'
    print(explanation)
    
    #OR show the average hourly usage by weekday
    mon = Magikarp.filter_weekday([0])
    tue = Magikarp.filter_weekday([1])
    wed = Magikarp.filter_weekday([2])
    thur = Magikarp.filter_weekday([3])
    fri = Magikarp.filter_weekday([4])
    sat = Magikarp.filter_weekday([5])
    sun = Magikarp.filter_weekday([6])
    weekday_data = [mon, tue, wed, thur, fri, sat, sun]
    colors =['b','g','r','c','m','y','k']
    week_hours = [] #for later use
    #average_by_hour replaces timestamps with a integer, so you have to do it last
    for i in range(7):
        hourly_data = Magikarp.average_by_hour(weekday_data[i])
        hourly_data = Magikarp.pulse_to_gallon(hourly_data)
        for hour in range(len(hourly_data[1])):
            week_hours.append(hourly_data[1][hour])
        plt.plot(hourly_data[0], hourly_data[1], colors[i])
        
    plt.title('Average Hourly Water Use by Day of Week')
    plt.legend(('Mon', 'Tue', 'Wed','Thur', 'Fri','Sat','Sun'))
    plt.ylabel('Average Water Use (gallons)')
    plt.xlabel('Time')
    plt.show()
    
    
    print('\n\n')
    explanation = 'You can view the typical week as a whole by averaging the water usage by weekday.'
    print(explanation)
    
    data = Magikarp.average_by_weekday()
    data = Magikarp.pulse_to_gallon(data)
    plt.plot(data[0], data[1], 'r')
    plt.title('Average Weekly Water Use')
    #plt.legend(('Mon', 'Tue', 'Wed','Thur', 'Fri','Sat','Sun'))
    plt.ylabel('Average Water Use (gallons)')
    plt.xlabel('Week Day (Monday - Sunday)')
    plt.show()
    
    
    print('\n\n')
    explanation = 'Or get creative, and tack together your hourly-average data into a more detailed graph.'
    print(explanation)
    
    hoursperweek = np.arange(24*7)
    #we saved "week_hours" earlier, when comparing days of the week 
    plt.plot(hoursperweek, week_hours)
    plt.title('Average Weekly Water Use')
    #plt.legend(('Mon', 'Tue', 'Wed','Thur', 'Fri','Sat','Sun'))
    plt.ylabel('Average Water Use (gallons)')
    plt.xlabel('Hours of the Week (Monday - Sunday)')
    plt.show()
    
    
    print('\n\n')
    explanation = 'Speaking of creative, what happens if you average water usage by the minute stamp?'
    print(explanation)
    explanation = '(i.e. all the water pulses at 1:43, 2:43, 3:43, 4:43, etc. belong to the same group)'
    print(explanation)
    explanation = 'Turns out that this unusual analysis show a pattern, too. Now we can see that Mon/Wed/Fri all have a similar schedule. So does Tue/Thurs.'
    print(explanation)

    #OR show it by the minute
    for i in range(7):
        minutely_data = Magikarp.average_by_unit('min',weekday_data[i])
        plt.plot(minutely_data[0], minutely_data[1], colors[i])
        
    plt.title('Average Water Use by Minute Stamp')
    plt.legend(('Mon', 'Tue', 'Wed','Thur', 'Fri','Sat','Sun'))
    plt.ylabel('Average Water Use')
    plt.xlabel('Minute Stamp')
    plt.show()
    
    
    print('\n\n')
    explanation = "What if you don't want averages, but a simple timeline instead? Just pick a timeframe and the appropriate filter & resolution."
    print(explanation)
    
    print('\n\n')
    explanation = "Watch daily water usage over a month."
    print(explanation)
    
    #task 3 - show total water use by daily total
    start = '2018-06-20 00:00:00'
    stop = '2018-07-27 10:58:00'
    data = Magikarp.timeframe(start , stop)
    #hrly = Magikarp.total_by_unit('hr', data)
    daily = Magikarp.total_by_unit(data=data)
    daily = Magikarp.pulse_to_gallon(daily)
    #plt.plot(hrly[0], hrly[1], 'r')
    plt.plot(daily[0], daily[1], 'b')
    plt.title('Household Water Usage (June 20th-July 27th)')
    plt.ylabel('Water Daily Usage (gallons)')
    plt.xlabel('Time')
    plt.show()
    
    #task 4 - show total water use by hour vs total use by minute
    #convert hour usage to gallons for better scale
   
    print('\n\n')
    explanation = "Compare the hourly use to the minute-by-minute use for a particular day."
    print(explanation)
    
    data = Magikarp.timeframe('2018-06-25 00:00:00','2018-06-25 23:59:59')
    
    hrly = Magikarp.total_by_unit('hr', data)
    hrly = Magikarp.pulse_to_gallon(hrly)
    mnt = Magikarp.total_by_unit('min',data=data)
    
    plt.plot(mnt[0], mnt[1], 'b')
    plt.plot(hrly[0], hrly[1], 'r')
    plt.title('Household Water Use (June 25th, 2018)')
    plt.legend(('Total by Minute (pulses)', 'Total by Hour (gallons)'))
    plt.ylabel('Water Usage')
    plt.xlabel('Time')
    plt.show()
    
    print('\n\n')
    explanation = "Or show the maximum resolution, water pulse counts every 4 seconds, for a given morning."
    print(explanation)
    data = Magikarp.timeframe('2018-06-25 00:00:00','2018-06-25 11:59:59')
    plt.plot(data[0], data[1], 'g')
    plt.title('Morning of June 25th, 2018 - Maximum Resolution')
    #plt.plot(hrly[0], hrly[1], 'r')
    plt.ylabel('Water Usage (pulses)')
    plt.xlabel('Time')
    plt.show()
    
    
    print('\n\n')
    explanation = "These examples just scratch the surface."
    print(explanation)
    explanation = "Whether you use Basilisk as-is or as a template for more complicated projects,"
    conclusion = "Basilisk provides the scaffolding you need to visualize residential water usage."
    print(explanation, conclusion)
    
        
sample_analysis() 
