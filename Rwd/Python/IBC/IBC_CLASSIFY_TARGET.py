'''
'''
import routineLviApplications
#input desired number of nearest neighbours
kNN = input("\n Input the maximum number of nearest neighbours and press ENTER ... ")
print '\n Input name of nearest neighbour output file, e.g. NNCQTLM, and press ENTER to continue'
nnOutFileName = raw_input(" ... ")
#Extract target dataset
targetTableName = 'SUMZ'
oldDict, newDict = routineLviApplications.createNewDataDictionaryFromFile(targetTableName, 'YES', 1000)
targetKeyVarNameList = ['UID']
targetTypedList = routineLviApplications.ReadCsvDataFile(newDict, targetTableName, 'ERROR-CHECK-SUMZ')
#Extract Y variable classification names from XVARSELV1
xVarSelvTableName = 'XVARSELV1'
oldXvarDict, newXvarDict = routineLviApplications.createNewDataDictionaryFromFile(xVarSelvTableName, 'YES', 1000)
dataSelectVarNameList = routineLviApplications.ReadXVarSelv1XorYVariableList(newXvarDict, 'X')
#Extract key Values in in target dataset and associated selected variable values in a separate list  
targetKeyList, targetTypedSubsetList = routineLviApplications.createNewListFromSelectVariableListAndIdList(targetKeyVarNameList, dataSelectVarNameList, targetTypedList)
normalizeFlag = 'No'
#Extract reference dataset
refTableName = 'INFRA'
refKeyVarNameList = ['NCLASS']
oldDict, newDict = routineLviApplications.createNewDataDictionaryFromFile(refTableName, 'YES', 1000)
refTypedList = routineLviApplications.ReadCsvDataFile(newDict, refTableName, 'ERROR-CHECK-INFRA')
#Extract key values in reference dataset and associated selected variable values in a separate list  
refKeyList, refTypedSubsetList = routineLviApplications.createNewListFromSelectVariableListAndIdList(refKeyVarNameList, dataSelectVarNameList, refTypedList)
#
print "\n If you would like to normalize the dataset print Y or y or Yes or yes and then press ENTER."
newFlag = raw_input(" ... ")
if newFlag == 'Y' or newFlag == 'y' or newFlag == 'Yes' or newFlag == 'yes':
    normalizeFlag = 'Yes'
    if normalizeFlag == 'Yes':
        print '\n Enter statsTableName, e.g. CQTLMSTATS and press ENTER to continue'
        statsTableName = raw_input(" ... ")
        readErrorFileName = 'ERROR_' + statsTableName
        statsKeyVarNameList = ['TABLENAME','VARNAME']
        oldStatsDict, newStatsDict = routineLviApplications.createNewDataDictionaryFromFile(statsTableName, 'YES', 1000)        
        statsHeader, statsTypedDict = routineLviApplications.ReadCsvDataFileAndTransformIntoDictionaryFormat_v2(oldStatsDict, newStatsDict, statsTableName , readErrorFileName , statsKeyVarNameList)
        dataNormTypedList = routineLviApplications.normalizeVariableDataset(targetTypedSubsetList, dataSelectVarNameList, statsTableName, statsTypedDict)
        normTableName = 'TARGNORM'
        #Join dataKeyVarNameList to dataSelectVarNameList and dataKeyList to dataNormTypedList for each observation and print to tableName
        routineLviApplications.printList2DWithSeparateVarNameListAndKeyVarNameListAndValues(dataSelectVarNameList, \
                                        dataNormTypedList, targetKeyVarNameList, targetKeyList,  normTableName)
        targetNNList = routineLviApplications.assignTargetObservationsTokNearestNeighboursUsingEuclideanDistance(targetKeyVarNameList, targetKeyList, dataNormTypedList, refKeyList, refTypedSubsetList, kNN)
else:
    targetNNList = routineLviApplications.assignTargetObservationsTokNearestNeighboursUsingEuclideanDistance(targetKeyVarNameList, targetKeyList, targetTypedSubsetList, refKeyList, refTypedSubsetList, kNN)
routineLviApplications.printList2DWithHeader(targetNNList, nnOutFileName)
    
raw_input(" Press Enter to Close This Session ... ")
