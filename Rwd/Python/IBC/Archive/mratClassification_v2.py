'''
'''
import miniApp
import dataMachete
import asaMVA
import asaClassifiers
import miniCli


#Get Configuration File Data

cmeansConfigName = 'cmeansConfig.txt'
cmeansConfigdefpath = '/Rwd/Python/Config/'
cmeansConfigaltpath = '/Users/Maxine/Documents/TSIAnalytics/Config/'
pathkeyslist=['cmeansDataInPath', 'cmeansDataOutPath']
configKeyList = ['normalizeData','cmeansMValue','cmeansError','cmeansGnoRange','normStatsTableName']
#Get Information About Configuration File 
cmeansConfigInfoName = 'cmeansConfigInfo.txt'
#cmeansConfig = miniApp.getConfig(cmeansConfigName, cmeansConfigdefpath, cmeansConfigaltpath, pathkeyslist)
cmeansConfig = miniCli.getConfig(cmeansConfigName, cmeansConfigdefpath, cmeansConfigaltpath, pathkeyslist, configKeyList, cmeansConfigInfoName)
dataInPath = cmeansConfig['cmeansDataInPath'][0]
dataOutPath = cmeansConfig['cmeansDataOutPath'][0]
myDataTableName = cmeansConfig['cmeansDataFileName'][0]
varSelTableName = cmeansConfig['cmeansVariableSelect'][0]
#Normalize Data
normalizeFlag = cmeansConfig['normalizeData'][0]
cmeansMValue = float(cmeansConfig['cmeansMValue'][0])
cmeansError = float(cmeansConfig['cmeansError'][0])
cmeansGnoMin = int(cmeansConfig['cmeansGnoRange'][0])
cmeansGnoMax = int(cmeansConfig['cmeansGnoRange'][1])
statsTableName = cmeansConfig['normStatsTableName'][0]



printTypes = 'YES'
oldDict, newDict = dataMachete.inferDataDictionary_v2(myDataTableName, dataInPath, '.txt', printTypes, -1 )
dataKeyVarNameList = ['UID']
readErrorFileName = 'ERROR_' + myDataTableName
dataTypedList = dataMachete.getTypedListArray(newDict, myDataTableName, dataInPath, '.txt',readErrorFileName, \
                                              dataInPath, '.txt')

#Extract Y variable classification names from XVARSELV1
varOldDict, varNewDict = dataMachete.inferDataDictionary_v2(varSelTableName, dataInPath, '.csv', printTypes, -1 )
readErrorFileName = 'ERROR_' + varSelTableName
varSelTypedList = dataMachete.getTypedListArray(varNewDict, varSelTableName, dataInPath,'.csv', readErrorFileName, \
                                              dataInPath, '.txt')
varSelCriteria = 'X'
xVariableList = miniApp.selectAnalysisVariables(varSelCriteria, varSelTypedList)

#Extract key Values (references to each observation) in one dataList and associated selected variable values in a separate list  
subsetIntegrity = True
uniqueSubset = True
uniqueCompleteSet = True
printDiagnostics = True
keyVarValueList, selVarValueList = dataMachete.createNewListFromSelectVariableListAndIdList(dataKeyVarNameList, xVariableList, dataTypedList, \
                                                 subsetIntegrity, uniqueSubset, uniqueCompleteSet, printDiagnostics)

#normalizeFlag = 'No'
#print "\n If you would like to normalize the dataset print Y or y or Yes or yes and then press ENTER."
#newFlag = raw_input(" ... ")
#if newFlag == 'Y' or newFlag == 'y' or newFlag == 'Yes' or newFlag == 'yes':
#    normalizeFlag = 'Yes'
if normalizeFlag == 'Yes' or normalizeFlag == 'YES' or normalizeFlag == 'yes' or normalizeFlag == 'Y' or normalizeFlag == 'y':
    #Normalize Y variable dataset
    #print " Enter name for table normalization statistics, MEAN and SDEV, e.g. STATSNORM"
    #statsTableName = raw_input("\n Enter table name and then press ENTER to continue ... ") 
    #statsHeader, statsKeyVarNameList, statsDict = asaMVA.getMeanAndStandardDeviationFor2DList(statsTableName, \
    #                                                                xVariableList, selVarValueList,{})
    statsHeader, statsKeyVarNameList, statsDict = asaMVA.getMeanAndStandardDeviationFor2DListNumpy(statsTableName,\
                                                                                              xVariableList, selVarValueList,{})
                                                                                              
    #print statsDict
    #routineLviApplications.printNestedDictionary(statsKeyVarNameList, statsHeader, statsDict, statsTableName)
    filePath = dataOutPath + statsTableName + '.txt'
    dataMachete.saveDictDB_v2(filePath,statsKeyVarNameList, statsHeader, statsDict)
    #normalize Y-variable set
    
    #dataNormTypedList = routineLviApplications.normalizeVariableDataset(dataTypedSubsetList, dataSelectVarNameList, statsTableName, statsDict)
    #dataNormList = asaMVA.normalizeVariableDataset(selVarValueList, xVariableList, statsTableName, statsDict)
    dataNormList = asaMVA.normalizeVariableDatasetNumpy(selVarValueList, xVariableList, statsTableName, statsDict)
    normTableName = 'REFNORM'
    #Join dataKeyVarNameList to dataSelectVarNameList and dataKeyList to dataNormTypedList for each observation and print to tableName
    normPrintData = dataMachete.joinTwo2DListsPlusHeaders(xVariableList, dataNormList, dataKeyVarNameList, keyVarValueList)
    dataMachete.writeListarrayToCSVFile(normPrintData, dataOutPath, normTableName, '%0.6f', '.csv')
    #Complete Fuzzy c-means classification
    #classList, centroidList, membershipList = asaClassifiers.runFuzzyCMeansClassification_v2(dataKeyVarNameList,keyVarValueList, xVariableList,dataNormList)
    classList, centroidList, membershipList = asaClassifiers.runFuzzyCMeansClassification_v3(dataKeyVarNameList,keyVarValueList, xVariableList,\
                                                                                             dataNormList, cmeansMValue, cmeansError, cmeansGnoMin, cmeansGnoMax)
else:
    #Complete Fuzzy c-means classification
    #classList, centroidList, membershipList = asaClassifiers.runFuzzyCMeansClassification_v2(dataKeyVarNameList,keyVarValueList, xVariableList,selVarValueList)
    classList, centroidList, membershipList = asaClassifiers.runFuzzyCMeansClassification_v3(dataKeyVarNameList,keyVarValueList, xVariableList,\
                                                                                             selVarValueList, cmeansMValue, cmeansError, cmeansGnoMin, cmeansGnoMax)
    
dataMachete.writeListarrayToCSVFile(classList, dataOutPath, 'FCLASS', '%0.6f', '.csv')
dataMachete.writeListarrayToCSVFile(centroidList, dataOutPath, 'FCENTROID', '%0.6f', '.csv')
dataMachete.writeListarrayToCSVFile(membershipList, dataOutPath, 'FCMEMBERSHIP', '%0.6f', '.csv')

#raw_input(" Press Enter to Close This Session ... ")
print ' Finished Processing Fuzzy C-Means'
