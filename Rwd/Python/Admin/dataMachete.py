#!/usr/bin/env python
"""
dataMachete: ported from Ian Moss modules readCSV, writeCSV, makeDD, typeDataset, fileUtilities, 
dictionaryDBUtilities to work with TSIAnalytics. Original modules (c) Ian Moss 2006-2012

CurrentRevisionDate:20121105


Author(s): Ian Moss
Contact: ian.moss@tesera.com
collated by: Mishtu Banerjee, mishtu.banerjee@tesera.com

Copyright: The Author(s)
License: Distributed under MIT License
    [http://opensource.org/licenses/mit-license.html]



Dependencies:
    Python interpreter and base libraries
    
""" 
from types import * 
import os
from operator import concat
import numpy
from copy import deepcopy

# ---------- Listarray Input Output and Manipulation Functions ----------
#read_csv_text_file originally in readCSV, (c) Ian Moss, 2006
# write TwoDListsToCSVFile, convertTwoDListToCSVFileFormat,  originally in writeCSV, (c) Ian Moss 2006
# from fileUtilities import newFilePath -- no longer an import, in dataMachete mb

def getListarray(filepath,table_name):
    '''
    From a CSV file create a Listarray data structure. 
    A List array is a 2D array of lists where each line of data is represented as a list
    and the lines of data represented as lists, are themselves organized in a list. 
    The top level list represents the dataset; while the second level lists are
    lines of data. 
    Last modified Jan 23, 2006 to match with changes in dictionary
    format.
    '''

    # This module will read files created using PRINT_MODULE.print_csv().
    #
    file_path = createNewFilePath(filepath, table_name)
    temp_file =open (file_path,'r')
    out_file=[]
    i=0
    for line in temp_file:
        #print i
        x = line.rstrip()
        x = x.split(',')
        out_file.append(x)
    temp_file.close()
    return out_file

def getListArrayBetweenMinMaxLineNos(filepath='',table_name='', fileExtension='', fromLine = 0, toLine = 10000):
    '''
    Developed Oct 21 2013 
    Ian Moss

    This is modified from getListarray to remove quotation
    marks associated with one or more fields.  This routine reads
    the first line (i.e. line 0) in the file and remaining
    lines between the start and end line number.

    This is designed to handle big datasets
    '''
    # This module will read files created using PRINT_MODULE.print_csv().
    # Check if table name includes file extension
    newTableNameList = table_name.split('.')
    if len(newTableNameList) >= 2:
        file_path = createNewFilePath_v2(filepath, table_name, fileExtension)
    else:
        file_path = createNewFilePath_v2(filepath, table_name, fileExtension)
    temp_file =open (file_path,'r')
    out_file=[]
    i=0
    j=0
    for line in temp_file:
        #print i
        x = line.rstrip()
        if i == 0:
            if not line == []:
                out_file.append([])
                if x.startswith('"') and x.endswith('"'):
                    x = x[1:-1]
                x = x.split(',')
                for item in x:
                    if item.startswith('"') and item.endswith('"'):
                        y = item[1:-1]
                    else:
                        y = item
                    out_file[j].append(y)
        else:
            if i >= fromLine and i < toLine:
                if not line == []:
                    j = j + 1
                    out_file.append([])
                    if x.startswith('"') and x.endswith('"'):
                        x = x[1:-1]
                    x = x.split(',')
                    for item in x:
                        if item.startswith('"') and item.endswith('"'):
                            y = item[1:-1]
                        else:
                            y = item
                        out_file[j].append(y)
        i = i + 1
        if i == toLine:
            break
    temp_file.close()
    return out_file

def getListarray_v2(filepath,table_name, fileExtension):
    '''
    Developed March 07 2013
    Ian Moss

    This is modified from getListarray to remove quotation
    marks associated with one or more fields.
    '''
    # This module will read files created using PRINT_MODULE.print_csv().
    # Check if table name includes file extension
    newTableNameList = table_name.split('.')
    if len(newTableNameList) >= 2:
        file_path = createNewFilePath_v2(filepath, table_name, fileExtension)
    else:
        file_path = createNewFilePath_v2(filepath, table_name, fileExtension)
    temp_file =open (file_path,'r')
    out_file=[]
    i=0
    for line in temp_file:
        #print i
        x = line.rstrip()
        if not line == []:
            out_file.append([])
            line = line.replace('"','').strip()
            x = x.split(',')
            for item in x:
                y = item.replace('"','').strip()
                out_file[i].append(y)
            i = i + 1
    temp_file.close()
    return out_file

def getPartialListarray_v2(filepath='',table_name='', fileExtension='.csv', nLines = 1):
    '''
    Developed March 07 2013
    Ian Moss

    This is modified from getListarray to remove quotation
    marks associated with one or more fields.  This routine only
    gets the top nLines of the Listarray.
    '''

    # This module will read files created using PRINT_MODULE.print_csv().
    #
    newFileNameList = table_name.split('.')
    lenFileNameList = len(newFileNameList)
    if lenFileNameList > 1:
        file_path = createNewFilePath_v2(filepath, table_name, fileExtension)
    else:
        file_path = createNewFilePath_v2(filepath, table_name, '')
    temp_file =open (file_path,'r')
    out_file=[]
    i=0
    for line in temp_file:
        #print i
        x = line.rstrip()
        if not line == []:
            out_file.append([])
            line = line.replace('"','').strip()
            x = x.split(',')
            for item in x:
                y = item.replace('"','').strip()
                out_file[i].append(y)
            i = i + 1
            if nLines > 0 and nLines == i:
                break
    temp_file.close()
    return out_file

def countNumberOfLinesInFile(filepath,table_name, fileExtension):
    '''
    Developed November 24 2013
    Ian Moss

    '''
    # This module will read files created using PRINT_MODULE.print_csv().
    # Check if table name includes file extension
    newTableNameList = table_name.split('.')
    if len(newTableNameList) >= 2:
        file_path = createNewFilePath_v2(filepath, table_name, fileExtension)
    else:
        file_path = createNewFilePath_v2(filepath, table_name, fileExtension)
    temp_file =open (file_path,'r')
    i=0
    for line in temp_file:
        i = i + 1
    temp_file.close()
    return i

    
def createNewListFromSelectVariableListAndIdList(keyVarNameList = [], selectVarList = [], dataList = [[]], \
                                                 subsetIntegrity = True, uniqueSubset = True, uniqueCompleteSet = True, printDiagnostics = True):
    '''
    Explanation:
        This routine is used to extract a list of cases that may have one or more key variables and
        also a list aof variables that are to be used in an analysis.  Note that the variables
        selected for analysis may include one or more variables identified as key variables.

    Inputs:
        keyVarSelList       A list of variable names used to identify each case or observation
        selectVarList       A list of X or Y variable names that are to be analyzed
        dataList            The dataset containing the variables (and names in the first row!)
                            in the keyVarSelList and in the selectVarList as well as perhaps other
                            variables.
                            
        The following pertain to dataMachete.getSubsetListIndices():
        
        subsetIntegrety:    This is set equal to True when all of the values contained within the
                            selectSubsetList must also be contained within the completeSetList, otherwise
                            set equal to False (python boolean type). If True then an empty set will be
                            returned if one or more of the items in the selectSubsetList do not match
                            with one of the items in the completeSetList.
        uniqueSubset        This is set equal to True when only the unique list of subset variables
                            is to be enumerated within the completeSetList.
        uniqueCompleteSet   This is set equal to True when the completeSetList must consist of values
                            that are unique within the entire unique set.
        printDiagnostics    This is et equal to True if users of this function desire a warning to be
                            be printed out when any one of the subsetIntegrity, uniqueSubset, or uniqueCompletSet
                            conditions are not met (when set equal to True); if printing is not required
                            then sent equal to false
                            
    Outputs:
        keyVarValueList     A 2D list, [[]], of key variable name value sets identifying each unique case or observation
        selVarValueList     A 2D list, [[]], of variables selected for analysis listed in the same order as the keyVarValueList

    July 31 2013
    '''
    #Initialize keyVarValueList and selVarValueList:
    keyVarValueList = []
    selVarValueList = []
    newKeyVarNameList, keyColNoList = getSubsetListIndices(keyVarNameList, dataList[0], subsetIntegrity, uniqueSubset, uniqueCompleteSet, printDiagnostics)
    newVarNameList, selColNoList = getSubsetListIndices(selectVarList, dataList[0], subsetIntegrity, uniqueSubset, uniqueCompleteSet, printDiagnostics)
    #Initialize the key value lists and the corresponding select value lists
    #These includes an embedded list for proper indexing with typedList 
    lenDataList = len(dataList)
    lenKeyVar = len(newKeyVarNameList)
    lenSelVar = len(newVarNameList)
    #For each line starting in line 1 in the typedList
    for i in range(1, lenDataList, 1):
        #add a new List
        keyVarValueList.append([])
        selVarValueList.append([])
        for j in range(0, lenKeyVar, 1):
            keyColNo = keyColNoList[j]
            keyVarValueList[i-1].append(dataList[i][keyColNo])
        for k in range(0,lenSelVar):
            selColNo = selColNoList[k]
            selVarValueList[i-1].append(dataList[i][selColNo])
    return keyVarValueList, selVarValueList

def createNewListFromSelectVariableList(selectVarList = [], dataList = [[]], \
                                                 subsetIntegrity = True, uniqueSubset = True, uniqueCompleteSet = True, printDiagnostics = True):
    '''
    Explanation:
        This routine is used to extract a list of cases that may have one or more key variables and
        also a list aof variables that are to be used in an analysis.  Note that the variables
        selected for analysis may include one or more variables identified as key variables.

    Inputs:
        selectVarList       A list of X or Y variable names that are to be analyzed
        dataList            The dataset containing the variables (and names in the first row!)
                            in the keyVarSelList and in the selectVarList as well as perhaps other
                            variables.
                            
        The following pertain to dataMachete.getSubsetListIndices():
        
        subsetIntegrety:    This is set equal to True when all of the values contained within the
                            selectSubsetList must also be contained within the completeSetList, otherwise
                            set equal to False (python boolean type). If True then an empty set will be
                            returned if one or more of the items in the selectSubsetList do not match
                            with one of the items in the completeSetList.
        uniqueSubset        This is set equal to True when only the unique list of subset variables
                            is to be enumerated within the completeSetList.
        uniqueCompleteSet   This is set equal to True when the completeSetList must consist of values
                            that are unique within the entire unique set.
        printDiagnostics    This is et equal to True if users of this function desire a warning to be
                            be printed out when any one of the subsetIntegrity, uniqueSubset, or uniqueCompletSet
                            conditions are not met (when set equal to True); if printing is not required
                            then sent equal to false
                            
    Outputs:
        keyVarValueList     A 2D list, [[]], of key variable name value sets identifying each unique case or observation
        selVarValueList     A 2D list, [[]], of variables selected for analysis listed in the same order as the keyVarValueList

    July 31 2013
    '''
    #Initialize keyVarValueList and selVarValueList:
    selVarValueList = []
    newVarNameList, selColNoList = getSubsetListIndices(selectVarList, dataList[0], subsetIntegrity, uniqueSubset, uniqueCompleteSet, printDiagnostics)
    #Initialize the key value lists and the corresponding select value lists
    #These includes an embedded list for proper indexing with typedList 
    lenDataList = len(dataList)
    lenSelVar = len(newVarNameList)
    #For each line starting in line 1 in the typedList
    for i in range(1, lenDataList, 1):
        #add a new List
        selVarValueList.append([])
        for k in range(0,lenSelVar):
            selColNo = selColNoList[k]
            selVarValueList[i-1].append(dataList[i][selColNo])
    return selVarValueList

def getSubsetListIndices(selectSubsetList=[], completeSetList = [], subsetIntegrity = True, uniqueSubset = True, uniqueCompleteSet = True, printDiagnostics = True):
    '''
    Inputs:
        selectSubsetList:   This is a list of items that may be contained within the completeSetList
        completeSetList:    This is a list of items that may contain one or more items in the subset
        subsetIntegrety:    This is set equal to True when all of the values contained within the
                            selectSubsetList must also be contained within the completeSetList, otherwise
                            set equal to False (python boolean type). If True then an empty set will be
                            returned if one or more of the items in the selectSubsetList do not match
                            with one of the items in the completeSetList.
        uniqueSubset        This is set equal to True when only the unique list of subset variables
                            is to be enumerated within the completeSetList.
        uniqueCompleteSet   This is set equal to True when the completeSetList must consist of values
                            that are unique within the entire unique set.
        printDiagnostics    This is et equal to True if users of this function desire a warning to be
                            be printed out when any one of the subsetIntegrity, uniqueSubset, or uniqueCompletSet
                            conditions are not met (when set equal to True); if printing is not required
                            then sent equal to false
    Outputs:
        
                            
    '''
    newColumnNumberList = []
    newVarNameList = []
    continueProcessFlag = True
    if subsetIntegrity == True:
        subsetIntegrityFlag = checkSubsetToCompleteSetIntegrity(selectSubsetList, completeSetList, printDiagnostics)
        if subsetIntegrityFlag == False:
            continueProcessFlag = False
    if uniqueSubset == True:
        uniqueSubsetFlag = checkForUniqueSet(selectSubsetList, printDiagnostics)
        if uniqueSubsetFlag == False:
            continueProcessFlag = False
    if uniqueCompleteSet == True:
        uniqueCompleteSetFlag = checkForUniqueSet(completeSetList, printDiagnostics)
        if uniqueCompleteSetFlag == False:
            continueProcessFlag = False
    if continueProcessFlag == True:
        for selName in selectSubsetList:
            if selName in completeSetList:
                newColumnNumberList.append(completeSetList.index(selName))
                newVarNameList.append(selName)
    return newVarNameList, newColumnNumberList

def checkSubsetToCompleteSetIntegrity(subsetList = [], completeSetList = [], printFalseIntegrity = True):
    '''
    '''
    subsetIntegrityFlag = True
    for item in subsetList:
        if item not in completeSetList:
            subsetIntegrityFlag = False
            if printFalseIntegrity == True:
                print 'dataMachete.checkSubsetToCompleteSetIntegrity'
                print 'not all items in subset found in complete set'
                print 'Item', item, 'missing from complete set'
    return subsetIntegrityFlag

def checkForUniqueSet(setList = [], printFalseUniqueSet = True):
    '''
    '''
    uniqueSetFlag = True
    testSet = []
    for item in setList:
        if not item in testSet:
            testSet.append(item)
        else:
            uniqueSetFlag = False
            if printFalseUniqueSet == True:
                print 'dataMachete.checkForUniqueSet'
                print 'not all items in set are unique'
                print 'Item', item, 'missing from complete set'
    return uniqueSetFlag
    

