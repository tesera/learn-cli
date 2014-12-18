#!/usr/bin/env python
"""
CurrentRevisionDate:20130506

Author(s):Ian Moss
Modified by: Ian Moss and Mishtu Banerjee
Based on the excel spreadsheet "IDFCurves_Apr_01_2013.xlsx" by Ian Moss
Contact: mishtu.banerjee@tesera.com, ian.moss@tesera.com

Copyright: The Author(s)
License: Distributed under MIT License
    [http://opensource.org/licenses/mit-license.html]


Dependencies:
    Python interpreter and base libraries
    TSIAnalytics: miniStats, miniGraph
"""

import sys
sys.path.append("D:\\Rwd\\Python\\Admin")

import miniGraph
import miniStats
#import asaPlot
import math
import copy


# mratIDFCurvesWorkFlow

# Inputs Needed:
    #SUMS.txt
    #IDFCoefficients.txt
    #PARAM.txt
    # IDFCurves (save excel psheet as csv)
    # IDF -- Data Manually Transfferred; Save this file at a .txt; filter by city/period
    #Primary Key: City, Period, Duration, Interval
    #Note -- interval is return interval
    #TRMM -- Total Rainflal in mm
    #HRAIN -- Amount of Rainfall/Hour  -- TRMM= HRAIN*DURATION/60*(1/INTERVAL)
    #1/INTERVAL is Probability of Rain
    #ALL ABOVE IS THE BASE DATA

# Windows and MAC file paths -- Depreciated
#Mac Paths
#codeDirFilePath = '/Users/Maxine/Documents/TSIAnalytics/'
#dataFilePath = '/Users/Maxine/Documents/TSIAnalytics/Data/Moncton/'
#analysisFilePath = '/Users/Maxine/Documents/TSIAnalytics/Data/Moncton/ANALYSIS.txt'
#sumzFilePath = '/Users/Maxine/Documents/TSIAnalytics/Data/Moncton/SUMZ.txt'
#idfFilePath =  '/Users/Maxine/Documents/TSIAnalytics/Data/Moncton/IDF.txt'
#paramFilePath = '/Users/Maxine/Documents/TSIAnalytics/Data/Moncton/PARAM.txt'
#idfcoeffFilePath = '/Users/Maxine/Documents/TSIAnalytics/Data/Moncton/IDFCoefficients.txt'
#idftypesFilePath = '/Users/Maxine/Documents/TSIAnalytics/Data/Moncton/IDFDataTypes.txt'
#sumztypesFilePath = '/Users/Maxine/Documents/TSIAnalytics/Data/Moncton/SUMZDataTypes.txt'

#Windows File Paths
#codeDirFilePath = '/apps/TSIAnalytics/'
#dataFilePath = '/apps/TSIAnalytics/Data/Moncton/'
#analysisFilePath = '/apps/TSIAnalytics/Data/Moncton/ANALYSIS.txt'
#sumzFilePath = '/apps/TSIAnalytics/Data/Moncton/SUMZ.txt'
#idfFilePath =  '/apps/TSIAnalytics/Data/Moncton/IDF.txt'
#paramFilePath = '/apps/TSIAnalytics/Data/Moncton/PARAM.txt'
#idfcoeffFilePath = '/apps/TSIAnalytics/Data/Moncton/IDFCoefficients.txt'
#idftypesFilePath = '/apps/TSIAnalytics/Data/Moncton/IDFDataTypes.txt'
#sumztypesFilePath = '/apps/TSIAnalytics/Data/Moncton/SUMZDataTypes.txt'
#sys.path.append(codeDirFilePath)
#sys.path.append(dataFilePath)



#Set paths to config file
defaultconfigFilePath = '/Rwd/Python/Config/mratConfig.txt' #Default Path
configFilePath = '/Users/Maxine/Documents/TSIAnalytics/Config/mratConfig.txt' #User Specific Path


