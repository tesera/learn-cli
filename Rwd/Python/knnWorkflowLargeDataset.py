'''
Reference and target data sets must have unique keys
'''

import sys
sys.path.append('D:\\Rwd\\Python\\Admin')
#import RESET_SYS_PATH
import miniApp
import dataMachete
import asaKnn
#import miniCli
import copy
import time

configName = 'knnConfigLdata.txt'
configInfoName = 'knnConfigLdataInfo.txt'
configdefpath = '/Rwd/Python/Config/'
configaltpath = '/Users/Maxine/Documents/TSIAnalytics/Config/'
pathkeyslist = ['dataInPath','dataDictPath','dataOutPath', 'errorDiagnosticPath']
configKeyList = ['knnTargRefDataDictionary','normalizeFlag','kNearestNeighbours','dfuncVarSetList','useDfuncVarCoef']
#config = miniCli.getConfig(configName, configdefpath, configaltpath, pathkeyslist, configKeyList, configInfoName)
config = miniApp.getConfig(configName, configdefpath, configaltpath, pathkeyslist)
dataInPath = config['dataInPath'][0]
dataDictPath = config['dataDictPath'][0]
dataOutPath = config['dataOutPath'][0]
errorDiagnosticPath = config['errorDiagnosticPath'][0]
refDataTableName = config['knnReferenceData'][0]
refKeyVarNames = config['refKeyVarNames']
targDataTableName = config['knnTargetData'][0]
targKeyVarNames = config['targKeyVarNames']
knnLviDict = config['knnLviDataDictionary'][0]  #Contains dictionary information on DFUNCT 
knnTargRefDataDictionary = config['knnTargRefDataDictionary'][0]  #Contains information on target and reference datasets
#Discriminant function table for multiple variable selection
dfuncTableName = config['knnDFuncTableName'][0]
dfuncKeyVarNames = config['dfuncKeyVarNames']
xVarSelectTableName = config['xVarSelectTableName'][0]
xVarKeyVarNames = config['xVarSelectKeyVarNames']
#k number of nearest neighbours selected
kNearestNeighbours = int(config['kNearestNeighbours'][0])
eps = float(config['eps'][0])
minkowski = int(config['minkowski'][0])
#Normalize Data - Yes or No
normalizeFlag = config['normalizeFlag'][0]
#Variable set selections (from dfunctTableName) 
dfuncVarSetList = config['dfuncVarSetList']
useDfuncVarCoef = config['useDfuncVarCoef'][0]
#Number of lines to read in large datasets
largeDatasetReadLines = int(config['largeDatasetReadLines'][0])
#Print mutliple files - YES or NO
printMultipleFiles = config['printMultipleFiles'][0]

#Open LVI Dictionary for DFUNCT.csv and XVARSELV1.csv
originalDict = {}
newDict = {}
#Open reference DATA Dictionary; if empy then infer dataDictionary
dictionaryFlag = False
printTypes = 'YES'
if not knnTargRefDataDictionary == '' and not dataDictPath == '':
    dictionaryFlag = True
    originalDict, newDict = dataMachete.getDatamacheteDictionary(dataDictPath, knnTargRefDataDictionary, '')
    tableNameInDict = dataMachete.checkIfTableNameInDictionary(refDataTableName, originalDict)
    if tableNameInDict == False:
        originalDict, newDict = dataMachete.inferDataDictionary_v2(refDataTableName, dataInPath, '', printTypes, largeDatasetReadLines)
else:
    originalDict, newDict = dataMachete.inferDataDictionary_v2(refDataTableName, dataInPath, '', printTypes, largeDatasetReadLines)

#Open target DATA Dictionary; if empty then infer dataDictionary
if dictionaryFlag == True:
    oldDictTarg = originalDict
    newDictTarg = newDict
    tableNameInDict = dataMachete.checkIfTableNameInDictionary(targDataTableName, originalDict)
    if tableNameInDict == False:
        oldDictTarg, newDictTarg = dataMachete.inferDataDictionary_v2(targDataTableName, dataInPath, '', printTypes, largeDatasetReadLines)
else:
    oldDictTarg, newDictTarg = dataMachete.inferDataDictionary_v2(targDataTableName, dataInPath, '', printTypes, largeDatasetReadLines)

#Open reference dataset (entire dataset to be held in memory)
readErrorFileName = 'ERROR_REF'
dataFileExtension = ''
readErrorExtension = '.txt'
refTypedList = dataMachete.getTypedListArray_v2(originalDict, refDataTableName, dataInPath, dataFileExtension, \
                      readErrorFileName, errorDiagnosticPath, readErrorExtension)

#
#Extract the list of unique ID's for each of the referenece datasets 
keyRefValueList = asaKnn.getSelectedVariableSet(refKeyVarNames, refTypedList)

