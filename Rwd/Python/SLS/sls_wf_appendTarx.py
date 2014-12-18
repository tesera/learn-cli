#!/usr/bin/env python
'''
Language: Python
Author(s): Carol Ann Crouse, Dwight Crouse, Mishtu Banerjee
Contact: carol.crouse@tesera.com, dwight.crouse@tesera.com, mishtu.banerjee@tesera.com
Type: wf (workflow)
Purpose: ETL
Keywords: ETL, parser, tarx, LIDAR, inventory

Description: Given a directory of tarx files in CSV format, this script reads in the files as datasets,
parses the tileID  from the finename and adds it to the dataset as an extra column. The modified datasets
are output as CSV files in another directory. That directory is then read, and a single CSV file is created
that appends all the output files. 

CurrentRevisionDate:20130313

Copyright: The Author(s)
Dependencies: TSIAnalytics -- miniStats
'''

import miniStats
import pprint
import os
import copy


# SET PATHS FOR FOLDER AND FILES
# mydirectorypath stores the input and output directories
#mydirectorypath = 'D:/Python_Training/test/'
mydirectorypath = 'Z:/1006_SLS_Inventory_GY_plan/fromWS_LiDAR1_instance/X_variables/checked_GTG/calc_units/calc_units_tarx/'
outdirectorypath = 'Z:/1006_SLS_Inventory_GY_plan/fromWS_LiDAR1_instance/X_variables/checked_GTG/calc_units/calc_units_tarx/out/set1/'
#outdirectorypath = 'D:/Python_Training/test/out/'

## STEP 1 -- PROCESS TARX FILES

# GET LIST OF FILES THAT WE WANT TO WORK WITH
# filelist stores the full listing of tarx files contained in the directory using the operating system command
# the for loop goes through all the files in the directory, identifying any file with the last four
# characters ending with 'tarx' and stores those file within the array mytarxlist
filelist = os.listdir(mydirectorypath)
mytarxlist = []
for file in filelist:
    if file[-4:] == 'tarx':mytarxlist.append(file)

# for each entry in mytarxlist do all the code below
for file in mytarxlist:
    myfilename = file
    myfilepath = mydirectorypath + myfilename
        
    # GET THE DATASET
    # mydata stores all the values of the single sample tarx file
    mydata = miniStats.getDataset(myfilepath)

    # FILE NAME TO PUT INTO DATASET
    # myfile stores the name of the first tarx file stored in the tarx file listing (mytarxlist)
    # myfileID stores only the number portion of the filename which occurs between position 3 and 9
    myfileID = myfilename[3:9]

    #ADD A VARIABLE TO THE VARIABLE LIST AND ADD A COLUMN TO THE DATASET
    newvars = copy.deepcopy(mydata['VARIABLES'])
    newvars['tileid'] = [len(newvars)]

    newdata = copy.deepcopy(mydata['DATA'])
    newdata[0].append('tileID')

    mykeys = newdata.keys()
    mykeys.remove(0)
    for key in mykeys:
        newdata[key].append(myfileID)


    # CREATE A NEW DATASET
    newdataset = {}
    newdataset['VARIABLES'] = newvars
    newdataset['DATA'] = newdata
    newfileout = miniStats.saveDataset(dataset=newdataset,filepath=outdirectorypath + 'tiled'+ myfilename)
    print 'file added'+myfilename
    newfileout.flush()
    newfileout.close()

print 'STEP 1 completed -- modified TARX files at:', outdirectorypath

## STEP 2 -- APPEND MODIFIED TARX FILES

outfilelist = os.listdir(outdirectorypath)
for outfile in outfilelist:
    if outfile <> 'tiledId_appended.tarx':
        outdata = miniStats.getDataset(outdirectorypath+outfile)
        append = miniStats.saveDataset(dataset=outdata,filepath=outdirectorypath+'tiledId_appended.tarx',append=1)
        append.flush()
        append.close()

print 'STEP 2 completed -- modified TARX files appended'

