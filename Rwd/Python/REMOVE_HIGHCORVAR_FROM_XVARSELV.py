'''
'''
import routineLviApplications
print '\n Removing highly correlated X-Variables in order of importance \n (least to most) from XVARSELV1.csv using importance in VARRANK.csv'
print '\n Reading UCORCOEF'
#
#Read file with variable pair correlation coefficients
tableName = 'UCORCOEF'
printTypes = 'YES'
nLines = 10000
oldDict, newDict = routineLviApplications.createNewDataDictionaryFromFile(tableName, printTypes, nLines)
corCoefKeyVarNameList = ['VARNAME1', 'VARNAME2']
readErrorFileName = 'ERROR_'+ tableName
corCoefHeader, corCoefDict = routineLviApplications.ReadCsvDataFileAndTransformIntoDictionaryFormat_v2(oldDict, newDict, tableName, \
                                                                                                       readErrorFileName, corCoefKeyVarNameList)
corCoefVarNameList = corCoefDict.keys()
corCoefVarNameList.sort()

#                                                                                                       
#Read file with variable importance indicators
print '\n Reading VARRANK.csv'
tableName = 'VARRANK'
printTypes = 'YES'
nLines = 10000
oldDict, newDict = routineLviApplications.createNewDataDictionaryFromFile(tableName, printTypes, nLines)
varRankKeyVarNameList = ['IMPORTANCE', 'VARNAME']
readErrorFileName = 'ERROR_'+ tableName
rankHeader, rankDict = routineLviApplications.ReadCsvDataFileAndTransformIntoDictionaryFormat_v2(oldDict, newDict, tableName, \
                                                                                                     readErrorFileName, varRankKeyVarNameList)
impValueList = rankDict.keys()
impValueList.sort()
#
print '\n Reading VARRANK.csv'
tableName = 'XVARSELV1'
printTypes = 'YES'
nLines = 10000
oldDict, newDict = routineLviApplications.createNewDataDictionaryFromFile(tableName, printTypes, nLines)
varSelKeyVarNameList = ['VARNAME']
readErrorFileName = 'ERROR_'+ tableName
varSelHeader, varSelDict = routineLviApplications.ReadCsvDataFileAndTransformIntoDictionaryFormat_v2(oldDict, newDict, tableName, \
                                                                                                     readErrorFileName, varSelKeyVarNameList)
xVarSelvUpdateFlag = False
for impValue in impValueList:
    impVarNameList = rankDict[impValue].keys()
    for impVarName in impVarNameList:
        if impVarName in corCoefVarNameList:
            corVarName2List = corCoefDict[impVarName].keys()
            flag = False
            for corVarName2 in corVarName2List:
                if not corVarName2==impVarName:
                    if corVarName2 in corCoefVarNameList:
                        corCoef = corCoefDict[impVarName][corVarName2]['CORCOEF']
                        if abs(corCoef)>= 0.8:
                            flag = True
            if flag == True:
                varSelDict[impVarName]['XVARSEL']='N'
                listIndex = corCoefVarNameList.index(impVarName)
                del corCoefVarNameList[listIndex]
                xVarSelvUpdateFlag = True    

if xVarSelvUpdateFlag == True:
    print '\n XVARSELV1 has been updated with changes in varibale status (XVARSEL) from X to N'
    routineLviApplications.printNestedDictionary(varSelKeyVarNameList, varSelHeader, varSelDict, tableName)
else:
    print '\n XVARSELV1 has not been updated.\n There are no correlations amongst selected X-Variable >= 0.8 or <= -0.8.'

                    
                
                
