'''
'''
import sys
sys.path.append("D://Rwd//Python//Admin")

import miniApp
import dataMachete
import asaMVA
import asaClassifiers
import miniCli


#Get Configuration File Data

cmeansConfigName = 'cmeansConfig.txt'
cmeansConfigdefpath = '/Rwd/Python/Config/'
cmeansConfigaltpath = '/Rwd/Python/Config/'
pathkeyslist=['cmeansDataInPath', 'cmeansDataOutPath']
configKeyList = ['cmeansDataFileName','normalizeData', 'varSelCriteria', 'cmeansMValue','cmeansError','cmeansGnoRange', \
                 'normStatsTableName', 'fuzzyCentroidFileName','fuzzyMembershipFileName','fuzzyClassFileName', \
                 'classBaseName']
#Get Information About Configuration File 
cmeansConfigInfoName = 'cmeansConfigInfo.txt'
#cmeansConfig = miniApp.getConfig(cmeansConfigName, cmeansConfigdefpath, cmeansConfigaltpath, pathkeyslist)
cmeansConfig = miniCli.getConfig(cmeansConfigName, cmeansConfigdefpath, cmeansConfigaltpath, pathkeyslist, configKeyList, \
                                 cmeansConfigInfoName)
dataInPath = cmeansConfig['cmeansDataInPath'][0]
dataOutPath = dataMachete.checkIfFileExistsAndSetToDefaultIfItDoesNot(cmeansConfig['cmeansDataOutPath'][0], dataInPath)
errorFilePath = dataMachete.checkIfFileExistsAndSetToDefaultIfItDoesNot(cmeansConfig['errorFilePath'][0], dataInPath)
dataDictionaryFilePath = dataMachete.checkIfFileExistsAndSetToDefaultIfItDoesNot(cmeansConfig['dataDictionaryFilePath'][0], dataInPath)
dataDictionary = cmeansConfig['dataDictionaryFileName'][0]
myDataTableName = cmeansConfig['cmeansDataFileName'][0]
dataKeyVarNameList = cmeansConfig['cmeansDataUniqueIds']
varSelTableName = cmeansConfig['cmeansVariableSelect'][0]
varSelCriteria = cmeansConfig['cmeansVariableSelectCriteria'][0]
#Normalize Data
normalizeFlag = dataMachete.checkYesOrNoDecisionRule(cmeansConfig['normalizeData'][0],'normalizeData')
#Fuzzy cmeans inputs
cmeansMValue = float(cmeansConfig['cmeansMValue'][0])
cmeansError = float(cmeansConfig['cmeansError'][0])
cmeansGnoMin = int(cmeansConfig['cmeansGnoRange'][0])
cmeansGnoMax = int(cmeansConfig['cmeansGnoRange'][1])
classificationType = cmeansConfig['classificationType'][0]
#Normalization statistics file (means and standard deviations) if normalizeFlag is YES 
statsTableName = cmeansConfig['normStatsTableName'][0]
statsTableNameList = statsTableName.split('.')
normalizedDataTableName = cmeansConfig['normalizedDataTableName'][0]
#Distance metric
classificationType = cmeansConfig['classificationType'][0]
#Output file names
fuzzyCentroidFileName = cmeansConfig['fuzzyCentroidFileName'][0]
fuzzyMembershipFileName = cmeansConfig['fuzzyMembershipFileName'][0]
fuzzyClassFileName = cmeansConfig['fuzzyClassFileName'][0]
#Base name used to label each system of classificiation (e.g. CLASS)
classBaseName = cmeansConfig['classBaseName'][0]
if classBaseName == '':
    classBaseName = 'CLASS'
#printTypes
printTypes = dataMachete.checkYesOrNoDecisionRule(cmeansConfig['printDataTypes'][0],'printDataTypes')

if dataDictionary == '':
    oldDict, newDict = dataMachete.inferDataDictionary_v2(myDataTableName, dataInPath, '.txt', printTypes, -1 )
else:
    oldDict, newDict = dataMachete.getDatamacheteDictionary(dataDictionaryFilePath, dataDictionaryFileName, fileExtension = '.txt')
    
readErrorFileName = 'ERROR_' + myDataTableName
dataTypedList = dataMachete.getTypedListArray(newDict, myDataTableName, dataInPath, '.txt',readErrorFileName, \
                                              dataInPath, '.txt')

#Extract Y variable classification names from XVARSELV1
varOldDict, varNewDict = dataMachete.inferDataDictionary_v2(varSelTableName, dataInPath, '.csv', printTypes, -1 )
readErrorFileName = 'ERROR_' + varSelTableName
varSelTypedList = dataMachete.getTypedListArray(varNewDict, varSelTableName, dataInPath,'.csv', readErrorFileName, \
                                              dataInPath, '.txt')
