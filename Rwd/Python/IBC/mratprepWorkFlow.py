#!/usr/bin/env python
"""
CurrentRevisionDate:20130506

Author(s):Ian Moss
Modified by: Ian Moss and Mishtu Banerjee
Contact: mishtu.banerjee@tesera.com, ian.moss@tesera.com

Copyright: The Author(s)
License: Distributed under MIT License
    [http://opensource.org/licenses/mit-license.html]


Dependencies:
    Python interpreter and base libraries
    TSIAnalytics: dataMachete, miniGraph
    
    
# This script processes and integrates claims and infrastructure data for the IBC MRAT
# The dataset is the Moncton dataset for MRAT
"""
print "Importing..." #333
import sys
import re
import pdb 

sys.path.append('/shared/GitHub/Tesera/Rwd/Python/Admin')

import dataMachete
import miniGraph
print "Done importing." ##333

#############################################################################
#Loading Config file

print;print "COMMAND:" #333
# defaultconfigFilePath = '/Rwd/Python/Config/mratConfig.txt' #Default Path (original)
# pdb.set_trace()
defaultconfigFilePath = '/shared/GitHub/Tesera/Rwd/Python/Config/mratConfig.txt' #Default Path
print "COMMAND: defaultconfigFilePath = '/shared/GitHub/Tesera/Rwd/Python/Config/mratConfig.txt'" #333 
print "defaultconfigFilePath = ", defaultconfigFilePath #333

# # pdb.set_trace()
print;print "COMMAND:" #333
print "Setting configFilePath..." #333
print "configFilePath = '/shared/GitHub/Tesera/Rwd/Python/Config/mratConfig.txt'" #333 #User Specific Path
configFilePath = '/shared/GitHub/Tesera/Rwd/Python/Config/mratConfig.txt' #User Specific Path
# configFilePath = 'D:/Rwd/Python/Config/mratConfig.txt' #User Specific Path
print "configFilePath = ", configFilePath #333

# # pdb.set_trace()
#Try the default path '/apps/TSIAnalytics/Config.txt'
#If it does not work, try configFilePath
print;print "COMMAND:" #333
print "Setting params with miniGraph..."
print "mratConfig = miniGraph.readGraph(filepath = defaultconfigFilePath)" #333
print "defaultconfigFilePath = ", defaultconfigFilePath #333
mratConfig = miniGraph.readGraph(filepath = defaultconfigFilePath)
print "mratConfig =", mratConfig #333
  
if mratConfig ==  'File not opened, could not find/apps/TSIAnalytics/Config/mratConfig.txt':
    mratConfig = miniGraph.readGraph(filepath = configFilePath)

#333 The following line changed to make linux compatible. 
# in future code, make the system OS blind. 
myDrive = mratConfig['drive'][0] # + ':' #333 removed for linux. 
for configAddress in mratConfig:
    if not configAddress == 'drive':
        mratConfig[configAddress] = [myDrive + mratConfig[configAddress][0]]
        print mratConfig[configAddress] #333

print "## LOADING DATA to dataMachete(GENERIC)..." #333
## LOADING DATA to dataMachete(GENERIC)

#Identify code directory and data directory
#MAC File Paths -- Depreciated
#mratprepcodeDirFilePath = 'E:/Apps/TSIAnalytics/'
#mratprepdataFilePath = 'E:/Apps/TSIAnalytics/Data/Moncton/'
#mratprepanalysisFilePath = 'E:/Apps/TSIAnalytics/Data/Moncton/ANALYSIS.txt'

#Windows File Paths -- Depreciated
#mratprepcodeDirFilePath = '/apps/TSIAnalytics/'
#mratprepdataFilePath = '/apps/TSIAnalytics/Data/Moncton/'
#mratprepanalysisFilePath = '/apps/TSIAnalytics/Data/Moncton/ANALYSIS.txt'

