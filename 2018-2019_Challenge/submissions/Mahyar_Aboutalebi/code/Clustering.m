%======================================================================================== 
% Analysis of High Temporal Resoultion Water Use Data For Single Family Residential Data 
% Developed by Mahyar Aboutalebi, Email: M.Aboutalebi@aggiemail.usu.edu
% Update Date: 2/28/2019
% Goal: Categorizing Residetial Water Use in Diffrent Water Use Class
% More info is provided in "Readme.doc"
%======================================================================================== 
%% Define The Main Function and the Required Inputs

function [VmEvent,DrEvent] = Clustering(Data,StartDate,EndDate) 
%% Extract Column Name of Data (The first one must be Time and The secon one must be The pulse values)
NameColumn=Data.Properties.VariableNames;
Column1=NameColumn{1};
Column2=NameColumn{2};
%% Extract Time and Convert data into "TimeTable"
Time=datetime(Data.(Column1));
Data_TT = timetable(Time,str2num(char(Data.(Column2))),'VariableNames',{Column2});

%% Developing an Algorithm to Detect the Class of Each Signal in Each Day
%% Step 1: Define Thresholds to Detect each Event based on Histogram Analysis
%figure;
%histogram(Data_TT.eval(Column2));

%prompt = 'What are the thresholds valuse? ';
%x = input(prompt);

UpperBound=[inf,30,19,(15:-1:1)];
LowerBound=[30,19,(15:-1:0)];

%% Step 2: Extract Data in a Daily timestep and Sort it
SDOY=day(datetime(StartDate),'dayofyear');  % DOY for the StartDate
EDOY=day(datetime(EndDate),'dayofyear');    % DOY for the EndDate

for i=1:1:EDOY-SDOY+1
    range1=[datestr(SDOY+i-1 + datenum('2018/01/01')),' ','00:00:00'];
    range2=[datestr(SDOY+i-1 + datenum('2018/01/01')),' ','23:59:59'];
    
    TR = timerange(range1,range2);
    
    DayX=Data_TT(TR,Column2);
    
    if numel(DayX)==0
        continue
    end
    SDayX=sort(DayX.(Column2));
    
    %% Step 3: Detect Each event based on the Thresholds Defined Before
    for j=1:numel(UpperBound)
        NpEvent(i,j)=numel(SDayX(and(SDayX>LowerBound(j),SDayX<=UpperBound(j))));       % Number of Pulse for Event 1
        DrEvent(i,j)=NpEvent(i,j)*4/3600;                                               % Duration of Event 1
        VmEvent(i,j)=sum(SDayX(and(SDayX>LowerBound(j),SDayX<=UpperBound(j))))*0.0087;  % Amount of Water for Event 1 (Gallon)
        
    end
end




% % Figures
% figure
% xAxis=categorical({'Toilet','Clothes Washer','Shower','Bath','Dishwasher','Other'});
% subplot(3,1,1)
% bar(xAxis,TNpEvent)
% subplot(3,1,2)
% bar(xAxis,TDrEvent)
% subplot(3,1,3)
% bar(xAxis,TVmEvent)
% datacursormode on
end