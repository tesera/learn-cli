#!/usr/bin/env python
"""
CurrentRevisionDate:20130416

Author(s):Ian Moss
Modified by: Ian Moss and Mishtu Banerjee
Based on the python module ANAL_FREQ_DISTR.py by Ian Moss
Contact: mishtu.banerjee@tesera.com, ian.moss@tesera.com

Copyright: The Author(s)
License: Distributed under MIT License
    [http://opensource.org/licenses/mit-license.html]


Dependencies:
    Python interpreter and base libraries, matplotlib
    TSIAnalytics: dataMachete, asaPlot, miniGraph
"""


import sys
sys.path.append('D:/Rwd/Python/Admin/')
sys.path.append('D:/Rwd/Python/')
import RESET_SYS_PATH
                
import dataMachete
import miniGraph
from math import *
import matplotlib.pyplot as plt
from scipy import stats


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
        mratConfig[configAddress] = [myDrive + mratConfig[configAddress][0]]

#Set Paths from Config File
#FilePaths from mratConfig
mratDiscrimcodeDirFilePath = mratConfig['mratDiscrimcodeDirFilePath'][0]
mratDiscrimdataFilePath = mratConfig['mratDiscrimdataFilePath'][0]
mratDiscrimanalysisFilePath = mratConfig['mratDiscrimanalysisFilePath'][0]



sys.path.append(mratDiscrimcodeDirFilePath)
sys.path.append(mratDiscrimdataFilePath)

#Depreciated -- MAC and WINDOWS Paths
#Mac Paths
#codeDirFilePath = '/Users/Maxine/Documents/TSIAnalytics/'
#dataFilePath = '/Users/Maxine/Documents/TSIAnalytics/Data/Moncton/'
#analysisFilePath = '/Users/Maxine/Documents/TSIAnalytics/Data/Moncton/ANALYSIS.txt'


#Windows File Paths
#codeDirFilePath = '/apps/TSIAnalytics/'
#dataFilePath = '/apps/TSIAnalytics/Data/Moncton/'
#analysisFilePath = '/apps/TSIAnalytics/Data/Moncton/ANALYSIS.txt'
#sys.path.append(codeDirFilePath)
#sys.path.append(dataFilePath)


## DATA INPUT AND OUTPUT
#Delete old error file and create a new error printfile path 
errorFileName = 'MYERROR'
errorFilePath = dataMachete.createNewFilePath(mratDiscrimdataFilePath, errorFileName) 
dataMachete.deleteFileIfItExists(errorFilePath)
dataMachete.createNewFileIfNotExisting(errorFilePath)

#Get SUMMARY
datdict = dataMachete.getDataDictionary(mratDiscrimdataFilePath, 'DATDIC')
table_name = 'SUMMARY_MUNICIPAL'
summaryList = dataMachete.getListarray(mratDiscrimdataFilePath,table_name)
typedsummarylist = dataMachete.typeDataset(summaryList, datdict,table_name,errorFilePath)
summaryHeader = summaryList[0]
summaryKeyVarnames = ['UID']
summaryDict = dataMachete.createDictDB({},summaryKeyVarnames,typedsummarylist)

#Get ANALYSIS dictionary 
analdict = dataMachete.getDataDictionary(mratDiscrimdataFilePath, 'ANALDICT')
#Get ANALYSIS
table_name = 'ANALYSIS_MUNICIPAL'
analysisList = dataMachete.getListarray(mratDiscrimdataFilePath,table_name)
typedanalysisList = dataMachete.typeDataset(analysisList,analdict,table_name, errorFilePath)
#Notes
#Original ANALYSIS.txt (Ian) did not have DRUID; and Removed variables with 0 Variation.
#Analysis.txt created by join on claims and insfraxtructure data -- Does have these
#These must be manually added to analdict:DRUID, AGE_COM0,AGE_SAN0, AGE_STR0
#DIA_COM0, DIA_SAN0, DIA_STR0, PCNT_AGR
analysisHeader = analysisList[0]
analysisKeyVarnames = ['UID']
analysisDict = dataMachete.createDictDB({},analysisKeyVarnames,typedanalysisList)
analysisDictUidList = analysisDict.keys()
analysisDictUidList.sort()

print '\n'
print 'DISCRIMINANT SCORES PROCESSING'

print 'STEP 1 DONE: Data and Metadata Loaded'

