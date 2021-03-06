function genSingleH5sWrapper(lat, lon, sample_date, h5nameOut)
%% Top level wrapper code to generate H5 file from lat, lon and date 
%% (inputs all config info and then calls genSingleH5s.m)
% USAGE:
%   genSingleH5sWrapper(lat, lon, sample_date, h5name)
% INPUT:
%   lat: lattitude for centre of datacube (string)
%   lon: lattitude for centre of datacube (string)
%   sample_date: date of sample (in single int format) (string)
%   h5nameOut: Name of output H5 datacube
% OUTPUT:
%   -
% THE UNIVERSITY OF BRISTOL: HAB PROJECT
% Author Dr Paul Hill 26th June 2018
% Updated March 2019 PRH

addpath('../extractData');
[~, pythonStr, tmpStruct] = getHABConfig;

%% load all config from XML file
confgData.inputFilename = tmpStruct.confgData.inputFilename.Text;
confgData.gebcoFilename = tmpStruct.confgData.gebcoFilename.Text;
confgData.wgetStringBase = tmpStruct.confgData.wgetStringBase.Text;
confgData.downloadDir = tmpStruct.confgData.downloadFolder.Text;
confgData.distance1 = str2double(tmpStruct.confgData.distance1.Text);
confgData.resolution = str2double(tmpStruct.confgData.resolution.Text);
confgData.numberOfDaysInPast = str2double(tmpStruct.confgData.numberOfDaysInPast.Text);
confgData.numberOfSamples = str2double(tmpStruct.confgData.numberOfSamples.Text);
confgData.mods = tmpStruct.confgData.Modality;
confgData.pythonStr = pythonStr;

inStruc.ii = 0;
inStruc.thisLat = str2double(lat);
inStruc.thisLon = str2double(lon);
inStruc.dayEnd =  str2num(sample_date);
inStruc.thisCount = 0;
inStruc.h5name = h5nameOut;

% Extract single datacube
genSingleH5s(inStruc, confgData);