if not '-1' in dfuncVarSetList:
    #DFUNCT.csv is the file that contains the X-variable names and the variable coefficients
    originalDict = {}
    newDict = {}
    #READ DFUNCT variable and coefficient sets and put them in a python dictionary format
    if dictionaryFlag == True: 
        tableNameInDict = dataMachete.checkIfTableNameInDictionary(dfuncTableName, originalDict)
        if tableNameInDict == False:
            originalDict, newDict = dataMachete.inferDataDictionary_v2(dfuncTableName, dataOutPath, '', printTypes, -1)
    else:
        originalDict, newDict = dataMachete.inferDataDictionary_v2(dfuncTableName,dataOutPath, 'YES', -1)
    dfuncTypedDict = asaKnn.readDFUNCTFile(dfuncTableName, dataOutPath, errorDiagnosticPath, dfuncKeyVarNames,\
                                 originalDict, newDict, '')
    if '-99' in dfuncVarSetList:
        dfuncVarSetList = dfuncTypedDict.keys()
        dfuncVarSetList.sort()
    
        print '\n All variable sets in dfuncVarSetList have been selected for nearest neighbour assignements'
    nVariableSets = len(dfuncVarSetList)
    print '\n There are: ',nVariableSets,' sets of variables to be processed'

    #For each variable set
    printFlag = True
    for varSet in dfuncVarSetList:
        #Start reading target dataset here
        #Initialize large dataset processing
        startReadLine = 0
        endOfFile = False
        batch = 0
        nnCount = 0
        while endOfFile == False:
            batch = batch + 1
            print ' Start processing varSet', varSet, 'batch number:', batch, startReadLine, nnCount, time.ctime()
            endReadLine = startReadLine + largeDatasetReadLines
            targTypedList = dataMachete.getLargeDatasetListArrayAndDictDB_v2(targDataTableName, dataInPath, \
                        errorDiagnosticPath, targKeyVarNames, oldDictTarg, newDictTarg, dataFileExtension,
                        printTypes, startReadLine, endReadLine, True, False)
            keyTargValueList = asaKnn.getSelectedVariableSet(targKeyVarNames, targTypedList)
            targLineCount = len(keyTargValueList)
            if targLineCount == 1:
                break
            else:
                if targLineCount < largeDatasetReadLines-1:
                    endOfFile = True
            knnComboList = asaKnn.getkNNUsingDiscriminantFunctions(varSet, dfuncTypedDict, keyRefValueList,keyTargValueList, \
                                                               refTypedList, targTypedList, kNearestNeighbours, \
                                                               eps, minkowski, useDfuncVarCoef, normalizeFlag)
            nnCount = nnCount + len(knnComboList)
            if printMultipleFiles == 'YES' or \
               printMultipleFiles == 'Yes' or \
               printMultipleFiles == 'yes' or \
               printMultipleFiles == 'Y' or \
               printMultipleFiles == 'y':              
                knnComboFileName = 'NN' + str(varSet)
                if batch == 1:
                    dataMachete.writeListarrayToCSVFile_v2(knnComboList, dataOutPath, knnComboFileName, '%0.9f', '.csv', True, True)
                else:
                    dataMachete.writeListarrayToCSVFile_v2(knnComboList, dataOutPath, knnComboFileName, '%0.9f', '.csv', False, False)
            else:
                knnComboFileName = 'NN0'
                if printFlag == True:
                    dataMachete.writeListarrayToCSVFile_v2(knnComboList, dataOutPath, knnComboFileName, '%0.9f', '.csv', True, True)
                    printFlag = False
                else:
                    dataMachete.writeListarrayToCSVFile_v2(knnComboList, dataOutPath, knnComboFileName, '%0.9f', '.csv', False, False)
            startReadLine = endReadLine
else:
    #XVARSELV1.csv is the file to be used to select the X-Variable dataset
    originalDict = {}
    newDict = {}
    if dictionaryFlag == True:
        tableNameInDict = dataMachete.checkIfTableNameInDictionary(xVarSelectTableName, originalDict)
        if tableNameInDict == False:
            originalDict, newDict = dataMachete.inferDataDictionary_v2(dfuncTableName, dataOutPath, '', printTypes, -1)
    else:
        originalDict, newDict = dataMachete.inferDataDictionary_v2(xVarSelectTableName,dataInPath, printTypes = 'YES', nLines = -1)
    #Read XVARSELV1.csv
    xvarselvTypedList = asaKnn.readXVARSELV1File(xVarSelectTableName, dataInPath, errorDiagnosticPath, xVarKeyVarNames,\
                                 originalDict={}, newDict={}, fileExtension='.txt')
    #Star looping
    #Start reading target dataset here
    #Initialize large dataset processing
    startReadLine = 0
    endOfFile = False
    batch = 0
    nnCount = 0
    while endOfFile == False:
        batch = batch + 1
        print ' Start processing batch number:', batch, startReadLineLeft, nnCount, time.ctime()
        endReadLine = startReadLine + largeDatasetReadLines
        targTypedList = dataMachete.getLargeDatasetListArrayAndDictDB_v2(targDataTableName, dataInPath, \
                        errorDiagnosticPath, targKeyVarNames, oldDictTarg, newDictTarg, dataFileExtension,
                        printTypes, startReadLine, endReadLine, True, False)
        keyTargValueList = asaKnn.getSelectedVariableSet(targKeyVarNames, targTypedList)
        targLineCount = len(keyTargValueList)
        if targLineCount == 1:
            break
        else:
            if targLineCount < largeDatasetReadLines-1:
                endOfFile = True
        knnComboList = asaKnn.getkNNUsingXVARSELV1(xvarselvTypedList, keyRefValueList,keyTargValueList, \
                                     refTypedList, targTypedList, kNearestNeighbours,  \
                                     eps, minkowski, normalizeFlag)
        nnCount = nnCount + len(knnComboList)
        knnComboFileName = 'NN0'
        if batch == 1:
            dataMachete.writeListarrayToCSVFile_v2(knnComboList, dataOutPath, knnComboFileName, '%0.6f', '.csv', True, True)
        else:
            dataMachete.writeListarrayToCSVFile_v2(knnComboList, dataOutPath, knnComboFileName, '%0.6f', '.csv', False, False)
        startReadLine = endReadLine
    
print '\n TARGET NEAREST NEIGHBOUR ANALYSIS COMPLETED'

raw_input(" Press Enter to Close This Session ... ")  
        