#Get Discriminant Aanlysis Z-score Parameter File
table_name = 'PARAM'
parameterList = dataMachete.getListarray(mratDiscrimdataFilePath,table_name)
typedparameterList = dataMachete.typeDataset(parameterList,analdict,table_name, errorFilePath)
parameterHeader = parameterList[0]
parameterKeyVarnames = ['EQUATION', 'PARAMNAME']
parameterDict = dataMachete.createDictDB({},parameterKeyVarnames,typedparameterList)
#paramNameList = parameterDict['EL6YT2YN'].keys() -- does not mattch PARAM.txt for Moncton
# Change so uses key fro param file
paramNameList = parameterDict['EL6YT1YN'].keys()
paramNameList.sort()
end_i = len(paramNameList)
paramValueList = []
paramAttrList = []
for parameter in paramNameList:
        if parameter == 'CONSTANT':
            paramValue = 0
        else:
            paramValue = parameterDict['EL6YT1YN'][parameter]['PARAMVALUE']
        paramValueList.append(paramValue)
        paramAttrList.append(parameterDict['EL6YT1YN'][parameter]['ATTR'])

#Compute Z-Scores for each analysisDict UID
zScoreDict = {}
uniqueZScoreDict = {}
minZScore = 9999
maxZScore = -9999
for uid in analysisDictUidList:
    zValue = 0
    #Caclulate some new variables from existing variables
    '''pcnt_r2 = analysisDict[uid]['PCNT_R2']
    pcnt_r3 = analysisDict[uid]['PCNT_R3']
    pcnt_r4 = analysisDict[uid]['PCNT_R4']
    #These have to be calculated manually per city -- or new process
    pcnt_com = analysisDict[uid]['PCNT_COM']
    pcnt_ins = analysisDict[uid]['PCNT_INS']
    pcnt_off = analysisDict[uid]['PCNT_OFF']
    pcnt_cio = pcnt_com + pcnt_ins + pcnt_off
    #end of manual additon of new variables to code
    pcnt_r234 = pcnt_r2 + pcnt_r3 + pcnt_r4'''
    #Calculate zScore always where low (negative) values represent low risk
    #and high (positive) values represent high risk.
    for i in range(0,end_i,1):
        paramName = paramNameList[i]
        paramAttr = paramAttrList[i]
        paramValue = paramValueList[i]
        if paramName == 'CONSTANT':
            zValue = zValue + paramValue
        else:
            '''if paramAttr == 'PCNT_CIO':
                zValue = zValue + paramValue * pcnt_cio
            else:'''
            attrValue = analysisDict[uid][paramAttr]
            zValue = zValue + paramValue * attrValue    
    #Keep zScores associated with each uid    
    zScoreDict.update({uid:{'ZSCORE':zValue}})
    #Keep track of all unique zScoreValues
    if not uniqueZScoreDict.has_key(zValue):
        uniqueZScoreDict.update({zValue:{'N':0}})
    uniqueZScoreDict[zValue]['N'] = uniqueZScoreDict[zValue]['N'] + 1
    #Track minimum and maximum ZScores
    if zValue > maxZScore:
        maxZScore = zValue
    if zValue < minZScore:
        minZScore = zValue

print 'Statistics related to original ZScore calculations using reference data' 
print 'maxZScore', maxZScore, 'minZScore', minZScore

#Compute unique z-score rank values
uniqueZScoreDictKeyList = uniqueZScoreDict.keys()
uniqueZScoreDictKeyList.sort()
totalRank = 0
for uniqueZScore in uniqueZScoreDictKeyList:
    nObs = uniqueZScoreDict[uniqueZScore]['N']
    if nObs > 1:
        uniqueZScoreDict[uniqueZScore].update({'RANK':float(totalRank + nObs/float(2))})
    else:
        uniqueZScoreDict[uniqueZScore].update({'RANK':float(totalRank + nObs)})
    totalRank = totalRank + nObs
    #print totalRank
#print 'totalRank', totalRank
#Adjust totalRank so that pRank (below) is always < 1
totalRank = totalRank + 1

maxRefZScore = maxZScore + 0.001
minRefZScore = minZScore - 0.001
print 'Adjusted maximum and minimum ZScores to ensure 0 < ZTRANS < 1'
print 'Maximum reference ZScore', maxRefZScore
print 'Minimum reference ZScore', minRefZScore