print "Setting filepaths..." #333
#FilePaths from mratConfig
print;print "COMMAND:" #333
print "mratprepcodeDirFilePath = mratConfig['mratprepcodeDirFilePath'][0]" #333
mratprepcodeDirFilePath = mratConfig['mratprepcodeDirFilePath'][0]
print "mratprepcodeDirFilePath =", mratprepcodeDirFilePath #333

# # pdb.set_trace()
print;print "COMMAND:" #333
print "mratprepdataFilePath = mratConfig['mratprepdataFilePath'][0]" #333
mratprepdataFilePath = mratConfig['mratprepdataFilePath'][0]
print "mratprepdataFilePath =", mratprepdataFilePath #333
print;print "COMMAND:" #333
print "mratprepanalysisFilePath = mratConfig['mratprepanalysisFilePath'][0]" #333
mratprepanalysisFilePath = mratConfig['mratprepanalysisFilePath'][0]
#print mratprepanalysisFilePath
print "mratprepanalysisFilePath =", mratprepanalysisFilePath #333

print "Appending filepaths to sys.path" #333
sys.path.append(mratprepcodeDirFilePath)
sys.path.append(mratprepdataFilePath)
print "sys.path = ", sys.path #33

print "Setting MYERROR filepath..." #333
## DATA INPUT AND OUTPUT
#Delete old error file and create a new error printfile path 
errorFileName = 'MYERROR'

# # pdb.set_trace()
print;print "COMMAND:" #333
print "errorFilePath = dataMachete.createNewFilePath(mratprepdataFilePath, errorFileName)" #333
errorFilePath = dataMachete.createNewFilePath(mratprepdataFilePath, errorFileName) 
print "mratprepdataFilePath = ", mratprepdataFilePath #333
print "errorFileName =", errorFileName #333
print "errorFilePath = ", errorFilePath #333

print;print "COMMAND:" #333
print "dataMachete.deleteFileIfItExists(errorFilePath)" #333
dataMachete.deleteFileIfItExists(errorFilePath)

print;print "COMMAND:" #333
print "dataMachete.createNewFileIfNotExisting(errorFilePath)" #333
dataMachete.createNewFileIfNotExisting(errorFilePath)

# # pdb.set_trace()
print "#Identify data type dictionary table name " #333
#Identify data type dictionary table name (note -- .txt filename suffix is excluded)
dataTypeDictTableName = 'DATDIC'
print "dataTypeDictTableName = ", dataTypeDictTableName #333

print "#Identify data table name used in type dictionary and in file " #333 
#Identify data table name used in type dictionary and in file on computer (note -- .txt filename suffix is excluded)
dataTableName = 'SUMMARY_MUNICIPAL'
print "dataTableName = ", dataTableName #333

# pdb.set_trace()
print "#Get standard data type file (a csv file)" #333
#Get standard data type file (a csv file)
print; print "COMMAND:"
print "myTypeDict = dataMachete.getDataDictionary(mratprepdataFilePath, dataTypeDictTableName) with " #333
print "mratprepdataFilePath = ", mratprepdataFilePath #333
print "dataTypeDictTableName = ", dataTypeDictTableName #333
myTypeDict = dataMachete.getDataDictionary(mratprepdataFilePath, dataTypeDictTableName)
print "------------------------------------------------"#333
print "myTypeDict.keys() = ", myTypeDict.keys() #333
print "------------------------------------------------" #333
print "myTypeDict['SUMMARY_MUNICIPAL'].keys() = ", myTypeDict['SUMMARY_MUNICIPAL'].keys() #333

pause = raw_input("Press any key...") #333

