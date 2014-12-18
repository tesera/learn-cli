def additive_nested_key_multiple_item_dictionary(NewDict,KeyVarnames,TwoDList):
    '''
    Created Jan 23, 2006
    Updated June 23, 2006
    
    This produces a dictionary as follows:
    
    A list of KeyVarnames is provided as follows:
    [KeyVar1, KeyVar2, KeyVar3, KeyVar4]
    ... up to 7 levels with each key being on a separate level.

    These are used to transform the dataset from a list format
    to a dictionary format as follows:

    {KeyVar1:{KeyVar2:{KeyVar3:{Var1:Value,Var2:Value...}}}}

    The items specified as keys are not repeated in the variable list.
    '''
    header = TwoDList[0]
    headerLength = len(header)
    #print headerLength
    #print header
    i=0
    for line in TwoDList:
        lineLength = len(line)
        if not i==0 and not line ==[]:
            j=0
            NKList=[]
            if not KeyVarnames == []:
                for Key in KeyVarnames:
                    k=0
                    for item in header:
                        if item == Key:
                            if j == 0:
                                if NewDict.has_key(line[k])==False:
                                    NewDict.update({line[k]:{}})
                                NKList.append(line[k])
                                j=j+1
                                break
                            else:
                                if j == 1:
                                    if NewDict[NKList[0]].has_key(line[k])==False:
                                        NewDict[NKList[0]].update({line[k]:{}})
                                    NKList.append(line[k])
                                    j=j+1
                                    break
                                else:
                                    if j == 2:
                                        if NewDict[NKList[0]][NKList[1]].has_key(line[k])==False:
                                            NewDict[NKList[0]][NKList[1]].update({line[k]:{}})
                                        NKList.append(line[k])
                                        j=j+1
                                        break
                                    else:
                                        if j == 3:
                                            if NewDict[NKList[0]][NKList[1]][NKList[2]].has_key(line[k])==False:
                                                NewDict[NKList[0]][NKList[1]][NKList[2]].update({line[k]:{}})
                                            NKList.append(line[k])
                                            j=j+1
                                            break
                                        else:
                                            if j == 4:
                                                if NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]].has_key(line[k])==False:
                                                    NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]].update({line[k]:{}})
                                                NKList.append(line[k])
                                                j=j+1
                                                break
                                            else:
                                                if j == 5:
                                                    if NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]][NKList[4]].has_key(line[k])==False:
                                                        NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]][NKList[4]].update({line[k]:{}})
                                                    NKList.append(line[k])
                                                    j=j+1
                                                    break
                                                else:
                                                    if j == 6:
                                                        if NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]][NKList[4]][NKList[5]].has_key(line[k])==False:
                                                            NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]][NKList[4]][NKList[5]].update({line[k]:{}})
                                                        NKList.append(line[k])
                                                        j=j+1
                                                        break

                                                    
                        k=k+1
            k=0
            #print NewDict.keys()
            for item in header:
                flag = 'True'
                if not lineLength == headerLength:
                    flag = 'False'
                    print 'Header item not found in line while constructing dictionary'
                    print 'Item k', k, 'in header'
                    print header
                    print 'line:'
                    print line
                    print 'Line 965 in READv1'
                for key in KeyVarnames:
                    if key == item:
                        flag = 'False'
                        break
                if flag == 'True':
                    if j == 0:
                        NewDict.update({item:line[k]})
                    else:
                        if j == 1:
                            NewDict[NKList[0]].update({item:line[k]})
                        else:
                            if j == 2:
                                #print NKList[0], NKList[1], item, line[k]
                                NewDict[NKList[0]][NKList[1]].update({item:line[k]})
                            else:
                                if j == 3:
                                    NewDict[NKList[0]][NKList[1]][NKList[2]].update({item:line[k]})
                                else:
                                    if j == 4:
                                        NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]].update({item:line[k]})
                                    else:
                                        if j == 5:
                                            NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]][NKList[4]].update({item:line[k]})
                                        else:
                                            if j == 6:
                                                NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]][NKList[4]][NKList[5]].update({item:line[k]})
                                            else:
                                                if j == 7:
                                                    NewDict[NKList[0]][NKList[1]][NKList[2]][NKList[3]][NKList[4]][NKList[5]][NKList[6]].update({item:line[k]})
                k=k+1
        i=i+1
    return NewDict

