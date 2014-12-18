def getDictKeySetValuesList(myDict = {}, keyVarnames=[]):
    '''
    Created by Ian Moss December 5 2012 as an extension of previous dictionaryDB handling
    utilities developed by Ian Moss

    The inputs are:

    1. The dictionary (myDict) from which the unique combinations of keys are to bee extracted.
    2. The list of key variable names (in the order that they occur) used top establish the order of the key values in the dictionary.   

    This function creates a list of all the unique combinations of keys in data dictionary
    By design the data dictionary is already organized around unique combinations of keys
        
    '''
    newKeyValueList = []
    nKeys = len(keyVarnames)
    if nKeys == 0:
        for Key0 in myDict:
            newKeyValueList.append([])
            newKeyValueList[0].append(Key0)
    if nKeys >= 1:
        for Key1 in myDict:
            if nKeys == 1:
                newKeyValueList.append([Key1])
            else:
                if nKeys >= 2:
                    for Key2 in myDict[Key1]:
                        if nKeys == 2:
                            newKeyValueList.append([Key1, Key2])                          
                        else:
                            if nKeys >= 3:
                                for Key3 in myDict[Key1][Key2]:
                                        if nKeys == 3:
                                            newKeyValueList.append([Key1, Key2, Key3])
                                        else:
                                            if nKeys >= 4:
                                                for Key4 in myDict[Key1][Key2][Key3]:
                                                    if nKeys == 4:
                                                        newKeyValueList.append([Key1, Key2, Key3, Key4])
                                                    else:
                                                        if nKeys >= 5:
                                                            for Key5 in myDict[Key1][Key2][Key3][Key4]:
                                                                if nKeys == 5:
                                                                    newKeyValueList.append([Key1, Key2, Key3, Key4, Key5])
                                                                else:
                                                                    if nKeys >= 6:
                                                                        for Key6 in myDict[Key1][Key2][Key3][Key4][Key5]:
                                                                            if nKeys == 6:
                                                                                newKeyValueList.append([Key1, Key2, Key3, Key4, Key5, Key6])
                                                                            else:
                                                                                if nKeys >= 7:
                                                                                    for Key7 in myDict[Key1][Key2][Key3][Key4][Key5][Key6]:
                                                                                        if nKeys == 7:
                                                                                            newKeyValueList.append([Key1, Key2, Key3, Key4, Key5, Key6, Key7])
                                                                                        else:
                                                                                            print 'innerJoinDictDB.getDictKeySetValuesList has dictionary with more than 7 levels'
                                                                                            print 'Cannot complete development of unique sets of keys in a hierarchical dictionary'
    return newKeyValueList

def getCommonInnerJoinKeyValueList(keyValueList1=[[]], keyValueList2=[[]]):
    '''
    Created December 14, 2010 by Ian Moss
    This function compares two keyValueLists and extracts only
    those subsets that are the same. Each unique set of key values
    is contained within a separate list contained within
    keyValueList1 and keyValueList2.

    keyValueLists can be generated from a dictionary (dictDB)
    using innerJoinDictDB.getDictKeySetValuesList().

    The oupput, a list containing only those combinations of keys
    in both keyValueList1 and keyValueList2 can then be used to
    do an inner join using innerJoinDictDB.extractDictDBForKeySetsList()
    '''
    commonKeyValueList = []
    for keyValueList in keyValueList1:
        if keyValueList in keyValueList2:
            commonKeyValueList.append(keyValueList)
    return commonKeyValueList


