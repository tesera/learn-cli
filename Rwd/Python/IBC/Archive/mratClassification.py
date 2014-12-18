'''
'''
import miniApp
import dataMachete
import asaMVA
import asaClassifiers

#Get Configuration File Information
cmeansConfigName = 'cmeansConfig.txt'
cmeansConfigdefpath = '/apps/TSIAnalytics/Config/'
cmeansConfigaltpath = '/Users/Maxine/Documents/TSIAnalytics/Config/'
cmeansConfig = miniApp.getConfig(filename=cmeansConfigName, defpath=cmeansConfigdefpath, altpath=cmeansConfigaltpath, pathkeyslist=['cmeansDataInPath', 'cmeansDataOutPath'])
#dataInPath = cmeansConfig['cmeansDataInPath'][0]
#dataOutPath = cmeansConfig['cmeansDataOutPath'][0]
#myDataTableName = cmeansConfig['cmeansDataFileName'][0]
#varSelTableName = cmeansConfig['cmeansVariableSelect'][0]

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

normalizeFlag = 'No'
print "\n If you would like to normalize the dataset print Y or y or Yes or yes and then press ENTER."
newFlag = raw_input(" ... ")
if newFlag == 'Y' or newFlag == 'y' or newFlag == 'Yes' or newFlag == 'yes':
    normalizeFlag = 'Yes'
if normalizeFlag == 'Yes':
    #Normalize Y variable dataset
    print " Enter name for table normalization statistics, MEAN and SDEV, e.g. STATSNORM"
    statsTableName = raw_input("\n Enter table name and then press ENTER to continue ... ")
    statsHeader, statsKeyVarNameList, statsDict = asaMVA.getMeanAndStandardDeviationFor2DList(statsTableName, xVariableList, selVarValueList, \
                                                                                              {})
    #print statsDict
    #routineLviApplications.printNestedDictionary(statsKeyVarNameList, statsHeader, statsDict, statsTableName)
    filePath = dataOutPath + statsTableName + '.txt'
    dataMachete.saveDictDB_v2(filePath,statsKeyVarNameList, statsHeader, statsDict)
    #normalize Y-variable set
    
    #dataNormTypedList = routineLviApplications.normalizeVariableDataset(dataTypedSubsetList, dataSelectVarNameList, statsTableName, statsDict)
    dataNormList = asaMVA.normalizeVariableDataset(selVarValueList, xVariableList, statsTableName, statsDict)
    normTableName = 'REFNORM'
    #Join dataKeyVarNameList to dataSelectVarNameList and dataKeyList to dataNormTypedList for each observation and print to tableName
    normPrintData = dataMachete.joinTwo2DListsPlusHeaders(xVariableList, dataNormList, dataKeyVarNameList, keyVarValueList)
    dataMachete.writeListarrayToCSVFile(normPrintData, dataOutPath, normTableName, '%0.6f', '.csv')
    #Complete Fuzzy c-means classification
    classList, centroidList, membershipList = asaClassifiers.runFuzzyCMeansClassification_v2(dataKeyVarNameList,keyVarValueList, xVariableList,dataNormList)
else:
    #Complete Fuzzy c-means classification
    classList, centroidList, membershipList = asaClassifiers.runFuzzyCMeansClassification_v2(dataKeyVarNameList,keyVarValueList, xVariableList,selVarValueList)
    
dataMachete.writeListarrayToCSVFile(classList, dataOutPath, 'FCCLASS', '%0.6f', '.csv')
dataMachete.writeListarrayToCSVFile(centroidList, dataOutPath, 'FCCENTROID', '%0.6f', '.csv')
dataMachete.writeListarrayToCSVFile(membershipList, dataOutPath, 'FCMEMBERSHIP', '%0.6f', '.csv')

raw_input(" Press Enter to Close This Session ... ")
