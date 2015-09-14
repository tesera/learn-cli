'''
This module ranks variables based on their position and frequency of occurence
in the R table output VARSELECT.csv.

Another file, UNIQUEVAR.csv provides a list of all of the variables
referred to in VARSELV.csv 
'''

import routineLviApplications

# 20150908 RANKVAR is now converted to a function to work in the Bridge SK

def RankVar():

    varSelTableName = 'VARSELECT'
    printTypes = 'YES'
    nLines = 10000
    oldDict, newDict = routineLviApplications.createNewDataDictionaryFromFile(varSelTableName, printTypes, nLines)
    varSelKeyVarNameList = ['UID']
    readErrorFileName = 'ERROR_'+varSelTableName
    varSelHeader, varSelDict = routineLviApplications.ReadCsvDataFileAndTransformIntoDictionaryFormat_v2(oldDict, newDict, varSelTableName, \
                                                                                                         readErrorFileName, varSelKeyVarNameList)
    keyVarValueList = varSelDict.keys()
    keyVarValueList.sort()
    nCases = len(keyVarValueList)
    #Create varRankDict
    #RANK is equal to the minimum number of variables
    #across all equations in which the variable is found
    #p is equal to the proportion of cases in which the variable was found
    rankDictHeader = ['VARNAME','RANK','P','IMPORTANCE']
    rankDictKeyList = ['VARNAME']
    rankDict = {}
    for i in range(0,nCases,1):
        uid = keyVarValueList[i]
        varName = varSelDict[uid]['VARNAME']
        rank = varSelDict[uid]['SOLTYPE']
        if not rankDict.has_key(varName):
            rankDict.update({varName:{'RANK':rank,'P':1,'IMPORTANCE':0}})
        else:
            if rank < rankDict[varName]['RANK']:
                rankDict[varName]['RANK']=rank
            rankDict[varName]['P'] = rankDict[varName]['P'] + 1
    #Convert rankDict Pvalues to proportions
    for varName in rankDict:
        rankDict[varName]['P'] = (rankDict[varName]['P']/float(nCases))**(1/float(2))
        rankDict[varName]['IMPORTANCE']= (rankDict[varName]['P']*(1/float(rankDict[varName]['RANK']))**(1/float(2)))**(1/float(2))
        
    print '\n VARRANK.csv is produced from VARSELECT.csv to identify variable importance'  
    print '\n importance = sqrt(sqrt(p)*sqrt(1/rank))'
    print '\n where: \n'
    print ' p       is the proportion of equations in which a variable occurs'
    print ' rank    is equal to the minimum number of variables in an equation where\n          1 is the highest ranked variable'
    
    tableName = 'VARRANK'    
    routineLviApplications.printNestedDictionary(rankDictKeyList, rankDictHeader, rankDict, tableName)
    return rankDict #20150908 added by SK

if __name__ == '__main__':
    
    RankVar()        