def getTypedListArray(dataDict = {}, dataTableName = '', dataFilePath = '', dataFileExtension = '', \
                      readErrorFileName = '', readErrorFilePath = '' , readErrorExtension = '.txt'):
    '''
    Inputs
        dataDict is the dictionary containing table name, variable name and variable types (i.e. originalDict or newDict
        dataPath is the file path 
        dataTableName must be a string variable without any file extension but referring to a CSV file
        readErrorFilePath is the read error file path relating to the use of the data dictionary to establish a variable type
        readErrorFileName is the desired name of the read error file without any extension
        fileExtension refers to the type of file, e.g. .txt or .csv
    '''
    #Check if readErrorFileName has file extension
    readErrorFileNameList = readErrorFileName.split('.')
    if len(readErrorFileNameList)>=2:
        dataErrorFilePath = readErrorFilePath + readErrorFileName
    else:
        dataErrorFilePath = readErrorFilePath + readErrorFileName + readErrorExtension
    dataStringList = getListarray_v2(dataFilePath, dataTableName, dataFileExtension)
    dataTypedList = typeDataset_v2(dataStringList, dataDict, dataTableName, dataErrorFilePath)
    return dataTypedList

def getTypedListArray_v2(dataDict = {}, dataTableName = '', dataFilePath = '', dataFileExtension = '', \
                      readErrorFileName = '', readErrorFilePath = '' , readErrorExtension = '.txt'):
    '''
    Inputs
        dataDict is the dictionary containing table name, variable name and variable types (i.e. originalDict or newDict
        dataPath is the file path 
        dataTableName must be a string variable without any file extension but referring to a CSV file
        readErrorFilePath is the read error file path relating to the use of the data dictionary to establish a variable type
        readErrorFileName is the dsired name of the read error file without any extension
        fileExtension refers to the type of file, e.g. .txt or .csv
    '''
    #Check if readErrorFileName has file extension
    readErrorFileNameList = readErrorFileName.split('.')
    if len(readErrorFileNameList)>=2:
        dataErrorFilePath = readErrorFilePath + readErrorFileName
    else:
        dataErrorFilePath = readErrorFilePath + readErrorFileName + readErrorExtension
    dataStringList = getListarray_v2(dataFilePath, dataTableName, dataFileExtension)
    dataTypedList = typeDataset_v2(dataStringList, dataDict, dataTableName, dataErrorFilePath)
    dataTypedList = replaceOldVariableNamesWithNewVariableNamesIn2DListHeader(dataDict, dataTypedList, dataTableName)
    return dataTypedList


def getListArrayAndDictDB(dataTableName = '', filePath = '', errorFilePath = '', keyVariableNameList = [], \
                          originalDict = {}, newDict = {}, fileExtension = '.txt'):
    '''
    WARNING
    
    If not newDict = {} (i.e. newDict is not empty) then the  keyVariableNameList must correspond
        to the list of key variables after the the new variable names in the newDict
        have been substituted for the original variable names in the originalDict.  This is only a problem
        if the names of key variables are to be changed from the original to the new dictionary.

    
    MINIMUM INPUTS

    
    At minimum this function requires the following inputs:

        1. A dataTableName, e.g. 'MYDATA', that is comma delimmeted text file
        2. A file path where 'MYDATA.txt' can be found, e.g. 'C:\\Python26\\DATA\\'
        3. An errorFilePath must be specified to record errors associated with identifying
            different variable types(). Note this must include the fileName plus '.txt' extension.
            e.g. 'C:\\Python26\\ERROR-CHECK.txt'
        4. The keyVariableNameList must be included - it must correspond to the originalVariableNames if
            newDict = {}, otherwise it the new variable names must be used in the keyVariableNameList .
        5. The originalDict must be included.
        6. If not newDict == {} (i.e. it is not left empty) then it will be produced using the new variable names, otherwise
            a blank newDictionary will be returned.

    Function RETURNS

        1. newDataTypedList - this is a 2D file in a list format, [[]], with data types assigned according to the data dictionary
        2. newDataTypedDict - this is a dictionary, {}, {{}}, up to 7 nested levels, with keys assigned according to the keyVariableNameList
        3. missingDict - this is empty unless both originalDict and newDict inputs are null, in which case a new dictionary
            is made from the original file using makeDD.makeNewDataDictionaryFromDataStringFile().
    

    Example of code used to access this module and function, including comments:

    #This filePath contains the locations of the data file and the data dictionary
    #indicating the variable types (comma delimmeted text files)

    filePath = 'E:\\Python26\\IBC\\'
    
    #Get data dictionary to identify variables and variable types

    ibcDataDictTableName = 'DATDICII'   #This is the name of the text file containing the data dictionary without the .txt extension.

    #Get the data dictionaries identifying the variable types

    originalDict, newDict = makeDD.dataDictionaryType_2(filePath,ibcDataDictTableName)

    #Specify location of file where errors are reported in terms of missing variables of invalid assignment of types
    #This is associated with typeDataset.typeDataset_v2()

    ibcErrorFilePath = filePath + 'ERROR-CHECK-IBC.txt'

    oldKeyVariableNameList = ['UID']    #This applies to both the original data 
    newKeyVariableNameList = ['UID']    #This applies to the new variable names and is important when the names of key variables are changed

    ibcDataTableName = 'SUMMARY'        #This is the name of the file containing the actual data without the '.txt' extension

    #input the instructions without any data dictionary
    #Returns a new dataDictionary referred to as missingDict using
    #makeNewDataDictionaryFromDataStringFile()
    
    print 'Geting typedList and typed dictionary without any data dictionary'
    ibcTypedList0, ibcTypedDict0, missingDict = fileImportTool.importAndProcessFile(ibcDataTableName, filePath, ibcErrorFilePath, \
                                                                oldKeyVariableNameList,{}, {})
    
    #Input the instructions without variable name changes, i.e. enter originalDict and not newDict
    #Assuming the originalDict is not empty (i.e. not originalDict == {}) it will return missingDict = {}

    print 'Getting typedList and typed dictionary with original data dictionary'
    ibcTypedList1, ibcTypedDict1, missingDict = fileImportTool.importAndProcessFile(ibcDataTableName, filePath, ibcErrorFilePath, \
                                                                oldKeyVariableNameList,originalDict, {})

    #Input the instructions with the variable name changes, i.e. with newDict
    #The originalKeyVariableName list is not required but the newKeyVariableNameList is required
    #Assuming both the originalDict and the newDict are not empty
    #(i.e. not originalDict == {} and not newDict == {}) it will return missingDict = {}

    print 'Getting typeedList and dictionary with new variableNames'
    ibcTypedList_new2, ibcTypedDict_new2, missingDict = fileImportTool.importAndProcessFile(ibcDataTableName, filePath, ibcErrorFilePath, \
                                                                newKeyVariableNameList, originalDict, newDict)
    POTENTIAL FUTURE DEVELOPMENT

    Another option is to provide for circumstances where no keyVarNames are input requiring that
        a new ID be developed for each row and added to the header.    
    
    '''
    #initialize missing data dictionary (in the event that there is no originalDict and no newDict)
    missingDict = {}
    #Check to make sure there is a non-empty dataTableName
    if dataTableName == '':
        print 'dataMachete.getListArrayAndDictDB()'
        print 'fileImportTool.importAndProcessFile() error'
        print 'No mandatory dataTableName provided to fileImportTool.importAndProcessFile()'
    else:
        #Check to make sure filePath is non-empty
        if filePath == '':
            print 'dataMachete.getListArrayAndDictDB()'
            print 'fileImportTool.importAndProcessFile() error'
            print 'No mandatory filePath provided to fileImportTool.importAndProcessFile()'
        else:
            #Create dataStringList
            if originalDict == {} and newDict == {}:
                #Import file as a string
                dataStringList = getListarray_v2(filePath, dataTableName, fileExtension)
                #There is no data dictionary
                print 'dataMachete.getListArrayAndDictDB()'
                print 'fileImportTool.importAndProcessFile()'
                print 'Table name', dataTableName, 'has no originalDict and no newDict'
                print 'Proceeding to process data according to data types assocated with data in row 1'
                #The variable type() will be established according to row 1 in the dataStringList
                #below row 0 with the list of variable names.
                #missingDict = makeDD.makeNewDataDictionaryFromDataStringFile(dataTableName,dataStringList,{})
                originalDict, newDict = inferDataDictionary_v2(dataTableName, filePath, fileExtension, printTypes = 'YES', nLines = -1)
                newDataTypedList, newDataTypedDict = processFile(dataTableName, filePath, errorFilePath, keyVariableNameList, \
                          originalDict, newDict, fileExtension)
            else:
                newDataTypedList, newDataTypedDict = processFile(dataTableName, filePath, errorFilePath, keyVariableNameList, \
                          originalDict, newDict, fileExtension)
            
    return newDataTypedList, newDataTypedDict

def getLargeDatasetListArrayAndDictDB(dataTableName = '', filePath = '', errorFilePath = '', keyVariableNameList = [], \
                          originalDict = {}, newDict = {}, fileExtension = '', printTypes = 'YES', fromLine = 0, toLine = 10000):
    '''
    WARNING
    
    If not newDict = {} (i.e. newDict is not empty) then the  keyVariableNameList must correspond
        to the list of key variables after the the new variable names in the newDict
        have been substituted for the original variable names in the originalDict.  This is only a problem
        if the names of key variables are to be changed from the original to the new dictionary.

    
    MINIMUM INPUTS

    
    At minimum this function requires the following inputs:

        1. A dataTableName, e.g. 'MYDATA', that is comma delimmeted text file
        2. A file path where 'MYDATA.txt' can be found, e.g. 'C:\\Python26\\DATA\\'
        3. An errorFilePath must be specified to record errors associated with identifying
            different variable types(). Note this must include the fileName plus '.txt' extension.
            e.g. 'C:\\Python26\\ERROR-CHECK.txt'
        4. The keyVariableNameList must be included - it must correspond to the originalVariableNames if
            newDict = {}, otherwise it the new variable names must be used in the keyVariableNameList .
        5. The originalDict must be included.
        6. If not newDict == {} (i.e. it is not left empty) then it will be produced using the new variable names, otherwise
            a blank newDictionary will be returned.

    Function RETURNS

        1. newDataTypedList - this is a 2D file in a list format, [[]], with data types assigned according to the data dictionary
        2. newDataTypedDict - this is a dictionary, {}, {{}}, up to 7 nested levels, with keys assigned according to the keyVariableNameList
        3. missingDict - this is empty unless both originalDict and newDict inputs are null, in which case a new dictionary
            is made from the original file using makeDD.makeNewDataDictionaryFromDataStringFile().
    

    Example of code used to access this module and function, including comments:

    #This filePath contains the locations of the data file and the data dictionary
    #indicating the variable types (comma delimmeted text files)

    filePath = 'E:\\Python26\\IBC\\'
    
    #Get data dictionary to identify variables and variable types

    ibcDataDictTableName = 'DATDICII'   #This is the name of the text file containing the data dictionary without the .txt extension.

    #Get the data dictionaries identifying the variable types

    originalDict, newDict = makeDD.dataDictionaryType_2(filePath,ibcDataDictTableName)

    #Specify location of file where errors are reported in terms of missing variables of invalid assignment of types
    #This is associated with typeDataset.typeDataset_v2()

    ibcErrorFilePath = filePath + 'ERROR-CHECK-IBC.txt'

    oldKeyVariableNameList = ['UID']    #This applies to both the original data 
    newKeyVariableNameList = ['UID']    #This applies to the new variable names and is important when the names of key variables are changed

    ibcDataTableName = 'SUMMARY'        #This is the name of the file containing the actual data without the '.txt' extension

    #input the instructions without any data dictionary
    #Returns a new dataDictionary referred to as missingDict using
    #makeNewDataDictionaryFromDataStringFile()
    
    print 'Geting typedList and typed dictionary without any data dictionary'
    ibcTypedList0, ibcTypedDict0, missingDict = fileImportTool.importAndProcessFile(ibcDataTableName, filePath, ibcErrorFilePath, \
                                                                oldKeyVariableNameList,{}, {})
    
    #Input the instructions without variable name changes, i.e. enter originalDict and not newDict
    #Assuming the originalDict is not empty (i.e. not originalDict == {}) it will return missingDict = {}

    print 'Getting typedList and typed dictionary with original data dictionary'
    ibcTypedList1, ibcTypedDict1, missingDict = fileImportTool.importAndProcessFile(ibcDataTableName, filePath, ibcErrorFilePath, \
                                                                oldKeyVariableNameList,originalDict, {})

    #Input the instructions with the variable name changes, i.e. with newDict
    #The originalKeyVariableName list is not required but the newKeyVariableNameList is required
    #Assuming both the originalDict and the newDict are not empty
    #(i.e. not originalDict == {} and not newDict == {}) it will return missingDict = {}

    print 'Getting typeedList and dictionary with new variableNames'
    ibcTypedList_new2, ibcTypedDict_new2, missingDict = fileImportTool.importAndProcessFile(ibcDataTableName, filePath, ibcErrorFilePath, \
                                                                newKeyVariableNameList, originalDict, newDict)
    POTENTIAL FUTURE DEVELOPMENT

    Another option is to provide for circumstances where no keyVarNames are input requiring that
        a new ID be developed for each row and added to the header.    
    
    '''
    #initialize missing data dictionary (in the event that there is no originalDict and no newDict)
    missingDict = {}
    #Check to make sure there is a non-empty dataTableName
    if dataTableName == '':
        print 'dataMachete.getListArrayAndDictDB()'
        print 'fileImportTool.importAndProcessFile() error'
        print 'No mandatory dataTableName provided to fileImportTool.importAndProcessFile()'
    else:
        #Check to make sure filePath is non-empty
        if filePath == '':
            print 'dataMachete.getListArrayAndDictDB()'
            print 'fileImportTool.importAndProcessFile() error'
            print 'No mandatory filePath provided to fileImportTool.importAndProcessFile()'
        else:
            #Create dataStringList
            dataStringList = getListArrayBetweenMinMaxLineNos(filePath,dataTableName, fileExtension, fromLine, toLine)
            newDataTypedList = [[]]
            newDataTypedDict = {}
            if len(dataStringList) > 1:
                if originalDict == {} and newDict == {}:
                    #Import file as a string
                    #dataStringList = getListarray_v2(filePath, dataTableName, fileExtension)
                    #There is no data dictionary
                    print 'dataMachete.getListArrayAndDictDB()'
                    print 'fileImportTool.importAndProcessFile()'
                    print 'Table name', dataTableName, 'has no originalDict and no newDict'
                    print 'Proceeding to process data according to data types assocated with data in row 1'
                    #The variable type() will be established according to row 1 in the dataStringList
                    #below row 0 with the list of variable names.
                    #missingDict = makeDD.makeNewDataDictionaryFromDataStringFile(dataTableName,dataStringList,{})
                    nLines = toLine-fromLine
                    if nLines < 1000:
                        nLines = 1000
                    originalDict, newDict = inferDataDictionary_v2(dataTableName, filePath, fileExtension, printTypes, nLines)
                #Data dictionary created
                newDataTypedList, newDataTypedDict = processDataStringList(dataStringList, dataTableName, filePath, \
                                                                           errorFilePath, keyVariableNameList, \
                                                                            originalDict, newDict, fileExtension)        
    return newDataTypedList, newDataTypedDict