#Try the default path '/apps/TSIAnalytics/Config.txt'
#If it does not work, try configFilePath
mratConfig = miniGraph.readGraph(filepath = defaultconfigFilePath)
if mratConfig ==  'File not opened, could not find/apps/TSIAnalytics/Config/mratConfig.txt':
    mratConfig = miniGraph.readGraph(filepath = configFilePath)

myDrive = mratConfig['drive'][0] + ':'
for configAddress in mratConfig:
    if not configAddress == 'drive':
        if not configAddress == 'mratIdfCity':
            mratConfig[configAddress] = [myDrive + mratConfig[configAddress][0]]

#Set Paths from Config File
#FilePaths from mratConfig
mratIDFcodeDirFilePath = mratConfig['mratIDFcodeDirFilePath'][0]
mratIDFdataFilePath = mratConfig['mratIDFdataFilePath'][0]
mratIDFanalysisFilePath = mratConfig['mratIDFanalysisFilePath'][0]
mratIDFsumzFilePath = mratConfig['mratIDFsumzFilePath'][0]
mratIDFidfFilePath =  mratConfig['mratIDFidfFilePath'][0]
mratIDFparamFilePath = mratConfig['mratIDFparamFilePath'][0]
mratIDFidfcoeffFilePath = mratConfig['mratIDFidfcoeffFilePath'][0]
mratIDFidftypesFilePath = mratConfig['mratIDFidftypesFilePath'][0]
mratIDFsumztypesFilePath = mratConfig['mratIDFsumztypesFilePath'][0]
mratIDFForecastsFilePath= mratConfig['mratIDFForecastsFilePath'][0]
mratIdfCity = mratConfig['mratIdfCity'][0]

sys.path.append(mratIDFcodeDirFilePath)
sys.path.append(mratIDFdataFilePath)



# STEP 1: UPLOAD DATA

#Get Data Sets
sumzDataset = miniStats.getDataset(filepath = mratIDFsumzFilePath)
idfDataset = miniStats.getDataset(filepath = mratIDFidfFilePath)
paramDataset = miniStats.getDataset(filepath = mratIDFparamFilePath)

#Get Data Graphs (Config files)
idfcoeffGraph = miniGraph.readGraph(filepath = mratIDFidfcoeffFilePath)
idftypesGraph = miniGraph.readGraph (filepath = mratIDFidftypesFilePath)
sumztypesGraph = miniGraph.readGraph (filepath = mratIDFsumztypesFilePath)

print '\n'
print 'MRAT IDF CURVE PROCESSING'
#print '\n'
print 'STEP 1 DONE -- DATA SETS LOADED'
#print '\n'

print 'Municipality: ', mratIdfCity

# STEP 2: FILTER IDF CURVES FOR CURRENT CITY

idfCurrentCity = miniStats.filterDataset(dataset = idfDataset, filterVar = 'CITY', filterValues = [mratIdfCity]) 

#print '\n'
print 'STEP 2 DONE -- DATA FILTERED'
#print '\n'


# STEP 3: PIVOT DATA FOR CITY -- COLUMNS ARE FORECAST PERIODS





#Renumber the Filtered Data Set from Step 1 (sequential keys requird for pivot 
#function, whereas non-sequential keys can occur after a filter opertion). 
renidfCurrentCity = {}
renidfCurrentCity['VARIABLES'] = idfCurrentCity['VARIABLES']
keys = idfCurrentCity['DATA'].keys()
reniddata = {}
counter=-1
for key in keys:
    counter= counter + 1
    reniddata[counter] = idfCurrentCity['DATA'][key]
    
renidfCurrentCity['DATA'] = reniddata

#typedataset
typedidfCurrentCity = miniStats.getTypes(dataset = renidfCurrentCity, typesGraph = idftypesGraph)

#Pivoted data set: ROWS are CITY (MONCTON) and Columns are distinct values for PERIOD; 
#Each cell of the pivot (cell--> rowX column) has a datalist for TRMM
# Pivot info is placed into varlist in the form: varlist = [DisplayVar, RowVar, ColumnVar]
idfpivot = miniStats.Pivot(dataset = typedidfCurrentCity, varlist = ['TRMM', 'CITY', 'PERIOD'], format='x')