# pdb.set_trace()
print;print "COMMAND:" #333
print "#Read in csv file in string format" #333
#Read in csv file in string format
print "myDataStringList = dataMachete.getListarray(mratprepdataFilePath, dataTableName)" #333
print "mratprepdataFilePath =", mratprepdataFilePath #333
print "dataTableName =", dataTableName #333
myDataStringList = dataMachete.getListarray(mratprepdataFilePath, dataTableName)
print "type(myDataStringList) = ", type(myDataStringList)
print "myDataStringList[0] = ", myDataStringList[0] #333
print "myDataStringList[1] = ", myDataStringList[1] #333
print "myDataStringList[2] = ", myDataStringList[2] #333

# pdb.set_trace()
print
# print "####################################################################"
print "#Convert csv file to standard data types as identified in myTypeDict" #333
#Convert csv file to standard data types as identified in myTypeDict
print; print "COMMAND:"
print "myDataTypedList = dataMachete.typeDataset(myDataStringList, myTypeDict, dataTableName, errorFilePath)" ##333
# print "dataMachete.typeDataset(" 
# print               str(c for c in myDataStringList if c in re.match('\c', c)) 
# print               str(c for c in myTypeDict if c in [A-Z,a-z,0-9,   ]) 
# print               str(c for c in dataTableName if c in [A-Z,a-z,0-9,   ]) 
# print               str(c for c in errorFilePath if c in [A-Z,a-z,0-9,   ])
# print               ")" #333
print "myTypeDict is a ", type(myTypeDict), "=", myTypeDict  #333
print "dataTableName is a ", type(dataTableName), "=",dataTableName #333
print "errorFilePath is a ", type(errorFilePath),"=",errorFilePath #333

# pdb.set_trace()
print
print "COMMAND:" #333
print "myDataTypedList = dataMachete.typeDataset(myDataStringList, myTypeDict, dataTableName, errorFilePath)" #333
print "myDataStringList[0] = ", myDataStringList[0] #333
print "myDataStringList[1] = ", myDataStringList[1] #333
print
print "myTypeDict =", myTypeDict #333
print
print "dataTableName =", dataTableName #333
print "errorFilePath = ", errorFilePath #333
myDataTypedList = dataMachete.typeDataset(myDataStringList, myTypeDict, dataTableName, errorFilePath)

# myDataStringList and myDataTypedList appear to come out identical
# print #333
# print "myDataStringList[0]= ",str(myDataStringList[0])
# print "myDataTypedList[0] = ", myDataTypedList[0] #333
# 
# for i in range(0,len(myDataStringList), 1):
# #     print myDataStringList[i], "and", myDataTypedList[i], 
#     if myDataStringList[i] != myDataTypedList[i]:
#         print
#         print "myDataStringList[",i,"] and myDataTypedList[",i,"] are DIFFERENT"
#     else:
# #         print "myDataStringList[",i,"] and myDataTypedList[",i,"] are SAME"
#         print ".",
        
# print "myDataStringList[1]= ",str(myDataStringList[1])
# print "myDataTypedList[1] = ", myDataTypedList[1] #333
# 
# print "myDataStringList[2]= ",str(myDataStringList[2])
# print "myDataTypedList[2] = ", myDataTypedList[2] #333

# pdb.set_trace()
print;print "#Create a Header list of variable names" #333
print "COMMAND:" #333
#Create a Header list of variable names
print "myDataHeader = myDataTypedList[0]" #333
print "myDataTypedList[0] =", myDataTypedList[0] #333
myDataHeader = myDataTypedList[0]

# pdb.set_trace()
print;print "#Convert myDataTypedList to DictDB format" #333
#Convert myDataTypedList to DictDB format (DictDB represents data in a tree-like database format)
#Identify KeyVarNames 
KeyVariableNameList = ['DRUID'] #DRUID was UID and removed POSTALCODE -- change d Dec 5th
print "KeyVariableNameList =", KeyVariableNameList #333
#Initialize a DictDB
myDataTypeDict = {}
print "myDataTypeDict =", myDataTypeDict #333