def getLargeDatasetListArrayAndDictDB_v2(dataTableName = '', filePath = '', errorFilePath = '', keyVariableNameList = [], \
                          originalDict = {}, newDict = {}, fileExtension = '', printTypes = 'YES', fromLine = 0, toLine = 10000, \
                            returnList = True, returnDict = True, returnHeader = False):
    '''
    WARNING
    
    If not newDict = {} (i.e. newDict is not empty) then the  keyVariableNameList must correspond
        to the list of key variables after the the new variable names in the newDict
        have been substituted for the original variable names in the originalDict.  This is only a problem
        if the names of key variables are to be changed from the original to the new dictionary.

    
    MINIMUM INPUTS

    
    At minimum this function requires the following inputs:

        1. A dataTableName, e.g. 'MYDATA', that is comma delimmeted text file
        2. A file path where 'MYDATA.txt' can be found, e.g. 'C:\\Python26\\DATA\\'
        3. An errorFilePath must be specified to record errors associated with identifying
            different variable types(). Note this must include the fileName plus '.txt' extension.
            e.g. 'C:\\Python26\\ERROR-CHECK.txt'
        4. The keyVariableNameList must be included - it must correspond to the originalVariableNames if
            newDict = {}, otherwise it the new variable names must be used in the keyVariableNameList .
        5. The originalDict must be included.
        6. If not newDict == {} (i.e. it is not left empty) then it will be produced using the new variable names, otherwise
            a blank newDictionary will be returned.

    Function RETURNS

        1. newDataTypedList - this is a 2D file in a list format, [[]], with data types assigned according to the data dictionary
        2. newDataTypedDict - this is a dictionary, {}, {{}}, up to 7 nested levels, with keys assigned according to the keyVariableNameList
        3. missingDict - this is empty unless both originalDict and newDict inputs are null, in which case a new dictionary
            is made from the original file using makeDD.makeNewDataDictionaryFromDataStringFile().
    
    #################################################################
    Added Oct 31 2013
    Ian Moss

    The function returns both a list and a dict if returnList == True and returnDict == True
    The function returns a list and not a dict if returnList == True and returnDict == False
    The function does not return a list and does return a dict if returnList == False and returnDict == True
    #############################################################################################
    
    Example of code used to access this module and function, including comments:

    #This filePath contains the locations of the data file and the data dictionary
    #indicating the variable types (comma delimmeted text files)

    filePath = 'E:\\Python26\\IBC\\'
    
    #Get data dictionary to identify variables and variable types

    ibcDataDictTableName = 'DATDICII'   #This is the name of the text file containing the data dictionary without the .txt extension.

    #Get the data dictionaries identifying the variable types

    originalDict, newDict = makeDD.dataDictionaryType_2(filePath,ibcDataDictTableName)

    #Specify location of file where errors are reported in terms of missing variables of invalid assignment of types
    #This is associated with typeDataset.typeDataset_v2()

    ibcErrorFilePath = filePath + 'ERROR-CHECK-IBC.txt'

    oldKeyVariableNameList = ['UID']    #This applies to both the original data 
    newKeyVariableNameList = ['UID']    #This applies to the new variable names and is important when the names of key variables are changed

    ibcDataTableName = 'SUMMARY'        #This is the name of the file containing the actual data without the '.txt' extension

    #input the instructions without any data dictionary
    #Returns a new dataDictionary referred to as missingDict using
    #makeNewDataDictionaryFromDataStringFile()
    
    print 'Geting typedList and typed dictionary without any data dictionary'
    ibcTypedList0, ibcTypedDict0, missingDict = fileImportTool.importAndProcessFile(ibcDataTableName, filePath, ibcErrorFilePath, \
                                                                oldKeyVariableNameList,{}, {})
    
    #Input the instructions without variable name changes, i.e. enter originalDict and not newDict
    #Assuming the originalDict is not empty (i.e. not originalDict == {}) it will return missingDict = {}

    print 'Getting typedList and typed dictionary with original data dictionary'
    ibcTypedList1, ibcTypedDict1, missingDict = fileImportTool.importAndProcessFile(ibcDataTableName, filePath, ibcErrorFilePath, \
                                                                oldKeyVariableNameList,originalDict, {})

    #Input the instructions with the variable name changes, i.e. with newDict
    #The originalKeyVariableName list is not required but the newKeyVariableNameList is required
    #Assuming both the originalDict and the newDict are not empty
    #(i.e. not originalDict == {} and not newDict == {}) it will return missingDict = {}

    print 'Getting typeedList and dictionary with new variableNames'
    ibcTypedList_new2, ibcTypedDict_new2, missingDict = fileImportTool.importAndProcessFile(ibcDataTableName, filePath, ibcErrorFilePath, \
                                                                newKeyVariableNameList, originalDict, newDict)
    POTENTIAL FUTURE DEVELOPMENT

    Another option is to provide for circumstances where no keyVarNames are input requiring that
        a new ID be developed for each row and added to the header.    
    
    '''
    #initialize missing data dictionary (in the event that there is no originalDict and no newDict)
    missingDict = {}
    #Check to make sure there is a non-empty dataTableName
    if dataTableName == '':
        print 'dataMachete.getListArrayAndDictDB()'
        print 'fileImportTool.importAndProcessFile() error'
        print 'No mandatory dataTableName provided to fileImportTool.importAndProcessFile()'
    else:
        #Check to make sure filePath is non-empty
        if filePath == '':
            print 'dataMachete.getListArrayAndDictDB()'
            print 'fileImportTool.importAndProcessFile() error'
            print 'No mandatory filePath provided to fileImportTool.importAndProcessFile()'
        else:
            #Create dataStringList
            dataStringList = getListArrayBetweenMinMaxLineNos(filePath,dataTableName, fileExtension, fromLine, toLine)
            newDataTypedList = [[]]
            newDataTypedDict = {}
            if len(dataStringList) > 1:
                if originalDict == {} and newDict == {}:
                    #Import file as a string
                    #dataStringList = getListarray_v2(filePath, dataTableName, fileExtension)
                    #There is no data dictionary
                    print 'dataMachete.getListArrayAndDictDB()'
                    print 'fileImportTool.importAndProcessFile()'
                    print 'Table name', dataTableName, 'has no originalDict and no newDict'
                    print 'Proceeding to process data according to data types assocated with data in row 1'
                    #The variable type() will be established according to row 1 in the dataStringList
                    #below row 0 with the list of variable names.
                    #missingDict = makeDD.makeNewDataDictionaryFromDataStringFile(dataTableName,dataStringList,{})
                    nLines = toLine-fromLine
                    if nLines < 1000:
                        nLines = 1000
                    originalDict, newDict = inferDataDictionary_v2(dataTableName, filePath, fileExtension, printTypes, nLines)
                #Data dictionary created
                if returnList == True and returnDict == True:
                    newDataTypedList, newDataTypedDict, newDataTypedHeader = processDataStringList_v2(dataStringList, dataTableName, filePath, \
                                                                           errorFilePath, keyVariableNameList, \
                                                                            originalDict, newDict, fileExtension, True, True)
                else:
                    if returnList == True and not returnDict == True:
                        newDataTypedList, newDataTypedHeader = processDataStringList_v2(dataStringList, dataTableName, filePath, \
                                                                           errorFilePath, keyVariableNameList, \
                                                                            originalDict, newDict, fileExtension, True, False)
                    else:
                        if not returnList == True and returnDict == True:
                            newDataTypedDict, newDataTypedHeader = processDataStringList_v2(dataStringList, dataTableName, filePath, \
                                                                           errorFilePath, keyVariableNameList, \
                                                                            originalDict, newDict, fileExtension, False, True)
    if returnList == True and returnDict == True:
        if returnHeader == True:
            return newDataTypedList, newDataTypedDict, newDataTypedHeader
        else:
            return newDataTypedList, newDataTypedDict
    else:
        if returnList == True and not returnDict == True:
            if returnHeader == True:
                return newDataTypedList, newDataTypedHeader
            else:
                return newDataTypedList
        else:
            if not returnList == True and returnDict == True:
                if returnHeader == True:
                    return newDataTypedDict, newDataTypedHeader
                else:
                    return newDataTypedDict


def processFile(dataTableName = '', filePath = '', errorFilePath = '', keyVariableNameList = [], \
                          originalDict = {}, newDict = {}, fileExtension = '.txt'):
    '''
    This is just an extension of importAndProcessFile() after having eliminated the possibility
    that no data dictionary of any kind was used as an input and after attempting to create
    a dictionary before proceeding further.
    '''
    #Check to make sure data table name does not include a file extension by splitting origDataTableName
    dictTableNameList = dataTableName.split('.')
    dictTableName = str(dictTableNameList[0])
    #Error Checks
    if dataTableName == '':
        print 'dataMachete.processFile() 1'
        print 'fileImportTool.processFile() error'
        print 'No mandatory dataTableName provided to fileImportTool.importAndProcessFile()'
    if filePath == '':
        print 'dataMachete.processFile() 2'
        print 'fileImportTool.processFile() error'
        print 'No mandatory filePath provided to fileImportTool.importAndProcessFile()'
    #Make sure dataDictionary includes dataTableName
    if originalDict.has_key(dictTableName) == False:
        print 'dataMachete.processFile() 3'
        print 'fileImportTool.processFile() error'
        print 'originalDictionary does not have dataTableName:', dictTableName
    #Check to make sure the originalKeyVariableList is non-empy
    if keyVariableNameList == []:
        print 'dataMachete.processFile() 4'
        print 'fileImportTool.processFile() error'
        print 'For dataTableName', dataTableName, 'The keyVariableNameList is empty', keyVariableNameList
        #Check to ensure that keyVariableList contains variables in the originalDict if the newDict == {}
    if newDict == {}:
        for keyVar in keyVariableNameList:
            if originalDict[dictTableName].has_key(keyVar) == False:
                print 'dataMachete.processFile() 5'
                print 'fileImportTool.processFile() error'
                print 'originalDict tableName', dictTableName, 'has no key variable name', keyVar, 'in data dictionary.'
    else:
        #Check to make sure newDict has dataTableName as a key
        if newDict.has_key(dictTableName) == False:
            print 'dataMachete.processFile() 6'
            print 'fileImportTool.processFile() error'
            print 'newDict does not have dataTableName:', dictTableName
        else:
            newVarNameList = newDict[dictTableName].keys()
            for keyVar in keyVariableNameList:
                if not keyVar in newVarNameList:
                    print 'fileImportTool.processFile() error 7'
                    print 'newDict tableName', dictTableName, 'has no new key variable name', keyVar, 'in data dictionary.'
    #End of error input checks

    #Start processing
    #Initialize dataTypedDict
    
    dataTypedDict = {}
    
    #Read comma delimited text file
    dataStringList = getListarray_v2(filePath, dataTableName, fileExtension)
    
    if newDict == {}:
        #The original variable names are to be applied
        #Type cast strings according to type specified in originalDict
        dataTypedList = typeDataset_v2(dataStringList, originalDict, dataTableName, errorFilePath)
        #dataTypedDict = dictionaryDBUtilities.additive_nested_key_multiple_item_dictionary(dataTypedDict, keyVariableNameList,dataTypedList)
        dataTypedDict = createDictDB(dataTypedDict, keyVariableNameList,dataTypedList)
    else:
        #Compile a list of new variable names from the original names in the dataStringList
        #Use the original names to identify the new names in the originalDataDictionary
        #Make a new list of new names in newDataStringVarNames
        originalDataStringVarNames = dataStringList [0]
        newDataStringVarNames = []
        #Remove any file extension from the dataTableName if present
        dictTableNameList = dataTableName.split('.')
        dictTableName = dictTableNameList[0]
        for originalVarName in originalDataStringVarNames:
            newVarName = originalDict[dictTableName][originalVarName]['NEWVARNAME']
            newDataStringVarNames.append(newVarName)
            
        #Replace the originalDataStringVarNames in dataStringList with with the newDataStringVarNames
        dataStringList[0] = newDataStringVarNames
        #Reset the variable types based on the newDataDictionary and the newKeyVariableNameList
        dataTypedList = typeDataset_v2(dataStringList, newDict, dictTableName, errorFilePath)
        #dataTypedDict = dictionaryDBUtilities.additive_nested_key_multiple_item_dictionary(dataTypedDict, keyVariableNameList,dataTypedList)
        dataTypedDict = createDictDB(dataTypedDict, keyVariableNameList,dataTypedList)
    return dataTypedList, dataTypedDict
        
