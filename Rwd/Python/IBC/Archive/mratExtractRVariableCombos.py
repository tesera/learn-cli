'''
This modeule identifies the unique variable sets and organizes them into
a new file VARSELV.csv; The purpose of this file is to allow
for all of the unique variable selection models to be processed
using discriminant analysis for comparison purposes.

Another file, UNIQUEVAR.csv provides a list of all of the variables
referred to in VARSELV.csv 
'''
import sys
import dataMachete
import miniGraph

print 'Extract R Variable Combinations from Discriminant Aanlysis'

#Identify code directory and data directory
#adminFilePath = 'D:\\Rwd\\Python\\Admin\\'
#inputDataPath = 'D:\\Rwd\\'
#dictFilePath = 'D:\\Rwd\\Python\\DATDICT\\'
#filePathReadError = 'D:\\Rwd\\Python\\PyReadError\\'
#sys.path.append(adminFilePath)
#sys.path.append(inputDataPath)

#Set paths to config file
defaultconfigFilePath = '/apps/TSIAnalytics/Config/mratConfig.txt' #Default Path
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
mratAutovarSelectFilePath = mratConfig['mratAutovarSelectFilePath'][0]
printFilePath = mratAutovarSelectFilePath + 'XVARSELV.csv'
printFilePath2 = mratAutovarSelectFilePath + 'UNIQUEVAR.csv'


sys.path.append(mratAutovarSelectFilePath)

#import makeDD
#$import PRINTv1
#import readCSV
#import typeDataset
#import dictionaryDBUtilities

#Get data dictionary to identify variables and variable types
#filename = 'PyRDataDict'
#fileExtension = '.csv'
#originalDict, newDict = makeDD.dataDictionaryType_21(dictFilePath,filename, fileExtension)

#Get R output file: XVARSELECT 
varSelTableName = 'VARSELECT'
oldDict, newDict = dataMachete.inferDataDictionary_v2(varSelTableName, mratAutovarSelectFilePath, '.csv', 'YES', -1)
varSelErrorFilePath =  mratAutovarSelectFilePath + 'ERROR-CHECK-VARSELECT.txt'
varSelKeyVarnames = ['MODELID','VARNUM']
fileExtension = '.csv'
varSelStringList = dataMachete.getListarray_v2(mratAutovarSelectFilePath, varSelTableName, fileExtension)
varSelTypedList = dataMachete.typeDataset_v2(varSelStringList, oldDict, varSelTableName, varSelErrorFilePath)

#Create CTABSUM data dictionary
varSelDict = {}
varSelHeader = varSelTypedList[0]
varSelDict = dataMachete.createDictDB(varSelDict,varSelKeyVarnames,varSelTypedList)
#
#Get ModelId key list and then sort it
varSelModelIdKeyList = varSelDict.keys()
varSelModelIdKeyList.sort()
#
#Get maximum number of variables 
maxN = 0
for modelId in varSelDict:
    nCount = 0
    for varNum in varSelDict[modelId]:
        nCount = nCount + 1
    if nCount > maxN:
        maxN = nCount

#Create newDictHeader
newDictHeader = ['VARSET','MODELID','NMODELS','NVAR']
newDictKeyList = ['VARSET']

#Initialize the list of unique variable names
uniqueVarList = []

#Use maxN to cretate new Header
for i in range(0, maxN, 1):
    newVarName = 'XVAR' + str(i+1)
    newDictHeader.append(newVarName)

#Initialize a list of unique newModelLists
newModelLists = []
#Initialize a list of former modelId's for reference
newModelIdList = []
#Get length of varSelModelIdKeyList
end_i = len(varSelModelIdKeyList)

for i in range(0,end_i,1):
    modelId = varSelModelIdKeyList[i]
    modelVarNames = []
    #Compile modelVarNames for current modelId
    for varNum in varSelDict[modelId]:
        varName = varSelDict[modelId][varNum]['VARNAME']
        modelVarNames.append(varName)
        #If varName not in unique variable name list - add to list
        if not varName in uniqueVarList:
            uniqueVarList.append(varName)
            
    modelVarNames.sort()
    #Check to see if variable name combination already exitss
    #If it does not exist then add it to newModelLists and record modelId in newModelIdList
    #Set default to False: No match is found between modelVarNames and the list of each model varnames in newModelLists
    flag = False
    end_j = len(newModelLists)
    for j in range(0,end_j,1):
        if modelVarNames == newModelLists[j]:
            flag = True
            newModelIdList[j][1] = newModelIdList[j][1] + 1
            break
    if flag == False:
        newModelLists.append([])
        #Add modelVarNames to
        end_k = len(newModelLists)
        end_l = len(modelVarNames)
        #Update newModelIdList with modelId, number of the same models, number of variables
        newModelIdList.append([modelId,1, end_l])
        #Add the new model name set, modelVarNames to newModelLists
        for l in range(0,end_l,1):
            newVar = modelVarNames[l]
            newModelLists[end_k-1].append(newVar)
                
#Create newDict
newDict = {}
end_i = len(newModelIdList)
end_j = len(newDictHeader)

for i in range(0,end_i,1):
    newDict.update({i+1:{}})
    modelId = newModelIdList[i][0]
    nModels = newModelIdList[i][1]
    nVar = newModelIdList[i][2]
    newDict[i+1].update({'MODELID':modelId,'NMODELS':nModels,'NVAR':nVar})
    end_k = len(newModelLists[i])
    #Get variable names for the current modelId and add them to the dictionary
    for k in range(0,end_k,1):
        varName = newModelLists[i][k]
        varLabel = 'XVAR' + str(k+1)
        newDict[i+1].update({varLabel:varName})
    #Assign 'N' to the remaining variables up to the maximum number oif variables
    for j in range(end_k,maxN,1):
        varName = 'N'
        varLabel = 'XVAR' + str(j+1)
        newDict[i+1].update({varLabel:varName})
            
dataMachete.initializeVariableHeader(newDictHeader,printFilePath)
dataMachete.saveDictDB(newDictKeyList,newDictHeader,newDict, printFilePath)       
            
#create unique varName dictionary
uniqueDict = {1:{}}
uniqueDictHeader = ['MYID',]
uniqueDictKeyList = ['MYID']
uniqueVarList.sort()
end_i = len(uniqueVarList)
for i in range(0,end_i,1):
    newVarName = 'X' + str(i+1)
    varValue = uniqueVarList[i]
    uniqueDict[1].update({newVarName:varValue})
    uniqueDictHeader.append(newVarName)
#    
dataMachete.initializeVariableHeader(uniqueDictHeader,printFilePath2)
dataMachete.saveDictDB(uniqueDictKeyList,uniqueDictHeader,uniqueDict, printFilePath2)       

print ' Two new csv files created: XVARSELV and UNIQUEVAR'
print '\n XVARSELV contains a list of all of the models, each with unique variable combinations within a variable set'
print '\n UNIQUEVAR contains a list of unique variable names used across all models'
                
#raw_input("\n Press ENTER to Close This Session ... ")         
    
    
    
        
    
