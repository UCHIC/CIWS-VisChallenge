 function A = ImportData() %ImportData function
     FileName =  uigetfile('*.mat','Select the MAT file');
     A = importdata(FileName); %import data from file, into structure A
 end