def processDataStringList(dataStringList= [[]], dataTableName='', filePath = '', errorFilePath = '', keyVariableNameList = [], \
                          originalDict = {}, newDict = {}, fileExtension = '.txt'):
    
    '''
    This is just an extension of importAndProcessFile() after having eliminated the possibility
    that no data dictionary of any kind was used as an input and after attempting to create
    a dictionary before proceeding further.
    '''
    #Check to make sure data table name does not include a file extension by splitting origDataTableName
    dictTableNameList = dataTableName.split('.')
    dictTableName = str(dictTableNameList[0])
    #Error Checks
    if dataTableName == '':
        print 'dataMachete.processFile() 1'
        print 'fileImportTool.processFile() error'
        print 'No mandatory dataTableName provided to fileImportTool.importAndProcessFile()'
    if filePath == '':
        print 'dataMachete.processFile() 2'
        print 'fileImportTool.processFile() error'
        print 'No mandatory filePath provided to fileImportTool.importAndProcessFile()'
    #Make sure dataDictionary includes dataTableName
    if originalDict.has_key(dictTableName) == False:
        print 'dataMachete.processFile() 3'
        print 'fileImportTool.processFile() error'
        print 'originalDictionary does not have dataTableName:', dictTableName
    #Check to make sure the originalKeyVariableList is non-empy
    if keyVariableNameList == []:
        print 'dataMachete.processFile() 4'
        print 'fileImportTool.processFile() error'
        print 'For dataTableName', dataTableName, 'The keyVariableNameList is empty', keyVariableNameList
        #Check to ensure that keyVariableList contains variables in the originalDict if the newDict == {}
    if newDict == {}:
        for keyVar in keyVariableNameList:
            if originalDict[dictTableName].has_key(keyVar) == False:
                print 'dataMachete.processFile() 5'
                print 'fileImportTool.processFile() error'
                print 'originalDict tableName', dictTableName, 'has no key variable name', keyVar, 'in data dictionary.'
    else:
        #Check to make sure newDict has dataTableName as a key
        if newDict.has_key(dictTableName) == False:
            print 'dataMachete.processFile() 6'
            print 'fileImportTool.processFile() error'
            print 'newDict does not have dataTableName:', dictTableName
        else:
            newVarNameList = newDict[dictTableName].keys()
            for keyVar in keyVariableNameList:
                if not keyVar in newVarNameList:
                    print 'fileImportTool.processFile() error 7'
                    print 'newDict tableName', dictTableName, 'has no new key variable name', keyVar, 'in data dictionary.'
    #End of error input checks

    #Start processing
    #Initialize dataTypedDict
    
    dataTypedDict = {}
    
    #Read comma delimited text file
    #dataStringList = getListarray_v2(filePath, dataTableName, fileExtension)
    
    if newDict == {}:
        #The original variable names are to be applied
        #Type cast strings according to type specified in originalDict
        dataTypedList = typeDataset_v2(dataStringList, originalDict, dataTableName, errorFilePath)
        #dataTypedDict = dictionaryDBUtilities.additive_nested_key_multiple_item_dictionary(dataTypedDict, keyVariableNameList,dataTypedList)
        dataTypedDict = createDictDB(dataTypedDict, keyVariableNameList,dataTypedList)
    else:
        #Compile a list of new variable names from the original names in the dataStringList
        #Use the original names to identify the new names in the originalDataDictionary
        #Make a new list of new names in newDataStringVarNames
        originalDataStringVarNames = dataStringList [0]
        newDataStringVarNames = []
        #Remove any file extension from the dataTableName if present
        dictTableNameList = dataTableName.split('.')
        dictTableName = dictTableNameList[0]
        for originalVarName in originalDataStringVarNames:
            newVarName = originalDict[dictTableName][originalVarName]['NEWVARNAME']
            newDataStringVarNames.append(newVarName)
            
        #Replace the originalDataStringVarNames in dataStringList with with the newDataStringVarNames
        dataStringList[0] = newDataStringVarNames
        #Reset the variable types based on the newDataDictionary and the newKeyVariableNameList
        dataTypedList = typeDataset_v2(dataStringList, newDict, dictTableName, errorFilePath)
        #dataTypedDict = dictionaryDBUtilities.additive_nested_key_multiple_item_dictionary(dataTypedDict, keyVariableNameList,dataTypedList)
        dataTypedDict = createDictDB(dataTypedDict, keyVariableNameList,dataTypedList)
    return dataTypedList, dataTypedDict


def processDataStringList_v2(dataStringList= [[]], dataTableName='', filePath = '', errorFilePath = '', keyVariableNameList = [], \
                          originalDict = {}, newDict = {}, fileExtension = '.txt', returnList = True, returnDict = True):
    
    '''
    This is just an extension of importAndProcessFile() after having eliminated the possibility
    that no data dictionary of any kind was used as an input and after attempting to create
    a dictionary before proceeding further.
    '''
    #Check to make sure data table name does not include a file extension by splitting origDataTableName
    dictTableNameList = dataTableName.split('.')
    dictTableName = str(dictTableNameList[0])
    #Error Checks
    if dataTableName == '':
        print 'dataMachete.processFile() 1'
        print 'fileImportTool.processFile() error'
        print 'No mandatory dataTableName provided to fileImportTool.importAndProcessFile()'
    if filePath == '':
        print 'dataMachete.processFile() 2'
        print 'fileImportTool.processFile() error'
        print 'No mandatory filePath provided to fileImportTool.importAndProcessFile()'
    #Make sure dataDictionary includes dataTableName
    if originalDict.has_key(dictTableName) == False:
        print 'dataMachete.processFile() 3'
        print 'fileImportTool.processFile() error'
        print 'originalDictionary does not have dataTableName:', dictTableName
    #Check to make sure the originalKeyVariableList is non-empy
    if keyVariableNameList == []:
        print 'dataMachete.processFile() 4'
        print 'fileImportTool.processFile() error'
        print 'For dataTableName', dataTableName, 'The keyVariableNameList is empty', keyVariableNameList
        #Check to ensure that keyVariableList contains variables in the originalDict if the newDict == {}
    if newDict == {}:
        for keyVar in keyVariableNameList:
            if originalDict[dictTableName].has_key(keyVar) == False:
                print 'dataMachete.processFile() 5'
                print 'fileImportTool.processFile() error'
                print 'originalDict tableName', dictTableName, 'has no key variable name', keyVar, 'in data dictionary.'
    else:
        #Check to make sure newDict has dataTableName as a key
        if newDict.has_key(dictTableName) == False:
            print 'dataMachete.processFile() 6'
            print 'fileImportTool.processFile() error'
            print 'newDict does not have dataTableName:', dictTableName
        else:
            newVarNameList = newDict[dictTableName].keys()
            for keyVar in keyVariableNameList:
                if not keyVar in newVarNameList:
                    print 'fileImportTool.processFile() error 7'
                    print 'newDict tableName', dictTableName, 'has no new key variable name', keyVar, 'in data dictionary.'
    #End of error input checks

    #Start processing
    #Initialize dataTypedDict
    
    dataTypedDict = {}
    
    #Read comma delimited text file
    #dataStringList = getListarray_v2(filePath, dataTableName, fileExtension)
    
    if newDict == {}:
        #The original variable names are to be applied
        #Type cast strings according to type specified in originalDict
        dataTypedList = typeDataset_v2(dataStringList, originalDict, dataTableName, errorFilePath)
        #dataTypedDict = dictionaryDBUtilities.additive_nested_key_multiple_item_dictionary(dataTypedDict, keyVariableNameList,dataTypedList)
        dataTypedDict = createDictDB(dataTypedDict, keyVariableNameList,dataTypedList)
    else:
        #Compile a list of new variable names from the original names in the dataStringList
        #Use the original names to identify the new names in the originalDataDictionary
        #Make a new list of new names in newDataStringVarNames
        originalDataStringVarNames = dataStringList [0]
        newDataStringVarNames = []
        #Remove any file extension from the dataTableName if present
        dictTableNameList = dataTableName.split('.')
        dictTableName = dictTableNameList[0]
        for originalVarName in originalDataStringVarNames:
            newVarName = originalDict[dictTableName][originalVarName]['NEWVARNAME']
            newDataStringVarNames.append(newVarName)
            
        #Replace the originalDataStringVarNames in dataStringList with with the newDataStringVarNames
        dataStringList[0] = newDataStringVarNames
        #Reset the variable types based on the newDataDictionary and the newKeyVariableNameList
        dataTypedList = typeDataset_v2(dataStringList, newDict, dictTableName, errorFilePath)
        #dataTypedDict = dictionaryDBUtilities.additive_nested_key_multiple_item_dictionary(dataTypedDict, keyVariableNameList,dataTypedList)
        if returnDict == True:
            dataTypedDict = createDictDB(dataTypedDict, keyVariableNameList,dataTypedList)
    dataTypedHeader = dataTypedList[0]
    if returnList == True and returnDict == True:
        return dataTypedList, dataTypedDict, dataTypedHeader
    else:
        if returnDict == True and not returnList == True:
            return dataTypedDict, dataTypedHeader
        else:
            return dataTypedList, dataTypedHeader 
        


#from types import *
# import fileUtilities -- no longer needed mb

def writeListarrayToCSVFile(TwoDList = [[]], filePath = '', fileName = '', floatFormat = '', fileExtension = '.txt'):
    '''
    This function takes a preformated printLine, opens a pre-existing file
    and writes the line to the file.

    Note that the floatFormat statement should not include a comma, ','!
    '''
    #print fileName, floatFormat
    floatFormatVar = floatFormat
    writeFilePath = createNewFilePath_v2(filePath, fileName, fileExtension)
    #print writeFilePath
    newFile = open(writeFilePath,'w')
    printLine = ''
    writeFile = convertListarrayToCSVFileFormat(TwoDList, printLine, floatFormat)
    for line in writeFile:
        print >> newFile, line
    newFile.close()
    return

def writeListarrayToCSVFile_v2(TwoDList = [[]], filePath = '', fileName = '', \
                               floatFormat = '', fileExtension = '.txt', dataOverwrite = True, \
                               includeHeader = True):
    '''
    This function takes a preformated printLine, opens a pre-existing file
    and writes the line to the file.

    Note that the floatFormat statement should not include a comma, ','!
    '''
    #print fileName, floatFormat
    floatFormatVar = floatFormat
    writeFilePath = createNewFilePath_v2(filePath, fileName, fileExtension)
    #print writeFilePath
    if dataOverwrite == True:
        #Overwrite existing file
        newFile = open(writeFilePath,'w')
    else:
        #Append to bottom of existing file
        newFile = open(writeFilePath,'a')
    printLine = ''
    writeFile = convertListarrayToCSVFileFormat(TwoDList, printLine, floatFormat)
    i = 0
    for line in writeFile:
        if i==0:
            if includeHeader == True:
                print >> newFile, line
            i = i + 1
        else:
            print >> newFile, line
    newFile.close()
    return

def convertListarrayToCSVFileFormat(TwoDList=[[]], printLine = '', floatFormat = ''):
    '''
    Prepares a list array for writing to CSV file
    '''
    writeList = []
    end_i = len(TwoDList)
    for i in range(0, end_i,1):
        varList = TwoDList[i]
        end_j = len(varList)
        writeLine = convertListLineToWriteString(varList, printLine, floatFormat)
        writeList.append(writeLine)
    return writeList


def convertTypeToString(varValue, printLine = '', floatFormat = ''):
    '''
    varValue is a variable value
    
    printLine is an existing string format that is to be
    extended into single lines with variable values delimmited by
    commas

    Note tha a default float format must be specified,
    e.g. floatFormat = '%0.3f,'
    '''
    varType = type(varValue)
    if varType == StringType:
        printLine = printLine + varValue
    else:
        if varType== IntType or varType == numpy.int32 or varType == numpy.int64:
            printLine = printLine + '%i' % varValue
        else:
            if varType == FloatType or varType == numpy.float32 or varType == numpy.float64:
                #print printLine, floatFormat, varValue
                printLine = printLine + floatFormat % varValue
                #printLine = printLine + '%0.3f' % varValue
            else:
                print 'dataMachete.convertTypeToString'
                print 'variable with value:', varValue, 'is of type:', varType,
                print 'no such type provided for in update_printLine'
    return printLine


def convertListLineToWriteString(varList = [], printLine = '', floatFormat = ''):
    '''
    Note tha a default float format must be specified,
    e.g. floatFormat = '%0.3f,'
    '''
    end_i = len(varList)
    for i in range(0,end_i,1):
        printLine = convertTypeToString(varList[i], printLine, floatFormat)
        if not i == end_i-1:
            printLine = printLine + ','
            
    return printLine

def saveHeader(header=[],printFilepath=''):
    '''
    This function takes a list of variable names, opens a new file
    or overwrites an old file of the same name and in the same directory
    and copies the variable names to a file in a csv format.
    '''
    newFile = open(printFilepath,'w')
    printline = ''
    for varName in header:
        printline = update_printline(varName, printline, '%0.0f,', varName)
    printline = printline.rstrip(',')
    print >> newFile, printline
    newFile.close()
    return

#Additional List Array Management Functions (Ian; August 1 2013)

def join2DListBToRightOf2DListA(listA2D = [[]], listB2D = [[]]):
    '''
    Explanation
        Each of the rows in listB is appended to the corresponding
        rows in listA and combined into a single row or  list.
        lisA and listB must have the same number of rows.
    '''
    new2DList = []
    aLength = len(listA2D)
    bLength = len(listB2D)
    if aLength == bLength:
        for i in range(0, aLength, 1):
            aVector = listA2D[i]
            bVector = listB2D[i]
            new1DList = join1DListBToRightOf1DListA(aVector, bVector)
            new2DList.append(deepcopy(new1DList))
    else:
        print 'dataMachete.join2DListBToRightOf2DListA'
        print 'list A length;', aLength, 'different from B length:', bLength
        print 'the two lists must be the same length to execute append'
        print 'function will return empty new2DList'
    return new2DList

def join1DListBToRightOf1DListA(listA1D = [], listB1D = []):
    '''
    Explanation
        ListB is appended to the end of listA and combined into a single list .  
    '''
    lenListA1D = len(listA1D)
    lenListB1D = len(listB1D)
    new1DList = []
    for i in range(0,lenListA1D,1):
        newVarValue = listA1D[i]
        new1DList.append(newVarValue)
    for i in range(0,lenListB1D,1):
        newVarValue = listB1D[i]
        new1DList.append(newVarValue)
    return new1DList

def joinOneDListBToRightOfOneDListAExcludingValuesAlreadyInA(listA1D = [], listB1D = []):
    '''
    '''
    lenListA1D = len(listA1D)
    lenListB1D = len(listB1D)
    new1DList = []
    for i in range(0,lenListA1D,1):
        newVarValue = listA1D[i]
        new1DList.append(newVarValue)
    for i in range(0,lenListB1D,1):
        newVarValue = listB1D[i]
        if not newVarValue in new1DList:
            new1DList.append(newVarValue)
    return new1DList


def removeItemsIn1DListBFrom1DListA(listA1D=[], listB1D=[]):
    '''
    '''
    newListA1D = deepcopy(listA1D)
    for item in listB1D:
        if item in newListA1D:
            itemNo = newListA1D.index(item)
            del newListA1D[itemNo]
    return newListA1D

def appendRowsFrom2DListBTo2DListA(listA2D = [[]], listB2D = [[]]):
    '''
    Explanation:
        ListB rows are appended to the bottom of listA.
        The lengths of each row in both listA and listB should be equal.
    '''
    newList = deepcopy(listA2D)
    flag = True
    for item in listB2D:
        newList.append(deepcopy(item))
    return newList

def appendRowsFrom2DListBTo2DListAExclusiveOfItemsAlreadyInA(listA2D = [[]], listB2D = [[]]):
    '''
    Explanation:
        ListB rows are appended to the bottom of listA.
        The lengths of each row in both listA and listB should be equal.
    '''
    newList = deepcopy(listA2D)
    flag = True
    for item in listB2D:
        if item not in newList:
            newList.append(deepcopy(item))
    return newList