def extractDictDBForKeySetsList(parentDict,childDict,keySetList):
    '''
    Created December 14, 2010 by Ian Moss
    A temporary dictionary with the same key variable name structure as the master dictionary
    is added to the master dictionary
    Assumptions:
        Keys in both parentDict and childDict match
        1. Can do equivalent of an append command, combined dictionary superset of parentDict and childDict
        and where parentDict and childDict have the same variables but different key values (append). 
        2. Have same keys, between parentDic and chiuldDict, but have different variables (1-1 join)
        3. For every key in parent dict, there are several keys (other key variable) in childDict, and other 
        non-key variables in childDict (inner join)
        
        If parentDict and childDict do not match the above 3 conditions, there are no guarantees
        as to what the code will output. 
        
    '''
    newDict = {}
    nSets = len(keySetList)
    nKeys = len(keySetList[0])
    if nKeys <= 0:
        #The dictionary is a one line dictionary
        for varName in parentDict:
            varValue = parentDict[varName]
            newDict.update({varName:varValue})
        for varName in childDict:
            if not newDict.has_key(varName):
                newValue = childDict[varName]
                newDict.update({varName:varValue})
    else:
        for newSet in keySetList:
            if nKeys >= 1:
                Key1 = newSet[0]
                newDict.update({Key1:{}})
                if nKeys == 1:
                    for varName in parentDict[Key1]:
                        varValue = parentDict[Key1][varName]
                        newDict[Key1].update({varName:varValue})
                    for varName in childDict[Key1]:
                        if not newDict[Key1].has_key(varName):
                            varValue = childDict[Key1][varName]
                            newDict[Key1].update({varName:varValue})
                else:
                    if nKeys >= 2:
                        Key2 = newSet[1]
                        newDict[Key1].update({Key2:{}})
                        if nKeys == 2:
                            for varName in parentDict[Key1][Key2]:
                                varValue = parentDict[Key1][Key2][varName]
                                newDict[Key1][Key2].update({varName:varValue})
                            for varName in childDict[Key1][Key2]:
                                if not newDict[Key1][Key2].has_key(varName):
                                    varValue = childDict[Key1][Key2][varName]
                                    newDict[Key1][Key2].update({varName:varValue})
                        else:
                            if nKeys >= 3:
                                Key3 = newSet[2]
                                newDict[Key1][Key2].update({Key3:{}})
                                if nKeys == 3:
                                    for varName in parentDict[Key1][Key2][Key3]:
                                        varValue = parentDict[Key1][Key2][Key3][varName]
                                        newDict[Key1][Key2][Key3].update({varName:varValue})
                                    for varName in childDict[Key1][Key2][Key3]:
                                        if not newDict[Key1][Key2][Key3].has_key(varName):
                                            varValue = childDict[Key1][Key2][Key3][varName]
                                            newDict[Key1][Key2][Key3].update({varName:varValue})
                                else:
                                    if nKeys >= 4:
                                        Key4 = newSet[3]
                                        newDict[Key1][Key2][Key3].update({Key4:{}})
                                        if nKeys == 4:
                                            for varName in parentDict[Key1][Key2][Key3][Key4]:
                                                varValue = parentDict[Key1][Key2][Key3][Key4][varName]
                                                newDict[Key1][Key2][Key3][Key4].update({varName:varValue})
                                            for varName in childDict[Key1][Key2][Key3][Key4]:
                                                if not newDict[Key1][Key2][Key3][Key4].has_key(varName):
                                                    varValue = childDict[Key1][Key2][Key3][Key4][varName]
                                                    newDict[Key1][Key2][Key3][Key4].update({varName:varValue})
                                        else:
                                            if nKeys >= 5:
                                                Key5 = newSet[4]
                                                newDict[Key1][Key2][Key3][Key4].update({Key5:{}})
                                                if nKeys == 5:
                                                    for varName in parentDict[Key1][Key2][Key3][Key4][Key5]:
                                                        varValue = parentDict[Key1][Key2][Key3][Key4][Key5][varName]
                                                        newDict[Key1][Key2][Key3][Key4][Key5].update({varName:varValue})
                                                    for varName in childDict[Key1][Key2][Key3][Key4][Key5]:
                                                        if not newDict[Key1][Key2][Key3][Key4][Key5].has_key(varName):
                                                            varValue = childDict[Key1][Key2][Key3][Key4][Key5][varName]
                                                            newDict[Key1][Key2][Key3][Key4][Key5].update({varName:varValue})
                                                else:
                                                    if nKeys >= 6:
                                                        Key6 = newSet[5]
                                                        newDict[Key1][Key2][Key3][Key4][Key5].update({Key6:{}})
                                                    if nKeys == 6:
                                                        for varName in parentDict[Key1][Key2][Key3][Key4][Key5][Key6]:
                                                            varValue = parentDict[Key1][Key2][Key3][Key4][Key5][Key6][varName]
                                                            newDict[Key1][Key2][Key3][Key4][Key5][Key6].update({varName:varValue})
                                                        for varName in childDict[Key1][Key2][Key3][Key4][Key5][Key6]:
                                                            if not newDict[Key1][Key2][Key3][Key4][Key5][Key6].has_key(varName):
                                                                varValue = childDict[Key1][Key2][Key3][Key4][Key5][Key6][varName]
                                                                newDict[Key1][Key2][Key3][Key4][Key5][Key6].update({varName:varValue})      
                                                    else:
                                                        if nKeys >= 7:
                                                            Key7 = newSet[6]
                                                            newDict[Key1][Key2][Key3][Key4][Key5][Key6].update({Key7:{}})
                                                            if nKeys == 7:
                                                                for varName in parentDict[Key1][Key2][Key3][Key4][Key5][Key6][Key7]:
                                                                    varValue = parentDict[Key1][Key2][Key3][Key4][Key5][Key6][Key7][varName]
                                                                    newDict[Key1][Key2][Key3][Key4][Key5][Key6][Key7].update({varName:varValue})
                                                                for varName in childDict[Key1][Key2][Key3][Key4][Key5][Key6][Key7]:
                                                                    if not newDict[Key1][Key2][Key3][Key4][Key5][Key6][Key7].has_key(varName):
                                                                        varValue = childDict[Key1][Key2][Key3][Key4][Key5][Key6][Key7][varName]
                                                                        newDict[Key1][Key2][Key3][Key4][Key5][Key6].update({varName:varValue})
                                                                else:
                                                                    print 'innerJoinDictDB number of Keys exceeds 7 - cannot complete inner join'
                                                                                                          
    return newDict

def createUniqueListFromTwoNewLists(listOne = [], listTwo = []):
    '''
    This function was developed, primarilly to create a new header
    relating to two dictionaries that are going to be combined in an
    an inner join.
    '''
    newList = []
    for item in listOne:
        if not item in newList:
            newList.append(item)
    for item in listTwo:
        if not item in newList:
            newList.append(item)
    return newList
