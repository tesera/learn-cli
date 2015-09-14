'''
'''
import routineLviApplications

# 20150908 COUNT_XVAR_IN_XVARSELV1 is now converted to a function to work in the Bridge by SK

def Count_XVar_in_XVarSelv1():

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

    return xVarCount #20150914 added by SK
    
if __name__ == '__main__':
    
    Count_XVar_in_XVarSelv1()        