#Transform unique z-score rank values to numbers between 0 and 1
#Also calculate ztrans to transform ZScore to a number between 0 and 1
for uniqueZScore in uniqueZScoreDictKeyList:
    pRank = uniqueZScoreDict[uniqueZScore]['RANK']/float(totalRank)
    odds = pRank/float(1-pRank)
    if odds <= 0: print odds
    lodds = log(odds)
    ztrans = (uniqueZScore - minRefZScore)/float(maxRefZScore-minRefZScore)
    #print uniqueZScore, ztrans
    uniqueZScoreDict[uniqueZScore].update({'pRANK':pRank,'ODDS':odds,'LODDS':lodds, 'ZTRANS':ztrans})
    

print 'STEP 2 DONE: Zscores and ZTRANS and LODDS calculated'

#Construct x and y vectors
x = []
y = []
for uniqueZScore in uniqueZScoreDictKeyList:
        pRank = uniqueZScoreDict[uniqueZScore]['pRANK']
        #Limit pRank range to remove outliers and
        #restrict analysis to most linear part
        #of LODDS versus log ZTRANS
        minpRank = 0.1
        maxpRank = 0.9
        if pRank >= minpRank and maxpRank <= maxpRank:
                xValue = log(uniqueZScoreDict[uniqueZScore]['ZTRANS'])
                yValue = uniqueZScoreDict[uniqueZScore]['LODDS']
                x.append(xValue)
                y.append(yValue)
                
#Calculate and report some summary statistics
minZtrans = exp(min(x))
maxZtrans = exp(max(x))
minLodds = exp(min(y))
maxLodds = exp(max(y))
print 'LODDS vs. log(ZTRANS) Regression Analysis'
print 'Minimum pRank', minpRank
print 'Maximum pRank', maxpRank
print 'Minimum ZTRANS', minZtrans
print 'Maximum ZTRANS', maxZtrans
print 'Minimum ODDS', minLodds
print 'Maximum ODDS', maxLodds

#Plot the observed LODDS vs. Log ZTRANS
#For range indicated above
plt.scatter(x,y)
plt.xlabel('log ZTRANS')
plt.ylabel ('log ODDS')
plt.show()

#Complete linear regression
#Note the only reason to do this is to enable a shift in the
#distribution of damage with respect to ZTRANS given a change in IDF;
#this could also be accomplished by shifting the median ZTRANS to
#the left in proportion to an increase in rainfall
#or to the right in proportion to a decrease in rainfall.
#Otherwise nearest neighbour (upper and lower bound) could be used
#estimate the odds statistics based on the actual distribution
#of DRUID-MONTH claims in the dataset.  The nearest neighbour concept
#would also make sure that more than Z-value was taken into account
#by matching DRUIDS with claims to DRUIDS without claims based on
#a weighting of the attributes in accordance with the Discriminant
#Analysis. Nearest neighbour analysis would allow units without claims
#to inherint the claims record associated with nearest neighbours with
#claims.  This would also allow units with a short record of claims
#to inherit a longer term record.
#
#Complete linear regression: LODDS vs. Log ZTRANS for indicated range
slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
print 'Slope Coefficient:', slope
print 'Intercept:', intercept
print 'Rsq:', r_value**2
print 'p Value:', p_value
print 'Standard Error:', std_err

#Create a XAYA format graph of coefficients required for IDF based forecasting
idfcoeffDict = {'Slope Coefficient': [slope],
                'Intercept': [intercept],
                'Rsq': [r_value**2],
                'p Value': [p_value],
                'Standard Error': [std_err]}
                
#Write idfcoeffDict to file
miniGraph.writeGraph(graph=idfcoeffDict, filepath=mratDiscrimdataFilePath + 'IDFCoefficients.txt')

#Get residuals
residuals = []
predictedY = []
end_i = len(x)
for i in range(0,end_i,1):
        predY = intercept + slope * x[i]
        predictedY.append(predY)
        yValue = y[i]
        resid = predY - yValue
        residuals.append(resid)
#Plot residuals
plt.scatter(x, residuals)
plt.xlabel('log ZTRANS')
plt.ylabel ('Residual: Predicted minus Observed Log ODDS')
plt.show()
#Plot predicted versus actual Y
plt.scatter(y, predictedY)
plt.xlabel('Observed Log ODDS')
plt.ylabel ('Predicted Log ODDS')
plt.show()

print 'STEP 3 DONE: Log Odds model fit to data; residuals calculated and plotted; p (ratings) calculated'


#Write statistics to UID's in SUMMARY for mapping purposes
summaryUidList = summaryDict.keys()
summaryUidList.sort()
end_i = len(paramNameList)
sumZDict = {}
sumZHeader = ['UID']
sumZKeyVarnames = ['UID']
for i in range(0,end_i,1):
        paramName = paramNameList[i]
        if not paramName == 'CONSTANT':
                sumZHeader.append(paramAttrList[i])
