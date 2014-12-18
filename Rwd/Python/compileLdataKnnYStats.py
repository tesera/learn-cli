'''
Reference and target data sets must have unique keys.
See asaKnn.compileNearestNeighbourStatistics() for details
regarding the use of this application.

'''
import sys
sys.path.append('D:\\Rwd\\Python\\Admin')

import miniApp
import dataMachete
import asaKnn
#import miniCli
import copy
import time

configName = 'knnYStatsConfig.txt'
configInfoName = 'knnYStatsConfigInfo.txt'
configdefpath = '/Tesera/Rwd/Python/Config/'
configaltpath = '/Users/Maxine/Documents/TSIAnalytics/Config/'
pathkeyslist = ['dataInPath','dataDictPath','dataOutPath', 'errorDiagnosticPath']
configKeyList = ['knnRefData','refKeyVarName','knnData','varSelectIndicator']
#config = miniCli.getConfig(configName, configdefpath, configaltpath, pathkeyslist, configKeyList, configInfoName)
config = miniApp.getConfig(configName, configdefpath, configaltpath, pathkeyslist)
dataInPath = config['dataInPath'][0]
dataDictPath = config['dataDictPath'][0]
dataDictTableName = config['dataDictTableName'][0]
dataOutPath = config['dataOutPath'][0]
errorDiagnosticPath = config['errorDiagnosticPath'][0]
refDataTableName = config['knnReferenceData'][0]
refKeyVarNames = config['refKeyVarNames']
knnTableNameList = config['knnTableNameList']
knnKeyVarNameList = config['knnKeyVarNameList']
knnMax = int(config['knnMax'][0])
varSelectTableName = config['varSelectTableName'][0]
varSelectKeyVarNames = config['varSelectKeyVarNames']
varSelectIndicator = config['varSelectIndicator'][0]
largeDatasetReadLines = int(config['largeDatasetReadLines'][0])
distanceWeight = float(config['distanceWeight'][0])
#note that we need a variable type for typing list ofExcludedValues and for
#data typing using data dictionary; never thought about this before
listOfExcludedValues = dataMachete.convert1DListofItemsUsingDynamicTyping(config['listOfExcludedValues'])
minIncludeValue = dataMachete.convertTypeUsingDynamicTyping(config['minIncludeValue'][0])
maxIncludeValue = dataMachete.convertTypeUsingDynamicTyping(config['maxIncludeValue'][0])                       
printTypes = config['printTypes'][0]
knnStatsOutputTableName = config['knnStatsOutputTableName'][0]
outputMean = config['outputMean'][0]
outputStdev = config['outputStdev'][0]
#
#Open reference DATA Dictionary; if empy then infer dataDictionary
dictionaryFlag = False
if not dataDictTableName == '' and not dataDictPath == '':
    dictionaryFlag = True
    origDictRefData, newDictRefData = dataMachete.getDatamacheteDictionary(dataDictPath, dataDictTableName, '')
    tableNameInDict = dataMachete.checkIfTableNameInDictionary(refDataTableName, originalDict)
    #tableNameDict equals False if table name not found in dictionary
    if tableNameInDict == False:
        origDictRefData, newDictRefData = dataMachete.inferDataDictionary_v2(refDataTableName, dataInPath, '', printTypes, largeDatasetReadLines)
else:
    origDictRefData, newDictRefData = dataMachete.inferDataDictionary_v2(refDataTableName, dataInPath, '', printTypes, largeDatasetReadLines)

#Open knnData Dictionary; if empty then infer dataDictionary
knnData = knnTableNameList[0]
if dictionaryFlag == True:
    oldDictKnnData = originalDict
    newDictKnnData = newDict
    tableNameInDict = dataMachete.checkIfTableNameInDictionary(knnData, originalDict)
    if tableNameInDict == False:
        oldDictKnnData, newDictKnnData = dataMachete.inferDataDictionary_v2(knnData, dataInPath, '', printTypes, largeDatasetReadLines)
else:
    oldDictKnnData, newDictKnnData = dataMachete.inferDataDictionary_v2(knnData, dataInPath, '', printTypes, largeDatasetReadLines)

#Open the X or Y variable selection dataset XVARSELV1
varOldDict, varNewDict = dataMachete.inferDataDictionary_v2(varSelectTableName, dataInPath, '.csv', printTypes, -1 )
readErrorFileName = 'ERROR_' + varSelectTableName
varSelTypedList = dataMachete.getTypedListArray(varNewDict, varSelectTableName, dataInPath,'.csv', readErrorFileName, \
                                              dataInPath, '.txt')

#Identify variable names in varSelTypedList according to those that meet the varSelCriteria
varSelList = miniApp.selectAnalysisVariables(varSelectIndicator, varSelTypedList)

