'''
'''
import routineLviApplications
#dataTableName = 'LCDISTR'
#dataTableName = 'RCDISTR'
dataTableName = 'ACDISTR'
#dataTableName = 'CDISTR'
printTypes = 'YES'
nLines = 10000
originalDict, newDict = routineLviApplications.createNewDataDictionaryFromFile(dataTableName, printTypes, nLines)
readErrorFileName = 'ERROR-CHECK-CDISTR'
#keyVarNameList = ['PLOTID']
keyVarNameList = ['NPLOTID']
cdistTypedList = routineLviApplications.ReadCsvDataFile(newDict, dataTableName, readErrorFileName)
cdistHeader = cdistTypedList[0]
dataSelectVarNameList = routineLviApplications.removeItemsInOneDListBFromOneDListA(cdistHeader, keyVarNameList)
dataKeyList, dataTypedSubsetList = routineLviApplications.createNewListFromSelectVariableListAndIdList(keyVarNameList, dataSelectVarNameList, cdistTypedList)
routineLviApplications.runFuzzyCMeansClassification_v2(keyVarNameList,dataKeyList,dataSelectVarNameList,dataTypedSubsetList)
