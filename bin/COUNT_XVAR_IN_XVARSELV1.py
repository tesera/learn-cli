import routineLviApplications
from rpy2.robjects.packages import importr
flog = importr("futile.logger")

def Count_XVar_in_XVarSelv1():

    flog.flog_info("Reading VARRANK.csv")
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
    
    flog.flog_info("There are %s eligible X-Variables remaining in XVARSELV1.", xVarCount)
    fileName = 'XVARSELV1_XCOUNT'
    floatFormat = '%0.6f'
    varCountList = [[xVarCount]]
    routineLviApplications.writeListArrayToCsvFile(varCountList, fileName, floatFormat)

    return xVarCount #20150914 added by SK
    
if __name__ == '__main__':
    
    Count_XVar_in_XVarSelv1()        