# pdb.set_trace()
print;print "#Add data to to the DictDB" #333
#Add data to to the DictDB
print "COMMAND:" #333
print "myDataTypedDict = dataMachete.createDictDB(myDataTypeDict,KeyVariableNameList,myDataTypedList)" #333
print "myDataTypeDict =", myDataTypeDict.keys() #333
print "KeyVariableNameList =", KeyVariableNameList #333
print "myDataTypedList[0] =", myDataTypedList[0] #333
print "myDataTypedList[1] =", myDataTypedList[1] #333
myDataTypedDict = dataMachete.createDictDB(myDataTypeDict,KeyVariableNameList,myDataTypedList)
print"<command completed>" #333
print "myDataTypedDict = ", #333
i = 0 #333
for j in myDataTypedDict.keys(): #333
    print j,",", #333
    i +=1 #333
    if i > 5: #333
        print "(etc.)" #333
        break#333

# pdb.set_trace()
print
print "# Extract primary key from the DictDB and sort in ascending order." #333
# Extract primary key from the DictDB and sort in ascending order.
distinctValueList = myDataTypedDict.keys()
distinctValueList.sort()
print "distinctValueList =", #333
for i in range(0,5,1): #333
    print distinctValueList,",", #333
print ",(etc)" #333    

print "###################################################" #333
print "# The data is now loaded into memory for processing" #333
print "###################################################"#333
# The data is now loaded into memory for processing


#############################################################################
## CLAIMS DATA PROCESSING (MRAT SPECIFIC)
print "## CLAIMS DATA PROCESSING (MRAT SPECIFIC)" #333

print "# Read CLAIMS file and convert to dictionary format" #333
# Read CLAIMS file and convert to dictionary format
claimsDataTableName = 'CLAIMS'
print "claimsDataTableName =", claimsDataTableName #333

pdb.set_trace()
print "COMMAND:" #333
print "#Import data as a Listarray. Data is represented as strings." #333
#Import data as a Listarray. Data is represented as strings.
print "claimsDataStringList = dataMachete.getListarray(mratprepdataFilePath, claimsDataTableName)"  #333
print "mratprepdataFilePath =", mratprepdataFilePath #333
print "claimsDataTableName =", claimsDataTableName #333
claimsDataStringList = dataMachete.getListarray(mratprepdataFilePath, claimsDataTableName)
#Convert the data to appropriate types using myTypeDict

print;print "---CHOKED HERE LAST TIME ON NO CLAIMS IN DICT---";print #333

# pdb.set_trace()
print "COMMAND:" #333
print "claimsDataTypedList = dataMachete.typeDataset(claimsDataStringList, myTypeDict, claimsDataTableName, errorFilePath)" #333
print "claimsDataStringList =", claimsDataStringList #333
print "myTypeDict =", myTypeDict #333
print "claimsDataTableName =", claimsDataTableName #333
print "errorFilePath =", errorFilePath #333
claimsDataTypedList = dataMachete.typeDataset(claimsDataStringList, myTypeDict, claimsDataTableName, errorFilePath)
#Note -- Data type lists and Data type dictionaries and (if necessary) the data dictionary,
#are also automatically created by one function:  getListArrayAndDictDB

# pdb.set_trace()
print "COMMAND:" #333
print "# Create a Header list" #333
print "claimsDataHeader = claimsDataTypedList[0]" #333
# Create a Header list -- Headers are usually the first line of the CSV file
claimsDataHeader = claimsDataTypedList[0]
print "claimsDataHeader =", claimsDataHeader #333

print; print "#Identify the names of variables which will act as keys" #333
#Identify the names of variables which will act as keys They are in the order from highest to lowest key in a nested schema
#NOTE: Varibale names for keys not maintained -- but the key order is. i,e first key is DRUID, last key is UID
#Other non-key data (variables in the header but not in keylist) is in the form name:value in the dictionary
#The claimsKeyVariableNameList identifies primary keys in a table schema, where each table has a one-to-many relationship
#with the next table. For example, For each DRUID there are many years, For each year, there are many months. For each month
#There are many Baciup types, and for each Backup ovent, there is a unique UID (1-1 relationship).
#This set of 1-many relationships is called a "tree". 
claimsKeyVariableNameList = ['DRUID','YEAR','MONTH','BACKUP_IBC','UID']
print "claimsKeyVariableNameList =", claimsKeyVariableNameList #33