# Do a summation on each cell (a data list) in the pivot. 
idfpivotsum={}
idfpivotsum['VARIABLES'] = idfpivot['VARIABLES']
idfpivotsum['DATA'] = {}
idfpivotsum['DATA'][0] = idfpivot['DATA'][0]
sumrow = []
sumrow.append(idfpivot['DATA'][1][0])
pivotlists = idfpivot['DATA'][1][1:]
for datalist in pivotlists:
    sumrow.append(sum(datalist))
idfpivotsum['DATA'][1] = sumrow

#print '\n'
print 'STEP 3 DONE -- IDF DATA PIVOTED'
#print '\n'

# STEP 4 -- CALCULATE IDF RATIO
#Note -- IDF stands forIntensity Duration Frequency curves
# http://www.idfcurve.org/
# http://www.flowworks.com/rainfall-blog/idf-curves-explained


#The divisor is the IDF value for the Historical period. 
divisor = idfpivotsum['DATA'][1][1]
ratiorow = []
ratiorow.append(sumrow[0])
for value in sumrow[1:]:
    ratio = value/float(divisor)
    ratiorow.append(ratio)

idfpivotratio={}
idfpivotratio['VARIABLES'] = idfpivot['VARIABLES']
idfpivotratio['DATA'] = {}
idfpivotratio['DATA'][0] = idfpivot['DATA'][0]  
idfpivotratio['DATA'][1] = ratiorow 

#print '\n'
print 'STEP 4 DONE IDF RATIO CALCULATED'
#print '\n'


# STEP 5 -- CALCULATE NEW RATINGS

# Get params for log odds model (calculated previously by mratDiscrimRatingsWorkflow.py)
intercept = float(idfcoeffGraph['Intercept'][0])
slope = float(idfcoeffGraph['Slope Coefficient'][0])
idfratioheaders = idfpivotratio['DATA'][0][1:]
idfratios = idfpivotratio['DATA'][1][1:]

# get p from the SUMZ.txt file
sumzp = miniStats.getNumberslist(dataGraph = sumzDataset['DATA'], varGraph = sumzDataset['VARIABLES'], variable = 'p')

# get ZTRANS from the SUMZ.txt file
sumzztrans = miniStats.getNumberslist(dataGraph = sumzDataset['DATA'], varGraph = sumzDataset['VARIABLES'], variable = 'ZTRANS')


# log transform the ZTRANS values in preparation for the log odds model
#Note could notuse asaPlot's applyTransforms function to do the log transform  -- as there are 0's in the data. Log 0 is
#undefined. Ian is handling as 0' -- based on spreadsheet.  See http://wiki.answers.com/Q/What_is_the_value_of_log_0
sumzlogztrans = []
for value in sumzztrans:
    if value == 0:
        sumzlogztrans.append(value)
    else:
        sumzlogztrans.append(math.log(value))
 

# predict p values (ratings) for historical and future periods based on IDF data
#lets test/sanity-check a few single predicd values -- The lines below are simply test values that can be checked

# BEGIN CHECK VALUES -- These are soecific to Moncton data set
idfratioH = idfratios[0]
idfratioL2020 = idfratios[1]
idfratioU2020 = idfratios[2]
idfratioL2050 = idfratios[3]
idfratioU2050 = idfratios[4]


logz = sumzlogztrans[0]
pH = (math.exp((intercept * idfratioH) + (slope * logz)))/(1 + math.exp((intercept* idfratioH) + (slope * logz)))
pL2020 = (math.exp((intercept * idfratioL2020) + (slope * logz)))/(1 + math.exp((intercept* idfratioL2020) + (slope * logz)))
pU2020 = (math.exp((intercept * idfratioU2020) + (slope * logz)))/(1 + math.exp((intercept* idfratioU2020) + (slope * logz)))
pL2050 = (math.exp((intercept * idfratioL2050) + (slope * logz)))/(1 + math.exp((intercept* idfratioL2050) + (slope * logz)))
pU2050 = (math.exp((intercept * idfratioU2050) + (slope * logz)))/(1 + math.exp((intercept* idfratioU2050) + (slope * logz))) 
 
