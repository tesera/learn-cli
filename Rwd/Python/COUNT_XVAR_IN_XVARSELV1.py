'''
'''
import routineLviApplications
print '\n Reading VARRANK.csv'
tableName = 'XVARSELV1'
printTypes = 'YES'
nLines = 10000
oldDict, newDict = routineLviApplications.createNewDataDictionaryFromFile(tableName, printTypes, nLines)
varSelKeyVarNameList = ['VARNAME']
readErrorFileName = 'ERROR_'+ tableName
varSelHeader, varSelDict = routineLviApplications.ReadCsvDataFileAndTransformIntoDictionaryFormat_v2(oldDict, newDict, tableName, \
                                                                                                     readErrorFileName, varSelKeyVarNameList)
#Count remaining X-Variables
xVarCount = 0
for varName in varSelDict:
    if varSelDict[varName]['XVARSEL']=='X':
        xVarCount = xVarCount + 1

print '\n There are',xVarCount,'eligible X-Variables remaining in XVARSELV1.'
fileName = 'XVARSELV1_XCOUNT'
floatFormat = '%0.6f'
varCountList = [[xVarCount]]
routineLviApplications.writeListArrayToCsvFile(varCountList, fileName, floatFormat)
