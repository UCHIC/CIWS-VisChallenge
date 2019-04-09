# GUI developed for Cyberinfrasructure for Intelligent Water Supply Data Visualization Challenge

This repository introduces an algorithm developed as an APP in Geographical User Interface (GUI) of **MATLAB** for [Cyberinfrastructure for Intelligent Water Supply Data Visualization Challenge](https://github.com/UCHIC/CIWS-VisChallenge). The App analyzes and classifies the high temporal resolution signal pulse of single house residential water usage into eight different categories including *Dishwasher, Bath, Leak, Clothes Washer, Faucet. Shower and Toilet, Outdoor Irrigation,* and *Other*.

This App and its results could be used to visualize and analyze high resolution water use data that would be useful for both water users and water providers. The advantage of the developed GUI is that it is easily understandable and may provide actionable information. For example, homeowner can see their water use visually and may change their behavior based on the information shown in this GUI. 

## What do you expect to see as the result of this APP?
<img src="https://github.com/Mahyarona/Project-for-CIWS-VisChallenge/blob/master/images/First_API.png?raw=true" width="700" height="400">

## Objective  
The goal of developing this App is to first detect the signals and then estimate and disaggregate the volume and duration of residential water usage into common water usage categories (i.e., the eight categories mentioned above). Even though this algorithm may not be as accurate as other algorithms such as Hidden Markov Model in literature, it is faster than those of algorithms. 

## Documentation
This README document is prepared in three different parts:

  1. How to prepare the datasets for the App
  2. How does the proposed algorithm cluster the signals into aforementioned categories
  3. Summary of steps to run the APP


  ### 1. How to prepare the datasets for the App
To run the APP, users only need to import the data (i.e., in CSV format file) in **.mat** format and define a period for the analysis. To convert data from .csv into .mat, the user needs to import the .csv file using the following icon of MATLAB software and then save it as **Data**. 

<img src="https://github.com/Mahyarona/Project-for-CIWS-VisChallenge/blob/master/images/ImportData.png?raw=true" width="100" height="100">

For analysis period, a user can define the starting and ending time using **pop of menu** in the APP.

<img src="https://github.com/Mahyarona/Project-for-CIWS-VisChallenge/blob/master/images/TimePeriod.png?raw=true" width="300" height="400">

  ### 2. How does the proposed algorithm cluster the signals into aforementioned categories
First, the data must be converted to **TimeTable** format. Next, several thresholds must be defined to separate all pulses into initial classes. These initial classes can be defined by users using the histogram or sorted values of pulses. These two graphs can be extracted and inspected for the entire datasets to define thresholds. Note that these are just initial thresholds that can be easily detected by users at the first step. Later, these initial thresholds are used to help the unsupervised classification procedure that is defined in the next step. The following shows examples of the histogram and sorted values of pulses for the given dataset (a 3-month period). 

<img src="https://github.com/Mahyarona/Project-for-CIWS-VisChallenge/blob/master/images/Histogram.png?raw=true" width="600" height="400">

<img src="https://github.com/Mahyarona/Project-for-CIWS-VisChallenge/blob/master/images/Ranked.png?raw=true" width="600" height="400">

According to these figures, it is obvious that there are some patterns and pulses which can be classified into different classes. In other words, similar pulses can be categorized as one class (category). These graphs indicate that the high value pulses rarely occurred. In contrast, the frequency of the low pulses is very high. Therefore, we need to separate high, medium, and low value pulses such that to be able to analyze the data in detail. For example, a user can define two thresholds (15 and 30) to separate the high, medium, and low value pulses. 

For example, let's say we consider 18 different classes for the pulses. One might argue that 18 classes is too many but this is just the initial guess and it will be decreased into eight classes (defined at the beginning of this documentation that is based on [Residential End Uses of Water](http://www.waterrf.org/PublicReportLibrary/4309A.pdf)). After defining initail classes, the number of pulses (NpEvent), duration of pulses (NpEvent *4) and water volume (NpEvent*0.0087) corresponding for each of 18 classes are computed. In this moment, we have two important features for initial 18 classes, **Duration** and **Water Volume**. . Now it is time to use an unsupervised classification to merge the similar group into one group based on these two features. In this study, k-means algorithm is used as an unsupervised classification technique with fixed eight categories. The results of applying k-means on small part of the datasets (just for 3 days) are reported below. The results of unsupervised method also are sorted and reported in the table designed in the APP model. 

Applying the unsupervised classification method leads to labeling the 18 classes into eight classes and with matching those classes with the order reported in [Residential End Uses of Water](http://www.waterrf.org/PublicReportLibrary/4309A.pdf), the eight classes can be labeled. Therefore, duration and water volume can be calculated in each categories.

<img src="https://github.com/Mahyarona/Project-for-CIWS-VisChallenge/blob/master/images/EightClassTable.png?raw=true" width="500" height="200">

Finally, the bar and pic chart are used in this model to show the estimated water usage volume and duration, respectively, in each class. The results shown in the table can be exported as a CSV file if the user needs to use it in other analyses. 

<img src="https://github.com/Mahyarona/Project-for-CIWS-VisChallenge/blob/master/images/Last_API.png?raw=true" width="700" height="400">

  ### 3. Summary of steps to run the APP
The APP is developed in MATLAB and a user just need to (1) import the data in **.mat** format using *import* push button, (2) define the time period for which he/she wants to see results using *pop up menu*, and (3) run the APP using *Run model* button to get results. 

## Contact Information
For information about the GUI or if you have general questions, contact Mahyar Aboutalebi at m.aboutalebi@aggiemail.usu.edu
