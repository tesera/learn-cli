'''
'''
import routineLviApplications
myDataTableName = 'LVINEW'
oldDict, newDict = routineLviApplications.createNewDataDictionaryFromFile(myDataTableName, 'YES', 10000)
dataKeyVarNameList = ['LVI_FCOID']
dataTypedList = routineLviApplications.ReadCsvDataFile(newDict, myDataTableName, 'ERROR-CHECK-LVUN')
#Extract Y variable classification names from XVARSELV1
xVarSelvTableName = 'XVARSELV1'
oldXvarDict, newXvarDict = routineLviApplications.createNewDataDictionaryFromFile(xVarSelvTableName, 'YES', 1000)
dataSelectVarNameList = routineLviApplications.ReadXVarSelv1XorYVariableList(newXvarDict, 'X')
#Extract key Values in one dataList and associated selected variable values in a separate list  
dataKeyList, dataTypedSubsetList = routineLviApplications.createNewListFromSelectVariableListAndIdList(dataKeyVarNameList, dataSelectVarNameList, dataTypedList)
normalizeFlag = 'No'
print "\n If you would like to normalize the dataset print Y or y or Yes or yes and then press ENTER."
newFlag = raw_input(" ... ")
if newFlag == 'Y' or newFlag == 'y' or newFlag == 'Yes' or newFlag == 'yes':
    normalizeFlag = 'Yes'
if normalizeFlag == 'Yes':
    #Normalize Y variable dataset
    print " Enter name for table normalization statistics, MEAN and SDEV, e.g. STATSNORM"
    statsTableName = raw_input("\n Enter table name and then press ENTER to continue ... ")
    statsHeader, statsKeyVarNameList, statsDict = routineLviApplications.getMeanAndStandardDeviationFor2DList(statsTableName, dataSelectVarNameList, dataTypedSubsetList,{})
    #print statsDict
    routineLviApplications.printNestedDictionary(statsKeyVarNameList, statsHeader, statsDict, statsTableName)
    #normalize Y-variable set
    dataNormTypedList = routineLviApplications.normalizeVariableDataset(dataTypedSubsetList, dataSelectVarNameList, statsTableName, statsDict)
    normTableName = 'REFNORM'
    #Join dataKeyVarNameList to dataSelectVarNameList and dataKeyList to dataNormTypedList for each observation and print to tableName
    routineLviApplications.printList2DWithSeparateVarNameListAndKeyVarNameListAndValues(dataSelectVarNameList, \
                                        dataNormTypedList, dataKeyVarNameList, dataKeyList,  normTableName)
    #Complete Fuzzy c-means classification
    routineLviApplications.runFuzzyCMeansClassification_v2(dataKeyVarNameList,dataKeyList, dataSelectVarNameList,dataNormTypedList)
else:
    #Complete Fuzzy c-means classification
    routineLviApplications.runFuzzyCMeansClassification_v2(dataKeyVarNameList,dataKeyList, dataSelectVarNameList,dataTypedSubsetList)
raw_input(" Press Enter to Close This Session ... ")