logz2 = sumzlogztrans[7] #9th vale in spht. Line 1 -- header; kube 2 values -- but list starts at 0 so off by 2
p2H = (math.exp((intercept * idfratioH) + (slope * logz2)))/(1 + math.exp((intercept* idfratioH) + (slope * logz2)))
p2L2020 = (math.exp((intercept * idfratioL2020) + (slope * logz2)))/(1 + math.exp((intercept* idfratioL2020) + (slope * logz2)))
p2U2020 = (math.exp((intercept * idfratioU2020) + (slope * logz2)))/(1 + math.exp((intercept* idfratioU2020) + (slope * logz2)))
p2L2050 = (math.exp((intercept * idfratioL2050) + (slope * logz2)))/(1 + math.exp((intercept* idfratioL2050) + (slope * logz2)))
p2U2050 = (math.exp((intercept * idfratioU2050) + (slope * logz2)))/(1 + math.exp((intercept* idfratioU2050) + (slope * logz2))) 
# END CHECK VALUES

# Forecast historical and future p values on the whole data set
#  Note -- the log odds model is being used for forecasting. 
# See notes after this section on the log odds model
forecastp = {} 
counter = 0
for logzvalue in sumzlogztrans:
    counter = counter+1
    forecastplist = []
    for idfratio in idfratios:
#        if logzvalue <> 0:
        forecastpvalue = (math.exp((intercept * idfratio) + (slope * logzvalue)))/(1 + math.exp((intercept* idfratio) + (slope * logzvalue)))
        forecastplist.append(forecastpvalue)
#        else: forecastplist.append(float(0))
    forecastp[counter] = forecastplist
        
        
# BEGIN NOTRS ON LOG ODDS MODEL APPLIED TO IDF AND ZTRANS DATA
# REUSE CODE FROM mratDiscriminantRatingsWorkflow
        #Keep zScores associated with each uid
        #Ensue that zValue is within range
#        if zValue < minZScore:
#                zValue = minZScore
#        if ztrans > maxZScore:
#                zValue = maxZScore
#        ztrans = (zValue - minRefZScore)/float(maxRefZScore-minRefZScore)
#        logZtrans = log(ztrans)
#        lodds = intercept + slope * logZtrans
#        oddsRatio = exp(lodds)
 #       p = oddsRatio/(1 + oddsRatio)
 #       sumZDict[uid].update({'ZSCORE':zValue, 'ZTRANS':ztrans, 'ODDS':oddsRatio, 'p':p})

# Expand out p:
    # p = oddsRatio/(1 + oddsRatio)
    # p = exp(lodds)/(1 + exp(lodds))
    # p = exp(intercept + slope * logZtrans/(1 + exp(intercept + slope * logZtrans))
    #Note -- idfratio works as a muliplier on the intercept:
        #    newp = exp((intercept * idfratio) + slope * logZtrans/(1 + exp((intercept* idfratio + slope * logZtrans))

#print '\n'
print 'STEP 5 DONE IDF BASED p values (FORECAST RATINGS) CALCULATED'
#print '\n'

# STEP 6 -- FILTER OUT ZONE OF UNCERTAINTY

#get the fields thatmust be filtered
paramvars = miniStats.getDatalist(dataGraph = paramDataset['DATA'], varGraph = paramDataset['VARIABLES'], variable = 'ATTR')
# Note -- first attribute in PARAMS, 'NA' must be excluded. 
zouvars = paramvars[1:]
#Note the first param is 'NA' -- tied to model constant, and ignored
zouindex = len(zouvars) + 1 # identifies variables to extract for zou comparison
zerolist = [] # a list of 0's to compare forzou
for item in range (1,zouindex):
    zerolist.append(0.0)
    


