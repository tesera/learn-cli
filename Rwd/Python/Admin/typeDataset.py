import makeDD
import fileUtilities
from types import *

def typeDataset(fileList = [], dataDict = {}, tableName = '', errorFilePath = ''):
    '''
    Created by Ian and Mishtu
    August 27, 2012
    
    Notes:
    fileList is a csv text file with all data in string format
    dataDict is a standard data dictionary format created in makeDD
    tableName refers to table in data dictionary
    errorFileName is the name of the file to which errors are written

    The dataDict format is as follows:
    {tableName:{varName:varType}}

    This is incompatible with the format used in typeDataset_v2    
    '''
    #i is the row, end_i is the number of rows
    #j is the column, end_j is the number of columns
    end_i = len(fileList)
    end_j = len(fileList[0])
    if not dataDict.has_key(tableName):
        print 'Table name', tableName, 'not found in dataDict'
    #start making conversions column by column
    for j in range(0,end_j,1):
        varName = fileList[0][j]
        #print varName
        if not dataDict[tableName].has_key(varName):
            print 'Table name', tableName, 'missing variable', varName
        varType = dataDict[tableName][varName]
        #print varName, varType
        if not varType == 'string':
            #for each row change the variable type
            #If not a string then it is either an integer or a float
            #Can set type to float in either case
            #Use try float for error detection (i.e. if some other type that can not be converted is in the column)
            for i in range(1, end_i,1):
                try:
                    float(fileList[i][j])
                    #Convert to float
                    fileList[i][j] = float(fileList[i][j])
                    if varType == 'integer':
                        fileList[i][j] = int(fileList[i][j])
                except:
                    textLine = 'Table Name: ' + tableName + ' Variable Name: ' + varName + ' Line Number: ' + str(i) + ' Value: ' + fileList[i][j]
                    fileUtilities.writeToFile(textLine, errorFilePath)
    return fileList

def typeDataset_v2(fileList = [], dataDict = {}, tableName = '', errorFilePath = ''):
    '''
    Created by Ian and Mishtu
    August 27, 2012
    
    Notes:
    fileList is a csv text file with all data in string format
    dataDict is a standard data dictionary format created in makeDD
    tableName refers to table in data dictionary
    errorFileName is the name of the file to which errors are written

    Note that the dataDict must be in a format consistent with
    makeDD.dataDictionaryType_2()

    ISM - Oct 2 2012
    This version makes one small change to the original version

    varType = dataDict[tableName][varName]['VARTYPE']

    instead of:
    
    varType = dataDict[tableName][varName]

    This change was nescessetated by a change in the format of the
    dataDict.  The dataDict format is as follows:

    {tableName:{varName:{'NEWVARNAME':newVarName,'VARTYPE':varType,'VARKIND':varKind, 'DESCRIPTION':description}}}
    '''
    #i is the row, end_i is the number of rows
    #j is the column, end_j is the number of columns
    end_i = len(fileList)
    end_j = len(fileList[0])
    if not dataDict.has_key(tableName):
        print 'Table name', tableName, 'not found in dataDict'
    #start making conversions column by column
    for j in range(0,end_j,1):
        varName = fileList[0][j]
        #print varName
        if not dataDict[tableName].has_key(varName):
            print 'Table name', tableName, 'missing variable', varName
            print 'Variable number:', j, 'lone 0 of the datafile'
        varType = dataDict[tableName][varName]['VARTYPE']
        varDefault = dataDict[tableName][varName]['VARDEFAULT']
        #print varName, varType
        if not varType == 'string' or not varType == 'character' or not varType == 'nominal' or not varType == '':
            #Then the variable type must be changed from a string format
            #for each row change the variable type
            #If not a string then it is either an integer or a float
            #Can set type to float in either case
            #Use try float for error detection (i.e. if some other type that can not be converted is in the column)
            for i in range(1, end_i,1):
                if varType == 'integer' or varType == 'boolean' or varType == 'dummy' or \
                   varType == 'ordinal' or varType == 'classint' or varType == 'count':
                    if fileList[i][j] == '':
                        fileList[i][j] = int(varDefault)
                    else:
                        try:
                            int(fileList[i][j])
                        except:
                            textLine = 'Not integer, boolean or ordinal type. Table Name: ' , tableName , ' Variable Name:', \
                                       varName, ' Line Number:', str(i), ' Value:', fileList[i][j]
                            fileUtilities.writeToFile(textLine, errorFilePath)
                        else:
                            fileList[i][j] = int(fileList[i][j])
                if varType ==  'float' or varType == 'continuous' or varType == 'proportion':
                    if fileList[i][j] == '':
                        if varDefault == '':
                            fileList[i][j] == float(0)
                        else:
                            fileList[i][j] = float(varDefault)
                    else:
                        try:
                            float(fileList[i][j])
                        except:
                            textLine = 'Not float or continuous type. Table Name: ' , tableName , ' Variable Name:', \
                                       varName, ' Line Number:', str(i), ' Value:', fileList[i][j]
                            fileUtilities.writeToFile(textLine, errorFilePath)
                        else:
                            fileList[i][j] = float(fileList[i][j])
    return fileList