def check2DListRecordLengths(list2D = [[]]):
    '''
    Explanation
        Under development
        This checks the number of rows and also checks the length of
        each row in the list.  It returns the numbers of rows, then length
        of the first row (row 0) and produces a Flag that is equal to True
        if the lengths of each row are all equal to the first row, otherwise
        false.
    '''
    Flag = True
    itemLength = len(list2D)
    #for item in list2D:
    return
        
def createNewListFromSelectColumnNumbersIn2DList(originalList = [[]], selectColList = []):
    '''
    Explanation:
        This function selects the columns indicated in the selectColList from
        the originalList and puts them into a new list.
    '''
    newList = []
    lenOriginalList = len(originalList)
    for row in range(0,lenOriginalList,1):
        newList.append([])
        for colNo in selectColList:
            if not colNo < len(originalList[row]):
                print 'createNewListFromSelectColumnNumbersIn2DList'
                print 'trying to select a colNo', colNo, 'that is greater than or equal to the length of the listItem', len(originalList[row])
                print 'column does not exist'
            else:
                newVarValue = originalList[row][colNo]
                newList[row].append(newVarValue)
    return newList                       


def addIndexToRowsOnLeftSideOfArray(xArray = [[]]):
    '''
    Indices are added, 0,1,,2 ... n on the left hand side of the array
    in each row
    '''
    newArray = []
    lenArray = len(xArray)
    for rowNo in range(0,lenArray, 1):
        newArray.append([rowNo])
        lenArrayRow = len(xArray[rowNo])
        for colNo in range(0,lenArrayRow, 1):
            newArray[rowNo].append(xArray[rowNo][colNo])
    return newArray

def addListOfNumbersToLeftSideOfArray(xArray = [[]], numberList = []):
    '''
    A column of numbers, x, to the left hand side of the array
    
    '''
    newArray = []
    lenArray = len(xArray)
    lenNumberList = len(numberList)
    for row in range(0,lenArray):
        newArray.append([])
        for col in range(0,lenNumberList,1):
            newArray[row].append(numberList[col])
        lenArrayRow = len(xArray[row])
        for col in range(0,lenArrayRow, 1):
            newArray[row].append(xArray[row][col])
    return newArray

def addHeaderListToDataList(myHeader = [], myData = [[]]):
    '''
    This function inserts myHeader in the top
    of the 2DList 
    '''
    newList = [myHeader]
    for lineItem in myData:
        newList.append(lineItem)
    return newList


def joinTwo2DListsPlusHeaders(varNameList = [], dataList = [[]], keyVarNameList = [], keyVarValueList = [[]]):
    '''
    Explanation:
        This function attaches a list of (compound) keys (keyVarValueList) to a new dataset (dataList)
        that was manufactured from the original dataset in the same order as the original data and creates
        a new dataset (obsList).  It also combines the keyVarNameList and the varNameList into a header and
        then inserts the header as the first row (row 0) above the new dataset (obslist) to create and return
        a final dataset (newDataList)
    '''
    newHeader = join1DListBToRightOf1DListA(keyVarNameList, varNameList)
    obsList = join2DListBToRightOf2DListA(keyVarValueList, dataList)
    newDataList = addHeaderListToDataList(newHeader, obsList)
    return newDataList

def convert1DListofItemsUsingDynamicTyping(varValueList = []):
    '''
    '''
    if not varValueList == []:
        newVarValueList = []
        for item in varValueList:
            newVarValue = convertTypeUsingDynamicTyping(item)
            newVarValueList.append(newVarValue)
    return newVarValueList

def convertTypeUsingDynamicTyping(varValue = '0'):
    '''
    '''
    try:
        newVarValue = int(varValue)
    except:
        try:
            newVarValue = float(newDataStringList[1][j])
        except:
            newVarValue = str(varValue)
        else:
            newVarValue = float(newDataStringList[1][j])
    else:
        newVarValue = int(varValue)
    return newVarValue

def checkYesOrNoDecisionRule(decision = 'Yes', decisionType = ''):
    '''
    '''
    if decision == 'YES' or decision == 'Yes' or decision == 'yes' or decision == 'Y' or decision == 'y':
        decision = 'YES'
    else:
        if decision == 'NO' or decision == 'No' or decision == 'N' or decision == 'n':
            decision == 'NO'
        else:
            print 'dataMachete.checkYesOrNoDecisionRule()'
            print 'Decision type: ', decisionType
            print 'Indicated decision: ', decision, 'is not a recognized decision rule'
            print 'Decision reset to default: NO'
            decision = 'NO'
    return decision



# ---------- File Utility Functions ----------
#checkFileIfItExists, createNewFileIfNotExisting, deleteFileIfItExists originally in fileUtilities,
# (c) Ian Moss, 2006


#import os
# from operator import concat

def removeFileExtension(fileName):
    newFileNameList = fileName.split('.')
    newTableName = newFileNameList[0]
    return newTableName

  
def checkFileIfItExists(filepath):
    fileExists = 1
    if filepath == '':
        fileExists = 0
    else:
        if not os.path.exists(filepath):
            fileExists = 0
    return fileExists

def checkIfFileExistsAndSetToDefaultIfItDoesNot(myFilePath = '', defaultFilePath = ''):
    '''
    '''
    filePathFlag =  checkFileIfItExists(myFilePath)
    if filePathFlag == 1:
        newFilePath = myFilePath
    else:
        #myFilePath does not exist; check if defaultFilePath exists
        filePathFlag = checkFileIfItExists(defaultFilePath)
        if filePathFlag == 1:
            newFilePath = defaultFilePath
            if not myFilePath == '':
                print ' dataMachete.checkIfFileExistsAndSetToDefaultIfItDoesNot()'
                print ' myFilePath: ', myFilePath, 'does not exist'
                print ' myFilePath reset to default: ', defaultFilePath
        else:
            print ' dataMachete.checkIfFileExistsAndSetToDefaultIfItDoesNot()'
            if myFilePath == '':
                print ' myFilePath is blank'
            else:
                print ' myFilePath: ', myFilePath, 'does not exist'
            print ' defaultFilePath: ', defaultFilePath, 'does not exist'
            print ' program or config file error'
            newFilePath = myFilePath
    return newFilePath

def createNewFileIfNotExisting(filepath):
    if not os.path.exists(filepath):
        newFile = open(filepath,'w')
        newFile.close()
    return

def deleteFileIfItExists(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)
    return

def writeToFile(textLine = '', writeFilePath = ''):
    fileExists = checkFileIfItExists(writeFilePath)
    if fileExists == 1:
        #print 'file exists'
        #print writeFilePath
        #print textLine
        myFile = open(writeFilePath,'a')
    else:
        #print 'file does not exist'
        #print writeFilePath
        #print textLine
        myFile = open(writeFilePath,'w')
    print >> myFile, textLine
    myFile.close()
    return

def createNewFilePath(filepath, filename):
    '''
    Author:  Ian Moss
    Last Modified Jan 23, 2006 (source file: READv1)
    Converted to following dictionary format:
    {('VariableName','TableName'):'Type'}
    where type is an integer, string or float
    Updated: August 27, 2012 (Mishtu Banerjee, Ian Moss)
    Copyright Ian Moss
    '''
    FileKind = '.txt'
    newFilename = concat(filename, FileKind)
    newFilePath = concat(filepath, newFilename)
    return newFilePath

def createNewFilePath_v2(filepath, filename, fileExtension):
    '''
    Author:  Ian Moss
    Last Modified Jan 23, 2006 (source file: READv1)
    Updated: August 27, 2012 (Mishtu Banerjee, Ian Moss)
    Updated Ian Moss January 2013
    Updated Ian Moss Feb 6 2014
    Copyright Ian Moss
    '''
    newFileNameList = filename.split('.')
    newFilePathList = filepath.split('.')
    if len(newFilePathList)==2:
        newFilePath = filepath
    else:
        if len(newFileNameList)==2:
            newFilename = filename
        else:
            if not fileExtension =='':
                newFilename = concat(filename, fileExtension)
            else:
                newFilename = concat(filename, '.txt')
        newFilePath = concat(filepath, newFilename)
    return newFilePath

# ---------- Data Dictionary  Functions ----------
#data_dictionary originally in makeDD, (c)  Ian Moss, 2006- 2012
# typeDataset originally in typeDataset, (c) Ian Moss, 2006-2012

# Originally in makeDD
# from fileUtilities import newFilePath -- note needed
# Must remove ref to fileUtilities

def getDataDictionary(filepath, filename):
    dict_path = createNewFilePath(filepath, filename)
    '''
    A Data Dictionary is a listing of variable names, the table they appear in, 
    as well as the typing information for the variable. 
    Author:  Ian Moss
    Last Modified Jan 23, 2006 (source file: READv1)
    Converted to following dictionary format:
    {('VariableName','TableName'):'Type'}
    where type is an integer, string or float
    Updated: August 27, 2012 (Mishtu Banerjee, Ian Moss)
    Copyright Ian Moss
    '''
    print "dict_path =", dict_path #333
    temp_file =open (dict_path,'r')
    outfile = {}
    i=0
    variables = {'VARIABLES':{}}
    data ={'DATA':{}}
    for line in temp_file:
        #This part of the program strips off linefeed symbol, '\n' that
        #is inserted by ACCESS or Python at the end of line(s)
        #when it reads files.
        x=line.split(',')
        end_j = len(x)
        j=end_j-1
        #x[j].rstrip()
        #print x[j]
        #break
        dummy = x[j]
        end_l = len(dummy)
        x[j] = ''
        l=0
        for l in range(0,end_l-1,1):
            x[j] = x[j]+dummy[l]
        #End of routine for stripping away of linefeed symbol at end
        #of line.
        if i == 0:
            j = 0
            for j in range(0,end_j):
                if x[j] == 'Variable':
                    var_col = j
                else:
                    if x[j] == 'Table':
                        table_col = j
                    else:
                        if x[j] == 'Type':
                            type_col = j
                    
        if not i==0:
            #Old method below
            #key = (str(x[var_col]), str(x[table_col]))
            #newline = {key:str(x[type_col])}
            #outfile.update(newline)
            #New method
            table_name = str(x[table_col])
            var_name = str(x[var_col])
            var_type = str(x[type_col])
            if not outfile.has_key(table_name):
                outfile.update({table_name:{}})
            if not outfile[table_name].has_key(var_name):
                outfile[table_name].update({var_name:var_type})
            
        i=i+1
    temp_file.close()
    return outfile

# Originally in typeDataset

# import fileUtilities -- no longer needed fix refs to filetiities
# from types import *

def typeDataset(fileList = [], dataDict = {}, tableName = '', errorFilePath = ''):
    '''
    Created by Ian and Mishtu
    August 27, 2012
    
    Notes:
    fileList is a csv text file with all data in string format
    dataDict is a standard data dictionary format created in makeDD
    tableName refers to table in data dictionary
    errorFileName is the name of the file to which errors are written
    
    '''
    print; print "####################################################" #333
    print "dataMachete.typeDataset(fileList = [], dataDict = {}, tableName = '', errorFilePath = '')" #333 
    print #333
    print "-----------------------------------------------------------" #333
    print "fileList = " #333
    for i in range(0,3,1):
        print fileList[i], 
    print #333
    print "-----------------------------------------------------------" #333
    print "dataDict = "
    for i in dataDict.keys():
        print i, 
    print #333
    print "-----------------------------------------------------------" #333
    print "tableName =", tableName #333
    print #333
    print "-----------------------------------------------------------" #333
    print "errorFilePath =", errorFilePath #333
    print "ENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDEND" #333
    print #333
    
    #i is the row, end_i is the number of rows
    #j is the column, end_j is the number of columns
    end_i = len(fileList)
    end_j = len(fileList[0])
    if not dataDict.has_key(tableName):
        print 'Table name', tableName, 'not found in dataDict'
    #start making conversions column by column
    for j in range(0,end_j,1):
        varName = fileList[0][j]
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
                    writeToFile(textLine, errorFilePath)
                    
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
    #Remove file extension from end of table name if it exists
    dictTableNameList = tableName.split('.')
    dictTableName = dictTableNameList[0]
    newErrorFilePathList = errorFilePath.split('.')
    if len(newErrorFilePathList)==1:
        newErrorFilePath = errorFilePath + 'ERROR_' + dictTableName + '.txt'
    else: 
        newErrorFilePath = errorFilePath
    #i is the row, end_i is the number of rows
    #j is the column, end_j is the number of column
    end_i = len(fileList)
    end_j = len(fileList[0])
    if not dataDict.has_key(dictTableName):
        print 'dataMachete.typeDataset_v2'
        print 'Table name', dictTableName, 'not found in dataDict'
    #start making conversions column by column
    for j in range(0,end_j,1):
        varName = fileList[0][j]
        #print varName
        if not dataDict[dictTableName].has_key(varName):
            print 'dataMachete.typeDataset_v2'
            print 'Table name', dictTableName, 'missing variable', varName
            print 'Variable number:', j, 'line 0 of the datafile'
        varType = dataDict[dictTableName][varName]['VARTYPE']
        varDefault = dataDict[dictTableName][varName]['VARDEFAULT']
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
                            textLine = 'Not integer, boolean or ordinal type. Table Name: ' + tableName + ' Variable Name:' + \
                                       varName + ' Line Number: ' + str(i) + ' Value:' + str(fileList[i][j])
                            #fileUtilities.writeToFile(textLine, errorFilePath)
                            writeToFile(textLine, newErrorFilePath)
                        else:
                            fileList[i][j] = int(fileList[i][j])
                if varType ==  'float' or varType == 'continuous' or varType == 'proportion':
                    if fileList[i][j] == '':
                        fileList[i][j] = float(varDefault)
                    else:
                        try:
                            float(fileList[i][j])
                        except:
                            textLine = 'Not float or continuous type. Table Name: ' + tableName  + ' Variable Name:' + \
                                       varName + ' Line Number:' + str(i) + ' Value:' + str(fileList[i][j])
                            #fileUtilities.writeToFile(textLine, errorFilePath)
                            writeToFile(textLine, newErrorFilePath)
                        else:
                            fileList[i][j] = float(fileList[i][j])
    return fileList