#Read reference dataset
refTableNameList = refDataTableName.split('.')
readErrorFileName = 'ERROR_' + refTableNameList[0] 
dataFileExtension = ''
readErrorExtension = '.txt'

#Get number of line in reference file
nRefLines = dataMachete.countNumberOfLinesInFile(dataInPath,refDataTableName,dataFileExtension)
print '\n There are:', nRefLines, 'records in the following reference dataset:', refDataTableName

#Load entire reference dataset into memory
fromLine = 0
toLine = nRefLines + 1
returnList = True
returnDict = False
returnHeader = False
refDataTypedList = dataMachete.getLargeDatasetListArrayAndDictDB_v2(refDataTableName, dataInPath, errorDiagnosticPath, refKeyVarNames, \
                          origDictRefData, newDictRefData, dataFileExtension, printTypes, fromLine, toLine, \
                            returnList, returnDict, returnHeader)

#Extract key Values (references to each observation) in one dataList and associated selected variable values in a separate list
#in order or 
subsetIntegrity = True
uniqueSubset = True
uniqueCompleteSet = True
printDiagnostics = True
refKeyValueList, refSelValueList = dataMachete.createNewListFromSelectVariableListAndIdList(refKeyVarNames, varSelList, refDataTypedList, \
                                                 subsetIntegrity, uniqueSubset, uniqueCompleteSet, printDiagnostics)

#Initialize Stats Header
#Add key variable names from knnKeyVarNameList usually containg TARGOBS and VARSET 
statsHeader = dataMachete.join1DListBToRightOf1DListA(['UID'],knnKeyVarNameList)
#Append column name containing number of nearest neighbours
statsHeader = dataMachete.join1DListBToRightOf1DListA(statsHeader,['KNN','STAT'])
#Append columns with variable names
statsHeader = dataMachete.join1DListBToRightOf1DListA(statsHeader,varSelList)
#Start looping
#Start reading target dataset here
#Initialize large dataset processing
#Turn of printTypes
printTypes = 'NO'
for knnTableName in knnTableNameList:
    print ' Start processing knnTableName:', knnTableName
    errorDiagnosticPath = 'ERROR_' + knnTableName
    fileNameList = knnTableName.split('.')
    printFileName = fileNameList[0] + '_' + knnStatsOutputTableName
    startReadLine = 0
    endOfFile = False
    batch = 0
    while endOfFile == False:
        batch = batch + 1
        print ' Start processing batch number:', batch, 'startReadLine:', startReadLine, time.ctime()
        endReadLine = startReadLine + largeDatasetReadLines
        knnTypedList = dataMachete.getLargeDatasetListArrayAndDictDB_v2(knnTableName, dataInPath, \
                        errorDiagnosticPath, knnKeyVarNameList, oldDictKnnData, newDictKnnData, dataFileExtension,
                        printTypes, startReadLine, endReadLine, True, False, False)

        #Check for end of file
        knnLineCount = len(knnTypedList)
        if knnLineCount == 1:
            break
        else:
            if knnLineCount < largeDatasetReadLines-1:
                endOfFile = True

        #Get knn Variable Selection Lists (nn IDS and associated Distances)
        knnNameList, knnDistNameList = asaKnn.compileKnnVariableSelectionLists(knnMax, knnTypedList[0])    
        #Extract key Values (references to each observation) in one dataList and associated list of nearest neighbour reference IDs in a separate list 
        knnKeyList, knnRefIdList = dataMachete.createNewListFromSelectVariableListAndIdList(knnKeyVarNameList, knnNameList, knnTypedList, \
                                                 subsetIntegrity, uniqueSubset, uniqueCompleteSet, printDiagnostics)
        #Extract nearest neighbour distances in order from nearest neighbour to most distant neighbour
        knnDistList = asaKnn.getSelectedVariableSet(knnDistNameList, knnTypedList)
        #Ready to generate new list with means and standard deviations (optional distance weighting, excluding certain values, including values within certain range)
        statsList = [statsHeader]
        statsList = asaKnn.compileNearestNeighbourStatistics(statsList, varSelList, refKeyValueList, \
                                                              refSelValueList, knnKeyList, knnRefIdList, \
                                                              knnDistList, knnMax, distanceWeight, \
                                                              listOfExcludedValues, minIncludeValue, \
                                                              maxIncludeValue, outputMean, outputStdev)
        if batch == 1:
            dataMachete.writeListarrayToCSVFile_v2(statsList, dataOutPath, printFileName, '%0.6f', '.csv', True, True)
        else:
            dataMachete.writeListarrayToCSVFile_v2(statsList, dataOutPath, printFileName, '%0.6f', '.csv', False, False)
        startReadLine = endReadLine
        
print '\n COMPILATION OF kNN Y-Stats or X-Stats COMPLETED'
raw_input(" Press Enter to Close This Session ... ")        