#Select variable according to varSelCriteria
xVariableList = miniApp.selectAnalysisVariables(varSelCriteria, varSelTypedList)

#Extract key Values (references to each observation) in one dataList and associated selected variable values in a separate list  
subsetIntegrity = True
uniqueSubset = True
uniqueCompleteSet = True
printDiagnostics = True
keyVarValueList, selVarValueList = dataMachete.createNewListFromSelectVariableListAndIdList(dataKeyVarNameList, xVariableList, dataTypedList, \
                                                 subsetIntegrity, uniqueSubset, uniqueCompleteSet, printDiagnostics)

if normalizeFlag == 'Yes' or normalizeFlag == 'YES' or normalizeFlag == 'yes' or normalizeFlag == 'Y' or normalizeFlag == 'y':
    if classificationType == 'FCM_CE':
        excludeZeros = True
    else:
        excludeZeros = False

    statsHeader, statsKeyVarNameList, statsDict = asaMVA.getMeanAndStandardDeviationFor2DListNumpy(statsTableNameList[0],\
                                                                                              xVariableList, selVarValueList,{}, \
                                                                                                   excludeZeros)
    if len(statsTableNameList)>1:
        filePath = dataOutPath + statsTableName
    else:
        filePath = dataOutPath + statsTableName + '.txt'
    #Overwrite old file if it exists with new header
    dataMachete.initializeVariableHeader(statsHeader,filePath)
    #Append remainder of file to existing file
    dataMachete.saveDictDB_v2(filePath,statsKeyVarNameList, statsHeader, statsDict)
    #normalize Y-variable set       
    dataNormList = asaMVA.normalizeVariableDatasetNumpy(selVarValueList, xVariableList, statsTableNameList[0], statsDict)
    #Join dataKeyVarNameList to dataSelectVarNameList and dataKeyList to dataNormTypedList for each observation and print to tableName
    normPrintData = dataMachete.joinTwo2DListsPlusHeaders(xVariableList, dataNormList, dataKeyVarNameList, keyVarValueList)
    dataMachete.writeListarrayToCSVFile(normPrintData, dataOutPath, normalizedDataTableName, '%0.6f', '.csv')
    #Complete Fuzzy c-means classification
    if classificationType == 'FCM_CE' or classificationType == 'FCM_E' or classificationType == 'FCM_M':
        classList, centroidList, membershipList = asaClassifiers.runFuzzyCMeansClassification_v3(dataKeyVarNameList,keyVarValueList, xVariableList,\
                                                                                             dataNormList, cmeansMValue, cmeansError, cmeansGnoMin, \
                                                                                             cmeansGnoMax, classificationType, classBaseName)
    else:
        #Distance metric set to Euclidean by default
        classList, centroidList, membershipList = asaClassifiers.runFuzzyCMeansClassification_v3(dataKeyVarNameList,keyVarValueList, xVariableList,\
                                                                                             dataNormList, cmeansMValue, cmeansError, cmeansGnoMin, \
                                                                                             cmeansGnoMax, 'FCM_E', classBaseName)
else:
    #Complete Fuzzy c-means classification
    if classificationType == 'FCM_CE' or classificationType == 'FCM_E' or classificationType == 'FCM_M':
        classList, centroidList, membershipList = asaClassifiers.runFuzzyCMeansClassification_v3(dataKeyVarNameList,keyVarValueList, xVariableList,\
                                                                                             dataNormList, cmeansMValue, cmeansError, cmeansGnoMin, \
                                                                                             cmeansGnoMax, classificationType, classBaseName)
    else:
        #Distance metric set to Euclidean by default
        classList, centroidList, membershipList = asaClassifiers.runFuzzyCMeansClassification_v3(dataKeyVarNameList,keyVarValueList, xVariableList,\
                                                                                             selVarValueList, cmeansMValue, cmeansError, cmeansGnoMin, \
                                                                                             cmeansGnoMax,'FCM_E', classBaseName)
    
dataMachete.writeListarrayToCSVFile(classList, dataOutPath, fuzzyClassFileName, '%0.6f', '.csv')
dataMachete.writeListarrayToCSVFile(centroidList, dataOutPath, fuzzyCentroidFileName, '%0.6f', '.csv')
dataMachete.writeListarrayToCSVFile(membershipList, dataOutPath, fuzzyMembershipFileName, '%0.6f', '.csv')

#raw_input(" Press Enter to Close This Session ... ")
print ' Finished Processing Fuzzy C-Means'