def replaceOldVariableNamesWithNewVariableNamesIn2DListHeader(originalDict = {}, list2D = [[]], tableName = ''):
    '''
    '''
    #Ensure that table name has no file extension
    newTableNameList = tableName.split('.')
    newTableName = newTableNameList[0]
    if type(list2D[0])==list:
        newHeader = deepcopy(list2D[0])
    else:
        if type(list2D)==list:
            newHeader = deepcopy(list2D)
    #
    if not originalDict.has_key(newTableName):
        print 'dataMachete.replaceOldVariableNamesWithNewVariableNamesIn2DListHeader()'
        print 'originalDict has not data table name:', newTableName
    oldVarNameList = originalDict[newTableName].keys()
    for oldVarName in oldVarNameList:
        if not originalDict[newTableName][oldVarName]['NEWVARNAME']=='':
            newVarName = originalDict[newTableName][oldVarName]['NEWVARNAME']
            if not oldVarName in newHeader:
                print 'dataMachete.replaceOldVariableNamesWithNewVariableNamesIn2DListHeader()'
                print 'originalDict table name:', newTableName, 'does not have original variable name:', oldVarName, 'found in originalDict'
                print 'can not assign new variable name:', newVarName
            else:
                colIndex = newHeader.index(oldVarName)
                newHeader[colIndex]= newVarName
    if type(list2D[0])==list:
        list2D[0] = newHeader
    else:
        if type(list2D)==list:
            list2D = newHeader
    return list2D





            
def getDatamacheteDictionary(filepath = '', filename = '', fileExtension = '.txt'):
    '''
    Author:  Ian Moss

    Input
    The file path indicates where the data dictionary can be found
    The filename indicates the name of the text (.txt) file where the comma delimmmited dictionary can be found,
        excluding the extension, for example 'DATDICT'. 
          
    This is a new dictionary type to allow for relabelling of input variables
    and to identify different kinds of variables.  Column names are provided
    in the first line and and can be provided in any order, but by convention they
    are used in the following order (the names must be used as column headings
    separated by a comma) after having been processued using this function:

    TVID        - This is a unique ID refering to each row in the data dictionary
                    This must be an integer (see below)
    TABLENAME   - This generaly refers to a comma delimmted text file containg data without the '.txt. extension
    VARNAME     - This is the list of variables found in the files
    NEWVARNAME  - This is the new name to be assigned to the input variable
                    (they may be the same as the original variable names) 
    VARTYPE     - This is defined as integer, float or string ... or any other Python variable type
    VARKIND     - This is nominal, ordinal or continuous (at the moment this is for reference purposes only)
    VARDEFAULT  - This is the default value for blank entries in a data table, i.e. ''
                - If the default is left blank then a '' will be used as the default for string types
                    a 0(zero) will be used as the default for integer types, and
                    a 0.0 (i.e. float(0)) will be used as the default for float types
                    Note that if VARTYPE is 'numeric' and VARDEFAULT' is left blank then the default will be a float, 0.0
    SELECT      - This is optional and for reference purposes only.  All of the data in the data file with a corresponding
                    variable name will be loaded into the Python module.
                    Use a 1 to indicate if a variable is to be included, otherwise 0. 
    DESCRIPTION - This is a description for reference purposes only

    The data dictionary itself must be a comma delimmeted file ... and as a result there must be no
    commas used under the 'Description' in the last column.
    No commas can be used anwhere in the data, other than to separate columns of variables 

    This function returns two dictionaries as follows:

    originalNameDict = {tableName:{varName:{'TVID':tvid, 'NEWVARNAME': 'newVarName','VARTYPE': varType,'VARKIND':varKind, 'VARDEFAULT':varDefault, 'DESCRIPTION':description}
    newNameDict = {tableName:{newVarName:{'TVID':tvid,'VARNAME': 'varName','VARTYPE': varType,'VARKIND':varKind, 'VARDEFAULT':varDefault, 'DESCRIPTION':description}

    Note if the newVarname is left blank then the original varName will be used to represent the newVarname.

    Note that the following variable types are permissible (all in lower case):

    boolean     - This will be type() cast as an integer in Python and must be coded as 1 or 0.
                    The rule above for declaring integer types apply. 
    character   - This will be type() cast as a string.
    classint    - This is a clas described as an integer(e.g; 1,2,,3 ... n classes undera single varName) generally to be used
                    when the classes do not qualify as being ordinal.
                    These will be type() cast as integers.
                    Generaly there will be more than 2 classes; 2 classes are better represented as boolean or dummy varTypes
                    Classes may also be described as nominal and therefore type() cast as string
    continuous  - This will be type() cast as a float, may or may not include decimal points, but must not include characters.
    count       - This is type() cast as an integer.
                    It should be reserved for actual counts of certain kinds or classes of objects 
    dummy       - This is type() cast as an integer (same as boolean) and must be coded as 1 or 0.
    float       - This may or may not include a decimal place but must not include characters.
    integer     - No decimal may be recorded next to a number declared as being integer anywhere in the data table;
                    If there is a decimal point included Python will not convert it from a string to an integer.
                    If characters are included Python will NOT convert it from a string to an integer.
    nominal     - This will be a type() cast as a string.
    ordinal     - This will be type() cast as an integer in Python.
                    The rule above for declaring integer types apply.
                    These kind of variables reflect a distinct order or rank and can be treated as continuous variables.
    proportion  - This is float type() between 0 and 1
    string      - This may be in any format since all values are initially imported in this format.

    The 'numeric' type (not a type used in Python but referred to elsewhere) was rejected due to ambiguity between a float and an integer
   
    This is a refactoring of code developed previously under ForesTree Dynamics Ltd 
    Copyright Ian Moss

    September 15 2013 - IMOSS
    Changed
    dict_path = newewFilePath(filepath, filename, fileExtension)
    dict_path = createNewFilePath_v2(filepath, filename, fileExtension)
    '''
    if filepath == '':
        print 'No filepath indicated for data dictionary'
    if filename == '':
        print 'No filename indicated for data data dictionary'
    #Initialize dictionary filepath
    dict_path = createNewFilePath_v2(filepath, filename, fileExtension)
    #Open dictionary
    
    temp_file = open (dict_path,'r')
    #Define original data dictionary (with original table and variable names as keys) and
    #Define new data dictionary (with original table names and new variable names as keys) 
    originalNameDict = {}
    newNameDict = {}
    #Set line index to 0
    i = 0 
    for line in temp_file:
        #This part of the program strips off linefeed symbol, '\n' that
        #is inserted by ACCESS or Python at the end of line(s)
        #when it reads files.
        x=line.split(',')
        end_j = len(x)
        j=end_j-1
        #x[j].rstrip()
        #print x[j]
        #break
        dummy = x[j]
        end_l = len(dummy)
        x[j] = ''
        l=0
        for l in range(0,end_l-1,1):
            x[j] = x[j]+dummy[l]
        #End of routine for stripping away of linefeed symbol at end
        #of line.
        if i == 0:
            #Get column numbers associated with variable names
            for j in range(0,end_j):
                if x[j] == 'TVID':
                    tvidCol = j
                else:
                    if x[j] == 'TABLENAME':
                        tableCol = j
                    else:
                        if x[j] == 'VARNAME':
                            varCol = j
                        else:
                            if x[j] == 'NEWVARNAME':
                                newVarCol = j
                            else:
                                if x[j] == 'VARTYPE':
                                    varTypeCol = j
                                else:
                                    if x[j] == 'VARDEFAULT':
                                        varDefaultCol = j
                                    else:
                                        if x[j] == 'SELECT':
                                            selectCol = j
                                        else:
                                            if x[j] == 'DESCRIPTION':
                                                descriptionCol = j
        if not i==0:
            #assign variable values from appropriate column numbers  
            tvid = int(x[tvidCol])
            tableName = str(x[tableCol])
            varName = str(x[varCol])
            newVarName = str(x[newVarCol])
            #if newVarName is left blank then replace with varName
            if newVarName == '':
                newVarName = varName
            varType = str(x[varTypeCol])
            varDefault = str(x[varDefaultCol])
            try:
                int(x[varDefaultCol])
            except:
                select = str(x[varDefaultCol])
            else:
                select = int(x[varDefaultCol])
            description = str(x[descriptionCol])
            #Start process of assigning appropriate types() to varDefault values
            #If variable type is not a string, character or nominal type() the change the type
            #Must either be related to a float or integer type
            if not varType == 'string' or not varType == 'character' or not varType == 'nominal':
                #If varType is integer, boolean or ordinal
                if varType == 'integer' or varType == 'boolean' or varType == 'dummy' or varType == 'ordinal' \
                   or varType == 'classint' or varType == 'count':
                    if varDefault == '':
                        varDefault = 0
                    else:
                        try:
                            int(varDefault)
                        except:
                            print 'Default value', varDefault, 'TABLENAME', tableName, 'VARNAME', varName, \
                                  'in DATA DICTIONARY TVID', tvid, 'cannot be converted to an integer'
                        else:
                            varDefault = int(varDefault)
                            
                #if varType is float or coninuous
                if  varType == 'float' or varType == 'continuous' or varType == 'proportion':
                    if varDefault == '':
                        varDefault = float(0)
                    else:
                        try:
                            float(varDefault)
                        except:
                            print 'Default value', varDefault, 'TABLENAME', tableName, 'VARNAME', varName, \
                                  'in DATA DICTIONARY TVID', tvid, 'cannot be converted to a float'
                        else:
                            varDefault = float(varDefault)
                        
                        
            #If the tableName has not been added as the primary key to the originalNameDict
            #Then by definition it has not yet been assigned to the newNameDict
            #Update these two dictionaries with the table names
            if not originalNameDict.has_key(tableName):
                originalNameDict.update({tableName:{}})
                newNameDict.update({tableName:{}})
            #If the variable name, varName has not yet been assigned as a key subdivision of tableName
            #Then    
            if not originalNameDict[tableName].has_key(varName):
                originalNameDict[tableName].update({varName:{'TVID':tvid,'NEWVARNAME':newVarName,'VARTYPE':varType, 'VARDEFAULT':varDefault, \
                                                             'SELECT':select,'DESCRIPTION':description}})
            else:
                #tableName in originalNameDict has duplicate variable names 
                print 'TABLE', tableName, 'has a duplicate VARNAME', varName, 'in data dictionary type 2'
                
            #Update the newVarName as a key in the newNameDict 
            #If newVarName is blank then replace blank with varName
            if newVarName == '':
                newVarName = varName    
            if not newNameDict[tableName].has_key(newVarName):
                newNameDict[tableName].update({newVarName:{'TVID':tvid,'VARNAME':varName, 'NEWVARNAME':varName,'VARTYPE':varType, \
                                                           'VARDEFAULT':varDefault,'SELECT':select,'DESCRIPTION':description}})
            else:
                #TableName in newNameDict has duplicate variable names
                print 'TABLE', tableName, 'has a duplicate NEWVARNAME', newVarName, 'TVID', tvid, 'in data dictionary type 2'
        i=i+1
    temp_file.close()
    return originalNameDict, newNameDict
     
def inferDataDictionary(dataTableName = '', newDataStringList = [], oldDict = {}):
    '''
    This function identifies the type to be assigned to each variable based
    on the type in row 1 of a dataStringList following after the
    list of variable names in row 0.  It is then assumed that
    the types of all of the remaining data in a given column are consistent
    with those indicated in the second row.  The types are cast hierarchically
    starting with integer, and if that fails (the variable can not be converted
    to an integer), then a float, and if that fails, then the variable must be in a
    string format.  As a result if there is a variable that is entered in row 1 as '5'
    and the variable in the same column in the next row is '5.6', then an error
    will occur.  This can be avoided by recording '5.' or '5.0' in the first row. 
    '''
    end_i = len(newDataStringList)
    if end_i <= 1:
        print 'typeDataset.typeDatasetWithoutDataDictionary() error'
        print 'newDataStringList has only 1 row but requires 2 rows'
        print 'the first row must contain the variable names'
        print 'the second row and all other rows must contain variable vaulues'
        
    else:
        if oldDict.has_key(dataTableName) == True:
            print 'makeDD.makeNewDataDictionary error'
            print 'cannot update oldDict due to pre-existing dataTableName:', dataTableName
        else:
            oldDict.update({dataTableName:{}})
            #Get variable name list from row 0 in newDataStringList
            varNamesList = newDataStringList[0]
            if varNamesList == []:
                print 'makeDD.makeNewDataDictionary error'
                print 'there are no variable names in dataTableName:', dataTableName
            else:
                end_j = len(varNamesList)
                #Establish variable type based on type according to first row
                #Note that all variables must be of a consitent type - either integer (no decimal place), float or string  
                for j in range(0,end_j,1):
                    varName = varNamesList[j]
                    try:
                        newVarValue = int(newDataStringList[1][j])
                    except:
                        try:
                            newVarValue = float(newDataStringList[1][j])
                        except:
                            varType = 'string'
                        else:
                            varType = 'float'
                    else:
                        varType = 'integer'
                    if oldDict[dataTableName].has_key(varName) == False:
                        oldDict[dataTableName].update({varName:{'TVID':j,'VARNAME':varName,'NEWVARNAME':'','VARTYPE':varType, \
                                                            'VARDEFAULT':'','SELECT':1,'DESCRIPTION':''}})
                    else:
                        print 'makeDD.makeNewDataDictionary error'
                        print 'dataTableName:', dataTableName, 'has duplicate variable names:', varName
                        print 'unable to include both variables in dictionary'
            return oldDict
     