newVar = ['ZSCORE','ZTRANS','ODDS', 'p']
for item in newVar:
        sumZHeader.append(item)
#Initialize SUMZ file
printSumZFilepath = mratDiscrimdataFilePath + 'SUMZ.txt'
dataMachete.initializeVariableHeader(sumZHeader,printSumZFilepath)
for uid in summaryUidList:
        sumZDict.update({uid:{}})
        zValue = 0
        #Caclulate some new variables from existing variables
        '''pcnt_r2 = summaryDict[uid]['PCNT_R2']
        pcnt_r3 = summaryDict[uid]['PCNT_R3']
        pcnt_r4 = summaryDict[uid]['PCNT_R4']
        pcnt_r234 = pcnt_r2 + pcnt_r3 + pcnt_r4
        pcnt_com = summaryDict[uid]['PCNT_COM']
        pcnt_ins = summaryDict[uid]['PCNT_INS']
        pcnt_off = summaryDict[uid]['PCNT_OFF']
        pcnt_cio = pcnt_com + pcnt_off + pcnt_ins'''
        #Calculate zScore always where low (negative) values represent low risk
        #and high (positive) values represent high risk.
        for i in range(0,end_i,1):
                paramName = paramNameList[i]
                paramAttr = paramAttrList[i]
                paramValue = paramValueList[i]
                if paramName == 'CONSTANT':
                    zValue = zValue + paramValue
                
                else:
                    '''if paramAttr == 'PCNT_CIO':
                        sumZDict[uid].update({'PCNT_CIO':pcnt_cio})
                        zValue = zValue + paramValue * pcnt_cio
                    
                    else:'''
                    attrValue = summaryDict[uid][paramAttr]
                    sumZDict[uid].update({paramAttr:attrValue})
                    zValue = zValue + paramValue * attrValue    
        #Keep zScores associated with each uid
        #Ensue that zValue is within range
        if zValue < minZScore:
                zValue = minZScore
        if ztrans > maxZScore:
                zValue = maxZScore
        ztrans = (zValue - minRefZScore)/float(maxRefZScore-minRefZScore)
        logZtrans = log(ztrans)
        lodds = intercept + slope * logZtrans
        oddsRatio = exp(lodds)
        p = oddsRatio/(1 + oddsRatio)
        sumZDict[uid].update({'ZSCORE':zValue, 'ZTRANS':ztrans, 'ODDS':oddsRatio, 'p':p})
#Graph distribution of uid's by p-values (bar chart)
dataMachete.saveDictDB(sumZKeyVarnames,sumZHeader,sumZDict, printSumZFilepath)                
print 'Done'


print 'STEP 4 DONE: Mapping Data Written to File SUMZ.txt'

# NOTES FROM IAN SESSIONS  
#NOTES ON MANUAL POINTS IN ORIGINAL RATINGS GENERTION TH#
# 1: NEED A ROUTINE TO APPEND ALL CALCULATED VARIABLES TO A DATA SET     
    #QUESTION: DO WE EVEN NEED TO DO THIS FROM AN AUTOMATED VARIE SELN STANDPOINT  
# 2: WE NEED AN ANALYSIS DATA DICTIONARY WITH ALL THE VARIABES IN IT
# 3 WE NEED A PROCEDURE TO CHECK FOR CORRELATD VARIBLES -- CAN MODIFY FROM LVI PROCEDURE (R CODE) 
    # IAN'S NEW IDEA ON HOW TO DO THIS:
        # HASTIE'S SUGGESTION -- REGRESS EACH X ON THE REMAINING X
        # REMOVE THOSE X VARIABLES THAT ARE LARELY EXPLAIED (ABOVE A THRESHOLD R-SQUARED)
        #IAN'S VERSION:
                # 1. USE ANOVA ETA-SQUARED  (OR F TEST) TO RANK VARIABLES
                #2 START AT LOWEST RANKED VARIABLE (LEAST DISTINGUISHER)
                #3. RUN THROUGH THE REGRESIONS IN THAT ORDDER.
                
# WE NEED TO WRITE SOME MOREFO TO FILE:(can use ASAPLOT)
    # SLOPE
    # INTCPT
    # RSQ
    # P VALUE
    # STANDAD ERROR
# DONE -- WRITTEN TO IDFCoefficients.txt
    
    






