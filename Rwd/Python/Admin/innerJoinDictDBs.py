from copy import deepcopy

def getDictKeySetValuesList(myDict = {}, keyVarnames=[]):
    '''
    Created by Ian Moss December 5 2012 as an extension of previous dictionaryDB handling
    utilities developed by Ian Moss

    The inputs are:

    1. The dictionary (myDict) from which the unique combinations of keys are to bee extracted.
    2. The list of key variable names (in the order that they occur) used top establish the order of the key values in the dictionary.   

    This function creates a list of all the unique combinations of keys in data dictionary
    By design the data dictionary is already organized around unique combinations of keys

    Modified Dec 6 2013
        
    '''
    newKeyValueList = []
    nKeys = len(keyVarnames)
    if nKeys == 0:
        newKeyValueList = myDict.keys()
    if nKeys >= 1:
        newKeyValueList1 = myDict.keys()
        newKeyValueList1.sort()
        for Key1 in newKeyValueList1:
            if nKeys == 1:
                newKeyValueList=newKeyValueList1
            else:
                newKeyValueList2 = myDict[Key1].keys()
                newKeyValueList2.sort()
                for Key2 in newKeyValueList2:
                    if nKeys == 2:
                        newKeyValueList.append([Key1, Key2])                          
                    else:
                        newKeyValueList3 = myDict[Key1][Key2].keys()
                        newKeyValueList.sort()
                        for Key3 in newKeyValueList3:
                            if nKeys == 3:
                                newKeyValueList.append([Key1, Key2, Key3])
                            else:
                                newKeyValueList4 = myDict[Key1][Key2][Key3].keys()
                                newKeyValueList4.sort()
                                for Key4 in newKeyValueList4:
                                    if nKeys == 4:
                                        newKeyValueList.append([Key1, Key2, Key3, Key4])
                                    else:
                                        newKeyValueList5 = myDict[Key1][Key2][Key3][Key4].keys()
                                        newKeyValueList5.sort()
                                        for Key5 in newKeyValueList5:
                                            if nKeys == 5:
                                                newKeyValueList.append([Key1, Key2, Key3, Key4, Key5])
                                            else:
                                                newKeyValueList6 = myDict[Key1][Key2][Key3][Key4][Key5].keys()
                                                newKeyValueList6.sort()
                                                for Key6 in newKeyValueList6:
                                                    if nKeys == 6:
                                                        newKeyValueList.append([Key1, Key2, Key3, Key4, Key5, Key6])
                                                    else:
                                                        newKeyValueList7 = myDict[Key1][Key2][Key3][Key4][Key5][Key6].keys()
                                                        newKeyValueList7.sort()
                                                        for Key7 in newKeyValueList7:
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