def inferDataDictionary_v2(dataTableName = '', filePath = '', fileExtension = '.csv', printTypes = 'YES', nLines = -1):
    '''
    This is adaptation of inferDataDictionary where nLines of the file are reviewed
    to determine the types associated with each field.  If nLines = -1 then
    the routine will process all of the lines in the dataTableName.

    This routine also returns an oldDict and a newDict consistent with the version 2
    type dict.  In this instance oldDict and newDict keyNames associated with a
    given table name are the same.
        
    This function declares the type to be assigned to each variable names identified
    in the top row after processing all of the rows in the file following after the
    top row.

    All variables are initially assigned as integers.  All of the values in column
    must be integer. If one of the values is identified as not an integer
    but a field or a string then the type is reset from integer to either a
    float or a string.  Similarly if a type has been reset to a float and
    one of the values in a column is later found to be a string then the
    type for that column will be reset to string.

    If printValues == 'YES" then the tableName, variable names and
    the assigned types will be printed to the screen at the end.

    Updated February 18 2013

    Ian Moss
    
    '''
    #Check if dataTableName already has file extension
    dataTableNameList = dataTableName.split('.')
    if len(dataTableNameList)>=2:
        file_path = filePath + dataTableName
        dictTableName = dataTableNameList[0]
    else:
        file_path = filePath + dataTableName + fileExtension
        dictTableName = dataTableName
    
    oldDict = {dictTableName:{}}
    newDict = {dictTableName:{}}
    temp_file =open (file_path,'r')
    header = []
    varTypeList = []
    end_j = 0
    i=0
    for line in temp_file:
        newList = []
        x = line.rstrip()
        if not line == []:
            line = line.replace('"','').strip()
            x = x.split(',')
            for item in x:
                y = item.replace('"','').strip()
                if i == 0:
                    header.append(y)
                    varTypeList.append('integer')
                    end_j = end_j + 1
                else:
                    newList.append(y)
        if i == 0:
            if header == []:
                print 'makeDD.makeNewDataDictionaryFromLargeDataStringFile error'
                print 'there are no variable names in dataTableName:', dataTableName
        else:
            if not len(newList) == end_j:
                print 'makeDD.makeNewDataDictionaryFromLargeDataStringFile error'
                print 'starting at row 0 the newList row number is:', i
                print 'newList', newList, 'has more variables than variable names in header:', header
            else:
                #Establish variable type based on type according to first row
                #Note that all variables must be of a consitent type - either integer (no decimal place), float or string
                #Initialize typeList
                for j in range(0,end_j,1):
                    try:
                        newVarValue = int(newList[j])
                    except:
                        try:
                            newVarValue = float(newList[j])
                        except:
                            varType = 'string'
                        else:
                            varType = 'float'
                    else:
                        varType = 'integer'
                    if varTypeList[j] == 'integer' and varType == 'float':
                        varTypeList[j] = 'float'
                    if varTypeList[j] == 'integer' and varType == 'string':
                        varTypeList[j] = 'string'
                    if varTypeList[j] == 'float' and varType == 'string':
                        varTypeList[j] = 'string'
        i = i + 1
        if not nLines <= 0:
            if i == nLines:
                break
    #Close temporary file
    temp_file.close()        
    if printTypes == 'YES' or printTypes == 'Yes' or printTypes == 'yes' or printTypes == 'Y' or printTypes == 'y':
        print '\n New data dictionary created for table name:', dataTableName
        print ' The followsing data types have been assigned to the associated variable names:'
        print '\n VARNAME', 'vartype \n'
    for j in range(0, end_j, 1):
        varName = header[j]
        varType = varTypeList[j]
        if printTypes == 'YES' or printTypes == 'Yes' or printTypes == 'yes' or printTypes == 'Y' or printTypes == 'y':
            print '', varName, varType                    
        if oldDict[dictTableName].has_key(varName) == False:
            oldDict[dictTableName].update({varName:{'TVID':j,'NEWVARNAME':varName,'VARTYPE':varType, \
                                                            'VARDEFAULT':'','SELECT':1,'DESCRIPTION':''}})
            newDict[dictTableName].update({varName:{'TVID':j,'VARNAME':varName,'VARTYPE':varType, \
                                                            'VARDEFAULT':'','SELECT':1,'DESCRIPTION':''}})
        else:
            print 'makeDD.makeNewDataDictionaryFromLargeDataStringFile error'
            print 'dataTableName:', dictTableName, 'has duplicate variable names:', varName
            print 'unable to include both variables in dictionary'
    return oldDict, newDict

def checkIfTableNameInDictionary(tableName = '', dataDict = {}):
    dictHasTableName = False
    #Check for file extension in tableName and remove if present  
    newTableName = removeFileExtension(tableName)
    if dataDict.has_key(newTableName):
       dictHasTableName = True 
    return dictHasTableName


# ---------- Dictionary Database  Input Output Functions and Join ----------
#additive_nested_key_multiple_item_dictionary originally in dictionaryDBUtilities, 
#(c)  Ian Moss, 2006- 2012



def createDictDB(NewDict,KeyVarnames,TwoDList):
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


def initializeVariableHeader(header=[],printFilepath=''):
    '''
    This function takes a list of variable names, opens a new file
    or overwrites an old file of the same name and in the same directory
    and copies the variable names to a file in a csv format.
    '''
    newFile = open(printFilepath,'w')
    printline = ''
    for varName in header:
        printline = updateDictDBline(varName, printline, '%0.0f,', varName)
    printline = printline.rstrip(',')
    print >> newFile, printline
    newFile.close()
    return

def saveDictDB(keyList=[],header =[],myFile={}, printFilepath=''):
    '''
    This function prints a nested dictionary to a file.  The keyList
    provides a list of key variable names where the first key is assigned to
    the first level, the second key assigned to the second level, etc.
    The header provides a complete list of variables including the keys.
    The keyList variables must have a unique match with 1 of the variables
    in the header file.
    '''
    if not os.path.isfile(printFilepath):
        print printFilepath, 'does not exist in print_to_nested_dictionary'
    printFile = open(printFilepath, 'a')
    numberOfKeys = len(keyList)
    #for every key0 in the file
    for key0 in myFile:
        if numberOfKeys == 0:
            remainingVar = myFile
            keyVar = []
            printDictDBline(keyList,keyVar,header,remainingVar,printFile)
            break
        else:
            if numberOfKeys == 1:
                remainingVar = myFile[key0]
                keyVar = [key0]
                printDictDBline(keyList,keyVar,header,remainingVar,printFile)
            else:
                for key1 in myFile[key0]:
                    if numberOfKeys == 2:
                        remainingVar = myFile[key0][key1]
                        keyVar = [key0,key1]
                        printDictDBline(keyList,keyVar,header,remainingVar,printFile)
                    else:
                        for key2 in myFile[key0][key1]:
                            if numberOfKeys == 3:
                                remainingVar = myFile[key0][key1][key2]
                                keyVar = [key0,key1,key2]
                                printDictDBline(keyList,keyVar,header,remainingVar,printFile)
                            else:
                                for key3 in myFile[key0][key1][key2]:
                                    if numberOfKeys == 4:
                                        remainingVar = myFile[key0][key1][key2][key3]
                                        keyVar = [key0,key1,key2,key3]
                                        printDictDBline(keyList,keyVar,header,remainingVar,printFile)
                                    else:
                                        for key4 in myFile[key0][key1][key2][key3]:
                                            if numberOfKeys == 5:
                                                remainingVar = myFile[key0][key1][key2][key3][key4]
                                                keyVar = [key0,key1,key2,key3,key4]
                                                printDictDBline(keyList,keyVar,header,remainingVar,printFile)
                                            else:
                                                for key5 in myFile[key0][key1][key2][key3][key4]:
                                                    if numberOfKeys == 6:
                                                        remainingVar = myFile[key0][key1][key2][key3][key4][key5]
                                                        keyVar = [key0,key1,key2,key3,key4,key5]
                                                        printDictDBline(keyList,keyVar,header,remainingVar,printFile)
                                                    else:
                                                        for key6 in myFile[key0][key1][key2][key3][key4][key5]:
                                                            if numberOfKeys == 7:
                                                                remainingVar = file[key0][key1][key2][key3][key4][key5][key6]
                                                                keyVar = [key0,key1,key2,key3,key4,key5,key6]
                                                                printDictDBline(keyList,keyVar,header,remainingVar,printFile)
                                                            else:
                                                                print 'The number of keys in print_to_nested_dictionary is exceeded'
                                                                print 'number of keys:', numberOfKeys
    printFile.close()
    return

def saveDictDB_v2(filepath,keyList,fileHeader,dictionaryName):
    '''
    This subroutine checks a filepath to see if it exists. If not it creates
    a new file with the first line as the field header. In any event it writes
    the data in the nested dictionary file (dictionaryName) to the file in
    the appropriate format.
    '''
    if os.path.exists(filepath):
        saveDictDB(keyList,fileHeader,dictionaryName,filepath)
    else:
        initializeVariableHeader(fileHeader,filepath)
        saveDictDB(keyList,fileHeader,dictionaryName,filepath)
    return



def printDictDBline(keyVarnames,keyVar,header,remainingVar,printFile):
    printline = ''
    floatFormat = '%0.3f,'
    end_i = len(keyVar)
    for varName in header:
        flag = 'False'
        if remainingVar.has_key(varName):
            varValue = remainingVar[varName]
            printline = updateDictDBline(varValue, printline, floatFormat, varName)
            flag = 'True'
        else:
            for i in range(0,end_i):
                if varName == keyVarnames[i]:
                    varValue = keyVar[i]
                    printline = updateDictDBline(varValue, printline, floatFormat, varName)
                    flag = 'True'
                    break
            if flag == 'False':
                print 'varName:', varName, 'not found in keyVarnames or remainingVar from saveDictionaryDB'
                print 'keyVarnames or header:', keyVarnames, 'keyVarValues:', keyVar
                #print 'remainingVar:', remainingVar
                #print 'keyVarnames:', keyVarnames
    printline = printline.rstrip(',')
    print >> printFile, printline
    return

def updateDictDBline(varValue, printline, floatFormat, varName):
    '''
    Note tha a default float format must be specified,
    e.g. floatFormat = '%0.3f,'
    '''
    varType = type(varValue)
    if varType == ListType:
        end_i = len(varValue)
        for i in range(0,end_i,1):
            varType = type(varValue[i])
            if varType == StringType:
                printline = printline + varValue[i]
            else:
                if varType== IntType:
                    printline = printline + '%i' % varValue[i]
                else:
                    if varType == numpy.int32:
                        printline = printline + '%i' % varValue[i]
                    else:
                        if varType == FloatType or varType == numpy.float64:
                            printline = printline + floatFormat % varValue[i]
                        else:
                            print 'type of variable varName', varName, 'with value:', varValue, 'is:', varType,
                            print 'no such type provided for in update_printline'
            if not i == end_i-1:
                printline = printline + ','
    else:
        if varType == StringType:
            printline = printline + varValue + ','
        else:
            if varType== IntType:
                printline = printline + '%i,' % varValue
#            else:
#                if varType == numpy.int32:
#                    printline = printline + '%i' % varValue
            else:
                if varType == FloatType or varType == numpy.float64:
                    printline = printline + floatFormat% varValue
                else:
                    print 'type of variable varName', varName, 'with value:', varValue, 'is:', varType,
                    print 'no such type provided for in update_printline'
    return printline
    
   
   
def joinDictDBs(parentDict,childDict, keyVarnames):
    '''
    Created December 14, 2010; Updated Dec 5th 2012
    A temporary dictionary with the same key variable name structure as the master dictionary
    is added to the master dictionary
    Assumptions:
        Keys in both parentDict and childDict match.
        1. Can do equivalent of an append command, combined dictionary superset of parentDict and childDict
        and where parentDict and childDict have the same variables but different key values (append). 
        2. Have same keys, between parentDic and chiuldDict, but have different variables (1-1 join)
        3. For every key in parent dict, there are several keys (other key variable) in childDict, and other 
        non-key variables in childDict (inner join)
        
        If parentDict and childDict do not match the above 3 conditions, there are no guarantees
        as to what the code will output. 
        
        Current Expected Behaviour (will have to add check's and unit tests for)
        1. Both dictionaries to join have same variable names, but different keys.
            Result is an append
        2. childDict does not have all the keys in parentDict. 
            Result is that there will be keys with no variable names
        3. parentDict does not have all the keys in childDict.
            Result is keys get added to parentDict
        4. Identical keys in parent and childDict, but mutually exclusive variable names
            Result is equivalent to an inner join
            
            
        
    '''
    nKeys = len(keyVarnames)
    if nKeys <= 0:
        for varName in childDict:
            newValue = childDict[varName]
            if not parentDict[Key1].has_key(varName):
                parentDict.update({varName:varValue})
    else:
        if nKeys >= 1:
            for Key1 in childDict:
                if not parentDict.has_key(Key1):
                    parentDict.update({Key1:{}})
                if nKeys == 1:
                    for varName in childDict[Key1]:
                        varValue = childDict[Key1][varName]
                        if not parentDict[Key1].has_key(varName):
                            parentDict[Key1].update({varName:varValue})
                else:
                    if nKeys >= 2:
                        for Key2 in childDict[Key1]:
                            if not parentDict[Key1].has_key(Key2):
                                parentDict[Key1].update({Key2:{}})
                            if nKeys == 2:
                                for varName in childDict[Key1][Key2]:
                                    varValue = childDict[Key1][Key2][varName]
                                    if not parentDict[Key1][Key2].has_key(varName):
                                        parentDict[Key1][Key2].update({varName:varValue})
                            else:
                                if nKeys >= 3:
                                    for Key3 in childDict[Key1][Key2]:
                                        if not parentDict[Key1][Key2].has_key(Key3):
                                            parentDict[Key1][Key2].update({Key3:{}})
                                        if nKeys == 3:
                                            for varName in childDict[Key1][Key2][Key3]:
                                                varValue = childDict[Key1][Key2][Key3][varName]
                                                if not parentDict[Key1][Key2][Key3].has_key(varName):
                                                    parentDict[Key1][Key2][Key3].update({varName:varValue})
                                        else:
                                            if nKeys >= 4:
                                                for Key4 in childDict[Key1][Key2][Key3]:
                                                    if not parentDict[Key1][Key2][Key3].has_key(Key4):
                                                        parentDict[Key1][Key2][Key3].update({Key4:{}})
                                                    if nKeys == 4:
                                                        for varName in childDict[Key1][Key2][Key3][Key4]:
                                                            varValue = childDict[Key1][Key2][Key3][Key4][varName]
                                                            if not parentDict[Key1][Key2][Key3][Key4].has_key(varName):
                                                                parentDict[Key1][Key2][Key3][Key4].update({varName:varValue})
                                                    else:
                                                        if nKeys >= 5:
                                                            for Key5 in childDict[Key1][Key2][Key3][Key4]:
                                                                if not parentDict[Key1][Key2][Key3][Key4].has_key(Key5):
                                                                    parentDict[Key1][Key2][Key3][Key4].update({Key5:{}})
                                                                if nKeys == 5:
                                                                    for varName in childDict[Key1][Key2][Key3][Key4][Key5]:
                                                                        varValue = childDict[Key1][Key2][Key3][Key4][Key5][varName]
                                                                        if not parentDict[Key1][Key2][Key3][Key4][Key5].has_key(varName):
                                                                            parentDict[Key1][Key2][Key3][Key4][Key5].update({varName:varValue})
                                                                else:
                                                                    if nKeys >= 6:
                                                                        for Key6 in childDict[Key1][Key2][Key3][Key4][Key5]:
                                                                            if not parentDict[Key1][Key2][Key3][Key4][Key5].has_key(Key6):
                                                                                parentDict[Key1][Key2][Key3][Key4][Key5].update({Key6:{}})
                                                                            if nKeys == 6:
                                                                                for varName in childDict[Key1][Key2][Key3][Key4][Key5][Key6]:
                                                                                    varValue = childDict[Key1][Key2][Key3][Key4][Key5][Key6][varName]
                                                                                    if not parentDict[Key1][Key2][Key3][Key4][Key5][Key6].has_key(varName):
                                                                                        parentDict[Key1][Key2][Key3][Key4][Key5][Key6].update({varName:varValue})
                                                                            else:
                                                                                if nKeys >= 7:
                                                                                    for Key7 in childDict[Key1][Key2][Key3][Key4][Key5][Key6]:
                                                                                        if not parentDict[Key1][Key2][Key3][Key4][Key5][Key6].has_key(Key7):
                                                                                            parentDict[Key1][Key2][Key3][Key4][Key5][Key6].update({Key7:{}})
                                                                                        if nKeys == 7:
                                                                                            for varName in childDict[Key1][Key2][Key3][Key4][Key5][Key6][Key7]:
                                                                                                varValue = childDict[Key1][Key2][Key3][Key4][Key5][Key6][Key7][varName]
                                                                                                if not parentDict[Key1][Key2][Key3][Key4][Key5][Key6][Key7].has_key(varName):
                                                                                                    parentDict[Key1][Key2][Key3][Key4][Key5][Key6][Key7].update({varName:varValue})                            
    return newDict