typedsumz = miniStats.getTypes(dataset = sumzDataset, typesGraph = sumztypesGraph)

#Do a check comparison on an area known to be in the zou -- specifico Moncton dataset
zouexample = typedsumz['DATA'][3][1:zouindex]
if zouexample == zerolist:
    zoucheck = True
else:
    zoucheck = False
    
zoukeys = []
for key in typedsumz['DATA']:
    if typedsumz['DATA'][key][1:zouindex] == zerolist:
        zoukeys.append(key)

#print '\n'
print 'STEP 6 DONE Zone of Uncertainty Identified'
#print '\n'

#Step 7
# when ZTRANS is 0, chk is 1; otherwise CHK is 0
chkeys = []
#Note -- ztrans is the -3 indexed item in sumz
for key in typedsumz['DATA']:
    if typedsumz['DATA'][key][-3] == 0.0:
        chkeys.append(key)

#print '\n'
print 'STEP 7 DONE chk on ztrans is 0 done'
#print '\n'



# STEP 8 -- CONSOLIDATE DATA TO RATINGS DATASET

mratforecastsDataset = {} # The final dataset
alldata = copy.deepcopy(sumzDataset['DATA'])

#Assemble the variables
finalvars = sumzDataset['VARIABLES']
finalvarkeys = finalvars.keys()
maxvarindex = len(finalvarkeys) +1
newvarslist = ['pH', 'pL2020', 'pU2020','pL2050', 'pU2050', 'ZOU', 'CHK' ]
for var in newvarslist:
    maxvarindex = maxvarindex+1
    finalvars[var] = [maxvarindex]

finalheaders = []
sumzheaders = sumzDataset['DATA'][0]
for sumzheader in sumzheaders:
    finalheaders.append(sumzheader)
for newvar in newvarslist:
    finalheaders.append(newvar)
alldata[0] = finalheaders

#Add in the forecast p's
for key in forecastp.keys():
    newvalues = forecastp[key]
    for newvalue in newvalues:
        alldata[key].append(newvalue)

#Add in ZOU and CHK
for key in forecastp.keys(): # simply used as does not have a 0 header key
    if key in zoukeys:
        alldata[key].append(1)
    else: 
        alldata[key].append(0)
    if key in chkeys:
        alldata[key].append(1)
    else:
        alldata[key].append(0)

mratforecastsDataset['VARIABLES'] = finalvars
mratforecastsDataset['DATA'] = alldata

#OUTPUT FILE for mapping: MRATForecasts..txt
mapdata = miniStats.saveDataset(dataset = mratforecastsDataset, filepath = mratIDFForecastsFilePath, append=0)

#print '\n'
print 'STEP 8 DONE MAPPING DATASET CREATED AND WRITTEN  TO FILE MRATForecasts.txt'
#print '\n'


#Original vars in sumz for referenc
#{'ZSCORE': [8],
#             'UID': [0],
#             'ZTRANS': [9],
#             'PDITC_500': [5],
#             'ODDS': [10], 
#             'DEN_BLDA': [2], 
#             'SLP_STR1': [7],
#             'p': [11], 
#             'DEN_ROAD': [3], 
#             'PCNT_CIO': [6],
#             'AGE_SAN2': [1],
#             'DIA_SAN1': [4]}







# IAN'S SKETCH OF PROCESS -- FOR REFERENCE WHILE BUILDING CODE AND AS A MEMORY AID   
#TRMM Summed b City and Period. 
    #TOTALRAINFALL: SUM ALL TRMM for HIstorical Period, and U and L forcasts. (Total Rainfall for all storm event)
    #For Each Period ssociated with a city:
            # IDFRATIO: Divde Total Ranfall by Historical Rainfall for each peiod and city
            
#Use Log Odss Formula from pg 44: p = (exp(INTERCEPT * IDFRATIO + SLOPE * ln ZTRANS) /(1 + above)
# Only IDF Ratio Changes
# ZOU -- Filter ALL Indicator Values are 0; Use PARAMs

            