pdb.set_trace()
print; print "#Initialize and populate the claims dictionary" #333
print "COMMAND:" #333
print "claimsDataTypeDict = dataMachete.createDictDB(claimsDataTypeDict,claimsKeyVariableNameList,claimsDataTypedList)" #333
#Initialize and populate the claims dictionary
print "claimsDataTypeDict[0] =", claimsDataTypeDict[0] #333 
print "claimsDataTypeDict[1] =", claimsDataTypeDict[1] #333 
print "claimsKeyVariableNameList[0] =", claimsKeyVariableNameList[0] #333
print "claimsKeyVariableNameList[1] =", claimsKeyVariableNameList[1] #333
print "claimsDataTypedList[0] =", claimsDataTypedList[0] #333
print "claimsDataTypedList[1] =", claimsDataTypedList[1] #333
claimsDataTypeDict = {}
claimsDataTypeDict = dataMachete.createDictDB(claimsDataTypeDict,claimsKeyVariableNameList,claimsDataTypedList)


print; print "#Get DRUID list from claimsDict" #333
#Get DRUID list from claimsDict
#Druids are the highest level keys in this dictionary of nested (tree-like) keys. 
druidList = claimsDataTypeDict.keys()
druidList.sort()

print '\n'
print 'MRAT CLAIMS AND INSFRASTRUCTURE PROCESSING'

print 'DATA LOADED FOR PROCESSING'

print 'CLAIMS DATA PROCESSING BEGINS'

#The claims processing is as follows:
# 1. Create a dictionary which has all the year-month-ids for claims data in 
#    order from initial month to last month, with no missing months
# 2. Get the earliest claim day for each DRUID.
# 3. Summarize the number of DRUIDS by earliest date
# 4. Establish a claims record for each DRUID and year month ID. The year and 
#    month in which a claim did or did not occur.
# 5. Create a summary record of claims for each DRUID: earliest year, total 
#    number of DRUID-MONTH-CLAIMS over entire period, etc. 
# 6  Add to DRUID summary, a record of number of claims for a desired interval 
#    of time
# 7. Print DRUID-YEAR claims record (write it to a file)
# 8. Print summary of DRUID claims record. This is the file that is used in 
#    further analysis and joined to infrastructure data.
# 8a Note -- join is only for those DRUIDS represented in the claims data.
# 9 Join infrastructure data to claims summary data .
# 10 Joined record written to ANALYSIS.txt 
# NOTE -- We are missing code for claims summary by month. Need to add this code
#      to dataMachete.



# 1. Create a dictionary which has all the year-month-ids for claims data in 
#    order from initial month to last month, with no missing months
# Call lambda dictionary DRUIDCLAIMSDIctionary (lambda was used cuz was 
#   parameter of Poisson distribution). 
# Create year-month ID Dict  from claimsDict
# The ymIdDict allows retrieval of the year-month ID based on knowledge of the 
#   year and month
# The revYmIdDict allows retrieval of year and month given the year-month ID
# These allow calculations such as get the total number of claim-months for the 
#   previous 12 months

print "dataMachete.create_year_and_month_id"#333
ymidDict, revYmidDict = dataMachete.create_year_and_month_id(claimsDataTypeDict, 
                                                             druidList)
# Year Month ID headers
#ymidDict = ymidDictList[0]
#revYmidDict = ymidDictList[1]
print "STEP 1 DONE: Year-month-ids in dictionary"

