# This script demonstrates how to generate a classification from a
# lat, lon and date (or a pre downloaded dataCube )
# Firstly, the lat, lon and date is defined and a working directory (output directory)
#
# The following scripts are called

# genSingleH5sWrapper.m: A Matlab script that generates a datacube (H5 format)

# outputImagesFromDataCubeScript: A Matlab script that generates quantised
# images that are put into outputDirectory (from the datacube)

# extract_features: A python script that extracts bottle neck features using
# CNNs defined in the config file xml.  The features are stored in
# outputDirectory

# testHAB: A python script that uses the model defined in the xml file and
# generates a classification based on the datacube extracted images
# The classification probablity is printed to stdout.
#
# THE UNIVERSITY OF BRISTOL: HAB PROJECT
# Author Dr Paul Hill March 2019

import sys
import os
import extract_features
import testHAB

from xml.etree import ElementTree as et


import pudb; pu.db

sample_date = 737174;
sample_date_string = str(sample_date)

#mstringApp = '/Applications/MATLAB_R2016a.app/bin/matlab'
xmlName = '/home/cosc/csprh/linux/HABCODE/code/HAB/extractData/configHABunderDesk.xml'

mstringApp = 'matlab'

tree = et.parse(xmlName)
tree.find('.//testDate').text = sample_date_string
imsDir = tree.find('.//testImsDir').text
tree.write(xmlName)

imsDir = os.path.join(imsDir, sample_date_string)
modelD = os.getcwd()
testHAB.main(['cnfgXMLs/NASNet11_lstm0.xml', imsDir])
os.chdir('../extractData')
# GENERATE DATACUBES FOR A BUNCH OF LAT, LON POSITIONS IN A GRID
mstring = mstringApp + ' -nosplash -r \"test_genAllH5s; quit;\"'
os.system(mstring)
os.chdir('postProcess')
# GENERATE IMAGES FROM DATA CUBES
# GENERATED LAT AND LONS latLonList.txt TEXT FILE IN imsDir
mstring = mstringApp + ' -nosplash -r \"test_cubeSequence; quit;\"'
os.system(mstring)

os.chdir(modelD)
# EXTRACT BOTTLENECK FEATURES FROM IMAGES
extract_features.main(['cnfgXMLs/NASNet11_lstm0.xml', imsDir])

# GENERATE CLASSIFICATION FROM BOTTLENECK FEATURES AND TRAINED MODEL
# GENERATED CLASSIFICATIONS ENTERED INTO classesProbs.txt TEXT FILE IN imsDir
testHAB.main(['cnfgXMLs/NASNet11_lstm0.xml', imsDir])


