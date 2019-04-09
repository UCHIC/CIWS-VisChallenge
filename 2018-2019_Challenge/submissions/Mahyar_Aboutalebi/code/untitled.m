function varargout = untitled(varargin)
% UNTITLED MATLAB code for untitled.fig
%      UNTITLED, by itself, creates a new UNTITLED or raises the existing
%      singleton*.
%
%      H = UNTITLED returns the handle to a new UNTITLED or the handle to
%      the existing singleton*.
%
%      UNTITLED('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in UNTITLED.M with the given input arguments.
%
%      UNTITLED('Property','Value',...) creates a new UNTITLED or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before untitled_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to untitled_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help untitled

% Last Modified by GUIDE v2.5 01-Mar-2019 23:05:24

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @untitled_OpeningFcn, ...
                   'gui_OutputFcn',  @untitled_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before untitled is made visible.
function untitled_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to untitled (see VARARGIN)

% Choose default command line output for untitled
handles.output = hObject;

axes(handles.axes4)
imshow('bathroom.png')

axes(handles.axes5)
imshow('Leak.png')

axes(handles.axes6)
imshow('Dishwasher.png')

axes(handles.axes7)
imshow('washer.png')

axes(handles.axes8)
imshow('toilet.png')

axes(handles.axes9)
imshow('Other.png')

axes(handles.axes10)
imshow('Faucet.png')

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes untitled wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = untitled_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on button press in PB1.
function PB1_Callback(hObject, eventdata, handles)
% hObject    handle to PB1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
%% Import Data
handles.Data=ImportData();


guidata(hObject, handles);




% --- Executes on selection change in PopM3.
function PopM3_Callback(hObject, eventdata, handles)
% hObject    handle to PopM3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns PopM3 contents as cell array
%        contents{get(hObject,'Value')} returns selected item from PopM3


% --- Executes during object creation, after setting all properties.
function PopM3_CreateFcn(hObject, eventdata, handles)
% hObject    handle to PopM3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on selection change in PopM4.
function PopM4_Callback(hObject, eventdata, handles)
% hObject    handle to PopM4 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns PopM4 contents as cell array
%        contents{get(hObject,'Value')} returns selected item from PopM4


% --- Executes during object creation, after setting all properties.
function PopM4_CreateFcn(hObject, eventdata, handles)
% hObject    handle to PopM4 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on selection change in PopM5.
function PopM5_Callback(hObject, eventdata, handles)
% hObject    handle to PopM5 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns PopM5 contents as cell array
%        contents{get(hObject,'Value')} returns selected item from PopM5


% --- Executes during object creation, after setting all properties.
function PopM5_CreateFcn(hObject, eventdata, handles)
% hObject    handle to PopM5 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on selection change in PopM2.
function PopM2_Callback(hObject, eventdata, handles)
% hObject    handle to PopM2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns PopM2 contents as cell array
%        contents{get(hObject,'Value')} returns selected item from PopM2


% --- Executes during object creation, after setting all properties.
function PopM2_CreateFcn(hObject, eventdata, handles)
% hObject    handle to PopM2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on selection change in PopM1.
function PopM1_Callback(hObject, eventdata, handles)
% hObject    handle to PopM1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns PopM1 contents as cell array
%        contents{get(hObject,'Value')} returns selected item from PopM1


% --- Executes during object creation, after setting all properties.
function PopM1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to PopM1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on selection change in PopM8.
function PopM8_Callback(hObject, eventdata, handles)
% hObject    handle to PopM8 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns PopM8 contents as cell array
%        contents{get(hObject,'Value')} returns selected item from PopM8


% --- Executes during object creation, after setting all properties.
function PopM8_CreateFcn(hObject, eventdata, handles)
% hObject    handle to PopM8 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on selection change in PopM9.
function PopM9_Callback(hObject, eventdata, handles)
% hObject    handle to PopM9 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns PopM9 contents as cell array
%        contents{get(hObject,'Value')} returns selected item from PopM9


% --- Executes during object creation, after setting all properties.
function PopM9_CreateFcn(hObject, eventdata, handles)
% hObject    handle to PopM9 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on selection change in PopM10.
function PopM10_Callback(hObject, eventdata, handles)
% hObject    handle to PopM10 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns PopM10 contents as cell array
%        contents{get(hObject,'Value')} returns selected item from PopM10


% --- Executes during object creation, after setting all properties.
function PopM10_CreateFcn(hObject, eventdata, handles)
% hObject    handle to PopM10 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on selection change in PopM7.
function PopM7_Callback(hObject, eventdata, handles)
% hObject    handle to PopM7 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns PopM7 contents as cell array
%        contents{get(hObject,'Value')} returns selected item from PopM7


% --- Executes during object creation, after setting all properties.
function PopM7_CreateFcn(hObject, eventdata, handles)
% hObject    handle to PopM7 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on selection change in PopM6.
function PopM6_Callback(hObject, eventdata, handles)
% hObject    handle to PopM6 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns PopM6 contents as cell array
%        contents{get(hObject,'Value')} returns selected item from PopM6


% --- Executes during object creation, after setting all properties.
function PopM6_CreateFcn(hObject, eventdata, handles)
% hObject    handle to PopM6 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes during object creation, after setting all properties.
function axes3_CreateFcn(hObject, eventdata, handles)
% hObject    handle to axes3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: place code in OpeningFcn to populate axes3


% --- Executes on button press in PB2.
function PB2_Callback(hObject, eventdata, handles)
% hObject    handle to PB2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
%StartDate=[num2str(get(handles.PopM3,'Value')),'-',num2str(get(handles.PopM4,'Value')),'-',num2str(get(handles.PopM5,'Value')),...
%    ' ',num2str(get(handles.PopM2,'Value')),':',num2str(get(handles.PopM1,'Value')),':00'];
%EndDate=[num2str(get(handles.PopM8,'Value')),'-',num2str(get(handles.PopM9,'Value')),'-',num2str(get(handles.PopM10,'Value')),...
%    ' ',num2str(get(handles.PopM7,'Value')),':',num2str(get(handles.PopM6,'Value')),':00'];
StringPM1=get(handles.PopM1,'String');
StringPM2=get(handles.PopM2,'String');
StringPM3=get(handles.PopM3,'String');
StringPM4=get(handles.PopM4,'String');
StringPM5=get(handles.PopM5,'String');

StartDate=[StringPM3{get(handles.PopM3,'Value')},'-',StringPM4{get(handles.PopM4,'Value')},'-',...
           StringPM5{get(handles.PopM5,'Value')},' ',StringPM2{get(handles.PopM2,'Value')},':',...
           StringPM1{get(handles.PopM1,'Value')},':00'];
EndDate =[StringPM3{get(handles.PopM8,'Value')},'-',StringPM4{get(handles.PopM9,'Value')},'-',...
           StringPM5{get(handles.PopM10,'Value')},' ',StringPM2{get(handles.PopM7,'Value')},':',...
           StringPM1{get(handles.PopM6,'Value')},':00']; 
%% Run Clustering Function
[VmEvent,DrEvent] = Clustering(handles.Data,StartDate,EndDate); 

%% Clustering (Unsupervised Classification) Based on Duration and Water Usage Volume
VmEvent(VmEvent==0)=nan;                             % Convert Zero into NaN (Zero for those days without data)
DrEvent(DrEvent==0)=nan;                             % Convert Zero into NaN (Zero for those days without data)
KmeanMatrix=[nanmean(VmEvent)' nanmean(DrEvent)'];   % Create a Matrix for K-mean clustering
[idx,C] = kmeans(KmeanMatrix,8);                     % Unsupervised Cluster into 8 Categories (Dishwasher,Bath, Other,Leak, Clothes Washer,Faucet, Shower+Toilet, Outdoor irrigation)

SClusters=sortrows(C);

%% Put the numbers in the Table in GUI
set(handles.uitable1,'data',SClusters)
% CName = ["Total","Duration"];                                                                                  % Set Column Name in Table
% RName=["Dishwasher","Bath", "Other","Leak", "Clothes Washer","Faucet", "Shower+Toilet", "Outdoor irrigation"]; % Set Rows Name in Table
% set(handles.uitable1,'columnname',cellstr(CName));
% set(handles.uitable1,'rowname',cellstr(RName));
for j=1:8
   
    TDrEvent(j)=nansum(DrEvent(:,idx'==j),'all');
    TVmEvent(j)=nansum(VmEvent(:,idx'==j),'all');
end
%% Bar Plot Data
 STVmEvent=sort(TVmEvent);   % Sort Volume to Remove Outdoor Irrigation
 xAxis=categorical({'Dishwasher','Bath','Other','Leak','Clothes Washer','Faucet','Shower+Toilet'});
 hb=bar(handles.axes1,xAxis,STVmEvent(1:7));
 set(handles.axes1,'fontweight','bold','fontsize',10)
 ylabel(handles.axes1,'Total Volume Water Consumption in Gallons')
 hb(1).FaceColor = 'b';
 datacursormode on
 
 %% Pi Plot Data
       
% Calculate the total water usage (gallon)
total = sum(STVmEvent(1:7));
percent = STVmEvent(1:7)/total;
% Create a pie chart with sections 3 and 6 exploded
explode = [1 0 1 0 1 0 0];
pie(handles.axes2,percent, explode)
legend(handles.axes2,cellstr(xAxis),'Location','southoutside','Orientation','vertical')
set(handles.axes2,'fontsize',10)


%% Save important output for export
handles.SClusters1=SClusters(:,1);
handles.SClusters2=SClusters(:,2);
handles.STVmEvent1=sort(TVmEvent);
handles.STDrEvent1=sort(TDrEvent);

guidata(hObject, handles);






% --- Executes on button press in PB3.
function PB3_Callback(hObject, eventdata, handles)
% hObject    handle to PB3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
set(handles.PopM1,'Value',1)
set(handles.PopM2,'Value',1)
set(handles.PopM3,'Value',1)
set(handles.PopM4,'Value',1)
set(handles.PopM5,'Value',1)
set(handles.PopM6,'Value',1)
set(handles.PopM7,'Value',1)
set(handles.PopM8,'Value',1)
set(handles.PopM9,'Value',1)
set(handles.PopM10,'Value',1)
handles.Data=[];
guidata(hObject, handles);


% --- Executes on button press in pushbutton4.
function pushbutton4_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton4 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
GroupName = {'Dishwasher','Bath','Other','Leak','Clothes Washer','Faucet','Shower+Toilet','Outdoor Irrigation'};
Volume=handles.SClusters1;
Duration=handles.SClusters2;
EstVolume=handles.STVmEvent1';
EstDuration=handles.STDrEvent1';
T = table(GroupName',Volume,Duration,EstVolume,EstDuration);
writetable(T,'result.txt')


% --- Executes on button press in PB5.
function PB5_Callback(hObject, eventdata, handles)
% hObject    handle to PB5 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
%% Bar Plot Data
 xAxis=categorical({'Dishwasher','Bath','Other','Leak','Clothes Washer','Faucet','Shower+Toilet'});
 hb=bar(handles.axes1,xAxis,handles.STVmEvent1(1:7));
 set(handles.axes1,'fontweight','bold','fontsize',10)
 ylabel(handles.axes1,'Total Volume Water Consumption in Gallons')
 hb(1).FaceColor = 'b';
 datacursormode on
 
 %% Pi Plot Data
       
% Calculate the total water usage (gallon)
total = sum(handles.STVmEvent1(1:7));
percent = handles.STVmEvent1(1:7)/total;
% Create a pie chart with sections 3 and 6 exploded
explode = [1 0 1 0 1 0 0];
pie(handles.axes2,percent, explode)
legend(handles.axes2,cellstr(xAxis),'Location','southoutside','Orientation','vertical')
set(handles.axes2,'fontsize',10)

set(handles.txt5,'String','Percentage of Water Consumption Per Class')
set(handles.txt6,'String','Water Consumption Per Class ')


% --- Executes on button press in pushbutton6.
function pushbutton6_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton6 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
%% Bar Plot Data
 xAxis=categorical({'Dishwasher','Bath','Other','Leak','Clothes Washer','Faucet','Shower+Toilet'});
 hb=bar(handles.axes1,xAxis,handles.STDrEvent1(1:7));
 set(handles.axes1,'fontweight','bold','fontsize',10)
 ylabel(handles.axes1,'Total Duration Water Consumption (hr)')
 hb(1).FaceColor = 'b';
 datacursormode on
 
 %% Pi Plot Data
       
% Calculate the total duration water usage (gallon)
total = sum(handles.STDrEvent1(1:7));
percent = handles.STDrEvent1(1:7)/total;
% Create a pie chart with sections 3 and 6 exploded
explode = [1 0 1 0 1 0 0];
pie(handles.axes2,percent, explode)
legend(handles.axes2,cellstr(xAxis),'Location','southoutside','Orientation','vertical')
set(handles.axes2,'fontsize',10)

set(handles.txt5,'String','Percentage of Duration Water Consumption Per Class')
set(handles.txt6,'String','Duration Water Consumption Per Class ')