# 2. Get the earliest claim day for each DRUID.
#Get earliest year and month for each druid
ymidList = revYmidDict.keys()
ymidList.sort()
earlyDateDict = dataMachete.get_earliest_druid_claims_dates(claimsDataTypeDict, 
                                                            druidList, 
                                                            ymidList,
                                                            revYmidDict)
print "STEP 2 DONE: Earliest Claim Day for each DRUID"

# 3. Summarize the number of DRUIDS by earliest date
#Summarize earliest date data by counting the number of druids associated with each earliest date (YMID)
earlyDateSummaryDict = dataMachete.summarize_earliest_date_results(earlyDateDict)
print "STEP 3 DONE:No of  DRUIDS summarized by Earliest Claim Date"

# 4. Establish a claims record for each DRUID and year month ID. The year and month in which a claim did or did not occur.
#Create LAMDA Dictionary - a list of DRUIDS and lambdaId's (e.g. YM1D) with 1 if an event occurred in the month - otherwise 0 for each DRUID
lamdaHeader = ['DRUID','YMID','YMCLAIM']
lamdaKeyVarnames = ['DRUID','YMID']
#Initialize lamda dictionary
lamdaDict = dataMachete.initialize_lamda_dictionary(druidList, ymidList)
#Assign ones to months in which claims occurred for each DRUID
lamdaDict = dataMachete.compile_lamda_claim_months(claimsDataTypeDict,druidList, ymidDict, lamdaDict)
print "STEP 4 DONE: Claims record established for each DRUID by year month ID"


#INTERPRETATION POINT 1-----------------------------------------------------
#Example: This is some code that can be used to produce data for a graph of number of claims per month (y-axis) and month (x-axis)
#Start process to produce graph of DRUID-CLAIM-MONTHS expressed as a proportion of DRUIDS
#This normalizes for the size of the city
#Initialize DRUID-CLAIM-MONTHS
druidClaimMonthList = dataMachete.create_a_list_of_zeros_of_length_equal_to_inputList(ymidList)
#FIXED.This line breaks the code
print "step 4b ok"
druidClaimMonthList = dataMachete.update_druidClaimMonthList(druidClaimMonthList,lamdaDict)
print "step 4c ok"
# Make a graph where the X axis is from ymidList and the Y is druidClaimMonthList
# druidClaimMonthList are normalized by the number of druids in the claims data
# This graph is useful for:
    # Identifying months in which extreme events are occurring

# 5. Create a summary record of claims for each DRUID: earliest year, total number of DRUID-MONTH-CLAIMS over entire period, etc.
ltimeDict = dataMachete.compile_average_number_of_events_per_unit_of_time_period_and_number_of_events(lamdaDict, druidList, ymidList)
print "STEP 5 DONE: Summary record of claims for each DRUID"

# 6  Add to DRUID summary, a record of number of claims for a desired interval of time
start_year = 2005
end_year = 2011
ltimeDict = dataMachete.compile_events_between_start_and_end_year(ltimeDict,earlyDateDict, claimsDataTypeDict, start_year, end_year)
print "STEP 6 DONE: LTIME summary of numbere of claims per DRUID for chosen start year to chosen end year"

# 7. Print DRUID-YEAR claims record (write it to a file)
#Print LAMDA File
printLamdaFilepath = mratprepdataFilePath + 'LAMDA.txt'
# Lamda refers to the exponent in a poisson distribution (which is both the mean and sd).
# Lamda is the number of events per unit time
# The LAMDA.txt file identifies the DRUID, the YMID and whether there was at least 1 claim in that month (YMCLAIM).


dataMachete.initializeVariableHeader(lamdaHeader,printLamdaFilepath)
dataMachete.saveDictDB(lamdaKeyVarnames,lamdaHeader,lamdaDict, printLamdaFilepath)
print "STEP 7 DONE: DRUID-YEAR claims record written to file LAMDA.txt"