# Code sent by Ian Dec 5 2012; added Feb 5 2013 to get MonctonWorklow to work
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
            newKeyValueList.append([]) # typo in Value fixed Feb 6 2013
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
                       # if not newDict[Key1].has_key(varName):
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

def appendNewDictToMasterDictionary(masterDict,tempDict, keyVarnames):
    '''
    Created December 14, 2010
    A temporary dictionary with the same key variable name structure as the master dictionary
    is added to the master dictionary
    '''
    nKeys = len(keyVarnames)
    if nKeys <= 0:
        for varName in tempDict:
            newValue = tempDict[varName]
            if not masterDict[Key1].has_key(varName):
                masterDict.update({varName:varValue})
    else:
        if nKeys >= 1:
            for Key1 in tempDict:
                if not masterDict.has_key(Key1):
                    masterDict.update({Key1:{}})
                if nKeys == 1:
                    for varName in tempDict[Key1]:
                        varValue = tempDict[Key1][varName]
                        if not masterDict[Key1].has_key(varName):
                            masterDict[Key1].update({varName:varValue})
                else:
                    if nKeys >= 2:
                        for Key2 in tempDict[Key1]:
                            if not masterDict[Key1].has_key(Key2):
                                masterDict[Key1].update({Key2:{}})
                            if nKeys == 2:
                                for varName in tempDict[Key1][Key2]:
                                    varValue = tempDict[Key1][Key2][varName]
                                    if not masterDict[Key1][Key2].has_key(varName):
                                        masterDict[Key1][Key2].update({varName:varValue})
                            else:
                                if nKeys >= 3:
                                    for Key3 in tempDict[Key1][Key2]:
                                        if not masterDict[Key1][Key2].has_key(Key3):
                                            masterDict[Key1][Key2].update({Key3:{}})
                                        if nKeys == 3:
                                            for varName in tempDict[Key1][Key2][Key3]:
                                                varValue = tempDict[Key1][Key2][Key3][varName]
                                                if not masterDict[Key1][Key2][Key3].has_key(varName):
                                                    masterDict[Key1][Key2][Key3].update({varName:varValue})
                                        else:
                                            if nKeys >= 4:
                                                for Key4 in tempDict[Key1][Key2][Key3]:
                                                    if not masterDict[Key1][Key2][Key3].has_key(Key4):
                                                        masterDict[Key1][Key2][Key3].update({Key4:{}})
                                                    if nKeys == 4:
                                                        for varName in tempDict[Key1][Key2][Key3][Key4]:
                                                            varValue = tempDict[Key1][Key2][Key3][Key4][varName]
                                                            if not masterDict[Key1][Key2][Key3][Key4].has_key(varName):
                                                                masterDict[Key1][Key2][Key3][Key4].update({varName:varValue})
                                                    else:
                                                        if nKeys >= 5:
                                                            for Key5 in tempDict[Key1][Key2][Key3][Key4]:
                                                                if not masterDict[Key1][Key2][Key3][Key4].has_key(Key5):
                                                                    masterDict[Key1][Key2][Key3][Key4].update({Key5:{}})
                                                                if nKeys == 5:
                                                                    for varName in tempDict[Key1][Key2][Key3][Key4][Key5]:
                                                                        varValue = tempDict[Key1][Key2][Key3][Key4][Key5][varName]
                                                                        if not masterDict[Key1][Key2][Key3][Key4][Key5].has_key(varName):
                                                                            masterDict[Key1][Key2][Key3][Key4][Key5].update({varName:varValue})
                                                                else:
                                                                    if nKeys >= 6:
                                                                        for Key6 in tempDict[Key1][Key2][Key3][Key4][Key5]:
                                                                            if not masterDict[Key1][Key2][Key3][Key4][Key5].has_key(Key6):
                                                                                masterDict[Key1][Key2][Key3][Key4][Key5].update({Key6:{}})
                                                                            if nKeys == 6:
                                                                                for varName in tempDict[Key1][Key2][Key3][Key4][Key5][Key6]:
                                                                                    varValue = tempDict[Key1][Key2][Key3][Key4][Key5][Key6][varName]
                                                                                    if not masterDict[Key1][Key2][Key3][Key4][Key5][Key6].has_key(varName):
                                                                                        masterDict[Key1][Key2][Key3][Key4][Key5][Key6].update({varName:varValue})
                                                                            else:
                                                                                if nKeys >= 7:
                                                                                    for Key7 in tempDict[Key1][Key2][Key3][Key4][Key5][Key6]:
                                                                                        if not masterDict[Key1][Key2][Key3][Key4][Key5][Key6].has_key(Key7):
                                                                                            masterDict[Key1][Key2][Key3][Key4][Key5][Key6].update({Key7:{}})
                                                                                        if nKeys == 7:
                                                                                            for varName in tempDict[Key1][Key2][Key3][Key4][Key5][Key6][Key7]:
                                                                                                varValue = tempDict[Key1][Key2][Key3][Key4][Key5][Key6][Key7][varName]
                                                                                                if not masterDict[Key1][Key2][Key3][Key4][Key5][Key6][Key7].has_key(varName):
                                                                                                    masterDict[Key1][Key2][Key3][Key4][Key5][Key6][Key7].update({varName:varValue})                            
    return masterDict

# ---------- Variable Extraction Functions ----------

# ---------- Data Transformation Functions: Relational Data Processing ----------
#Data Transformation Functions from IBCCLAIMS and LINK_LTIME_TO_DRUID_ATTR, (c) Ian Moss, 2012

def create_year_and_month_id(claimsDict, druidList):
    '''
    This function creates does the following
    1. Finds a list of all the years associated with the claims in a dictionary.
    2. Creates a unique year-month ID (YMID) starting at 1 in the first month
    of the first (earliest) year and ending at N in the 12th month of the latest
    year, in increments of 1 month at a time.
    3. Creates a dictionary (ymIdDict) with key varnames as [YEAR][MONTH] to access unique YMID.
    4. Creates another (reverse dictionary; revYmIdDict) dictionary with key varname [YMID] to access [YEAR] and [MONTH]
    5. Returns the two dictionaries
    '''
    #Create  Year-Month ID
    ymIdDict = {}
    newYearList = []
    revYmIdDict = {}
    newDruidList = []
    for druid in druidList:
        yearList = claimsDict[druid].keys()
        yearList.sort()
        #Get complete list of years from dictionary
        for year in yearList:
            if not year in newYearList:
                newYearList.append(year)
    #Start compiling ymidDict
    newYearList.sort()
    maxYear = max(newYearList)
    minYear = min(newYearList)
    #initialize year month count and assign as YMID
    yearMonthCount = 1
    for year in range(minYear,maxYear+1,1):
        ymIdDict.update({year:{}})
        for month in range(1,13,1):
            #Create Year Month to YMID dictionary
            ymIdDict[year].update({month:{'YMID':yearMonthCount}})
            #Create YMID to Year Month Dictionary
            revYmIdDict.update({yearMonthCount:{'YEAR':year, 'MONTH':month}})
            #Increment yearMonthCount 
            yearMonthCount = yearMonthCount + 1
    return ymIdDict,revYmIdDict


def get_earliest_druid_claims_dates(claimsDict, druidList, ymidList,revYmidDict):
    '''
    For each DRUID the earlies YMID, YEAR and MONTH are identifed and
    entered into a new dictionary
    '''
    newDict = {}
    #Create DRUID start date dictionary
    for druid in druidList:
        for ymid in ymidList:
            if newDict.has_key(druid):
                break
            year = revYmidDict[ymid]['YEAR']
            if claimsDict[druid].has_key(year):
                month = revYmidDict[ymid]['MONTH']
                if claimsDict[druid][year].has_key(month):
                    year = revYmidDict[ymid]['YEAR']
                    month = revYmidDict[ymid]['MONTH']
                    newDict.update({druid:{'EYMID':ymid,'EYEAR':year,'EMONTH':month}})            
    return newDict


def summarize_earliest_date_results(earliestDateDict):
    '''
    This generates a summary of the number of DRUIDS associated with each
    eariest data and puts it in a dictionary using
    earliest month YMID (EYMID) as the key and incrementing the DRUID count (DCOUNT)
    for each DRUID with that eariest date.  This information is for descriptive purposes
    ... providing a basic summary of the nature of the claims data being used in
    the analyses.
    '''
    earlyDateSummaryDict = {}
    for druid in earliestDateDict:
        eymid = earliestDateDict[druid]['EYMID']
        if not earlyDateSummaryDict.has_key(eymid):
            eyear = earliestDateDict[druid]['EYEAR']
            emonth = earliestDateDict[druid]['EMONTH']
            earlyDateSummaryDict.update({eymid:{'EYEAR':eyear,'EMONTH':emonth,'DCOUNT':0}})
        #earlyDateSummaryDict[eymid]['DAREA'] = earlyDateSummaryDict[eymid]['DAREA'] + earliestDateDict[druid]['DAREA']
        earlyDateSummaryDict[eymid]['DCOUNT'] = earlyDateSummaryDict[eymid]['DCOUNT'] + 1
    return earlyDateSummaryDict

def initialize_lamda_dictionary(druidList, ymidList):
    '''
    '''
    newDict = {}
    for druid in druidList:
        newDict.update({druid:{}})
        for ymid in ymidList:
            ymidVarName = 'YM' + str(ymid)
            newDict[druid].update({ymidVarName:{'YMCLAIM':0,'YMID':ymid}})
    return newDict


def compile_lamda_claim_months(claimsDict,druidList, ymidDict, lamdaDict):
    '''
    This enters a 1 for every DRUID year and month where a damage claim was recorded 
    '''
    for druid in druidList:
        yearList = claimsDict[druid].keys()
        yearList.sort()
        for year in yearList:
            monthList = claimsDict[druid][year].keys()
            monthList.sort()
            for month in monthList:
                ymid = ymidDict[year][month]['YMID']
                ymidVarName = 'YM'+str(ymid)
                lamdaDict[druid][ymidVarName]['YMCLAIM'] = 1
    return lamdaDict

def create_a_list_of_zeros_of_length_equal_to_inputList(inputList = []):
    '''
    Creates a new list of zeros of length equal length equal to the input list
    '''
    newList = []
    listLength = len(inputList)
    for i in range(0,listLength):
        newList.append(0)
    return newList



def update_druidClaimMonthList(claimsList = [],claimsDict = {}):
    '''
    This takes an initial claimsList (druidClaimMonthList) with zeros
    assigned to each year-month-id and adds 1 for each month where a claim was
    made in a DRUID as recorded in the lamdaDict.
    
    '''
    #Get number of DRUIDS to tally proportion of DRUID-MONTH-CLAIMS
    druidKeyList = claimsDict.keys()
    nDruids = len(druidKeyList)
    for druid in claimsDict:
        for ymidVarName in claimsDict[druid]:
            #ymid is the year and month identifier starting at 1
            ymid = claimsDict[druid][ymidVarName]['YMID']
            noClaims = claimsDict[druid][ymidVarName]['YMCLAIM']
            claimsList[ymid-1] = claimsList[ymid-1] + noClaims/float(nDruids)
            #Check the results
            #if noClaims == 1:
            #    print druid, ymidVarName, ymid, noClaims
    return claimsList

def compile_average_number_of_events_per_unit_of_time_period_and_number_of_events(lamdaDict={}, druidList=[], ymidList = []):
    '''
    For each DRUID count the number of months starting at the time of the earliest claim
    until the end of the record (NPERIODS).  Also count the number of months in which a
    claim occurred (NEVENTS). Calulate the ratio of the number of events divided
    by the number of periods (EPT); this is lamda in the Poisson ditribution.
    Note that the Poisson ditribution is an approximation of the binomial distribution
    and works well for long periods of time (e.g. for 100 months or more) but does poorly
    for shorter periods of time (i.e. the binomial distribution shoulod be used instead.)

    These calculations are done over the whole period of record of claim.
    '''
    newDict = {}
    #For each DRUID count the
    for druid in druidList:
        nEvents = 0
        nPeriods = 0
        start = False
        for ymid in ymidList:
            ymidVarName = 'YM'+str(ymid)
            if lamdaDict[druid][ymidVarName]['YMCLAIM'] == 1:
                start = True
            if start == True:
                nPeriods = nPeriods + 1
                if lamdaDict[druid][ymidVarName]['YMCLAIM'] == 1:
                    nEvents = nEvents + 1
        ept = nEvents / float(nPeriods)
        newDict.update({druid:{'NEVENTS':nEvents,'NPERIODS':nPeriods, 'EPT':ept}})
    return newDict



def compile_events_between_start_and_end_year(ltimeDict={},earlyDateDict={}, claimsDict={}, start_year=1900, end_year=2000):
    '''
    Change input and output variable names
    
    For each DRUID determine whether the earliest claim date (from the earlyDateDict)
    occurs on or before the last year - if so it is eligible for inclusion in the
    analysis (eventYear = 1), if not it is excluded (eventYear = 0).If at least 1
    claim event occurs between the start and end years then claimEvent = 1, otherwise
    claimEvent = 0.  Finaly the total number of DRUID-CLAIM months that occurred during
    the period are recorded from, 0, 1, 2, ...n (cumEvents).
    '''
    newDruidList = ltimeDict.keys()
    newDruidList.sort()
    for druid in newDruidList:
        eventYear = 0
        claimEvent = 0
        earlyDateYear = earlyDateDict[druid]['EYEAR']
        cumEvents = 0
        if earlyDateYear <= end_year:
            eventYear = 1
            for year in range(start_year, end_year + 1, 1):
                if claimsDict[druid].has_key(year):
                    claimEvent = 1
                    cumEvents = cumEvents + 1
        ltimeDict[druid].update({'EYDRUID': eventYear, 'EL5Y': claimEvent, 'NEL5Y': cumEvents})                        
    return ltimeDict