def appendInnerJoinKeyValueLists(keyValueList1=[[]], keyValueList2=[[]]):
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
    commonKeyValueList = deepcopy(keyValueList1)
    for keyValueList in keyValueList2:
        if not keyValueList in keyValueList2:
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
        2. Have same keys, between parentDic and childDict, but have different variables (1-1 join)
        3. For every key in parent dict, there are several keys (other key variable) in childDict, and other 
        non-key variables in childDict (inner join)
        
        If parentDict and childDict do not match the above 3 conditions, there are no guarantees
        as to what the code will output. 
        
    '''
    newDict = {}
    nSets = len(keySetList)
    if type(keySetList[0])==list:
        nKeys = len(keySetList[0])
    else:
        nKeys = -1
    #print nSets, nKeys
    if nKeys == -1:
        #The dictionary is a one line dictionary
        for Key1 in keySetList:
            newDict.update({Key1:{}})
            for varName in parentDict[Key1]:
                varValue = parentDict[Key1][varName]
                newDict[Key1].update({varName:varValue})
            for varName in childDict[Key1]:
                if not newDict[Key1].has_key(varName):
                    varValue = childDict[Key1][varName]
                    newDict[Key1].update({varName:varValue})
    else:
        for newSet in keySetList:
            nKeysCrossValidate = len(newSet)
            if not nKeysCrossValidate == nKeys:
                print 'innerJoinDictDBs.extractDictDBForKeySetsList()'
                print 'Inconsistent number of unique keys in dataset'
                print 'nKeys expected:', nKeys, 'but nKeysCrossValidate:', nKeysCrossValidate
            if nKeys < 1:
                print 'innerJoinDictDBs.extractDictDBForKeySetsList()'
                print 'Key set is empty:', newSet
                print 'Cannot process inner join'
            else:
                Key1 = newSet[0]
                if not newDict.has_key(Key1):
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
                        if not newDict[Key1].has_key(Key2):
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
                                if not newDict[Key1][Key2].has_key(Key3):
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
                                        if not newDict[Key1][Key2][Key3].has_key(Key4):
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
                                                if not newDict[Key1][Key2][Key3][Key4].has_key(Key5):
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
                                                        if not newDict[Key1][Key2][Key3][Key4][Key5].has_key(Key6):
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
                                                            if not newDict[Key1][Key2][Key3][Key4][Key5][Key6].has_key(Key7):
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

def createNewLinkTableIndexFromKeyComboList(keyVarNamesList = [], keyValueComboList = [[]]):
    '''
    '''
    linkDict = {}
    nKeyComboCount = len(keyValueComboList)
    nVarNamesCount = len(keyVarNamesList)
    linkDictKeyVarNameList = ['UID']
    for nKeyCombo in range(0,nKeyComboCount,1):
        linkDict.update({nKeyCombo:{}})
        nVarCount = len(keyValueComboList[nKeyCombo])
        if not nVarCount == nVarNamesCount:
            print ' innerJoinDictDBs.cerateNewLinkTableIndexFromKeyComboList'
            print ' the numbre of variables in the keyValueCombo list \n does not correspond with the number in the keyVarNamesList'
            print ' linkTable error'
        for varNo in range(0,nVarNamesCount,1):
            varName = keyVarNamesList[varNo]
            varValue = keyValueComboList[nKeyCombo][varNo]
            linkDict[nKeyCombo].update({varName:varValue})
    return linkDictKeyVarNameList, linkDict

def extractDictDBDataUsingLinkDictTable(dataDict = {}, linkDict = {}, keyVarNameList = [], mismatchNotification = 'Yes', tableName = ''):
    '''       
    '''
    newDict = {}
    setListKeys = linkDict.keys()
    setListKeys.sort()
    nSets = len(setListKeys)
    for newSet in setListKeys:
        keySet = []
        for varName in keyVarNameList:
            varValue = linkDict[newSet][varName]
            keySet.append(varValue)
        nKeys = len(keySet)
        if not newDict.has_key(newSet):
            newDict.update({newSet:{}})
        if nKeys >= 1:
            Key1 = keySet[0]
        if dataDict.has_key(Key1):
            if nKeys == 1:
                for varName in dataDict[Key1]:
                    if not newDict[newSet].has_key(varName):
                        varValue = dataDict[Key1][varName]
                        newDict[newSet].update({varName:varValue})
            else:
                if nKeys >= 2:
                    Key2 = keySet[1]
                if dataDict[Key1].has_key(Key2):
                    if nKeys == 2:
                        for varName in dataDict[Key1][Key2]:
                            if not newDict[newSet].has_key(varName):
                                varValue = dataDict[Key1][Key2][varName]
                                newDict[newSet].update({varName:varValue})
                    else:
                        if nKeys >= 3:
                            Key3 = keySet[2]
                        if dataDict[Key1][Key2].has_key(Key3):
                            if nKeys == 3:
                                for varName in dataDict[Key1][Key2][Key3]:
                                    if not newDict[newSet].has_key(varName):
                                        varValue = dataDict[Key1][Key2][Key3][varName]
                                        newDict[newSet].update({varName:varValue})
                            else:
                                if nKeys >= 4:
                                    Key4 = keySet[3]
                                if dataDict[Key1][Key2][Key3].has_key(Key4):
                                    if nKeys == 4:
                                        for varName in dataDict[Key1][Key2][Key3][Key4]:
                                            if not newDict[newSet].has_key(varName):
                                                varValue = dataDict[Key1][Key2][Key3][Key4][varName]
                                                newDict[newSet].update({varName:varValue})
                                    else:
                                        if nKeys >= 5:
                                            Key5 = keySet[4]
                                        if dataDict[Key1][Key2][Key3][Key4].has_key(Key5):
                                            if nKeys == 5:
                                                for varName in dataDict[Key1][Key2][Key3][Key4][Key5]:
                                                    if not newDict[newSet].has_key(varName):
                                                        varValue = dataDict[Key1][Key2][Key3][Key4][Key5][varName]
                                                        newDict[newSet].update({varName:varValue})
                                            else:
                                                if nKeys >= 6:
                                                    Key6 = keySet[5]
                                                    if dataDict[Key1][Key2][Key3][Key4][Key5].has_key(Key6):
                                                        if nKeys == 6:
                                                            for varName in dataDict[Key1][Key2][Key3][Key4][Key5][Key6]:
                                                                if not newDict[newSet].has_key(varName):
                                                                    varValue = dataDict[Key1][Key2][Key3][Key4][Key5][Key6][varName]
                                                                    newDict[newSet].update({varName:varValue})
                                                        else:
                                                            if nKeys >= 7:
                                                                Key7 = keySet[6]
                                                            if dataDict[Key1][Key2][Key3][Key4][Key5][Key6].has_key(Key7):
                                                                if nKeys == 7:
                                                                    for varName in dataDict[Key1][Key2][Key3][Key4][Key5][Key6][key7]:
                                                                        if not newDict[newSet].has_key(varName):
                                                                            varValue = dataDict[Key1][Key2][Key3][Key4][Key5][Key6][Key7][varName]
                                                                            newDict[newSet].update({varName:varValue})
                                                                else:
                                                                    print 'innerJoinDictDB.extractDictDBDataUsingLinkTable number of Keys exceeds 7 - cannot complete link table extract'
                                                            else:
                                                                if mismatchNotification == 'Yes':
                                                                    print 'innerJoinDictDB.extractDictDBDataUsingLinkTable'
                                                                    print tableName, Key1, Key2, Key3, Key4, Key5, Key6, 'does not have Key7 equal to:', Key7
                                                    else:
                                                        if mismatchNotification == 'Yes':
                                                            print 'innerJoinDictDB.extractDictDBDataUsingLinkTable'
                                                            print tableName, Key1, Key2, Key3, Key4, Key5, 'does not have Key6 equal to:', Key6
                                        else:
                                            if mismatchNotification == 'Yes':
                                                print 'innerJoinDictDB.extractDictDBDataUsingLinkTable'
                                                print tableName, Key1, Key2, Key3, Key4, 'does not have Key5 equal to:', Key5
                                else:
                                    if mismatchNotification == 'Yes':
                                        print 'innerJoinDictDB.extractDictDBDataUsingLinkTable'
                                        print tableName, Key1, Key2, Key3, 'does not have Key4 equal to:', Key4
                        else:
                            if mismatchNotification == 'Yes':
                                print 'innerJoinDictDB.extractDictDBDataUsingLinkTable'
                                print tableName, Key1, Key2, 'does not have Key3 equal to:', Key3
                else:
                    if mismatchNotification == 'Yes':
                        print 'innerJoinDictDB.extractDictDBDataUsingLinkTable'
                        print tableName, Key1, 'does not have Key2 equal to:', Key2               
        else:
            if mismatchNotification == 'Yes':
                print 'innerJoinDictDB.extractDictDBDataUsingLinkTable'
                print tableName, 'does not have Key1 equal to:', Key1
    return newDict                                                    
                                                                    
def collapseDictKeysUsingALinkTable(dataDict = {}, linkDict = {}, keyVarNameList = [], mismatchNotification = 'Yes', tableName = ''):
    '''       
    '''
    newDict = {}
    setListKeys = linkDict.keys()
    setListKeys.sort()
    nSets = len(setListKeys)
    for newSet in setListKeys:
        keySet = []
        for varName in keyVarNameList:
            varValue = linkDict[newSet][varName]
            keySet.append(varValue)
        nKeys = len(keySet)
        if not newDict.has_key(newSet):
            newDict.update({newSet:{}})
        if nKeys >= 1:
            Key1 = keySet[0]
        if dataDict.has_key(Key1):
            if nKeys == 1:
                subsetDict = dataDict[Key1]
                newDict[newSet].update(subsetDict)
            else:
                if nKeys >= 2:
                    Key2 = keySet[1]
                if dataDict[Key1].has_key(Key2):
                    if nKeys == 2:
                        subsetDict = dataDict[Key1][Key2]
                        newDict[newSet].update(subsetDict)
                    else:
                        if nKeys >= 3:
                            Key3 = keySet[2]
                        if dataDict[Key1][Key2].has_key(Key3):
                            if nKeys == 3:
                                subsetDict = dataDict[Key1][Key2][Key3]
                                newDict[newSet].update(subsetDict)
                            else:
                                if nKeys >= 4:
                                    Key4 = keySet[3]
                                if dataDict[Key1][Key2][Key3].has_key(Key4):
                                    if nKeys == 4:
                                        subsetDict = dataDict[Key1][Key2][Key3][Key4]
                                        newDict[newSet].update(subsetDict)
                                    else:
                                        if nKeys >= 5:
                                            Key5 = keySet[4]
                                        if dataDict[Key1][Key2][Key3][Key4].has_key(Key5):
                                            if nKeys == 5:
                                                subsetDict = dataDict[Key1][Key2][Key3][Key4][Key5]
                                                newDict[newSet].update(subsetDict)
                                            else:
                                                if nKeys >= 6:
                                                    Key6 = keySet[5]
                                                    if dataDict[Key1][Key2][Key3][Key4][Key5].has_key(Key6):
                                                        if nKeys == 6:
                                                            subsetDict = dataDict[Key1][Key2][Key3][Key4][Key5][Key6]
                                                            newDict[newSet].update(subsetDict)
                                                        else:
                                                            if nKeys >= 7:
                                                                Key7 = keySet[6]
                                                            if dataDict[Key1][Key2][Key3][Key4][Key5][Key6].has_key(Key7):
                                                                if nKeys == 7:
                                                                    subsetDict = dataDict[Key1][Key2][Key3][Key4][Key5][Key6][Key7]
                                                                    newDict[newSet].update(subsetDict)
                                                                else:
                                                                    print 'innerJoinDictDB.extractDictDBDataUsingLinkTable number of Keys exceeds 7 - cannot complete link table extract'
                                                            else:
                                                                if mismatchNotification == 'Yes':
                                                                    print 'innerJoinDictDB.extractDictDBDataUsingLinkTable'
                                                                    print tableName, Key1, Key2, Key3, Key4, Key5, Key6, 'does not have Key7 equal to:', Key7
                                                    else:
                                                        if mismatchNotification == 'Yes':
                                                            print 'innerJoinDictDB.extractDictDBDataUsingLinkTable'
                                                            print tableName, Key1, Key2, Key3, Key4, Key5, 'does not have Key6 equal to:', Key6
                                        else:
                                            if mismatchNotification == 'Yes':
                                                print 'innerJoinDictDB.extractDictDBDataUsingLinkTable'
                                                print tableName, Key1, Key2, Key3, Key4, 'does not have Key5 equal to:', Key5
                                else:
                                    if mismatchNotification == 'Yes':
                                        print 'innerJoinDictDB.extractDictDBDataUsingLinkTable'
                                        print tableName, Key1, Key2, Key3, 'does not have Key4 equal to:', Key4
                        else:
                            if mismatchNotification == 'Yes':
                                print 'innerJoinDictDB.extractDictDBDataUsingLinkTable'
                                print tableName, Key1, Key2, 'does not have Key3 equal to:', Key3
                else:
                    if mismatchNotification == 'Yes':
                        print 'innerJoinDictDB.extractDictDBDataUsingLinkTable'
                        print tableName, Key1, 'does not have Key2 equal to:', Key2               
        else:
            if mismatchNotification == 'Yes':
                print 'innerJoinDictDB.extractDictDBDataUsingLinkTable'
                print tableName, 'does not have Key1 equal to:', Key1
    return newDict
                                    
def selectRowsInKeySetsList(parentDict ={},keySetList=[]):
    '''
    Created December 14, 2010 by Ian Moss
    Rows are observations are selected based on those in keySet list that have been extracted using getDictKeySetValuesList()
        
    '''
    newDict = {}
    nSets = len(keySetList)
    nKeys = len(keySetList[0])
    if nKeys <= 0:
        #The dictionary is a one line dictionary
        for varName in parentDict:
            varValue = parentDict[varName]
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
                else:
                    if nKeys >= 2:
                        Key2 = newSet[1]
                        newDict[Key1].update({Key2:{}})
                        if nKeys == 2:
                            for varName in parentDict[Key1][Key2]:
                                varValue = parentDict[Key1][Key2][varName]
                                newDict[Key1][Key2].update({varName:varValue})
                        else:
                            if nKeys >= 3:
                                Key3 = newSet[2]
                                newDict[Key1][Key2].update({Key3:{}})
                                if nKeys == 3:
                                    for varName in parentDict[Key1][Key2][Key3]:
                                        varValue = parentDict[Key1][Key2][Key3][varName]
                                        newDict[Key1][Key2][Key3].update({varName:varValue})
                                else:
                                    if nKeys >= 4:
                                        Key4 = newSet[3]
                                        newDict[Key1][Key2][Key3].update({Key4:{}})
                                        if nKeys == 4:
                                            for varName in parentDict[Key1][Key2][Key3][Key4]:
                                                varValue = parentDict[Key1][Key2][Key3][Key4][varName]
                                                newDict[Key1][Key2][Key3][Key4].update({varName:varValue})
                                        else:
                                            if nKeys >= 5:
                                                Key5 = newSet[4]
                                                newDict[Key1][Key2][Key3][Key4].update({Key5:{}})
                                                if nKeys == 5:
                                                    for varName in parentDict[Key1][Key2][Key3][Key4][Key5]:
                                                        varValue = parentDict[Key1][Key2][Key3][Key4][Key5][varName]
                                                        newDict[Key1][Key2][Key3][Key4][Key5].update({varName:varValue})
                                                else:
                                                    if nKeys >= 6:
                                                        Key6 = newSet[5]
                                                        newDict[Key1][Key2][Key3][Key4][Key5].update({Key6:{}})
                                                    if nKeys == 6:
                                                        for varName in parentDict[Key1][Key2][Key3][Key4][Key5][Key6]:
                                                            varValue = parentDict[Key1][Key2][Key3][Key4][Key5][Key6][varName]
                                                            newDict[Key1][Key2][Key3][Key4][Key5][Key6].update({varName:varValue})    
                                                    else:
                                                        if nKeys >= 7:
                                                            Key7 = newSet[6]
                                                            newDict[Key1][Key2][Key3][Key4][Key5][Key6].update({Key7:{}})
                                                            if nKeys == 7:
                                                                for varName in parentDict[Key1][Key2][Key3][Key4][Key5][Key6][Key7]:
                                                                    varValue = parentDict[Key1][Key2][Key3][Key4][Key5][Key6][Key7][varName]
                                                                    newDict[Key1][Key2][Key3][Key4][Key5][Key6][Key7].update({varName:varValue})
                                                                else:
                                                                    print 'innerJoinDictDB number of Keys exceeds 7 - cannot complete inner join'
                                                                                                          
    return newDict