# 8. Print summary of DRUID claims record. This is the file that is used in further analysis and joined to infrastructure data.
#Print LTIME File
printLtimeFilepath = mratprepdataFilePath + 'LTIME.txt'
ltimeHeader = ['DRUID','NPERIODS','EYDRUID','NEVENTS','EL5Y','EPT','NEL5Y']
# This file lists for each Druid the number of periods since the first claim (NPERIOD), whether the druid is in the claims period of interest (EYDRUID),
# the number of events that have occurred (NEVENTS) since and including the first claim, if an event occurred during the claims period (EL5Y),
# the number of events per period NEVENTS/NPERIOD (the lamda exponent) , and the total nuber of events that occurred over the period of interest (NEL5Y).
# EL5Y designates groups in the disriminant analysis.
#INTERPRETATION POINT 2: Do a frequency histogram on NEL5Y in LTIME  -----------------------------------------------------
# Use Graphical Technques to check and interpret the LAMDA and LTIME files

ltimeKeyVarnames = ['DRUID']
dataMachete.initializeVariableHeader(ltimeHeader,printLtimeFilepath)
#FIXED. This line breaks the code
dataMachete.saveDictDB(ltimeKeyVarnames,ltimeHeader,ltimeDict, printLtimeFilepath)
print "STEP 8 DONE: Summary of DRUID claims record written to LTIME.txt"

# 9 Join infrastructure data to claims summary data .
# Step 9 creates the  dataset  which will be converted to csv and submitted to discriminant analysis
infrastructure = myDataTypedDict
claimsummary = ltimeDict

# The inner join is done via 3 functions working together: getDictKeySetValuesList, getCommonInnerJoinKeyValueList, extractDictDBForKeySetsList

#Step 9a
# First we must get a unique set of key values (the values with a key). The keys are put in a list of lists.
infrakeys = dataMachete.getDictKeySetValuesList(myDict = infrastructure, keyVarnames= ['DRUID'])
claimskeys = dataMachete.getDictKeySetValuesList(myDict = claimsummary, keyVarnames= ['DRUID'])

#Step 9b
# Next we need to get a common key set which is the inner join
joinkeys = dataMachete.getCommonInnerJoinKeyValueList(keyValueList1= infrakeys, keyValueList2 = claimskeys)

#Step 9c
#Now we do the inner join
joineddata = dataMachete.extractDictDBForKeySetsList(parentDict= infrastructure,childDict= claimsummary, keySetList= joinkeys)

# joineddata = dataMachete.joinDictDBs(infrastructure,claimsummary, ['DRUID']) -- Old Join Method -- depreciated in dataMachete
print "STEP 9 DONE: Infrastructure and Claims Record joined"

#10 Creation of CSV file for submission to Discriminant Analysis in R
# myDataHeader -- list of infrastructure variables
# ltimeHeader -- list of variables created from claims data

# Combine the two set of headers, and make sure DRUID is the first variable in the header list
unionheaders = list(set(myDataHeader).union(set(ltimeHeader)))
unionheaders.remove('DRUID')
unionheaders.sort()
joinedheaders = ['DRUID']
for header in unionheaders:
    joinedheaders.append(header)
print "Step 10a ok"

#Create a csv file with just the list of headers
dataMachete.initializeVariableHeader(header=joinedheaders, printFilepath= mratprepanalysisFilePath)
print "Step 10b ok"

#Add the data matching those headers to the csv file
discriminantdata = dataMachete.saveDictDB(keyList=KeyVariableNameList,header =joinedheaders,myFile=joineddata, printFilepath= mratprepanalysisFilePath)
print "Step 10c ok"

print "STEP 10 DONE: Joined Infrastructure and Claims Record written to ANALYSIS.txt"

# Interpretation Step 3: Use Graphical Techniques to explore ANALYSIS (particularly indicator pattterns) before submitting to discriminant analysis -----------------------------------------------------
#Interpretation Step 4 will occur after discriminant analysis in R
