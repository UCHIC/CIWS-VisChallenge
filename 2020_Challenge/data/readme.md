# 2020 Visualization Challenge Datasets

The following are the datasets for the 2020 visualization challenge. Visualization challenge entries may use either or both of these datasets.

## Single-Household Residential Raw Water Use Data
This dataset consists of raw water use data collected on the residential water meter of a single-family residence for a period of approximately two weeks. Data were collected using a custom datalogger (see https://doi.org/10.3390/s20133655) that senses the number of "pulses" generated by the water meter and records the count of pulses approximately every four seconds. Each individual "pulse" corresponds to a volume of 0.041619 gallons that have passed through the meter. 

This file includes a three line header with a unique identifier for the site at which the datalogger was installed, a unique identifier for the datalogger, and the meter resolution for the meter on which it is installed (the number of gallons per recorded pulse). The datalogger records three variables during the logging process: 

1. Datetime, a datetime value including the date and time in format “Year-Month-Day Hour:Minute:Second” 
2. Record, a numerical ID used to keep track of the number of values logged
3. Pulses, an integer indicating the number of pulses registered in the four second time interval.

Data for the entire time period were compiled into a single comma-separated values file that is available at the following link:

[Link to file here](https://github.com/UCHIC/CIWS-VisChallenge/blob/master/2020_Challenge/data/Raw_Data.csv)

## Single-Household Residential Water Use Event Data
This dataset consists of water use event data for the same single-family residence. These events were extracted from the raw data file posted above.

[Link to file here](https://github.com/UCHIC/CIWS-VisChallenge/blob/master/2020_Challenge/data/Classified_Events.csv)