def find_list_of_items_in_mutilevel_dictionary(someDict ={}, KeyVarValueList = [], varNameList = []):
    '''
    The KeyVarValueList must have the var values listed in the same order as the keys in someDict.
    The VarName must be in a string format and is the name of the variable to be found.
    The main advantage of this function is that it checks for the variable names in the
    KeyVarValueList and prints an error statement if it can not be found in someDict.
    June 5, 2008
    '''
    varValueList = []
    newDict = {}
    end_i = len(KeyVarValueList)
    if end_i == 0:
        for varName in varNameList:
            if someDict.has_key(varName):
                varValue = someDict[Key0][varName]
                varValueList.append(varValue)
            else:
                print 'for KeyVarValueList', KeyVarValueList, 'varName', varName, 'not found in dictionary'
    else:
        for i in range(0,end_i,1):
            if i == 0:
                Key0 = KeyVarValueList[0]
                if someDict.has_key(Key0):
                    if i == end_i-1:
                        for varName in varNameList:
                            if someDict[Key0].has_key(varName):
                                varValue = someDict[Key0][varName]
                                varValueList.append(varValue)
                            else:
                                print 'for KeyVarValueList', KeyVarValueList, 'varName', varName, 'not found in dictionary'
                    else:
                        if i == 1:
                            Key1 = KeyVarValueList[1]
                            if someDict[Key0].has_key(Key1):
                                if i == end_i-1:
                                    for varName in varNameList:
                                        if someDict[Key0][Key1].has_key(VarName):
                                            varValue = someDict[Key0][Key1][varName]
                                            varValueList.append(varValue)
                                        else:
                                            print 'for KeyVarValueList', KeyVarValueList, 'varName', varName, 'not found in dictionary'
                                else:
                                    if i == 2:
                                        Key2 = KeyVarValueList[2]
                                        if someDict[Key0][Key1].has_key(Key2):
                                            if i == end_i-1:
                                                for varName in varNameList:
                                                    if someDict[Key0][Key1][Key2].has_key(varName):
                                                        varValue = someDict[Key0][Key1][Key2][varName]
                                                        varValueList.append(varValue)
                                                    else:
                                                        print 'for KeyVarValueList', KeyVarValueList, 'varName', varName, 'not found in dictionary'
                                            else:
                                                if i == 3:
                                                    Key3 = KeyVarValueList[3]
                                                    if someDict[Key0][Key1][Key2].has_key(Key3):
                                                        if i == end_i-1:
                                                            for varName in varNameList:
                                                                if someDict[Key0][Key1][Key2][Key3].has_key(varName):
                                                                    varValue = someDict[Key0][Key1][Key2][Key3][varName]
                                                                    varValueList.append(varValue)
                                                                else:
                                                                    print 'for KeyVarValueList', KeyVarValueList, 'varName', varName, 'not found in dictionary'
                                                        else:
                                                            if i == 4:
                                                                Key4 = KeyVarValueList[4]
                                                                if someDict[Key0][Key1][Key2][Key3].has_key(Key4):
                                                                    if i == end_i-1:
                                                                        for varName in varNameList:
                                                                            if someDict[Key0][Key1][Key2][Key3][Key4].has_key(varName):
                                                                                varValue = someDict[Key0][Key1][Key2][Key3][Key4][varName]
                                                                                varValueList.append(varValue)
                                                                            else:
                                                                                print 'for KeyVarValueList', KeyVarValueList, 'varName', varName, 'not found in dictionary'
                                                                    else:
                                                                        if i == 5:
                                                                            Key5 = KeyVarValueList[5]
                                                                            if someDict[Key0][Key1][Key2][Key3][Key4].has_key(Key5):
                                                                                if i == end_i:
                                                                                    for varName in varNameList:
                                                                                        if someDict[Key0][Key1][Key2][Key3][Key4][Key5].has_key(varName):
                                                                                            varValue = someDict[Key0][Key1][Key2][Key3][Key4][Key5][varName]
                                                                                            varValueList.append(varValue)
                                                                                        else:
                                                                                            print 'for KeyVarValueList', KeyVarValueList, 'varName', varName, 'not found in dictionary'
                                                                                else:                                                   
                                                                                    if i == 6:
                                                                                        Key6 = KeyVarValueList[6]
                                                                                        if someDict[Key0][Key1][Key2][Key3][Key4][Key5].has_key(Key6):    
                                                                                            if i == end_i - 1:
                                                                                                for varName in varNameList:
                                                                                                    if someDict[Key0][Key1][Key2][Key3][Key4][Key5].has_key(varName):
                                                                                                        varValue = someDict[Key0][Key1][Key2][Key3][Key4][Key5][varName]
                                                                                                        varValueList.append(varValue)
                                                                                                    else:
                                                                                                        print 'for KeyVarValueList', KeyVarValueList, 'varName', varName, 'not found in dictionary'
                                                                                        else:
                                                                                            print 'someDict in dictionaryDBUtilities.find_list_of_items_in_mutilevel_dictionary'
                                                                                            print ' missing Key6, KeyVarValueList:'
                                                                                            print Key6, KeyVarValueList
                                                                            else:
                                                                                print 'someDict in dictionaryDBUtilities.find_list_of_items_in_mutilevel_dictionary'
                                                                                print ' missing Key5, KeyVarValueList:'
                                                                                print Key5, KeyVarValueList
                                                                else:
                                                                    print 'someDict in dictionaryDBUtilities.find_list_of_items_in_mutilevel_dictionary'
                                                                    print ' missing Key4, KeyVarValueList:'
                                                                    print Key4, KeyVarValueList
                                                    else:
                                                        print 'someDict in dictionaryDBUtilities.find_list_of_items_in_mutilevel_dictionary'
                                                        print ' missing Key3, KeyVarValueList:'
                                                        print Key3, KeyVarValueList
                                        else:
                                            print 'someDict in dictionaryDBUtilities.find_list_of_items_in_mutilevel_dictionary'
                                            print ' missing Key2, KeyVarValueList:'
                                            print Key2, KeyVarValueList
                            else:
                                print 'someDict in dictionaryDBUtilities.find_list_of_items_in_mutilevel_dictionary'
                                print ' missing Key1, KeyVarValueList:'
                                print Key1, KeyVarValueList                 
                else:
                    print 'someDict in dictionaryDBUtilities.find_list_of_items_in_mutilevel_dictionary'
                    print ' missing Key0, KeyVarValueList:'
                    print Key0, KeyVarValueList                                                     
                                            
    return varValueList
