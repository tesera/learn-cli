'''
Set file paths
'''
import sys
import config
#Identify admin code directory
#adminPath = '/shared/GitHub/Tesera/Rwd/Python/Admin/'
#self.filePath = '/shared/GitHub/Tesera/Rwd/'
#self.dataFilePath = '/shared/GitHub/Tesera/Rwd/'
#dictFilePath = '/shared/GitHub/Tesera/Rwd/Python/DATDICT/'
#fileExtension = '.csv'
#readErrorFilePath = '/shared/GitHub/Tesera/Rwd/Python/PyReadError/'

# ammended 20150828 by MB and SK
adminPath = '/opt/MRAT_Refactor/Rwd/Python/Admin'
dictFilePath = '/opt/MRAT_Refactor/Rwd/Python/DATDICT/'
fileExtension = '.csv'
readErrorFilePath = '/opt/MRAT_Refactor/Rwd/Python/PyReadError/'

#Add directory to sys.path 
sys.path.append(adminPath)

import makeDD
import dataMachete
import readCSV
import typeDataset
import fuzzyC_v2
import PRINTv1
import addToDataMachette20121026
import dictionaryDBUtilities
import innerJoinDictDBs
import fileUtilities
import MATRIX_MAN
from copy import deepcopy
import numpy
import math
import bisect
import time
import datetime
from dbfpy import dbf
from types import *
import os
from scipy import linalg

class RoutineLviApplications:
    filePath = ''
    dataFilePath = ''

    def __init__(self):
        self.filePath = config.args['OUTPUT-DIR']
        self.dataFilePath = config.args['OUTPUT-DIR']

    def ReadLviDataDictionary(self, filename = 'PyRDataDict'):
        '''
        Read LVI data dictionary contained in
        /Rwd/Python/DATDICT/ ... directory with filename
        PyRDataDict.csv

        Note that this dictionary estblishes variable names and types. 
        '''
        originalDict, newDict = makeDD.dataDictionaryType_21(dictFilePath,filename, fileExtension)
        return originalDict, newDict

    def ReadStandardDataDictionary(self, filename = ''):
        '''
        Read Standard data dictionary contained in
        /Rwd/ ... directory with filename
        PyRDataDict.csv

        Note that this dictionary estblishes variable names and types. 
        '''
        originalDict, newDict = makeDD.dataDictionaryType_21(self.dataFilePath,filename, fileExtension)
        return originalDict, newDict

    def UpdateDataDictionaryWithNewTableName(self, myDataDict={}, oldTableName = '', newTableName = ''):
        '''
        This program takes a standard version 2 data dictionary with a given
        table name as the primary key and adds a table name to represent a current
        file, allowing for processing of multiple files. 

        The data dictionary in this case is used for type casting of variables

        Ian Moss
        Aporil 18 2013
        '''
        myDataDict.update({newTableName:myDataDict[oldTableName]})
        return myDataDict


    def GetNewHeader(self, originalDataDict = {}, dataStringList=[[]], dataTableName = ''):
        '''
        '''
        newHeader = []
        varCount = 0
        for oldVarName in dataStringList[0]:
            if not originalDataDict[dataTableName].has_key(oldVarName):
                print ' originalDataDict dataTableName: ', dataTableName, 'does not have variable name: ', oldVarName
                print ' Old variable name: ', oldVarName, 'used as newVariablename'
                newHeader.append(oldVarName)
            else:
                newVarName = originalDataDict[dataTableName][oldVarName]['NEWVARNAME']
                if newVarName == '' or newVarName == ' ' or newVarName == '   ':
                    newHeader.append(oldVarName)
                else:
                    newHeader.append(newVarName)
        return newHeader

    def ReadCsvDataFile(self, dataDict = {}, dataTableName = '', readErrorFileName = ''):
        '''
        Inputs
            dataDict is the dictionary containing table name, variable name and variable types (i.e. originalDict or newDict
            dataPath is the file path 
            dataTableName must be a string variable without any file extension but referring to a CSV file
            readErrorFilePath is the read error file path relating to the use of the data dictionary to establish a variable type
            readErrorFileName is the dsired name of the read error file without any extension
            fileExtension refers to the type of file, e.g. .txt or .csv
        '''
        dataErrorFilePath = readErrorFilePath + readErrorFileName + '.txt'
        dataStringList = readCSV.read_csv_text_file_v2(self.filePath, dataTableName, fileExtension)
        dataTypedList = typeDataset.typeDataset_v2(dataStringList, dataDict, dataTableName, dataErrorFilePath)
        return dataTypedList

    def ReadFirstNlinesInCsvDataFile_v2(self, originalDataDict = {}, newDataDict = {}, dataTableName = '', readErrorFileName = '', nLines = 1):
        '''
        '''
        dataErrorFilePath = readErrorFilePath + readErrorFileName + '.txt'
        PRINTv1.deleteFileIfItExists(dataErrorFilePath)
        dataStringList = readCSV.read_first_nLines_csv_text_file_v2(self.filePath, dataTableName, fileExtension, nLines)
        if originalDataDict == {} and newDataDict == {}:
            originalDataDict = makeDD.makeNewDataDictionaryFromDataStringFile(dataTableName , dataStringList, oldDict = {})
            newDataDict = originalDataDict
        oldHeader = dataStringList[0]
        newHeader = self.GetNewHeader(originalDataDict, dataStringList, dataTableName)
        dataStringList[0] = newHeader
        dataTypedList = typeDataset.typeDataset_v2(dataStringList, newDataDict, dataTableName, dataErrorFilePath)
        return dataTypedList
                                        


    def ReadCsvDataFile_v2(self, originalDataDict = {}, newDataDict = {}, dataTableName = '', readErrorFileName = ''):
        '''
        Inputs
            dataDict is the dictionary containing table name, variable name and variable types (i.e. originalDict or newDict
            dataPath is the file path 
            dataTableName must be a string variable without any file extension but referring to a CSV file
            readErrorFilePath is the read error file path relating to the use of the data dictionary to establish a variable type
            readErrorFileName is the dsired name of the read error file without any extension
            fileExtension refers to the type of file, e.g. .txt or .csv
            #Note that this version accounts for changes from old (i.e. VARNAME) to new (i.e. NEWVARNAME) variable names

            If the originalDataDict = {} and the newDataDict = {} then the program will try to make a new dictionary from
            the first line below the header after importing the file as a string list.

            #Note that this version does not account for changes from old (i.e. VARNAME) to new (i.e. NEWVARNAME) variable names
            #This deficiency was corrected in ReadCsvDataFile_v2
        '''
        dataErrorFilePath = readErrorFilePath + readErrorFileName + '.txt'
        PRINTv1.deleteFileIfItExists(dataErrorFilePath)
        dataStringList = readCSV.read_csv_text_file_v2(self.filePath, dataTableName, fileExtension)
        if originalDataDict == {} and newDataDict == {}:
            originalDataDict = makeDD.makeNewDataDictionaryFromDataStringFile(dataTableName , dataStringList, oldDict = {})
            newDataDict = originalDataDict
        oldHeader = dataStringList[0]
        newHeader = self.GetNewHeader(originalDataDict, dataStringList, dataTableName)
        dataStringList[0] = newHeader
        dataTypedList = typeDataset.typeDataset_v2(dataStringList, newDataDict, dataTableName, dataErrorFilePath)
        return dataTypedList

    def ReadCsvDataFileAndTransformIntoDictionaryFormat(self, dataDict = {}, dataTableName = '', readErrorFileName = '', keyVarNameList = []):
        '''
        Inputs
            dataDict is the dictionary containing table name, variable name and variable types (i.e. originalDict or newDict
            dataPath is the file path 
            dataTableName must be a string variable without any file extension but referring to a CSV file
            keyVarNameList is a list of key variable names in string format starting with Primary, Secondary, Tertiary ... keys
            readErrorFilePath is the read error file path relating to the use of the data dictionary to establish a variable type
            readErrorFileName is the dsir name of the read error file without any extension
            fileExtension refers to the type of file, e.g. .txt or .csv

            Note that this version does not adequately account for transition from old to new variable names.
            To correct for this problem ReadCsvDataFileAndTransformIntoDictionaryFormat_v2 as created instead
        '''
        newDict = {}
        dataTypedList = ReadCsvDataFile(dataDict, dataTableName, readErrorFileName)
        newHeader = dataTypedList[0]
        newDict = dictionaryDBUtilities.additive_nested_key_multiple_item_dictionary(newDict,keyVarNameList,dataTypedList)
        return newHeader, newDict

    def ReadCsvDataFileAndTransformIntoDictionaryFormat_v2(self, originalDataDict = {}, newDataDict = {}, dataTableName = '', readErrorFileName = '', keyVarNameList = []):
        '''
        Inputs
            originalDataDict is the dictionary containing table name, variable name and variable types (i.e. VARNAME and VARTYPE)
            newDataDict is the dictionary containing table name, new variable names and variable types (i.e. NEWVARNAME and VARTYPE)
            dataPath is the file path 
            dataTableName must be a string variable without any file extension but referring to a CSV file
            keyVarNameList is a list of key variable names in string format starting with Primary, Secondary, Tertiary ... keys
            readErrorFilePath is the read error file path relating to the use of the data dictionary to establish a variable type
            readErrorFileName is the dsired name of the read error file without any extension
            fileExtension refers to the type of file, e.g. .txt or .csv

            Note that this version corrects a deficiency in the original ReadCsvDataFileAndTransformIntoDictionaryFormat
            It allows for the original variable names (i.e. VARNAME) in the data DICTIONARY to be replaced by the new names (i.e. NEWVARNAME)
            
        '''
        newDict = {}
        dataTypedList = self.ReadCsvDataFile_v2(originalDataDict, newDataDict, dataTableName, readErrorFileName)
        newHeader = dataTypedList[0]
        newDict = dictionaryDBUtilities.additive_nested_key_multiple_item_dictionary(newDict,keyVarNameList,dataTypedList)
        return newHeader, newDict


    def TransformDataTypedListIntoDictionaryFormat(self, keyVarNameList = [], dataTypedList = [], newDict = {}):
        '''
        Inputs
            newDict is an existing dataset already in a dictionary format - usually assumed to be empty to begin with
            dataTypedList is a dataset that has been brought into the Python environment with variables transformed into the correct data types
            keyVarNameList is a list of key variable names in string format starting with Primary, Secondary, Tertiary ... keys
        '''
        newHeader = dataTypedList[0]
        newDict = dictionaryDBUtilities.additive_nested_key_multiple_item_dictionary(newDict,keyVarNameList,dataTypedList)
        return newHeader, newDict



    def ReadXVarSelv1XorYVariableList(self, dataDict = {}, varSelCriteria = 'Y', dataTableName = 'XVARSELV1', readErrorFileName = 'ERROR-CHECK-XVARSELV1'):
        '''
        Inputs
            datDict         A data dictionary containing the data
            varSelCriteria  Select a variable that has a value 
        '''
        varSelvTypedList = ReadCsvDataFile(dataDict, dataTableName, readErrorFileName)
        end_i = len(varSelvTypedList)
        varSelList = []
        for i in range(0,end_i,1):
            if varSelvTypedList[i][2] == varSelCriteria:
                newVar = varSelvTypedList[i][1]
                varSelList.append(newVar)   
        return varSelList

    def createNewListFromSelectVariableListAndIdList(self, keyVarNameList = [], selectVarList = [], typedList = [[]]):
        '''
        '''
        #Initialize keyVarValueList and selVarValueList:
        keyColNoList = getVariableNameColumnNumbers(keyVarNameList, typedList[0])
        selColNoList = getVariableNameColumnNumbers(selectVarList, typedList[0])
        #Initialize the key value lists and the corresponding select value lists
        #These includes an embedded list for proper indexing with typedList 
        keyVarValueList = [[]]
        selVarValueList = [[]]
        #Get Length of typedList
        lenTypedList = len(typedList)
        lenKeyVar = len(keyVarNameList)
        if lenKeyVar < len(keyColNoList):
            print 'some variable names in keyVarNameList', keyVarNameList, 'not found in typed list'
            checkForMissingVariableNameInVariableList(typedList[0], keyVarNameList)    
        lenSelVar = len(selectVarList)
        if lenSelVar < len(selColNoList):
            print 'some variable names in selectVarList', selectVarList, 'not found in typed list'
            checkForMissingVariableNameInVariableList(typedList[0], selectVarList)
        #For each line starting in line 1 in the typedList
        for i in range(1, lenTypedList, 1):
            #add a new List
            keyVarValueList.append([])
            selVarValueList.append([])
            for j in range(0, lenKeyVar, 1):
                keyColNo = keyColNoList[j]
                keyVarValueList[i].append(typedList[i][keyColNo])
            for l in range(0,lenSelVar):
                selColNo = selColNoList[l]
                selVarValueList[i].append(typedList[i][selColNo])
        del(keyVarValueList[0])
        del (selVarValueList[0])
        return keyVarValueList, selVarValueList

    def createSelectVariableListFromXvarselv1TypedDict(self, varSelTypedDict = {}, varSelectCriteria = 'Y'):
        '''
        '''
        #Get Yvariable List
        tvidKeyList = varSelTypedDict.keys()
        tvidKeyList.sort()
        varNameList = []
        varSelectCriteria = 'Y'
        for tvid in tvidKeyList:
            if varSelTypedDict[tvid]['XVARSEL'] == varSelectCriteria:
                varName = varSelTypedDict[tvid]['VARNAME']
                varNameList.append(varName)
        varNameList.sort()
        return varNameList


    def getSelectVariableMeanAndSdev(self, varSetNo = 0, varNameList = [], lviTypedDict = {}):
        '''
        '''
        #
        #Get Variable Sets
        varValueDict = {}
        obsValueList = []
        #
        #Get Y-vectors and put in varValueDict
        for varName in varNameList:
            varValueDict.update({varName:[]})
        uidKeyList = lviTypedDict.keys()
        uidKeyList.sort()
        end_i = len(uidKeyList)
        for i in range(0,end_i,1):
            uid = uidKeyList[i]
            for varName in varNameList:
                varValue = lviTypedDict[uid][varName]
                varValueDict[varName].append(varValue)
        #
        #Get Y-stats
        ystatHeader = ['VARSET','VARNAME','MEAN','SDEV']
        ystatKeys = ['VARSET','VARNAME']
        ystatsDict = {}
        for varName in varNameList:
            mean = numpy.mean(varValueDict[varName])
            sdev = numpy.std(varValueDict[varName])
            ystatsDict.update({varName:{'MEAN':mean,'SDEV':sdev}})
        ystatsDict = {varSetNo:ystatsDict}
        return ystatHeader, ystatKeys, ystatsDict


    def getNormalizedAndNonNormalizedVariableStatistics(self, varSetNo = 0, varNameList = [], lviTypedDict = {}, ystatsDict = {}):
        '''
        '''
        #Get normalized and nonNormalized Y-statistcs
        uidKeyList = lviTypedDict.keys()
        uidKeyList.sort()
        end_i = len(uidKeyList)
        yvarKeyVarNames = ['VARSET','LVI_FCIOD']
        yvarHeader = joinOneDListBToRightOfOneDListA(yvarKeyVarNames, varNameList)
        yvarDict = {}
        yvarNormDict = {}
        yvarList = []
        yvarNormList = []
        for i in range(0,end_i,1):
            uid = uidKeyList[i]
            yvarDict.update({uid:{}})
            yvarNormDict.update({uid:{}})
            for varName in varNameList:
                varValue = lviTypedDict[uid][varName]
                mean = ystatsDict[varSetNo][varName]['MEAN']
                sdev = ystatsDict[varSetNo][varName]['SDEV']
                varValueNorm = (varValue - mean)/float(sdev)
                yvarDict[uid].update({varName:varValue})
                yvarNormDict[uid].update({varName:varValueNorm})

        #Add VARSET Keys to standardize dictionaries
        yvarDict = {varSetNo:yvarDict}
        yvarNormDict = {varSetNo:yvarNormDict}
        return yvarKeyVarNames, yvarHeader, yvarDict, yvarNormDict


    def getVariableNameColumnNumbers(self, selectNameList=[], header = []):
        newColumnNumberList = []
        for selName in selectNameList:
            colNo = header.index(selName)
            newColumnNumberList.append(colNo)
        return newColumnNumberList

    def checkForMissingVariableNameInVariableList(self, sourceList=[], newList=[]):
        '''
        '''
        for varName in newList:
            if not varName in sourceList:
                print 'variable name', varName, 'missing from sourceList'
        return

    def joinOneDListBToRightOfOneDListA(self, listA1D = [], listB1D = []):
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
            new1DList.append(newVarValue)
        return new1DList

    def joinOneDListBToRightOfOneDListAExcludingValuesAlreadyInA(self, listA1D = [], listB1D = []):
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

    def removeItemsInOneDListBFromOneDListA(self, listA1D=[], listB1D=[]):
        '''
        '''
        newListA1D = deepcopy(listA1D)
        for item in listB1D:
            if item in newListA1D:
                itemNo = newListA1D.index(item)
                del newListA1D[itemNo]
        return newListA1D

    def joinItemsInOneDListBExcludingThoseInOneDListCToOneDListA(self, listA1D = [], listB1D = [], listC1D = []):
        '''
        '''
        newListB1D = removeItemsInOneDListBFromOneDListA(listB1D, listC1D)
        newListA1D = joinOneDListBToRightOfOneDListA(listA1D, newListB1D)
        return newListB1D

    def joinTwoDListBToRightOfTwoDListA(self, listA2D = [[]], listB2D = [[]]):
        '''
        
        '''
        lenListA2D = len(listA2D)
        lenListB2D = len(listB2D)
        if not lenListA2D == lenListB2D:
            print 'joinTwoDListBToRightOfTwoDListA'
            print 'Cannot complete join two lists of differnet lengths. listA2D length:', lenListA2D, 'listB2D length:', lenListB2D
        else:
            lenListA1D0 = len(listA2D[0])
            lenListB1D0 = len(listB2D[0])
            new2DList = []
            lenNewAB1DList0 = lenListA1D0 + lenListB1D0
            for i in range(0,lenListA2D,1):        
                listA1D = listA2D[i]
                listB1D = listB2D[i]
                newAB1DList = joinOneDListBToRightOfOneDListA(listA1D, listB1D)
                lenNewAB1DList = len(newAB1DList)
                if not lenNewAB1DList == lenNewAB1DList0:
                    print 'joinTwoDListBToRightOfTwoDListA'
                    print 'Irregular 1D list lengths inside 2D List'
                    print 'new list length is:', lenNewAB1DList, 'versus standard list length:', lenNewAB1DList0
                    print 'proceeding with append to to new2DList'
                new2DList.append(newAB1DList)
        return new2DList


    def removeRecordsFromDictWithSpecifiedValues(self, myDataDict = {}, varNamesList = [], removeVarValuesList = [], keyVarNameList = []):
        '''
        Note this could be expanded to a larger number of keys.
        Inputs
            myDataDict:             a data dictionary with 0 (only one line), 1 or 2 primary keys
            varNamesList:           a list variable names eligible for removal
            removeVarValuesList:    a list of values that if found in association with one of the variables in the variable names list will be reomoved
            keyVarNameList:         a list of variable names assocated with 0 (i.e. the list is empty), 1 or 2 primary keys
                                    this list is used as the basis for determining the number of primary keys

        Outputs
            myDataDict:             that does not contain any records with the associated variable name AND variable value combinations  
        '''
        removeKeyList = []
        nKeys = len(keyVarNameList)
        if nKeys == 0:
            #This is a one line dictionary
            for keyVar in varNamesList:
                if myDataDict.has_key(keyVar):
                    if myDataDict[keyVar] in removeVarValuesList:
                        del myDataDict[keyVar]
        else:
            key0List = myDataDict.keys()
            key0List.sort()
            for key0 in key0List:
                if nKeys == 1:
                    for keyVar in varNamesList:
                        if myDataDict[key0].has_key(keyVar):
                            if myDataDict[key0][keyVar] in removeVarValuesList:
                                if not [key0] in removeKeyList:
                                    removeKeyList.append([key0])
                else:
                    key1List = myDataDict.keys()
                    key1List.sort()
                    for key1 in key1List:
                        if nKeys == 2:
                            for keyVar in varNamesList:
                                if myDataDict[key0][key1].has_key(keyVar):
                                    if myDataDict[key0][keyVar] in removeVarValuesList:
                                        if not [key0, key1] in removeKeyList:
                                            removeKeyList.append([key0, key1])

            #Remove keys from myDataDict
            #print removeKeyList
            for keyLists in removeKeyList:
                key0 = keyLists[0]
                if nKeys == 1:
                    del myDataDict[key0]
                else:
                    key1 = keyLists[1]
                    if nKeys == 2:
                        del myDataDict[key0][key1]
                        
            #Remove key0 records without any key1 keys
            if nKeys == 2:
                for keyLists in removeKeyList:
                    key0 = keyLists[0]
                    if myDataDict.has_key(key0):
                        newKeyList = myDataDict[key0].keys()
                        if newKeyList == []:
                            del myDataDict[key0]
        return myDataDict

    def extractNewDictVariableSubset(self, myDataDict={}, keyVarNamesList = [], varNameSubset = []):
        '''
        '''
        newDataDict = {}
        nKeys = len(keyVarNamesList)
        newDataHeader = joinOneDListBToRightOfOneDListA(keyVarNamesList, varNameSubset)
        if nKeys == 0:
            #Data dictionary is one line only
            for vaName in varSubset:
                if varName in myDataDict:
                    newDataDict.update({varName:myDataDict[varName]})
        else:
            key0List = myDataDict.keys()
            key0List.sort()
            for key0 in key0List:
                if not newDataDict.has_key(key0):
                    newDataDict.update({key0:{}})
                if nKeys == 1:
                    for varName in varNameSubset:
                        if varName in myDataDict[key0]:
                            newDataDict[key0].update({varName:myDataDict[key0][varName]})
                else:
                    key1List = myDataDict[key0].keys()
                    key1List.sort()
                    for key1 in key1List:
                        if not newDataDict[key0].has_key(key1):
                            newDataDict[key0].update({key1:{}})
                        if nKeys == 2:
                            for varName in varNameSubset:
                                if varName in myDataDict[key0][key1]:
                                    newDataDict[key0][key1].update({varName:myDataDict[key0][key1][varName]})
                        else:
                            key2List = myDataDict[key0][key1].keys()
                            key2List.sort()
                            for key2 in key1List:
                                if not newDataDict[key0][key1].has_key(key2):
                                    newDataDict[key0][key1].update({key2:{}})
                            if nKeys == 3:
                                for varName in varNameSubset:
                                    if varName in myDataDict[key0][key1]:
                                        newDataDict[key0][key1].update({varName:myDataDict[key0][key1][varName]})
        return keyVarNamesList, newDataHeader, newDataDict


              
    def createNewListFromSelectColumnNumbersIn2DList(self, originalList = [[]], selectColList = []):
        '''
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

    def addIndexToRowsOnLeftSideOfArray(self, xArray = [[]]):
        '''
        Rows are indexed, 0,1,,2 ... n on the left hand side of the array
        
        '''
        newArray = []
        lenArray = len(xArray)
        for row in range(0,lenArray):
            newArray.append([row])
            lenArrayRow = len(xArray[row])
            for col in range(0,lenArrayRow, 1):
                newArray[row].append(xArray[row][col])
        return newArray

    def addListOfNumbersToLeftSideOfArray(self, xArray = [[]], numberList = []):
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

    def appendListB2DToBottomOfListA2D(self, listA2D = [], listB2D = []):
        '''
        This function appends the row in listB2D to the bottom of listA2D 
        '''
        lenListB2D = len(listB2D)
        lenListA2D = len(listA2D)
        for row in range(lenListB2D):
            listA2D.append([])
            lenListB2DRow = len(listB2D[row])
            rowA = row + lenListA2D
            for col in range(0, lenListB2DRow,1):
                varValue = listB2D[row][col]
                listA2D[rowA].append(varValue)
        return listA2D

    def addHeaderListToDataList(self, myHeader, myData):
        newList = [myHeader]
        for lineItem in myData:
            newList.append(lineItem)
        return newList

    def identifyUniqueValuesInAColumnofNumbers(self, dataList = [[]], colNo = 0):
        '''
        '''
        newUniqueValueList = []
        end_i = len(dataList)
        for i in range(1,end_i,1):
            newValue = dataList[i][colNo]
            if not newValue in newUniqueValueList:
                newUniqueValueList.append(newValue)
        newUniqueValueList.sort()
        return newUniqueValueList

    def identifyUniqueValuesForAGivenListOfVariableNamesInRow0(self, dataList = [[]], varNameList = []):
        '''
        '''
        uniqueVarValueList = []
        dataListLength = len(dataList)
        for varName in varNameList:
            if varName in dataList[0]:
                varNameIndex = dataList[0].index(varName)
                for dataRecord in range(1,dataListLength,1):
                    varValue = dataList[dataRecord][varNameIndex]
                    if not varValue in uniqueVarValueList:
                        uniqueVarValueList.append(varValue)
        return uniqueVarValueList

    def makeACopyOfD2List(self, D2List = [[]]):
        '''
        '''
        myNewList = []
        end_i = len(D2List)
        for i in range(0,end_i,1):
            myNewList.append([])
            end_j = len(D2List[i])
            for j in range(0, end_j,1):
               newVarValue = D2List[i][j]
               myNewList[i].append(newVarValue)
        return myNewList

    def makeACopyOfD1List(self, D1List = []):
        '''
        '''
        myNewList = []
        end_i = len(D1List)
        for i in range(0,end_i,1):
            newVarValue = D1List[i]
            myNewList.append(newVarValue)
        return myNewList
                
    def calculateVariableWeights(self, varSet = 0, bwrTypedDict = {}, inputVarWeights = False, squareWeights = False, inverseWeights = False, constrainWeightsToAddToOne = False):
        '''
        '''
        varWeightList = []
        funcLabelList = bwrTypedDict[varSet].keys()
        funcLabelList.sort()
        for funcLabel in funcLabelList:
            if inputVarWeights == True or squareWeights == True or inverseWeights == True:
                newVarWeight = bwrTypedDict[varSet][funcLabel]['BTWTWCR4']
                varWeightList.append(newVarWeight)
            else:
                varWeightList.append(1)
        end_i = len(varWeightList)
        if squareWeights == True:
            for i in range(0,end_i,1):
                newVarWeight = varWeightList[i]**2
                varWeightList[i] = newVarWeight
        if inverseWeights == True:
            for i in range(0,end_i,1):
                newVarWeight = 1/float(varWeightList[i])
                varWeightList[i] = newVarWeight
        if constrainWeightsToAddToOne == True:
            totalVarWeight = 0
            for i in range(0,end_i,1):
                totalVarWeight = totalVarWeight + varWeightList[i]
            for i in range(0,end_i,1):
                varWeightList[i] = varWeightList[i]/float(totalVarWeight)
        return funcLabelList, varWeightList

    def applyWeights(self, weightList = [],variableArray = [[]]):
        '''
        '''
        newArray = []
        end_i = len(variableArray)
        end_j = len(weightList)
        for i in range(0,end_i,1):
            newArray.append([])
            for j in range(0,end_j,1):
                newVarValue = weightList[j] * variableArray[i][j]
                newArray[i].append(newVarValue)
        return newArray


    def calculateVariableWeights_v2(self, varSet=0, zvarStatDict = {}, zvarDict = {}, uidList = []):
        '''
        '''
        varNamesList = []
        varWeightList = []
        for newUid in uidList:
            newVarNameList = zvarDict[varSet][newUid].keys()
            for varName in newVarNameList:
                if not zvarStatDict[varSet][varName]['SDEV'] == 0:
                    if not varName in varNamesList:
                        varNamesList.append(varName)
                        varWeightList.append(1)
        return varNamesList, varWeightList

    def getNewType(self, variable):
        NewType = ''
        if type(variable) == IntType:
            NewType = 'integer'
        else:
            if type(variable) == FloatType:
                NewType = 'float'
            else:
                NewType = 'string'
        return NewType


    def runFuzzyCMeansClassification(self, dataKeyVarNameList = [],dataKeyList = [], dataSelectVarNameList = [],dataTypedSubsetList = [[]]):
        '''
        '''
        #
        fuzzyInit = readCSV.read_csv_text_file_v2(self.filePath, 'FUZZYC_INITIALIZATION', '.csv')
        m_value = int(fuzzyInit[1][2])
        minError = float(fuzzyInit[2][2])
        classificationType = fuzzyInit[3][2]
        llNclass = int(fuzzyInit[4][2])
        ulNclass = int(fuzzyInit[5][2]) + 1
        if llNclass < 2:
            llNclass = 2
        if ulNclass < llNclass:
            ulNclass = llNclass + 1
        nGroupList = []
        for i in range(llNclass,ulNclass,1):
            nGroupList.append(i)
        lenNGroups = len(nGroupList)
        classListHeader = ['CID','CLASS']
        centroidHeader = joinOneDListBToRightOfOneDListA(['NCLASSES','CLASSNO'], dataSelectVarNameList)
        newCentroidList = []
        for nG in range(0, lenNGroups, 1):
            nGroups = nGroupList[nG]
            #If classification type is Fuzzy C-Means - Euclidean Distances
            if classificationType == 'FCM_E':
                classList, centroidList = fuzzyC_v2.run_fuzzy_c_means_euclidean(m_value,nGroups,dataTypedSubsetList, minError)
            #If classification type is Fuzzy C-Means - Censored Euclidean Distances - ignore zeros in determining distances
            if classificationType == 'FCM_CE':
                classList, centroidList = fuzzyC_v2.run_censored_fuzzy_c_means_euclidean(m_value,nGroups,dataTypedSubsetList, minError)
            #If classification type is Fuzzy C-Means - Mahalanobis (Note that this needs review)
            if classificationType == 'FCM_M':
                classList, centroidList, covMatrix = fuzzyC_v2.run_fuzzy_c_means_mahalonobis(m_value,nGroups,dataTypedSubsetList, minError)
            #Get a list of only the classifications in column 1 of the classList that includes record id in column 0
            newClassList = createNewListFromSelectColumnNumbersIn2DList(classList, [1])
            #compile newClassListHeader by adding the number of groups to the end of 'CLASS'
            newClassLabel = 'CLASS' + str(nGroups)
            if nG == 0:
                #Combine the lviKeyList with the classes - Include ID's produced by Fuzzy C-means algorithm in the first instance
                #Also initialize classification header and join with keyVarNames 
                classListHeader = ['CID',newClassLabel]
                updatedHeader = joinOneDListBToRightOfOneDListA(dataKeyVarNameList, classListHeader)
                classDataList = joinTwoDListBToRightOfTwoDListA(dataKeyList, classList)    
            else:
                #Get only the class assignments, not the FUZZYC id's. 
                newClassList = createNewListFromSelectColumnNumbersIn2DList(classList, [1])
                classListHeader = [newClassLabel]
                updatedHeader = joinOneDListBToRightOfOneDListA(updatedHeader, classListHeader)
                classDataList = joinTwoDListBToRightOfTwoDListA(classDataList, newClassList)
            centroidList = addIndexToRowsOnLeftSideOfArray(centroidList)
            centroidList = addListOfNumbersToLeftSideOfArray(centroidList, [nGroups])
            newCentroidList = appendListB2DToBottomOfListA2D(newCentroidList, centroidList)
        
        finalClassList = addHeaderListToDataList(updatedHeader, classDataList)
        finalCentroidList = addHeaderListToDataList(centroidHeader, newCentroidList)

        printFilePathClass = self.filePath + 'FCLASS.csv'
        addToDataMachette20121026.printList2D(finalClassList,printFilePathClass,'OVERWRITE')
        printFilePathCentroid = self.filePath + 'FCENTROID.csv'
        addToDataMachette20121026.printList2D(finalCentroidList,printFilePathCentroid,'OVERWRITE')
        return

    def runFuzzyCMeansClassification_v2(self, dataKeyVarNameList = [],dataKeyList = [], dataSelectVarNameList = [],dataTypedSubsetList = [[]]):
        '''
        '''
        #
        
        m_value = 2
        print '\n Fuzzy c-means m-value default is equal to 2.'
        print '\n Enter Y if you wish to change the m-value and then press ENTER, otherwise press ENTER'
        flag = raw_input("\n ... ")
        if flag == 'Y' or flag == 'y' or flag == 'Yes' or flag == 'yes':
            print ' \n m-value should be greater than or equal to 1'
            m_value = input("\n Enter new m-value and then press ENTER ... ")
            if m_value < 1:
                m_value = 1
        minError = 0.01
        print '\n Fuzzy c-means acceptable error default is equal to 0.01'
        print '\n Enter Y if you wish to change the acceptable error and then press ENTER, otherwise press ENTER'
        flag = raw_input("\n ... ")
        if flag == 'Y' or flag == 'y' or flag == 'Yes' or flag == 'yes':
            print '\n Acceptable error should be less than 0.1'
            minError = input("\n Enter new error threshold and then press ENTER ... ")
            if minError > 0.1:
                minError = 0.1
        classificationType = 'FCM_E'
        print '\n Enter the lower limit in number of classes within classification'
        llNclass = input("\n ... ")
        print '\n Enter the upper limit in number of classes within classification'
        ulNclass = input("\n ... ")
        ulNclass = ulNclass + 1
        if llNclass < 2:
            llNclass = 2
        if ulNclass < llNclass:
            ulNclass = llNclass + 1
        nGroupList = []
        for i in range(llNclass,ulNclass,1):
            nGroupList.append(i)
        lenNGroups = len(nGroupList)
        classListHeader = ['CID','CLASS']
        centroidHeader = joinOneDListBToRightOfOneDListA(['NCLASSES','CLASSNO'], dataSelectVarNameList)
        newCentroidList = []
        for nG in range(0, lenNGroups, 1):
            nGroups = nGroupList[nG]
            #If classification type is Fuzzy C-Means - Euclidean Distances
            if classificationType == 'FCM_E':
                classList, centroidList = fuzzyC_v2.run_fuzzy_c_means_euclidean(m_value,nGroups,dataTypedSubsetList, minError)
            #If classification type is Fuzzy C-Means - Censored Euclidean Distances - ignore zeros in determining distances
            if classificationType == 'FCM_CE':
                classList, centroidList = fuzzyC_v2.run_censored_fuzzy_c_means_euclidean(m_value,nGroups,dataTypedSubsetList, minError)
            #If classification type is Fuzzy C-Means - Mahalanobis (Note that this needs review)
            if classificationType == 'FCM_M':
                classList, centroidList, covMatrix = fuzzyC_v2.run_fuzzy_c_means_mahalonobis(m_value,nGroups,dataTypedSubsetList, minError)
            #Get a list of only the classifications in column 1 of the classList that includes record id in column 0
            newClassList = createNewListFromSelectColumnNumbersIn2DList(classList, [1])
            #compile newClassListHeader by adding the number of groups to the end of 'CLASS'
            newClassLabel = 'CLASS' + str(nGroups)
            if nG == 0:
                #Combine the lviKeyList with the classes - Include ID's produced by Fuzzy C-means algorithm in the first instance
                #Also initialize classification header and join with keyVarNames 
                classListHeader = ['CID',newClassLabel]
                updatedHeader = joinOneDListBToRightOfOneDListA(dataKeyVarNameList, classListHeader)
                classDataList = joinTwoDListBToRightOfTwoDListA(dataKeyList, classList)    
            else:
                #Get only the class assignments, not the FUZZYC id's. 
                #newClassList = createNewListFromSelectColumnNumbersIn2DList(classList, [1])
                classListHeader = [newClassLabel]
                updatedHeader = joinOneDListBToRightOfOneDListA(updatedHeader, classListHeader)
                classDataList = joinTwoDListBToRightOfTwoDListA(classDataList, newClassList)
            centroidList = addIndexToRowsOnLeftSideOfArray(centroidList)
            centroidList = addListOfNumbersToLeftSideOfArray(centroidList, [nGroups])
            newCentroidList = appendListB2DToBottomOfListA2D(newCentroidList, centroidList)
        
        finalClassList = addHeaderListToDataList(updatedHeader, classDataList)
        finalCentroidList = addHeaderListToDataList(centroidHeader, newCentroidList)

        printFilePathClass = self.filePath + 'FCLASS.csv'
        addToDataMachette20121026.printList2D(finalClassList,printFilePathClass,'OVERWRITE')
        printFilePathCentroid = self.filePath + 'FCENTROID.csv'
        addToDataMachette20121026.printList2D(finalCentroidList,printFilePathCentroid,'OVERWRITE')
        return


    def computeXXCovarianceMatrix(self, varArray1):
        '''
        Array has variables listed in rows
        and observations in columns
        '''
        varArrayT = numpy.transpose(varArray1)
        covArray = numpy.cov(varArrayT)
        return covArray


    def convertDbfFileToCsvFile(self, dbfFileName = '', newCsvFileName = '', newDataDictFileName = ''):
        '''
        This is a function to convert a dbf file into a csv file format.
        It uses dbf.py in site tools to recover the original data.
        It assumes that the first field in each record is a unique ID and
        that the remaining fields are associated with that unique ID. It then
        '''
        from dbfpy import dbf
        
        printFilePath = self.filePath + newCsvFileName + '.csv'
        printDictFilePath = self.filePath + newDataDictFileName + '.csv'
        dbfFilePath = self.filePath + dbfFileName + '.dbf'
        addToDataMachette20121026.deleteFileIfItExists(printFilePath)
        addToDataMachette20121026.deleteFileIfItExists(printDictFilePath)
        dbf = dbf.Dbf(dbfFilePath, True)
        header = ['NEWID']
        keyList = ['NEWID']
        NewDict = {}
        #Initialize NewDict Dictionary
        DictionaryHeader = ['TVID','TABLENAME','VARNAME','NEWVARNAME','VARTYPE','VARDEFAULT','SELECT','DESCRIPTION']
        DictionaryKeyList = ['TABLENAME','VARNAME']
        NewDictDictionary = {newCsvFileName:{}}
        printCount = 1000
        i = 1
        for rec in dbf:
            #print rec
            j = 1
            #Update MewDict with key variable NEWID = i
            NewDict.update({i:{}})
            k = 1
            for fldName in dbf.fieldNames:
                if i == 1:
                    NewType = ''
                    #Create NewDict Header
                    header.append(fldName)
                    #Create NewDict Dictionary
                    NewType = getNewType(rec[fldName])
                    NewDictDictionary[newCsvFileName].update({fldName:{'VARTYPE':NewType,'NEWVARNAME':fldName,'TVID':k,'VARDEFAULT':'','SELECT':'','DESCRIPTION':''}})
                    k = k + 1
                #Get Key Variable Value             
                NewVarValue = rec[fldName]
                NewDict[i].update({fldName:NewVarValue})
                j = j + 1
            i = i + 1
            #if i == 2: break
            if i == printCount:
                #print printCount
                printCount = printCount + 1000
                #Print NewDict
                addToDataMachette20121026.check_for_filepath_then_print(printFilePath,keyList,header,NewDict)
                NewDict = {}
        #Print NewDictDictionary
        addToDataMachette20121026.check_for_filepath_then_print(printDictFilePath,DictionaryKeyList,DictionaryHeader,NewDictDictionary)
        #Print blast remaining records in NewDict
        if not NewDict == {}:
            addToDataMachette20121026.check_for_filepath_then_print(printFilePath,keyList,header,NewDict)
        #Print number of records
        return

    def assignVariableSetZscoresToObservations(self, dfuncTypedList = [], dfuncTypedDict = {}, lviTypedDict = {}, columnNo = 0, fileName = '', batchNo = 0, printFlag = 'Yes'):
        '''
        INPUTS
            dfuncTypedList and dfuncTypedDict are derived from DFUNC.csv
            lviTypedDict is the original LVI data
            columnNo refers to DFUNC.csv and dfuncTypedList
                If the focus of the analysis is on ZSCORES then the column is set equal to 2
                    indicating that the variables are derived from discriminant functions (FUNCLABEL3)
                If the focus of the analysis is on XSCORES then the column is set equal to 1
                    indicating that the variables are derived from discriminant functions (VARSET3)
                (Remember the first row or column in Python is always designated as 0 (zero))

            fileName is the file name that will be used to print the data
                If the focus of the analysis is on ZSCORES then the fileName should be set to ZSCORE.csv
                If the focus of the anlysis is on XSCORES then the fileName should be set to XSCORE.csv

            Note that the primary keys in dfuncTypedDict also vary
                If the focus of the analysis is on ZSCORES then the keyVarNamesList is ['VARSET3','FUNCLABEL3', 'VARNAMES3'] 
                If the focus of the analysis is on XSCORES then the keyVarNamesList is ['VARSET3','VARNAMES3','FUNCLABEL3'] 
                The header in both cases is ['VARSET3','VARNAMES3','FUNCLABEL3','DFCOEF']
                The DFUNC.csv file is produced using R script.
                
        OUTPUT
            The output file (ZSCORE.csv or XSCORE.csv):
                KeyVariable Names: ['VARSET3', 'LVI_FCOID']
                    'VARSET3' relates to the variable set in DFUNC.csv and to either FUNCLABEL3 (for ZSCORE)
                        or VARNAMES3 (for XSCORE) associated with each variable set depending which analysis
                        is being carried out.
                The remaining variables in the header is a unique set of variable names spanning all of the variable sets.
                    If a given variable is not associated with a given variable set then that variable is assigned a 0 (zero)
                    All other variables (ones associated with a variable set) are assigned a value.

            Finaly note that ZSCORES must be calculated using the variable parameters associated with the discriminant functions (FUNCLABEL3)
                associated with each variable set.

            The XSCORES are simply the X values associated with each of the variable names (VARNAMES3) in each variable set.    

        The Python syntax used herein was first developed to work with ZSCORES in mind and then modified to accomodate XSCORES or values.
            The interpretation is more easilly understood with reference to the ZSCORE analysis.
            Ulitimately the code should be modified to be made more transparent
            The code could also be reduced to further sub-modules in a manner that would be consistent with a third type of analysis: YSCORE        
        
        '''
        #Get a complete list of function labels (ZSCORE) or variable names (XSCORE) across all variable sets 
        uniqueVarnames = identifyUniqueValuesInAColumnofNumbers(dfuncTypedList, columnNo)
        #Initialize keyVarNames
        zvarKeyVarNames = ['VARSET3','LVI_FCOID']
        #Initialize header by adding uniqueVarnames to the right of zvarKeyVarNames
        zvarHeader = joinOneDListBToRightOfOneDListA(zvarKeyVarNames, uniqueVarnames)
        #Initialize the dictionary, zvarDict, that will contain the ZSCORE or XSCORE values of interest
        zvarDict = {}
        #Get the list of LVI_FCOID's - i.e. unique observation i.d. numbers
        lviKeyValueList = lviTypedDict.keys()
        #Sort the list from lowest to highest
        lviKeyValueList.sort()
        #Get the list of variable sets and sort them too
        varSetList = dfuncTypedDict.keys()
        varSetList.sort()
        #For each variable set
        for varSet in varSetList:
            #Update the zvarDict with the new variable set
            zvarDict.update({varSet:{}})
            #Get the FUNCLABEL3 (ZSCORES) or VARNAMES3 (XSCORES) key value list and sort them
            funcLabelList = dfuncTypedDict[varSet].keys()
            funcLabelList.sort()
            #For each 'LVI_FCOID' in the list of lviTypedDict keys 
            for lviKey in lviKeyValueList:
                #Add the 'LVI_FCOID' to zvarDict
                zvarDict[varSet].update({lviKey:{}})
                #For each FUNCLABEL3 (ZSCORES) or VARNAMES3 (XSCORES) in the uniqueVarnames list
                for funcLabel in uniqueVarnames:
                    #If the variable is also in the list associated with a given variable set
                    if funcLabel in funcLabelList:
                        #If the analysis pertains to XSCORES
                        if columnNo == 1:
                            #Get the X value directly from the lviTypedDict
                            zValue = lviTypedDict[lviKey][funcLabel]
                        #If the analysis pertains to ZSCORES
                        if columnNo == 2:
                            #Initialize the zValue
                            zValue = 0
                            #Get the variable list associated with a given variable set and discriminant function; sort the list
                            varNameList = dfuncTypedDict[varSet][funcLabel].keys()
                            varNameList.sort()
                            #print varSet, funcLabel, varNameList
                            #For each variable name in the list
                            for varName in varNameList:
                                #Multiply the variable coeficient in DFUNC.csv by the variable value in the original LVI dataset
                                #if dfuncTypedDict[varSet][funcLabel].has_key(varName):
                                zValue = zValue + dfuncTypedDict[varSet][funcLabel][varName]['DFCOEF3'] * lviTypedDict[lviKey][varName]
                    else:
                        #The variable is not in the list associated with a given variable set
                        #Make it equal to zero
                        zValue = 0
                    #Update the ZVAR dictionary with the zValue (i.e. zScore in ZSCORE or x-value in XSCORE)
                    zvarDict[varSet][lviKey].update({funcLabel:zValue})
        #Print the file to a self.filePath indicated at the top of this module and to a fileName used as input into this function
        printFilePath = self.filePath + fileName
        if batchNo == 0:
            #Initialize the file (by overwriting the old one if it exists or starting a new one if it does not) with a new header as the top line
            #fileName is either 'ZSCORE.csv' or 'XSCORE.csv' depending on the anlysis
            addToDataMachette20121026.initialize_header(zvarHeader,printFilePath)
            if printFlag == 'Yes' or printFlag == 'yes' or printFlag == 'y' or printFlag == 'Y':
                print ' Creating new file:', fileName
        #Write the remainder of the file, zvarDict to the fileName
        addToDataMachette20121026.print_to_nested_dictionary(zvarKeyVarNames,zvarHeader, zvarDict, printFilePath)
        if printFlag == 'Yes' or printFlag == 'yes' or printFlag == 'y' or printFlag == 'Y':
            print ' Adding to file:', fileName, 'batchNo:', batchNo
        return zvarKeyVarNames, zvarHeader, zvarDict


    def normalizeZscores(self, dfuncTypedDict = {}, zvarDict = {}, zvarHeader = [], zvarKeyVarNames = [], zstatKeyVarNames = [], zstatHeader = [], fileNames = [], batchNo = 0, printFlag = 'Yes'):
        '''
        
        '''
        #Calculate Mean and Standard Devations for varSet Functions
        varSetKeyList = zvarDict.keys()
        varSetKeyList.sort()
        zvarStatDict = {}
        #zstatKeyVarNames = ['VARSET3','FUNCLABEL3']
        #zstatHeader = ['VARSET3','FUNCLABEL3','MEAN','SDEV']
        zvarNormDict = {}
        for varSet in varSetKeyList:
            zvarStatDict.update({varSet:{}})
            zvarNormDict.update({varSet:{}})
            funcLabelList = dfuncTypedDict[varSet].keys()
            funcLabelList.sort()
            uidKeyList = zvarDict[varSet].keys()
            uidKeyList.sort()
            for funcLabel in zvarHeader:
                if not funcLabel in zvarKeyVarNames:
                    zvarStatDict[varSet].update({funcLabel:{}})
                    newDataList = []
                    for uid in uidKeyList:
                        newValue = zvarDict[varSet][uid][funcLabel]
                        newDataList.append(newValue)
                    meanValue = numpy.mean(newDataList)
                    sdevValue = numpy.std(newDataList)
                    zvarStatDict[varSet][funcLabel].update({'MEAN':meanValue,'SDEV':sdevValue})
                    for uid in uidKeyList:
                        if not zvarNormDict[varSet].has_key(uid):
                            zvarNormDict[varSet].update({uid:{}})
                        if sdevValue == 0:
                            newValue = 0
                        else:
                            newValue = (zvarDict[varSet][uid][funcLabel] - meanValue)/float(sdevValue)
                        #print newValue
                        zvarNormDict[varSet][uid].update({funcLabel:newValue})
        #
        printFilePath1 = self.filePath + fileNames[0]
        printFilePath2 = self.filePath + fileNames[1]
        if batchNo == 0:
            addToDataMachette20121026.initialize_header(zvarHeader,printFilePath1)
            addToDataMachette20121026.initialize_header(zstatHeader,printFilePath2)
            if printFlag == 'Yes' or printFlag == 'yes' or printFlag == 'y' or printFlag == 'Y':
                print ' Creating two new files:', fileNames[0], fileNames[1]
        if printFlag == 'Yes' or printFlag == 'yes' or printFlag == 'y' or printFlag == 'Y':
            print ' Writing to file names:', fileNames[0], fileNames[1], 'batch Number:', batchNo  
        addToDataMachette20121026.print_to_nested_dictionary(zvarKeyVarNames,zvarHeader, zvarNormDict, printFilePath1)
        addToDataMachette20121026.print_to_nested_dictionary(zstatKeyVarNames,zstatHeader, zvarStatDict, printFilePath2)
        return zvarNormDict, zvarStatDict


    def getNearestNeighboursInReferenceDataset(self, zvarDict = {}, zvarStatDict = {}, bwrTypedDict = {}, kNN = 1, zscores = False, inputVarWeights = False, squareWeights = False, inverseWeights = False, constrainWeightsToAddToOne = False, fileNameModifier = 'Z', batchNo = 0, printFlag = 'Yes'):
        '''
        INPUT
            zvarDict is a dictionary of observations with Z or X or Y (all referred to as zValues  below) or normalized zValues (recommended)
                associated with each discriminant function for a given (Z or X or Y) variable set.

            zvarStatDict contains the means and standard deviations for each variable value - these are used to exclude any variables that have
                a zero standard deviation

            bwrTypedDict (BWRATIO) contains the weights associated with each discriminant function within a given variable set (aka eigen values)
                bwrTypedDict should be left empty if the nearest neighboour analysis does not pertain to ZSCORES, i.e. if the focus is on
                XSCORES or values or YSCORES or values

            kNN is the maximum number of nearest neighbours for consideration

            inputVarWeights is set to True if variable weights in bwrTypedDict other than equal weights are to be applied in estimating distances
                May be True or False when pertaining to ZSCORES otherwise it should be set to false

            squareWeights is set to True if the weights should be squared
                May be True or False when pertaining to ZSCORES otherwise it should be set to false

            inverseWeights is set to True if the inverse weight is to be applied
                May be True or False when pertaining to ZSCORES otherwise it should be set to false

            fileNameModifier should be specified as Z (for Zscores from discriminant analyses or similar kinds of functions), X for X-Variables or Y for Y-Variables 


            Note that provided that bwrTypedDict is not empty if either inputVarWeights, squareWeights, or inverse weights are set equal to True
                then an initial set of variable weights 0are derived from bwrTypedDictionary.  In the next step if squareWeights is equal to True
                then the weights are squared.  In the second to last step, if inverseWeights is equal to true then the inverse is taken regardless
                of whether the weights have or have not been squared. Finaly if constrainWeightsToAddToOne the weights are summed across all
                variables and then each of the weights is divided by the total. This is all accomplished before the weights are applied to a given
                variable set (generally to only the ZSCORES).
        OUTPUT
            NNM.csv, NNE.csv and NNA.csv preceded by a Z (e.g. ZNNM.csv) or an X or a Y (k = 1)  
                VARSET3 - The variable set number associated with a given set of discriminant functions
                REFOBS - Observation number equivalent to LVI_FCOID
                NNOBS - Nearest neighbour observation for all nearest neighbours <= k

            COV.csv (Z covariance matrix)preceded by a Z (e.g. ZCOV.csv) or an X or a Y  
                VARSET3 - The variable set number associated with a given set of discriminant functions
                ROWNAME - Discriminant Function Row Label, e.g. LD1, LD2 ...
                COLNAME - Discriminant Function Column Label, e.g. LD1, LD2 ...
                COV - Covariance associated with row x column names

                Note that ZCOV tends to be a diagonal matrix with the diagonals equal to 1 and the off diagonals equal to zero.
                However this is not a requirement in Discriminant analysis.
                Initial tests of weights suggest that no differential; weights should be applied
                    with the result that after normalization Euclidean and Mahalanobis distances are the same.

        CURRENT LIMITATIONS
            With 2900 observations and 17 variable sets each variable set takes about 10 minutes to process or
                170 minute (2 hours and 50 minutes) in total on the machine used to develop this program.
                
            A much larger number of variables will take longer to process.
            
            The number of observations multiplied by the number of variables can also be used as an indicator
                of memory overload. The potential for overload could be reduced by printing interim results
                rather than holding all of the results in memory until the end, but this would some modification
                of the code developed herein.

            Note also that this code accomplishes a number of tasks that could be broken into smaller functions
                making the code easier to understand and more robust.  In this context this code is a first
                approximation.

            This program refers to another function, calculateVariableWeights, and a related function,
                calculateVariableWeights_v2. In the second case a check is applied using zvarStatDict
                to ensure that only those variable are used with standard deviation > 0.  This is necessary
                because different variable sets are asssociated with different numbers and kinds of variables
                contained within the same file.  The first case may also have to be modifed to enforce the
                same kind of rules where there are a different number of discriminant functions associated
                with different variable sets.
                
        '''
        #Ensure that kNN is a positive integer greater than or equal to 1
        kNN = int(kNN)
        if kNN < 1: kNN = 1 
        #Initialize print filenames
        newNNMFile = fileNameModifier + 'NNM.csv'
        kNNMPrintFilePath = self.filePath + newNNMFile                       #Mahalanobis print file path
        newNNEFile = fileNameModifier + 'NNE.csv'
        kNNEPrintFilePath = self.filePath + newNNEFile                       #Euclidean distance file path
        newNNAFile = fileNameModifier + 'NNA.csv'
        kNNAPrintFilePath = self.filePath + newNNAFile                       #Absolute distance file path
        newCOVFile = fileNameModifier + 'COV.csv'
        covPrintFileName = self.filePath + newCOVFile                        #Covariance Matrix file path
        varSetList = zvarDict.keys()                                    #Get the Z or X or Y variable set i.d.'s and sort them 
        varSetList.sort()
        #Initialize k nearest neighbour dictionary, header and names of the key variables: nnKeyVarNames
        nnMDict = {}                                                    #Nearest neighbour Mahalanobis Distance Dictionary
        nnEDict = {}                                                    #Nearest neighbour Euclidean Distance Dictionary
        nnADict = {}                                                    #Nearest neighbour Absolute Distnace Dictionary
        nnHeader = ['VARSET3','REFOBS','NNOBS','DIST']
        nnKeyVarNames = ['VARSET3','REFOBS','NNOBS']
        zcovDict = {}   #Initialize covariance matrix dictionary for printing including header and key variables: zcovKeyVarNames
        zcovHeader = ['VARSET3','ROWNAME','COLNAME','COV']
        zcovKeyVarNames = ['VARSET3','ROWNAME', 'COLNAME']
        #myCount = 100          #This is code used to check progress during the code development and modification process
        #For each variable set
        for varSet in varSetList:
            print ' Processing Variable Set Number', varSet, time.ctime()        #Print the following statement so that the progress of the routine can be monitored
            nnMDict.update({varSet:{}})     #Update the nearest neighbour Mahalanobis dictionary with the new variable set i.d. number
            nnEDict.update({varSet:{}})     #Update the nearest neighbour Euclidean dictionary with the new variable set i.d. number
            nnADict.update({varSet:{}})     #Update the nearest neighbour Absolute dictionary with the new variable set i.d. number
            zcovDict.update({varSet:{}})    #Update the covariance dictionary with the new variable set i.d. number
            uidList = zvarDict[varSet].keys()   #Get the unique variable set observation keys, uidList (in the original dvelopment 'LVI_FCOID'), and sort them. 
            uidList.sort()
            end_i = len(uidList)            #Get the number of i.d. in the list to be used later in the porcess of referring to a location in the list by way of an index 
            #If the bwrTypedDict is NOT empty (The BWRATIO.csv file has been used in this case, usually only where the focus of the nearest neighbour
            #anslysis is on ZSCORES
            if not bwrTypedDict == {}:
                #bwrTypedDict is not empty: Use version 1 of the calculateVariableWeights 
                funcLabelList, funcWeightList = calculateVariableWeights(varSet,bwrTypedDict,inputVarWeights,squareWeights,inverseWeights, constrainWeightsToAddToOne)
            else:
                #bwrTypedDict is empty: Use version 2 of the calculateVariableWeights which effectively eliminates the use of weights
                #and onsly selects variables for use if they have a standard deviation greater than 0 (zero)
                funcLabelList, funcWeightList = calculateVariableWeights_v2(varSet, zvarStatDict, zvarDict, uidList)
            #Initialize a selected X or Y variable or Z-Score matrix, referred to as zscoreM1
            #This matrix has observations listed in rows and variables in columns. Each observation is embedded
            #within a separate list in the same order as they occur in uidList with variable values within each list
            #assigned in the same order as they occur in funcLabelList.
            zscoreM1 = []
            for i in range(0,end_i,1):      #For each observation number 0, to end_i in the uidList
                uid = uidList[i]            #Get the unique i.d.
                zscoreM1.append([])         #Add a new row to represent that observation in the X, Y or Z matrix, zscoreM1
                for varName in funcLabelList:   #For each variable name in the selecte variable list, funcLabelList
                    #If the variable name can be found in zvarDict with X, Y, or Z values given the
                    #variable set number and observation i.d.
                    if zvarDict[varSet][uid].has_key(varName):
                        zscore = zvarDict[varSet][uid][varName]     #Get the variable value
                    else:
                        #The variable name has not been found - assign a value of 0
                        #Note that this may cause the program to crash when it comes time to taking the inverse
                        #of the covariance matrix below.
                        print ' getNearestNeighboursInReferenceDataset in routineLviApplications'
                        print ' Variable name', varName, 'not found in zvarDict'
                        print ' variable value set equal to 0 - may cause singularity'
                        zscore = 0
                    zscoreM1[i].append(zscore)      #Add the X, Y or Z variable value to observation i in zscoreM1
                        
            if bwrTypedDict == {}:                                  #If bwrTypedDict is empty
                zscoreM1W = zscoreM1                                #No weights apply - simply make the weighted version of zscoreM1, i.e. zscoreM1W, equal to zscoreM1 
            else:
                zscoreM1W = applyWeights(funcWeightList,zscoreM1)   #bwrTypedDict is NOT empty and weights apply (even if they are equal weights); apply weights
            
            covM1 = computeXXCovarianceMatrix(zscoreM1W)            #Compute covariance matrix (for estimation of mahalanobis distances)
            #The covariance matrix should be square, where the rows and columns correspond to the names
            #of the variable names in the funcLabelList. Get the number of variables in the list
            end_k = len(funcLabelList)
            for k in range(0,end_k,1):
                rowName = funcLabelList[k]
                zcovDict[varSet].update({rowName:{}})
                for m in range(0,end_k,1):
                    colName = funcLabelList[m]
                    if end_k == 1:                                  #If the covariance matrix has a dimension of 1
                        covkm = covM1
                    else:
                        covkm = covM1[k][m]                         #The covariance matrix has a dimension greater than 1
                    zcovDict[varSet][rowName].update({colName:{'COV':covkm}})
                    
            if end_k == 1:                                          #Compute inverse of covariance matrix
                invCovM1 = 1/covM1
            else:
                invCovM1 = linalg.inv(covM1)
            #Get nearest neightbours
            end_k = len(funcLabelList)
            #Compute Euclidean, Mahalanobis and Absolute differences in Z-values; find nearest neighbours
            #This is the time consuming part - searching through the list of reference observations to find the nearest neighbours
            for i in range(0,end_i,1):                          #For each initial observation
                refObs = uidList[i]                             #Get the observation i.d.
                nnMDict[varSet].update({refObs:{}})             #Update the NN Mahalanobis dictionary
                nnEDict[varSet].update({refObs:{}})             #Update the NN Euclidean dictionary
                nnADict[varSet].update({refObs:{}})             #Update the NN Absolute distance dictionary
                minMDistList = []                               #Initialize the Mahalanobis distance list
                minEDistList = []                               #Initialize the Euclidean distance list
                minADistList = []                               #Initialize the Absolute distance list
                obsMNoList = []                                 #Initialize the Mahalnaobis nearest neighbour i.d. list
                obsENoList = []                                 #Initialize the Euclidean nearest neighbour i.d. list
                obsANoList = []                                 #Initialize the Absolute nearest neighbour i.d. list
                for j in range (0, end_i,1):                    #For each observation
                    if not j == i:                              #If not the same as the initial observation
                        absDist = 0                             #Initialize absolute distance equal to 0
                        euclDist = 0                            #Initialize Euclidean distance equal to 0
                        newDistVector = []
                        for k in range(0,end_k,1):                              #For each variable in the funcLabelList
                            newDist = abs(zscoreM1W[i][k] - zscoreM1W[j][k])    #Get the absolute difference in variable value between the referenc observation, i, and the potential neighbour j, not equal to i
                            newDistVector.append(newDist)                       #Append the absolute distance to a newDistVector
                            absDist = absDist + newDist                         #Update the Absolute distance
                            euclDist = euclDist + newDist**2                    #Update the Euclidean distance
                        newDArray = numpy.inner(invCovM1, newDistVector)        #Multiply the newDistVector by the inverse of the covariance matrix to produce Mahalanobis distance
                        mahDist = numpy.inner(newDistVector, newDArray)         #Repeat the process of multiplication to finalize the Mahalanobis distance (Note for ZScores this is also equivalent to Most Similar Neighbour)
                        if len(obsMNoList)< kNN:                                #If the observation list has not yet been populated with k Nearest Neighbours then
                            minMDistList.append(mahDist)                        #Add another distance to the Mahalanobis distance list
                            minEDistList.append(euclDist)                       #Add another distance to the Euclidean distance list
                            minADistList.append(absDist)                        #Add another distance to the Absolute distance list
                            obsMNoList.append(uidList[j])                       #Add another corresponding observation i.d. to the Mahalanobis observation list
                            obsENoList.append(uidList[j])                       #Add another corresponding observation i.d. to the Euclidean observation list
                            obsANoList.append(uidList[j])                       #Add another corresponding observation i.d. to the Absolute observation list
                            maxMDist = max(minMDistList)                        #Update the maximum distance in the Mahalanobis distance list
                            maxMDistIndex = minMDistList.index(maxMDist)        #Update the index associated with the location of the maximum distance in the Mahalanobis distance list
                            maxEDist = max(minEDistList)                        #Update the maximum distance in the Euclidean distance list
                            maxEDistIndex = minEDistList.index(maxEDist)        #Update the index associated with the location of the maximum distance in the Euclidean distance list
                            maxADist = max(minADistList)                        #Update the maximum distance in the Absolute distance list
                            maxADistIndex = minADistList.index(maxADist)        #Update the index associated with the location of the maximum distance in the Absolute distance list
                            #print 'start', obsMNo, minMDist, minEDist, minADist
                        else:                                                   #The lists all have the maximum number of observations equal to kNN as specified by the user
                            if mahDist < maxMDist:                              #If the Mahalanobis distance associated with a new observation is less than the maximum distance 
                                del minMDistList[maxMDistIndex]                 #Delete the maximum distance from the minimum distance list          
                                del obsMNoList[maxMDistIndex]                   #Delete the corresponding observation from the corresponding observation list
                                minMDistList.append(mahDist)                    #Add the new distance to the end minimum distance list
                                obsMNoList.append(uidList[j])                   #Add the new observation to the end of the corresponding obsevation list
                                maxMDist = max(minMDistList)                    #Update the maximum distance in the minimum distance list
                                maxMDistIndex = minMDistList.index(maxMDist)    #Update the index locating the maximum distance as ti its position in the list 
                            if euclDist < maxEDist:                             #If the Euclidean distance associated with a new observation is less than the maximum distance 
                                del minEDistList[maxEDistIndex]
                                del obsENoList[maxEDistIndex]
                                minEDistList.append(euclDist)
                                obsENoList.append(uidList[j])
                                maxEDist = max(minEDistList)
                                maxEDistIndex = minEDistList.index(maxEDist)
                            if absDist < maxADist:                              #If the Absolute distance associated with a new observation is less than the maximum distance 
                                minADist = absDist
                                obsANo = uidList[j]
                                del minADistList[maxADistIndex]
                                del obsANoList[maxADistIndex]
                                minADistList.append(absDist)
                                obsANoList.append(uidList[j])
                                maxADist = max(minADistList)
                                maxADistIndex = minADistList.index(maxADist)
                for j in range(0,kNN,1):                                                        #For each kNN from 0 to kNN minus 1
                    nnMDict[varSet][refObs].update({obsMNoList[j]:{'DIST':minMDistList[j]}})    #Update each of the observations, j, and associated minimum distances assigned to each reference observation, i
                    nnEDict[varSet][refObs].update({obsENoList[j]:{'DIST':minEDistList[j]}})
                    nnADict[varSet][refObs].update({obsANoList[j]:{'DIST':minADistList[j]}})
                #print i, refObs, obsMNo, obsENo, obsANo    #This is code used to check progress during the code development and modification process
                #if i == myCount:                           #This is code used to check progress during the code development and modification process
                #    print myCount                          #This is code used to check progress during the code development and modification process
                #    myCount = myCount + 100                #This is code used to check progress during the code development and modification process
        #
        
        if batchNo == 0:
            addToDataMachette20121026.initialize_header(nnHeader,kNNMPrintFilePath)                                    #Initialize the Mahalanobis file by overwriting it with a new header
            addToDataMachette20121026.initialize_header(nnHeader,kNNEPrintFilePath)                                    #Initialize the Euclidean file by overwriting it with a new header
            addToDataMachette20121026.initialize_header(nnHeader,kNNAPrintFilePath)                                    #Initialize the Absolute file by overwriting it with a new header
            if printFlag == 'Yes' or printFlag == 'yes' or printFlag == 'y' or printFlag == 'Y':
                print ' New Nearest Neighbour Distance files created:', newNNMFile, newNNEFile, newNNAFile
            addToDataMachette20121026.initialize_header(zcovHeader,covPrintFileName)                                    #Initialize the Covariance file by overwriting it with a new header
            if printFlag == 'Yes' or printFlag == 'yes' or printFlag == 'y' or printFlag == 'Y':
                print ' New covariance file created:', newCOVFile
            
        addToDataMachette20121026.print_to_nested_dictionary(nnKeyVarNames,nnHeader, nnMDict, kNNMPrintFilePath)       #Print the nearest neighbours and distances to file
        addToDataMachette20121026.print_to_nested_dictionary(zcovKeyVarNames,zcovHeader, zcovDict, covPrintFileName)    #Print the covariance matrices to the file
        addToDataMachette20121026.print_to_nested_dictionary(nnKeyVarNames,nnHeader, nnEDict, kNNEPrintFilePath)       #Print Euclidean distance kNN file
        addToDataMachette20121026.print_to_nested_dictionary(nnKeyVarNames,nnHeader, nnADict, kNNAPrintFilePath)       #Print Absolute distance kNN file
        if printFlag == 'Yes' or printFlag == 'yes' or printFlag == 'y' or printFlag == 'Y':
            print ' Writing to files:', newNNMFile, newNNEFile, newNNAFile, newCOVFile, 'batchNo:', batchNo
        return nnADict, nnEDict, nnMDict, zcovDict

    def getZNearestNeighbourRMSE(self, nnDict = {}, varSelTypedDict = {}, lviTypedDict = {}, kNN = 1, fileNameModifier = 'ZM', rule = 'M', batchNo = 0, printFlag = 'Yes'):
        '''
        This routine calculates nearest neighbour statistics for a selected Y variable dataset.

        INPUTS
            nnDict contains a list of each observation a k Nearest neighbours (equal to kNN)
            varSelTypedDict contains a list of the selected Y-Variable - XVARSEV1.csv
            lviTypedDict contains the original LVI X and Y datasets plus anyclassifications derived therefrom
            kNN is the maximum number (integer) of nearest neighbours to be averaged to estimate a given Y-variable
            fileNameModifier is used to modify thye file name to indicate its contents. The following conventions apply:
                ZM - The nearest neighbour dictionary contains disctances associated with ZScores derived in Discriminant Analysis with Mahalanobis Distance
                ZE - The nearest neighbour dictionary contains disctances associated with ZScores derived in Discriminant Analysis with Euclidean Distance
                ZA - The nearest neighbour dictionary contains disctances associated with ZScores derived in Discriminant Analysis with Absolute Distance
                XM - The nearest neighbour dictionary contains disctances associated with normalized X-Values with X-Variables derived from Discriminant Analysis with Mahalanobis Distance
                XE - The nearest neighbour dictionary contains disctances associated with normalized X-Values with X-Variables derived from Discriminant Analysis with Euclidean Distance
                XA - The nearest neighbour dictionary contains disctances associated with normalized X-Values with X-Variables derived from Discriminant Analysis with Absolute Distance
                YM - The nearest neighbour dictionary contains disctances associated with Y-Values with Y-Variables derived using XVARSELV1.csv with Mahalanobis Distance (kNN = 1)
                YE - The nearest neighbour dictionary contains disctances associated with Y-Values with Y-Variables derived using XVARSELV1.csv with Euclidean Distance (kNN = 1)
                YA - The nearest neighbour dictionary contains disctances associated with Y-Values with Y-Variables derived using XVARSELV1.csv with Absolute Distance (kNN = 1)
           rule
               M - Mahalanobis Distances
               E - Euclidean Distances
               A - Absolute Distances

        OUTPUTS
            RMSE.csv with fileNameModifier appended to the front of the file name (.e.g. ZMRMSE.csv)

            This file contains the following fields:
                VARSET  indicating the variable set
                KNN     indicating the value of k Nearest Neighbours, where k = 1,2,3 ... kNN
                VARNAME specifying the Y-Variable name associated with each variable set KNN value
                RMSE    the root mean squared error associated with each VARSET, KNN and VARNAME combination
                BIAS    the mean bias
                BRMSE   the mean bias squared
        '''
        newRMSEFile = fileNameModifier + 'RMSE.csv'
        rmseFilePath = self.filePath + newRMSEFile                           #Create the RMSE output file pathname
        varSetList = nnDict.keys()                                      #Get the variable set list of key i.d's from the nearest neighbour dictionary
        varSetList.sort()                                               #Sort the variable set list of key i.d.'s
        varSelKeys = varSelTypedDict.keys()                             #Get the variable selection key i.d.'s (VARSELV1.csv)
        varSelKeys.sort()                                               #Sort the variable selection key i.d.'s
        rmseHeader = ['VARSET','KNN','VARNAME','RMSE', 'BIAS','BRMSE']  #Initialize the RMSE file header
        rmseKeyVarNames = ['VARNAME','VARSET','KNN']                    #Initialize the RMSE key field names
        rmseDict = {}                                                   #Initialize the output RMSE dictionary
        for varSel in varSelKeys:                                       #For each variable in the variable selection dictionary (VARSELV1.csv)
            if varSelTypedDict[varSel]['XVARSEL'] == 'Y':               #If the XVARSEL field is equal to 'Y' indicating that it is a selected Y variable
                varName = varSelTypedDict[varSel]['VARNAME']            #Get the variable name
                if not rmseDict.has_key(varName):                       #If the variable name has not yet been entered as a key in the RMSE dictionary 
                    rmseDict.update({varName:{}})                       #Update the dictionary with the new variable name
                for varSet in varSetList:                               #For each set of X-variables in the variable set list
                    uidKeyList = nnDict[varSet].keys()                  #Get the list observation unique i.d.'s
                    uidKeyList.sort()                                   #Sort the observation i.d.'s
                    if not rmseDict[varName].has_key(varSet):           #If the RMSE dictionary does not have the variable set associated the variable name
                        rmseDict[varName].update({varSet:{}})           #Then update the RMSE dictionary to ensure that the combinations of variable name and variable set combination are properly identified
                    biasMseDict = {}                                         #Initialize the standard error dictionary
                    biasDict = {}
                    seDict = {}
                    for i in range(0,kNN,1):                        #For each number of kNN sets, from 0,1,2,3 ... kNN-1 
                        seDict.update({i:[]})                       #Initialize a standard error vector or list
                        biasDict.update({i:[]})
                        biasMseDict.update({i:[]})
                    for uid in uidKeyList:                          #For each reference observation in the dataset
                        nnObsList = nnDict[varSet][uid].keys()          #Get the list of kNN nearest neighbours
                        nnObsList.sort()                                #Sort the list of nearest neighbours
                        expYValue = lviTypedDict[uid][varName]          #Get the reference Y-variable value ... as the expected Y-value 
                        distList = []                                   #Initialize a list of distances from the reference observation to each of the kNN nearest neighbours
                        sortList = []                                   #Initialize a second list of the same distances that can be sorted from lowest to heighest
                        estYValueList = []                              #Initialize an estimated Y-variable value list associated with each of the distances in the distList 
                        for nnObs in nnObsList:                                                             #For each nearest neighbour to given observation (uid)
                            estYValueList.append(lviTypedDict[nnObs][varName])                              #Get the associated Y-variable value and add it to the estimated YValue List
                            distList.append(nnDict[varSet][uid][nnObs]['DIST'])                             #Add the distance of the nearest neighbour to the reference observation to the distance list
                            sortList.append(nnDict[varSet][uid][nnObs]['DIST'])                             #Add the same distance to the list for later sorting
                        sortList.sort()                                                                     #Sort the distances in the sort list from lowest to highest
                        end_i = len(sortList)                                                               #Get the length of the sort list
                        if not end_i == kNN:                                                                #Check to make sure that the length of the sort list is the same as the value of the maximum kNN
                            print 'Error in nnDict - fewer NN:', end_i, 'than expected:', kNN               #If it is not the same length as maximum kNN then there is something wrong    
                            print 'Rule:', rule, 'Varset', varSet, 'UID:', uid
                            print 'Error found in routineLviApplications_v2.getZNearestNeighbourRMSE()'
                        totalValue = 0                                                                      #Initialize a total value
                        newEstYValueList = []
                        for i in range(0,kNN,1):                                                            #For each of the nearest neighbours
                            dist = sortList[i]                                                              #Get the distance starting with the most nearest neighbour and working toward the next most nearest up until the maximum kNN
                            yIndex = distList.index(dist)                                                   #Find the index of position where that same distance can be found in the unsorted distance list 
                            estYValue = estYValueList[yIndex]                                               #Using the index get the corresponding estimated Y-value
                            newEstYValueList.append(estYValue)
                            totalValue = totalValue + estYValue                                             #Add the estimated Y-value to the previous Y value
                            meanNNValue = totalValue /float(i+1)                                            #Calculate the mean estimated Y-value for k nearest neighbours, 1,2,3 ... up to kNN
                            bias = expYValue - meanNNValue
                            biasDict[i].append(bias)
                            biasMse = bias**2                                                               #Subtract the mean estimated Y-value from the expected Y-value and square it to estimated the squared error
                            #print i, dist, expYValue, estYValue, meanNNValue, se
                            biasMseDict[i].append(biasMse)                                                  #Add the squared error associated kNN set, i
                            se = (numpy.std(newEstYValueList))**2
                            seDict[i].append(se) 
                    for i in range(0,kNN,1):                                                                #For each set of NN from 1 to kNN
                        rmse = (numpy.mean(seDict[i]))** 0.5                                                #Calculate root mean squared error associated with the estimated mean
                        bias = numpy.mean(biasDict[i])                                                      #Calculate the mean bias
                        BRmse = (numpy.mean(biasMseDict[i]))** 0.5                                          #Calculate the root mean squared error associated with bias
                        rmseDict[varName][varSet].update({(i+1):{'RMSE':rmse, 'BIAS':bias, 'BRMSE':BRmse}}) #Add the RMSE, BIAS, and BIAS2 assocated with each number of nearest neighbours, i+1
        if batchNo == 0:
            addToDataMachette20121026.initialize_header(rmseHeader,rmseFilePath)                                    #Initialize the print file by overwriting any pre-existing file with the new header
            if printFlag == 'Yes' or printFlag == 'yes' or printFlag == 'y' or printFlag == 'Y':
                print ' New RMSE.csv created:', newRMSEFile    
        addToDataMachette20121026.print_to_nested_dictionary(rmseKeyVarNames,rmseHeader, rmseDict, rmseFilePath)    #Print the remaining RMSE's to the print file
        if printFlag == 'Yes' or printFlag == 'yes' or printFlag == 'y' or printFlag == 'Y':
            print ' Writing to fileName:', newRMSEFile, 'batchNo', batchNo
        return rmseDict

    def GetSpeciesList(self, myTypedDict = {},spColumnNames = []):
        '''
        '''
        myTypedDictKeyList = myTypedDict.keys()
        myTypedDictKeyList.sort()
        spList = []
        for keyValue in myTypedDictKeyList:
            for spFieldName in spColumnNames:
                treeSpecies = myTypedDict[keyValue][spFieldName]
                if not treeSpecies == '' and not treeSpecies == ' ' and not treeSpecies == '  ':
                    if not treeSpecies in spList:
                        spList.append(treeSpecies)
        spList.sort()
        return spList


    def GetSpeciesListFromPlotAndTreeData(self, myTypedDict = {},spColNamesList = []):
        '''
        '''
        spList = []
        plotKeyList = myTypedDict.keys()
        plotKeyList.sort()
        for plot in plotKeyList:
            treeKeyList = myTypedDict[plot].keys()
            treeKeyList.sort()
            for tree in treeKeyList:
                for spColName in spColNamesList:
                    treeSp = myTypedDict[plot][tree][spColName]
                    if not treeSp in spList:
                        spList.append(treeSp)
        spList.sort()
        return spList

    def GetSpeciesListFromPlotOrTreeData(self, myTypedDict = {},spColNamesList = []):
        '''
        '''
        spList = []
        keyList = myTypedDict.keys()
        keyList.sort()
        for newKey in keyList:
            for spColName in spColNamesList:
                treeSp = myTypedDict[newKey][spColName]
                if not treeSp in spList:
                        spList.append(treeSp)
        spList.sort()
        return spList



    def GetSpeciesCodesFromFileOrAssigneNewSpeciesCodes(self, myTreeDict = {}, spColNamesList = [], spTableName = 'SPDICT', dataDictType = 'TWOKEY'):
        '''
        The purpose of this routine is to take a set of codes in certain fields and allow the user to reassign new codes.
        This program is interactive using input and raw_input statements.
        
        Inputs 
            myTreeDict is a data file
            spColNamesList gives a list of column headings or dictionary field names under which species in myTreeDict are recorded
            spTableName is the name of the table containing current and or future species translation tables
                        is also the name of a .csv file containing the species translations
            dataDictType is used to indicate whether there are one or two key variable names needed to access myTreeDict field names
                         ... in the spColNamesList.  At the moment this is limited to TWOKEY data; also in the future this can be dropped
                         and generalized as per other data dictionary routines.
        OUTPUTS
            New File:
                A data file with name spTableName and file extension .csv written to self.dataFilePath (i.e. location of Rwd directory
                
            Variables Returned to Main Program:
                spKeyNameList   i.e. keyVariableNames associated with the species dictionary
                spHeader        i.e. list of variable names including keyVariableNames in species dictionary
                spDict          a dictionary with the original species as the primary key as follows: {origSpecies:{'NEWSP: newSp}}
                newSpList       a list containing the new species assignments

        The program was first developed with COMPILE_MOF_TREE_DATASET.py

        Ian Moss
        April 17 2013
        '''
        spTableFilePath = self.dataFilePath + spTableName + fileExtension                                                #Create a new file path 
        readSpErrorFileName = 'ERROR_' + spTableName                                                                #Create a read error file
        spHeader = ['ORIGSP','NEWSP']                                                                               #Species file header
        spKeyNameList = ['ORIGSP']                                                                                  #List of key variable names for constructing dictionary
        newSpList = []                                                                                              #Start a list of new species
        spDict = {}
        flag = False                                                                                                #Indicates that no species translation file exists or the old file is not going to be used
        if fileUtilities.checkFileIfItExists(spTableFilePath)== 1:
            useExistingFile = 'NO'                                                                                  #File exists - set the default for using the file to NO  
            print "\n Species translation table at self.filePath: ", spTableFilePath
            print "\n Enter NO if you DO NOT wish to use this table, \n Otherwise press ENTER"
            useExistingFile = raw_input("\n ... ")
            if useExistingFile == '' or useExistingFile == ' ':
                flag = True                                                                                         #File exists and user wishes to use that file to determine the species translations
                oldSpDict, newSpDict = createNewDataDictionaryFromFile(spTableName, 'YES', 1000)
                spHeader, spDict = ReadCsvDataFileAndTransformIntoDictionaryFormat_v2(oldSpDict, newSpDict, spTableName, readSpErrorFileName, spKeyNameList)
                print "\n Do you wish to check for new tree species and add them to the current species dictionary?"
                print " Enter YES if you do and then press ENTER, otherwise press ENTER to continue."
                appendNewSpecies = raw_input("\n ... ")
                if appendNewSpecies == 'YES' or appendNewSpecies == 'Yes' or appendNewSpecies == 'yes' or appendNewSpecies == 'Y' or appendNewSpecies == 'y':
                    flag = False
        if flag == False:                                                                                           #Species translation file exists but user wishes to change the newSpecies designations or it doesn't exist
            if dataDictType == 'TWOKEY':                                                                            #The data dictionary has two keys
                spList = GetSpeciesListFromPlotAndTreeData(myTreeDict,spColNamesList)                               #Get species list from tree dictionary
            if dataDictType == 'ONEKEY':
                spList = GetSpeciesListFromPlotOrTreeData(myTreeDict,spColNamesList)
            spDict = AssignNewSpeciesCodes(spList, spDict)                                                          #Get new species dictionary
            addToDataMachette20121026.initialize_header(spHeader,spTableFilePath)
            addToDataMachette20121026.print_to_nested_dictionary(spKeyNameList, spHeader, spDict, spTableFilePath)  #Print new species dictionary to spTableFilePath
        for spOrig in spDict:                                                                                       #Make a list of new tree species
            if not spDict[spOrig].has_key('NEWSP'):
                spDict[spOrig].update({'NEWSP':spOrig})
            newSp = spDict[spOrig]['NEWSP']
            if not newSp in newSpList:
                newSpList.append(newSp)
            newSpList.sort()                                                                                        #Sort the list of new tree species
        return spKeyNameList, spHeader, spDict, newSpList


    def AssignNewSpeciesCodes(self, spList = [], spDict = {}):
        '''
        '''
        print 'The list of tree species in this file is as follows:'
        for sp in spDict:
            if not sp in spList:
                spList.append(sp)
        spList.sort()
        for sp in spList:
            if not spDict.has_key(sp):
                spDict.update({sp:{'NEWSP':sp}})
            if not spDict[sp].has_key('NEWSP'):
                spDict[sp].update({'NEWSP':sp})
        print ' The following new species codes have been assigned to replace the original species codes:'
        print '\n Original:New'
        for sp in spList:
            print sp, ':', spDict[sp]['NEWSP']
        print '\n Do you accept the new species list?'
        acceptSpeciesList = raw_input('\n Enter NO and then press ENTER if you wish to re-enter one or more new labels,\n otherwise press ENTER ... ')
        while acceptSpeciesList == 'NO' or acceptSpeciesList == 'No' or acceptSpeciesList == 'N' or acceptSpeciesList == 'n' or acceptSpeciesList == 'no' :
            for sp in spList:
                print sp,':',spDict[sp]['NEWSP']
                newSpecies = raw_input('\n Enter new species replacement code and press ENTER,\n or press ENTER to keep the existing new species code ... ')
                if not newSpecies == '':
                    spDict[sp]['NEWSP']=newSpecies
                else:
                    if sp == '' and newSpecies == '':
                        spDict[sp]['NEWSP']=newSpecies
            print ' The following new species codes have been assigned to replace the original species codes:'
            print '\n Original:New'
            for sp in spList:
                print sp, ':', spDict[sp]['NEWSP']
            print '\n Do you accept the new species list?'
            acceptSpeciesList = raw_input('\n Enter NO and then press ENTER if you wish to re-enter one or more new labels,\n otherwise press ENTER ... ')   
        print ' The following new species codes have been assigned to replace the original species codes:'
        print '\n Original:New'
        for sp in spList:
            print sp, ':', spDict[sp]['NEWSP']
        return spDict

    def GetStandardDataInputFiles(self, ):
        '''
        '''
        print ' A new standard data dictionary for new dataset \n identifying variable names and data types \n should be located in the: /Rwd/Python/DATDICT/ file path'
        raw_input(" Press ENTER to continue ... ")
        #Ask user to input name of data dictionary without .csv extension and then read data dictionary
        print ("\n Enter NODICT without '' if there is no data DICTIONARY associated with a data file") 
        myDataDictName = raw_input("\n Input name of DICTIONARY without .csv extension\n and without '' and press ENTER to continue ... ")
        if not myDataDictName == 'NODICT':
            myDataDictName = checkForFilePath(dictFilePath, myDataDictName, '.csv')
        else:
            myDataDictName = {}
        raw_input("\n The .csv DATA file should be in the top of the /Rwd/ directory\n press ENTER to continue ... ")
        newDataTableName = raw_input("\n Input name of DATA file without .csv extension\n and without '' and press ENTER to continue ... ")
        newDataTableName = checkForFilePath(self.filePath, newDataTableName, '.csv')
        keyVarNameList = raw_input("\n Input list of the KEY VARIABLE NAMES (NEWVARNAME in DICTIONARY)\n in square parenthesis, e.g. ['KEY1','KEY2'], in the order that they occur separated by commas\n and press ENTER to continue ... ")
        print "\n A read error file is created in the Admin directory to indicate problems\n in assigning certain data dictionary data types to certain fields"  
        readErrorFileName = raw_input("\n Input that name of the read error file in case there are errors\n without .csv extensions and without '' and press ENTER ... ")
        return myDataDictName, newDataTableName, keyVarNameList, readErrorFileName

    def GetSpeciesColumnNames(self, ):
        spColumnNames = raw_input("\n Enter list of species column names, e.g. ['SP1_CD','SP2_CD']\n and then press ENTER ... ")
        return spColumnNames

    def GetSpeciesPercentColumnNames(self, ):
        spPcntColumnNames = raw_input("\n Enter list of species percentage column names, e.g. ['SP1_PCT','SP2_PCT']\n and then press ENTER ... ")
        return spPcntColumnNames

    def checkForFilePath(self, filePath = '', tableName = '', fileExtension = '.txt'):
        '''
        '''
        newFilePath = self.filePath + tableName + fileExtension
        if os.path.exists(newFilePath):
            flag = True
        else:
            flag = False
        if flag == False:
            while flag == False:
                print '\n There is no fileName', tableName, 'in self.filePath', self.filePath, 'with file extension', fileExtension
                tableName = raw_input(' Please input new fileName without self.filePath or file extension and press ENTER ... ')
                newFilePath = self.filePath + tableName + fileExtension
                if os.path.exists(newFilePath):
                    flag = True
                else:
                    flag = False
            print '\n FileName', tableName, 'FOUND IN self.filePath', self.filePath, 'with file extension', fileExtension
            raw_input (' Press ENTER to continue ... ')
        return tableName

     
    def getTargetDatasetNearestNeighboursForManyVarsets(self, maxKNN = 1, varSetList = [], targetTypedDict = {}, targetHeader = [], refTypedDict = {}, \
                                                         refHeader = [], dfuncTypedDict = {},zNorm = 'YES', printFileName = 'NNTARGET'):
        '''
        Inputs
            maxKNN          is the maximum number of nearest neighbours
            varSetList      is a list of variable set numbers associated with xStatTypedDict for which nearest neighbours are requested.
            targetTypedDict contains the target data that includes the variable names associated with a given varSet in the xStatTypedDict
            targetHeader    is used to check to make sure that the variables associated with a given variable set in xStatTypedDict are also in the targetTypedDict
            refTypedDict    contains the reference dataset consisting of zscores
            refHeader       contains the variable names in the reference dataset
            dfuncTypedDict  contains the discriminant functions and parameters to be applied to each X variable name to estimate zScores
            zNorm           is 'YES' if normalized zScores are to be used, otherwise 'NO' or left blank
            
        '''
        print '\n Start nearest neighbour processing', time.ctime()
        for varSet in varSetList:
            printFilePath = self.filePath + printFileName + str(varSet) + '.csv'
            addToDataMachette20121026.deleteFileIfItExists(printFilePath)
            nnDict, nnHeader, nnKeyNameList = getTargetDatasetNearestNeighbousForSingleVarsetsUsingZScores(maxKNN, varSet, targetTypedDict, targetHeader, refTypedDict, \
                                                         refHeader, dfuncTypedDict, zNorm, printFilePath)
        return nnDict                                                   
        

    def getTargetDatasetNearestNeighbousForSingleVarsetsUsingZScores(self, maxKNN = 1, varSet = 1, targetTypedDict = {}, targetHeader = [], refTypedDict = {}, \
                                                         refHeader = [], dfuncTypedDict = {}, zNorm = 'YES', printFilePath = ''):
        '''
        ''' 
        #Initialize Nearest Neighbour Dictionary Header
        nnHeader = ['TARGOBS']
        nnKeyNameList = ['TARGOBS']
        nnHeaderNameLabels = []
        nnHeaderDistLabels = []
        #Initialize nearest neighbour dictionary
        nnDict = {}   
        for i in range(1, maxKNN+1,1):
            #Nearest Neighbour Names ranked from 1 to maxKNN in order of distance
            newName = 'NN' + str(i)
            nnHeader.append(newName)
            nnHeaderNameLabels.append(newName)
        for i in range(1, maxKNN+1,1):
            #Associated distances ranked from closest (1) to farthest away (kNN) 
            newName = 'DIST' + str(i)
            nnHeader.append(newName)
            nnHeaderDistLabels.append(newName)
        #Get list of Target dataset Unique ID's                                                
        targetObsList = targetTypedDict.keys()
        targetObsList.sort()
        #Get list of Reference dataset Unique ID's
        refObsList = refTypedDict.keys()
        refObsList.sort()
        #Get discriminant function labels
        dfuncLabelList = dfuncTypedDict[varSet].keys()
        dfuncLabelList.sort()
        #Extract X-Variables Names
        xVarNamesList = dfuncTypedDict[varSet][dfuncLabelList[0]].keys()
        #Get number of discriminant functions
        nDfunc = len(dfuncLabelList)
        #Check to make sure all of the variable names can be found in both the target and reference datasets
        for varName in xVarNamesList:
            if not varName in targetHeader:
                print 'Variable name', varName, 'not found in TARGET dataset'
                print 'Review data dictionary to ensure proper new variable name assignments for TARGET dataset'
            if not varName in refHeader:
                print 'Variable name', varName, 'not found in REFERENCE dataset'
                print 'Review data dictionary to ensure proper new variable name assignments for REFERENCE dataset'
        #Compute zscores for reference dataset
        refZScoreDict = assignZScoresToDictionarDataset(refTypedDict,varSet, dfuncTypedDict)
        targetZScoreDict = assignZScoresToDictionarDataset(targetTypedDict,varSet, dfuncTypedDict)
        #
        if zNorm == 'YES':
            #Compute standard deviations for the discriminant scores associated with each function using the reference dataset
            normStats = computeVariableMeansAndStandardDeviations(refZScoreDict)   
        #Start processing nearest neighbours
        numberObs = 0
        countObs = 5000
        for targetObs in targetObsList:
            newVarValueList = []
            newZValueList = []
            nnIdList = []
            nnDistList = []
            nnDict.update({targetObs:{}})
            for refObs in refObsList:
                diffDist = 0
                for varName in dfuncLabelList:
                    #Get normalized difference in ZScores
                    if zNorm == 'YES':
                        diffValue = (targetZScoreDict[targetObs][varName] - refZScoreDict[refObs][varName])/float(normStats[varName]['SDEV'])
                    else:
                        diffValue = (targetZScoreDict[targetObs][varName] - refZScoreDict[refObs][varName])
                    #Euclidean distance
                    diffDist = diffDist + diffValue**2
                    #if targetObs==refKey:
                    #    print targetObs, dfuncLabel, refZValue, newZValueList[j], diffDist
                if not len(nnIdList)== maxKNN:
                    nnIdList.append(refObs)
                    nnDistList.append(diffDist)
                else:
                    if diffDist < max(nnDistList):
                        colIndex = nnDistList.index(max(nnDistList))
                        del nnDistList[colIndex]
                        del nnIdList[colIndex]
                        nnDistList.append(diffDist)
                        nnIdList.append(refObs)
            #print targetObs, nnIdList, nnDistList
            for i in range(0,maxKNN,1):
                colIndex = nnDistList.index(min(nnDistList))
                nnDict[targetObs].update({nnHeaderNameLabels[i]:nnIdList[colIndex],nnHeaderDistLabels[i]:nnDistList[colIndex]})
                del nnDistList[colIndex]
                del nnIdList[colIndex]
            numberObs = numberObs + 1
            if numberObs == countObs:
                print '', numberObs, time.ctime()
                addToDataMachette20121026.check_for_filepath_then_print(printFilePath, nnKeyNameList, nnHeader, nnDict)
                countObs = countObs + 5000
                nnDict = {}
        if not nnDict == {}:
            addToDataMachette20121026.check_for_filepath_then_print(printFilePath, nnKeyNameList, nnHeader, nnDict)
            print '', numberObs, time.ctime()
        return nnDict, nnHeader, nnKeyNameList

    def getTargetDatasetNearestNeighbousForSingleVarsetsUsingZScores_v2(self, maxKNN = 1, varSet = 1, targTypedList = [[]], targKeyVarNames = [], refTypedList = [], \
                                                         refKeyVarNames = [], dfuncTypedDict = {}, zNorm = 'YES', printFilePath = ''):
        '''
        '''
        tarHeader = targTypedList[0]
        refHeader = refTypedList[0]
        #Initialize Nearest Neighbour Dictionary Header
        nnHeader = ['TARGOBS']
        nnKeyNameList = ['TARGOBS']
        nnHeaderNameLabels = []
        nnHeaderDistLabels = []
        #Initialize nearest neighbour List
        nnList = [[]]
        for i in range(1, maxKNN+1,1):
            #Associated distances ranked from closest (1) to farthest away (kNN) 
            newName = 'DIST' + str(i)
            nnHeader.append(newName)
            nnList.append(newName)    
        for i in range(1, maxKNN+1,1):
            #Nearest Neighbour Names ranked from 1 to maxKNN in order of distance
            newName = 'NN' + str(i)
            nnHeader.append(newName)
            nnList.append(newName)
        #Extract X-Variables Names
        xVarNamesList = dfuncTypedDict[varSet][dfuncLabelList[0]].keys()
        xvarTargKeyIndexList = getVariableNameColumnNumbers(targKeyVarNames, targHeader)
        xVarTargVarIndexList = getVariableNameColumnNumbers(xVarNameList, targHeader)
        xvarRefKeyIndexList = getVariableNameColumnNumbers(refKeyVarNames, refHeader)
        xVarRefVarIndexList = getVariableNameColumnNumbers(xVarNameList, refHeader)
        #Get number of discriminant functions
        nDfunc = len(dfuncLabelList)
        #Check to make sure all of the variable names can be found in both the target and reference datasets
        for varName in xVarNamesList:
            if not varName in targHeader:
                print 'Variable name', varName, 'not found in TARGET dataset'
                print 'Review data dictionary to ensure proper new variable name assignments for TARGET dataset'
            if not varName in refHeader:
                print 'Variable name', varName, 'not found in REFERENCE dataset'
                print 'Review data dictionary to ensure proper new variable name assignments for REFERENCE dataset'
        

        ###################################################################################################################################################
        #Get list of Target dataset Unique ID's                                                
        targetObsList = targetTypedDict.keys()
        targetObsList.sort()
        #Get list of Reference dataset Unique ID's
        refObsList = refTypedDict.keys()
        refObsList.sort()
        #Get discriminant function labels
        dfuncLabelList = dfuncTypedDict[varSet].keys()
        dfuncLabelList.sort()
        
        #Compute zscores for reference dataset
        refZScoreDict = assignZScoresToDictionarDataset(refTypedDict,varSet, dfuncTypedDict)
        targetZScoreDict = assignZScoresToDictionarDataset(targetTypedDict,varSet, dfuncTypedDict)
        #
        if zNorm == 'YES':
            #Compute standard deviations for the discriminant scores associated with each function using the reference dataset
            normStats = computeVariableMeansAndStandardDeviations(refZScoreDict)   
        #Start processing nearest neighbours
        numberObs = 0
        countObs = 5000
        for targetObs in targetObsList:
            newVarValueList = []
            newZValueList = []
            nnIdList = []
            nnDistList = []
            nnDict.update({targetObs:{}})
            for refObs in refObsList:
                diffDist = 0
                for varName in dfuncLabelList:
                    #Get normalized difference in ZScores
                    if zNorm == 'YES':
                        diffValue = (targetZScoreDict[targetObs][varName] - refZScoreDict[refObs][varName])/float(normStats[varName]['SDEV'])
                    else:
                        diffValue = (targetZScoreDict[targetObs][varName] - refZScoreDict[refObs][varName])
                    #Euclidean distance
                    diffDist = diffDist + diffValue**2
                    #if targetObs==refKey:
                    #    print targetObs, dfuncLabel, refZValue, newZValueList[j], diffDist
                if not len(nnIdList)== maxKNN:
                    nnIdList.append(refObs)
                    nnDistList.append(diffDist)
                else:
                    if diffDist < max(nnDistList):
                        colIndex = nnDistList.index(max(nnDistList))
                        del nnDistList[colIndex]
                        del nnIdList[colIndex]
                        nnDistList.append(diffDist)
                        nnIdList.append(refObs)
            #print targetObs, nnIdList, nnDistList
            for i in range(0,maxKNN,1):
                colIndex = nnDistList.index(min(nnDistList))
                nnDict[targetObs].update({nnHeaderNameLabels[i]:nnIdList[colIndex],nnHeaderDistLabels[i]:nnDistList[colIndex]})
                del nnDistList[colIndex]
                del nnIdList[colIndex]
            numberObs = numberObs + 1
            if numberObs == countObs:
                print '', numberObs, time.ctime()
                addToDataMachette20121026.check_for_filepath_then_print(printFilePath, nnKeyNameList, nnHeader, nnDict)
                countObs = countObs + 5000
                nnDict = {}
        if not nnDict == {}:
            addToDataMachette20121026.check_for_filepath_then_print(printFilePath, nnKeyNameList, nnHeader, nnDict)
            print '', numberObs, time.ctime()
        return nnDict, nnHeader, nnKeyNameList


    def assignZScoresToDictionarDataset(self, myTypedDict = {}, varSet = 1, dfuncTypedDict = {}):
        '''
        '''
        zscoreDict = {}
        if not dfuncTypedDict.has_key(varSet):
            print 'routineLviApplications.assignZscoresToDictionaryDataset'
            print 'Discriminant Function Dictionary does not have variable set number:', varSet
            print 'Cannot compute Z-Scores'
        for obsName in myTypedDict:
            zscoreDict.update({obsName:{}})
            for dfunc in dfuncTypedDict[varSet]:
                zscoreDict[obsName].update({dfunc:0})
                for varName in dfuncTypedDict[varSet][dfunc]:
                    varValue = myTypedDict[obsName][varName]
                    paramValue = dfuncTypedDict[varSet][dfunc][varName]['DFCOEF3']
                    zscoreDict[obsName][dfunc] = zscoreDict[obsName][dfunc] + paramValue * varValue
        return zscoreDict

    def computeVariableMeansAndStandardDeviations(self, myDict = {}):
        '''
        '''
        vectorDict = {}
        normStatsDict = {}
        for obsName in myDict:
            for varLabel in myDict[obsName]:
                if not vectorDict.has_key(varLabel):
                    vectorDict.update({varLabel:[]})
                varValue = myDict[obsName][varLabel]
                vectorDict[varLabel].append(varValue)
        for varLabel in vectorDict:
            sdevValue = numpy.std(vectorDict[varLabel])
            meanValue = numpy.mean(vectorDict[varLabel])
            normStatsDict.update({varLabel:{'SDEV':sdevValue, 'MEAN':meanValue}})
        return normStatsDict

    def compileTargetNearestNeighbourYStatistics(self, targetHeader = [], targetTypedDict = {}, lvinewTypedDict = {}, yVarNameList = [], nnTargetTableNo = '0'):
        '''
        '''
        print '\n Start compiling nearest neighbour y-variable statistics for target dataset'
        print '', time.ctime()
        


        #Compute number of nearest neighbours
        kNN = 0
        nnNameList = []
        for i in range(1,101,1):
            newVarName = 'NN' + str(i)
            if newVarName in targetHeader:
                kNN = kNN + 1
                nnNameList.append(newVarName)
            else:
                break
        #Initialize target nearest neighbour Y-variable dataset
        targStatKeyVarNames = ['TARGOBS','VARNAME','KNN']
        targStatHeader = ['TARGOBS','VARNAME','KNN','MEAN','SDEV']
        targNNStats = {}

        targStatFileName = 'TNNSTATS' + nnTargetTableNo
        targStatFileType = '.csv'
        targStatFilePath = initializeFilePath(targStatFileName, targStatFileType)

        #Intialize file with new header
        initializeHeader(targStatHeader, targStatFilePath)

        #Get key target Observation values list
        targObsKeyValueList = targetTypedDict.keys()
        targObsKeyValueList.sort()

        #Start compiling target variable name statistics from reference dataset
        nRecords = 10000
        nRec = 0
        for targObs in targObsKeyValueList:
            targNNStats.update({targObs:{}})
            for yVarName in yVarNameList:
                targNNStats[targObs].update({yVarName:{}})
                i = 0
                yVarValueList = []
                for nnName in nnNameList:
                    i = i + 1
                    nNeighbour = targetTypedDict[targObs][nnName]
                    yVarValue = lvinewTypedDict[nNeighbour][yVarName]
                    yVarValueList.append(yVarValue)
                    yVarMean = numpy.mean(yVarValueList)
                    if i == 1:
                        yVarStd = 0
                    else:
                        yVarStd = numpy.std(yVarValueList)
                    targNNStats[targObs][yVarName].update({i:{'MEAN':yVarMean,'SDEV':yVarStd}}) 
            nRec = nRec + 1
            if nRec == nRecords:
                print '', nRecords, time.ctime()
                #Write data to file
                addDataToFile(targStatFilePath, targStatKeyVarNames, targStatHeader, targNNStats)
                targNNStats = {}
                nRecords = nRecords + 10000
        if not targNNStats == {}:
            addDataToFile(targStatFilePath, targStatKeyVarNames, targStatHeader, targNNStats)
        print '', nRec, time.ctime()   
        return targStatHeader, targStatKeyVarNames, targNNStats

    def initializeFilePath(self, newFileName = '', newFileType = '.csv'):
        newFilePath = self.dataFilePath + newFileName + newFileType
        return newFilePath


    def initializeHeader(self, newFileHeader = [], newFilePath = ''):
        '''
        '''
        addToDataMachette20121026.initialize_header(newFileHeader,newFilePath)
        return

    def addDataToFile(self, printFilePath = '', keyVarNameList = [], header=[], dataTypedDict = {}):
        
        addToDataMachette20121026.check_for_filepath_then_print(printFilePath, keyVarNameList, header, dataTypedDict)
        return

    def readDataStringListHeader(self, table_name = ''):
        '''
        '''
        newHeader = readCSV.read_csv_text_file_header_v2(self.dataFilePath,table_name, fileExtension)
        return newHeader

    def createNewDataDictionaryFromFile(self, dataTableName = '', printTypes = 'YES', nLines = 1000):
        '''
        This routine creates a data dictionary including a list of data types based
        on the first nLines (e.g. 1000) for the dataTableName given the self.filePath and
        fileExtension attached to this module.  printTypes = 'YES' provides a listing
        of the variable names in the file header and the data types assigned based on
        the first nLines in the file - as output in the IDE to enable the user to check
        that everything is ok.  This is created directly from from a file instead of a
        string table that has already been loaded into memmory for cases where the file
        size is too big to hold in  memory.
        '''
        oldDict, newDict = makeDD.makeNewDataDictionaryFromLargeDataStringFile(dataTableName, self.filePath, fileExtension, printTypes, nLines)
        return oldDict, newDict

    def writeListArrayToCsvFile(self, TwoDList = [[]], fileName = '', floatFormat = ''):
        '''
        '''
        dataMachete.writeListarrayToCSVFile(TwoDList, self.dataFilePath, fileName, floatFormat, fileExtension)
        return
                                
    def createPivotTable(self, dataTableName = [], dataDict = {}, keyRowVarNameList = [], keyColumnVarName = '', keyVarValueName = '', nObs = -1, nnTargetTableNo = 0):
        '''
        '''
        print '\n Start identifying column variables in pivot table'
        print '', time.ctime()
        file_path = fileUtilities.newFilePath_v2(self.filePath, dataTableName, fileExtension)              #Input self.filePath
        newDataTableName = 'TNNSTATP' + str(nnTargetTableNo)                            #Initialize print file name including target table number
        if keyVarValueName == 'MEAN':
            newDataTableName = newDataTableName + '_MEAN'
        if keyVarValueName == 'SDEV':
            newDataTableName = newDataTableName + '_SDEV'
        print '\n ', newDataTableName, '.csv file is being created in Rwd directory'
        newFilePath = fileUtilities.newFilePath_v2(self.filePath, newDataTableName, fileExtension)
        readErrorFileName = 'ERROR_' + dataTableName
        readErrorFilePath = fileUtilities.newFilePath_v2(self.filePath, readErrorFileName, fileExtension)
        colNamesList = []
        keyRowNoList = []   
        newHeader = deepcopy(keyRowVarNameList)
        temp_file = open (file_path,'r')
        i = 0
        targObs = -1
        prevTargObs = -1
        #Start by getting list of
        for newLine in temp_file:
            if i == 0:
                header = readCSV.createStringListFromCsvFileLine(newLine)
                nestedStringList = [header]
                #Get the column number holding the names of variables to be put in columns
                if not keyColumnVarName in header:
                    print ' Error in routineLviApplications.createPvotTable()'
                    print ' dataTableName self.filePath is:', file_path
                    print ' keyColumnVarName:', keyColumnVarName, 'not found in header'
                    print ' header:', header
                    keyColNo = 'none'
                else:
                    keyColNo = header.index(keyColumnVarName)
                #Get the column numbers holding the key variables to establish a unique set of rows, keyRowNoList
                for keyRowVarName in keyRowVarNameList:
                    if not keyColumnVarName in header:
                        print ' Error in routineLviApplications.createPvotTable()'
                        print ' dataTableName self.filePath is:', file_path
                        print ' keyRowVarName:', keyRowVarName, 'not found in header'
                        print ' header:', header
                        keyRowNoList.append('none')
                    else:
                        keyRowNo = header.index(keyRowVarName)
                        keyRowNoList.append(keyRowNo)
                #Get the column number, keyVarValueNo, for assigning values to each of the variable names in the keyColNo
                if not keyVarValueName in header:
                    print ' Error in routineLviApplications.createPvotTable()'
                    print ' dataTableName self.filePath is:', file_path
                    print ' keyVarValueName:', keyVarValueName, 'not found in header'
                    print ' header:', header
                    keyVarValueNo = 'none'
                else:
                    keyVarValueNo = header.index(keyVarValueName)
            else:
                #i is > 0
                newStringList = readCSV.createStringListFromCsvFileLine(newLine)    #Convert line to string list
                newTypedList = typeDataset.typeDataset_v2([header,newStringList], dataDict, dataTableName, readErrorFileName)   #Convert list to dataTyped List
                newColName = newTypedList[1][keyColNo]                              #Get new column name
                if not newColName in colNamesList:                                  #Check to make sure column name is in list
                    colNamesList.append(newColName)
            i = i + 1
        colNamesList.sort()                                                     #Sort colNamesList
        for colName in colNamesList:
            newHeader.append(colName)                                           #Append colNames to newHeader
        #newHeader = ['TARGOBS','KNN','LVI_AGE_AT','LVI_AGE_FD','LVI_AGE_PL','LVI_AGE_SX', \
        #             'LVI_BPH_AT', 'LVI_BPH_FD','LVI_BPH_PL', 'LVI_BPH_SX', \
        #             'LVI_DVPH', \
        #             'LVI_ESI_AT', 'LVI_ESI_FD','LVI_ESI_PL','LVI_ESI_SX', \
        #             'LVI_HT_AT', 'LVI_HT_FD','LVI_HT_PL', 'LVI_HT_SX', \
        #             'LVI_LSPH']
        #keyVarValueNo = 3
        #keyColNo = 1
        #keyRowNoList = [0,2]
        addToDataMachette20121026.initialize_header(newHeader,newFilePath)      #Initialize printFile
        i = 0
        j = 0
        newDict = {}
        obsCount = 0
        print '\n Start creating pivot table'
        print '', time.ctime()
        temp_file.close()
        temp_file = open (file_path,'r')
        for newLine in temp_file:
            if i == 0:
                i = i + 1
                #header = readCSV.createStringListFromCsvFileLine(newLine)
            else:
                newStringList = readCSV.createStringListFromCsvFileLine(newLine)                                                #Convert line to string list
                newTypedList = typeDataset.typeDataset_v2([header,newStringList], dataDict, dataTableName, readErrorFileName)   #Get typed list
                newColName = newTypedList[1][keyColNo]                                                                          #Get new column name
                newColValue = newTypedList[1][keyVarValueNo]
                targObs = newTypedList[1][keyRowNoList[0]]
                kNN = newTypedList[1][keyRowNoList[1]]
                if not targObs == prevTargObs:
                    i = i + 1
                    prevTargObs = targObs
                    #print i, j, targObs
                if nObs <= 0 or i < nObs + 1:
                #if i < nObs:
                    if not newDict.has_key(targObs):
                        newDict.update({targObs:{}})
                    if not newDict[targObs].has_key(kNN):
                        newDict[targObs].update({kNN:{}})
                    if not newDict[targObs][kNN].has_key(newColName):
                        newDict[targObs][kNN].update({newColName:newColValue})
                else:
                    addToDataMachette20121026.print_to_nested_dictionary(keyRowVarNameList,newHeader,newDict, newFilePath)
                    newDict = {}
                    newDict.update({targObs:{kNN:{newColName:newColValue}}})
                    obsCount = obsCount + i
                    print ' Observation count:', obsCount, time.ctime()
                    i = 1
            j = j + 1
        if not newDict == {}:
            addToDataMachette20121026.print_to_nested_dictionary(keyRowVarNameList,newHeader,newDict, newFilePath)
            print ' Observation count:', obsCount, time.ctime()
        return colNamesList
                    
    def assignTargetObservationsTokNearestNeighboursUsingEuclideanDistance(self, targetKeyVarNameList = [], targetKeyList = [[]], targetTypedSubsetList = [[]], refKeyList = [[]], refTypedSubsetList = [[]], kNN = 1):
        '''
        '''
        newFileHeader = deepcopy(targetKeyVarNameList)
        if kNN > len(refKeyList):
            kNN = len(refKeyList)
        if kNN < 1:
            kNN = 1
        for k in range(0,kNN,1):
            newVarName = 'NN' + str(k)
            newFileHeader.append(newVarName)
        for k in range(0,kNN,1):
            newVarName = 'DIST' + str(k)
            newFileHeader.append(newVarName)
        targetNNList = [newFileHeader]
        nRefObs = len(refKeyList)
        nTargetKeys = len(targetKeyList)
        for targetKeyNo in range(0,nTargetKeys,1):
            targetKeyNameList = targetKeyList[targetKeyNo]
            for targetKeyName in targetKeyNameList:
                targetNNList.append([targetKeyName])
            targetObsVector = targetTypedSubsetList[targetKeyNo]
            end_i = len(targetObsVector)
            newRefDistList = []
            newRefObsList = []
            for refObsNo in range(0,nRefObs,1):
                refObsName = refKeyList[refObsNo][0]
                refObsVector = refTypedSubsetList[refObsNo]
                end_j = len(refObsVector)
                if not end_j == end_i:
                    print 'roundineLviApplications.assignTargetObservationsTokNearestNeighboursUsingEuclideanDistance'
                    print 'targetTypedSubsetList is not the same length a refTypedSubsetList'
                    print 'nearestNeighbourError - different numbers of variables in sets'
                newDist = 0
                for i in range(0,end_i,1):
                    newDist = newDist + (targetObsVector[i]-refObsVector[i])**2
                if len(newRefObsList) < kNN: 
                    newRefObsList.append(refObsName)
                    newRefDistList.append(newDist)
                else:
                    maxDist = max(newRefDistList)
                    if newDist < maxDist:
                        maxObsIndex = newRefDistList.index(maxDist)
                        del newRefDistList[maxObsIndex]
                        del newRefObsList[maxObsIndex]
                        newRefDistList.append(newDist)
                        newRefObsList.append(refObsName)
            minDistList = []
            for k in range(0,kNN,1):
                minDist = min(newRefDistList)
                minDistList.append(minDist)
                minDistIndex = newRefDistList.index(minDist)
                minDistObs = newRefObsList[minDistIndex]
                targetNNList[targetKeyNo + 1].append(minDistObs)
                del newRefDistList[minDistIndex]
                del newRefObsList[minDistIndex]
            for k in range(0,kNN,1):
                minDist = minDistList[k]
                targetNNList[targetKeyNo + 1].append(minDist)
        return targetNNList   
                
    def getMeanAndStandardDeviationFor2DList(self, statsTableName = '', varNameList = [], dataTypedList = [], statsDict = {}):
        '''
        '''
        statsHeader = ['TABLENAME','VARNAME','MEAN','SDEV']
        statsKeyVarNameList = ['TABLENAME','VARNAME']
        numberOfVariables = len(varNameList)
        statsDict.update({statsTableName:{}})
        for varNo in range(0,numberOfVariables,1):
            varName = varNameList[varNo]
            varValueList = []
            for observation in dataTypedList:
                varValue = observation[varNo]
                varValueList.append(varValue)
            meanValue = numpy.mean(varValueList)
            sdevValue = numpy.std(varValueList)
            statsDict[statsTableName].update({varName:{'MEAN':meanValue,'SDEV':sdevValue}})
        return statsHeader, statsKeyVarNameList, statsDict
                       
    def normalizeVariableDataset(self, dataTypedList = [], varNameList =[], statsTableName = '', statsDict = {}):
        '''
        '''
        dataNormTypedList = []
        nVar = len(varNameList)
        nObs = len(dataTypedList)
        for obsNo in range(0,nObs,1):
            dataNormTypedList.append([])
            for varNo in range(0,nVar,1):
                varName = varNameList[varNo]
                meanValue = statsDict[statsTableName][varName]['MEAN']
                sdevValue = statsDict[statsTableName][varName]['SDEV']
                normValue = (dataTypedList[obsNo][varNo]-meanValue)/float(sdevValue)
                dataNormTypedList[obsNo].append(normValue)
        return dataNormTypedList
                                     
    def printList2DWithSeparateVarNameListAndKeyVarNameListAndValues(self, varNameList = [], varList2D = [[]], keyVarNameList = [], keyVarValueList = [[]],  tableName = ''):
        '''
        '''
        printFilePath = self.dataFilePath + tableName + '.csv'
        printFile = open(printFilePath, 'w')
        newHeader = joinOneDListBToRightOfOneDListA(keyVarNameList, varNameList)
        addToDataMachette20121026.compilePrintLineFromList(newHeader, newHeader, printFile)
        nObs = len(keyVarValueList)
        for obsNo in range(0, nObs,1):
            obsList = joinOneDListBToRightOfOneDListA(keyVarValueList[obsNo], varList2D[obsNo])
            addToDataMachette20121026.compilePrintLineFromList(obsList, newHeader, printFile)
        return

    def printNestedDictionary(self, keyVarNames = [], header = [], dataTypedDict = {}, tableName = ''):
        '''
        '''
        printFilePath = self.dataFilePath + tableName + '.csv'
        addToDataMachette20121026.initialize_header(header, printFilePath)
        addToDataMachette20121026.print_to_nested_dictionary(keyVarNames,header, dataTypedDict, printFilePath)
        return

    def printList2DWithHeader(self, varList2D =[[]], tableName = ''):
        '''
        '''
        printFilePath = self.dataFilePath + tableName + '.csv'
        addToDataMachette20121026.printList2D(varList2D, printFilePath, printOption = 'OVERWRITE')
        return
                    
    def createUniqueIdLinkTable(self, keyVarNameList = [], myDataDict = {}):
        '''
        '''
        linkKeyComboValueList = innerJoinDictDBs.getDictKeySetValuesList(myDataDict,keyVarNameList)
        linkKeyVarNamesList, linkDict = innerJoinDictDBs.createNewLinkTableIndexFromKeyComboList(keyVarNameList, linkKeyComboValueList)
        linkHeader = joinOneDListBToRightOfOneDListA(linkKeyVarNamesList, keyVarNameList)
        return linkHeader, linkKeyVarNamesList, linkDict

    def reassignDictKeysUsingLinkTable(self, dataDict = {}, linkDict = {}, keyVarNameList = [], mismatchNotification = 'Yes', tableName = ''):
        '''
        '''
        revisedDict = innerJoinDictDBs.extractDictDBDataUsingLinkDictTable(dataDict, linkDict, msimatchNotification, tableName)
        return revisedDict
                                       
    def collapseDictKeysUsingLinkTableData(self, dataDict = {}, linkDict = {}, keyVarNameList = [], mismatchNotification = 'Yes', tableName = ''):
        '''
        '''
        revisedDict = innerJoinDictDBs.collapseDictKeysUsingALinkTable(dataDict, linkDict, keyVarNameList, mismatchNotification, tableName)
        return revisedDict

    def removeMoFPspPlotNameBlankAndReestablishKeys(self, linkDict= {}):
        '''
        '''
        newDict = {}
        keyVarList = linkDict.keys()
        keyVarList.sort()
        newKey = 0
        for keyVar in keyVarList:
            if not linkDict[keyVar]['plot_no']== '':
                newKey = newKey + 1
                newDict.update({newKey:linkDict[keyVar]})
        return newDict

    def SelectCertainTreeClassesForPSPTreeLists(self, treeDict={}, treeDictColName = '', treeAttrList = []):
        '''
        Note that the tree dictionary contains a unique ID for each plot and has a list of
        trees as secondary keys.
        '''
        
        newTreeDict = {}
        plotList = treeDict.keys()
        plotList.sort()
        for plot in plotList:
            newTreeDict.update({plot:{}})
            treeList = treeDict[plot].keys()
            treeList.sort()
            for tree in treeList:
                flag = False
                for attribute in treeAttrList:
                    if treeDict[plot][tree][treeDictColName] == attribute:
                        flag = True
                if flag == True:
                    newTreeDict[plot].update({tree:treeDict[plot][tree]})
        return newTreeDict

    def SelectTreesAboveMinimumThrehsold(self, treeDict={}, treeDictColName = '', minimumThreshold = 0):
        '''
        Note that the tree dictionary contains a unique ID for each plot and has a list of
        trees as secondary keys.
        '''
        
        newTreeDict = {}
        plotList = treeDict.keys()
        plotList.sort()
        for plot in plotList:
            treeList = treeDict[plot].keys()
            treeList.sort()
            for tree in treeList:
                if treeDict[plot][tree][treeDictColName] >= minimumThreshold:
                    if not newTreeDict.has_key(plot):
                        newTreeDict.update({plot:{}})
                    newTreeDict[plot].update({tree:treeDict[plot][tree]})
        return newTreeDict


    def ReplaceTreeSpeciesInPlotDataWithNewSpecies(self, treeDict={},spDict={}, spColNamesList=[]):
        '''
        '''
        plotKeyList = treeDict.keys()
        plotKeyList.sort()
        for plot in plotKeyList:
            treeKeyList=treeDict[plot].keys()
            treeKeyList.sort()
            for tree in treeKeyList:
                for spColName in spColNamesList:
                    oldSpecies = treeDict[plot][tree][spColName]
                    newSpecies = spDict[oldSpecies]['NEWSP']
                    treeDict[plot][tree][spColName] = newSpecies
        return treeDict

    def ReplaceTreeSpeciesInOneKeyDataWithNewSpecies(self, dataDict={}, spDict={}, spColNamesList=[], dictKeyNo = 'ONEKEY'):
        '''
        '''
        print '\n Do you wish to replace old species with new species names?'
        renameSpecies = raw_input("Type YES and press ENTER if you do, \n otherwise press ENTER ... ")
        if renameSpecies == 'YES' or \
           renameSpecies == 'Y' or \
           renameSpecies == 'y' or \
           renameSpecies == 'yes':
            print '\n Proceeding with overwriting old with new species names.'
            oneKeyList = dataDict.keys()
            oneKeyList.sort()
            for oneKey in oneKeyList:
                if dictKeyNo == 'ONEKEY':
                    for spColName in spColNamesList:
                        oldSpecies = dataDict[oneKey][spColName]
                        newSpecies = spDict[oldSpecies]['NEWSP']
                        dataDict[oneKey][spColName] = newSpecies
                else:
                    if dictKeyNo == 'TWOKEY':
                        twoKeyList = dataDict[oneKey].keys()
                        twoKeyList.sort()
                        for twoKey in twoKeyList:
                            for spColName in spColNamesList:
                                oldSpecies = dataDict[oneKey][twoKey][spColName]
                                newSpecies = spDict[oldSpecies]['NEWSP']
                                dataDict[oneKey][twoKey][spColName] = newSpecies
        else:
            print '\n Original species names have been retained ...'
        return dataDict

    def CompilePerHectarePlotLevelStatisticsBySpeciesFromTreeLists(self, treeDict = {}, spColNamesList = [], mySpList = [], spVarValuesNamesList = []):
        '''
        Inputs
            treeDict is a two level dictionary structured according plot or sample id's and correspnding unique tree number id's
            spColumnNamesList list the names of the columns with species recorded in them
            spVarNameList includes the names if the variables corresponding to the speciesColumnNames that must be summed by species 
        '''
        newPlotDict = {}                                                                    #Create a newPlotDict
        spColCount = len(spColNamesList)
        spVarCount = len(spVarValuesNamesList)
        if not spColCount == spVarCount:
            print 'routineLviApplications.CompilePerHectarePlotLevelStatisticsBySpeciesFromTreeLists()'
            print 'Number of species columns',spColCount, 'is not equal to number of variable names,', spVarCount
            print 'spColNamesList:', spColNamesList
            print 'spVarNamesList:', spVarNamesList
        newPlotKeyVarList = ['PLOTID']                                                      #Create a newPlotDict keyVarNamesList
        newPlotHeader = joinOneDListBToRightOfOneDListA(newPlotKeyVarList, mySpList)        #Create a newPlotDict header
        plotKeyList = treeDict.keys()                                                       #Get list of plot keys from treeDict
        plotKeyList.sort()                                                                  #Sort the plot keys
        for plot in plotKeyList:                                                            #For each plot do the following
            if not newPlotDict.has_key(plot):
                newPlotDict.update({plot:{}})                                               #Add a new plot to the plot dictionbary
            for species in mySpList:                                                        #Initialize the variable sums by species with a zero 
                newPlotDict[plot].update({species:0})
            treeKeyList = treeDict[plot].keys()                                             #Get the tree id's for each plot 
            treeKeyList.sort()                                                              #Sort the id's
            for tree in treeKeyList:                                                        #For each tree in the tree list
                for i in range(0,spColCount,1):                                             #For each column in which species are listed
                    spColName = spColNamesList[i]                                           #identify the column name
                    spName = treeDict[plot][tree][spColName]                                #Identify the species name in that column name 
                    varColName = spVarValuesNamesList[i]                                    #Identify the corresponding column name with the variable values 
                    varValue = treeDict[plot][tree][varColName]                             #Identify the variable value
                    newPlotDict[plot][spName] = newPlotDict[plot][spName] + varValue        #Add the value associated with that species to the previous sum
        return newPlotKeyVarList, newPlotHeader, newPlotDict

    def CompilePerHectarePlotLevelStatisticsFromTreeLists(self, treeDict={}, spVarValuesNamesList = []):
        '''
        '''
        newPlotKeyVarList = ['PLOTID']
        newPlotHeader = ['PLOTID', 'SUM']
        newPlotDict = {}
        plotKeyList = treeDict.keys()                                                       #Get list of plot keys from treeDict
        plotKeyList.sort()                                                                  #Sort the plot keys
        for plot in plotKeyList:                                                            #For each plot do the following
            if not newPlotDict.has_key(plot):
                newPlotDict.update({plot:{'SUM':0}})
            treeKeyList = treeDict[plot].keys()                                             #Get the tree id's for each plot 
            treeKeyList.sort()                                                              #Sort the id's
            for tree in treeKeyList:                                                        #For each tree in the tree list
                for varColName in spVarValuesNamesList:
                    varValue = treeDict[plot][tree][varColName]
                    newPlotDict[plot]['SUM'] = newPlotDict[plot]['SUM'] + varValue
        return newPlotKeyVarList, newPlotHeader, newPlotDict

    def CompilePlotLevelSpeciesPercentages(self, plotDict = {},speciesList = []):
        '''
        '''
        newPlotKeyVarList = ['PLOTID']
        newPlotHeader = joinOneDListBToRightOfOneDListA(newPlotKeyVarList, speciesList)
        newPlotDict = {}
        for plot in plotDict:
            newPlotDict.update({plot:{}})
            totalSum = 0
            for species in speciesList:
                if plotDict[plot].has_key(species):
                    totalSum = totalSum + plotDict[plot][species]
            for species in speciesList:
                if plotDict[plot].has_key(species):
                    if totalSum > 0:
                        pcntVal = plotDict[plot][species]/float(totalSum)*100
                        newPlotDict[plot].update({species:pcntVal})
                    else:
                        newPlotDict[plot].update({species:0})
                else:
                    newPlotDict[plot].update({species:0})
        return newPlotDict

    def CompilePlotLevelSpeciesProportions(self, plotDict = {},plotDictKeyVarNameList = [], speciesList = [], spColNameList = [], spPcntNameList = []):
        '''
        '''
        newPlotHeader = joinOneDListBToRightOfOneDListA(plotDictKeyVarNameList, speciesList)
        if not 'NA' in newPlotHeader and not '' in newPlotHeader:
            newPlotHeader.append('NA')
        newPlotDict = {}
        nSpeciesCols = len(spColNameList)
        nSpPcntCols = len(spPcntNameList)
        if not nSpeciesCols == nSpPcntCols:
            print 'routineLviApplications.CompilePlotLevelSpeciesPercentages'
            print 'Number of columns containing species not equal to number of columns containing percentages'
            print 'Species Column Names:', spColNameList
            print 'Species Percent Column Names:', spPcntNameList
        for plot in plotDict:
            newPlotDict.update({plot:{}})
            spPcntSum = 0
            for species in speciesList:
                newPlotDict[plot].update({species:0})
            for spColNo in range(0,nSpeciesCols,1):
                spColName = spColNameList[spColNo]
                spPcntName = spPcntNameList[spColNo]
                species = plotDict[plot][spColName]
                spPcnt = plotDict[plot][spPcntName]
                if not spPcnt == '' and spPcnt > 0:
                    spPcntSum = spPcntSum + spPcnt
                if species in speciesList:
                    newPlotDict[plot][species] = newPlotDict[plot][species] + spPcnt
                else:
                    print 'routineLviApplications.CompilePlotLevelSpeciesProportions'
                    print 'Species:', species, 'not found in list:', speciesList
            if spPcntSum <= 0:
                if 'NA' in newPlotHeader:
                    newPlotDict[plot]['NA'] = float(1)
                else:
                    if '' in newPlotHeader:
                        newPlotDict[plot][''] = float(1)
            else:
                for species in speciesList:
                    newPlotDict[plot][species] = newPlotDict[plot][species]/float(spPcntSum)
        return newPlotHeader, newPlotDict

    def DeepCopyList(self, dataList = []):
        newList = deepcopy(dataList)
        return newList

    def InnerJoinDictAAndDictBAndExtractVariableSubset(self, dataDictA = {}, dataKeyVarNames = [], dataDictB = {}, extractVarNameList = []):
        '''
        This function allows different combinations of variables to be extracted from the originalDataDict and a dataDictB on the basis
        that they have the same key structure and contain the same key variable values.  The keyVariableNames are listed in the dataKeyVarNames.
        It allows the user to extract a new variable subset (extractVarNameList) from the dataDictA or derrivativeDict in that order of priority.  The output
        data may or may not include the original key variables (listed in dataKeyVarNames) and it may consist of a new set of key variable names.
        The output is in a list format that may then be converted back into dictionary format if so desired.

        The only constraint of this routine is that only thos key variable sets and values contained in dataKeyVarNames that are held in common
        amongst the dataDictA and the dataDictB are included in the output.  Aka this accomplishes an inner join of two dataets
        with some combinations of keys held in common and the subselection of selected variables listed in extractVarNameList
        that may be contained in the originDataDict (first priority) or the dataDictB (second priority) or failing that set equal
        to '' if not found in either of the other two datasets (third priority).
        
        Inputs
            dataDictA           The original data dictionary containing data that is structured according dataKeyVarNames
            dataKeyVarNames     The list of key variable names used to structure both the originaDataDict and the dictionary derived from it (dataDictB)
            dataDictB           A dictionary structured in the same way with the same keys as the dataDictA perhaps with some of the same variables
            extractVarNameList  A list of new variables that include the key variables (that may be the same as the dataKeyVarNames) plus any other variables to
                                 be included in a new dataFile that is to be extracted from the originalDataDict or the dataDictB in that order of priority.

        Outputs
            newDataList         The variables listed in the extractVarNameList extracted in order based on the dataKeyVarNames,
                                from the dataDictA, or if not in the dataDictA then from dataDictB, or if
                                not in either dictionary then entered as a ''. 
        
        Warning: This routine is currently limited to dealing with 0 to 3 levels of nested key variables. It could be further
        extended to deal with deeper levels of nesting based on more key variables.

        This function extended from previous data dictionary manipulation functions. It is an improvement over previous inner-join routines to allow
        for extraction of variable subsets across datasets as well as the felxibility and includes the option to also extract new or old key variables
        sets.  Also by providing the output in list format the user has the option of continueing with a list or converting the new
        dataset into a new dictionary in subsequent processing offering more flexibility in application.
        
        Ian Moss
        July 9 2013
        
        '''  
       
        
        #Initialize a new list with extractVarNameList as the first row
        newDataList = [extractVarNameList]
        nCurrentKeys = len(dataKeyVarNames)
        lineCount = 0
        if nCurrentKeys == 0:
            #One line Dict
            newDataList.append([])
            for newVar in extractVarNameList:
                if dataDictA.has_key(newVar):
                    newDataList[1].append(dataDictA[newVar])
                else:
                    if dataDictB.has_key(newVar):
                        newDataList[1].append(dataDictB[newVar])
                    else:
                        newDataList[1].append('')
            
        else:
            for keyVar0 in dataDictA:
                if dataDictB.has_key(keyVar0):
                    if nCurrentKeys == 1:
                        newDataList.append([])
                        lineCount = lineCount + 1
                        keyVarValueList = [keyVar0]
                        for newVar in extractVarNameList:
                            if newVar in dataKeyVarNames:
                                varValue = keyVarValueList[0]
                            else:
                                if dataDictA[keyVar0].has_key(newVar):
                                    varValue = dataDictA[keyVar0][newVar]
                                else:
                                    if dataDictB[keyVar0].has_key(newVar):
                                        varValue = dataDictB[keyVar0][newVar]
                                    else:
                                        varValue = ''
                            newDataList[lineCount].append(varValue)
                    else:
                        for keyVar1 in dataDictA[keyVar0]:
                            if dataDictB[keyVar0].has_key(keyVar1):
                                if nCurrentKeys == 2:
                                    newDataList.append([])
                                    lineCount = lineCount + 1
                                    keyVarValueList = [keyVar0, keyVar1]
                                    for newVar in extractVarNameList:
                                        if newVar in dataKeyVarNames:
                                            varIndex = dataKeyVarNames.index(newVar)
                                            varValue = keyVarValueList[varIndex]
                                        else:
                                            if dataDictA[keyVar0][keyVar1].has_key(newVar):
                                                varValue = dataDictA[keyVar0][keyVar1][newVar]
                                            else:
                                                if dataDictB[keyVar0][keyVar1].has_key(newVar):
                                                    varValue = dataDictB[keyVar0][keyVar1][newVar]
                                                else:
                                                    varValue = ''
                                    newDataList[lineCount].append(varValue)
                                else:
                                    for keyVar2 in dataDictA[keyVar0][keyVar1]:
                                        if dataDictB[keyVar0][keyVar1].has_key(keyVar2):
                                            if nCurrentKeys == 3:
                                                newDataList.append([])
                                                lineCount = lineCount + 1
                                                keyVarValueList = [keyVar0, keyVar1, keyVar2]
                                                for newVar in extractVarNameList:
                                                    if newVar in dataKeyVarNames:
                                                        varIndex = dataKeyVarNames.index(newVar)
                                                        varValue = keyVarValueList[varIndex]
                                                    else:
                                                        if dataDictA[keyVar0][keyVar1][keyVar2].has_key(newVar):
                                                            varValue = dataDictA[keyVar0][keyVar1][keyVar2][newVar]
                                                        else:
                                                            if dataDictB[keyVar0][keyVar1][keyVar2].has_key(newVar):
                                                                varValue = dataDictB[keyVar0][keyVar1][keyVar2][newVar]
                                                            else:
                                                                varValue = ''
                                                    newDataList[lineCount].append(varValue)
        return newDataList

    def compileSpeciesDominance(self, spPcntDict = {}, spList =[]):
        '''
        '''
        spDomKeyVarList = ['PLOTID']
        spDomHeader = ['PLOTID']
        nSpecies = len(spList)
        spDomDict = {}
        for i in range(0,nSpecies,1):
            spNo = 'SP'+ str(i+1)
            spDomHeader.append(spNo)
        for i in range(0,nSpecies,1):
            spPctNo = 'SP_PCT'+ str(i+1)
            spDomHeader.append(spPctNo)
        newPlotDict = {}
        plotKeyList = spPcntDict.keys()                                                       #Get list of plot keys from treeDict
        plotKeyList.sort()
        for plot in plotKeyList:
            plotSpPcntList = []
            spPcntTotal = 0
            if not spDomDict.has_key(plot):
                spDomDict.update({plot:{}})
            for i in range(0,nSpecies,1):
                plotSpPcntList.append(0)
            spKeyList = spPcntDict[plot].keys()
            for species in spKeyList:
                if not species in spList:
                    print 'routineLviApplications.compileSpeciesDominance'
                    print 'Species:', species, 'in plot:', plot, 'not already included in spList'
                    print 'Error in species dominance'
                spPcnt = spPcntDict[plot][species]
                spIndex = spList.index(species)
                plotSpPcntList[spIndex]=plotSpPcntList[spIndex]+spPcnt
                spPcntTotal = spPcntTotal + spPcnt
                #print plot, species, spPcnt, spPcntTotal
            #Ensure species percentages add up to 100 and are rounded to nearest integer
            newSpPctTotalDiff = 0
            newSpPctTotal = 0
            if spPcntTotal > 0:
                for i in range(0, nSpecies, 1):
                    spPcnt = round(plotSpPcntList[i]/float(spPcntTotal)*100,0)
                    plotSpPcntList[i]= spPcnt
                    newSpPctTotal = newSpPctTotal + spPcnt
                #Check for rounding errors such that species percentages no longer add up to 100
                newSpPcntTotalDiff = 100 - newSpPctTotal
            #Create new lists 
            newSpPcntList = deepcopy(plotSpPcntList)
            newSpList = deepcopy(spList)
            for i in range(0, nSpecies,1):
                maxPercent = max(newSpPcntList)
                spNo = 'SP'+ str(i+1)
                spPctNo = 'SP_PCT'+ str(i+1)
                if maxPercent <= 0:
                    newSpIndex = i
                    newSp = 'NA'
                    newSpPcnt = 0
                else:
                    newSpIndex = newSpPcntList.index(maxPercent)
                    newSp = newSpList[newSpIndex]
                    newSpPcnt = newSpPcntList[newSpIndex]
                    #Apply correction factor for rounding errors to dominant species
                    if i == 0:
                        newSpPcnt = newSpPcnt + newSpPcntTotalDiff
                    del newSpList[newSpIndex]
                    del newSpPcntList[newSpIndex]
                spDomDict[plot].update({spNo:newSp,spPctNo:newSpPcnt})
        return spDomKeyVarList,spDomHeader,spDomDict


    def CompilePlotQuadraticMeanTreeDiameters(self, plotBaphSumDict = {}, plotTphSumDict = {}):
        '''
        '''
        qmdDict = {}
        qmdDictKeyVarnameList = ['PLOTID']
        qmdHeader = ['PLOTID', 'DG']
        plotKeyValueList = plotBaphSumDict.keys()
        plotKeyValueList.sort()
        for plot in plotKeyValueList:
            baph = plotBaphSumDict[plot]['SUM']
            sph = plotTphSumDict[plot]['SUM']
            if sph == 0:
                qmd = 0.0
            else:
                qmd = 200 *((baph/float(sph))*(1/numpy.pi))**0.5
            qmdDict.update({plot:{'DG':qmd}})
        return qmdDictKeyVarnameList, qmdHeader, qmdDict

    def CompileSpeciesPlotStatisticsIntoOneDictionary(self, plotSpDict = {}, plotSpDictAdd={}, plotSpHeader = [], plotSpKeyVarNameList=['PLOTID'], \
                                                      newSpList = [], attributeLabel = ''):
        '''
        '''
        plotSpKeyVarName = plotSpKeyVarNameList[0]
        #Check to make sure key variable name is in header
        if not plotSpKeyVarName in plotSpHeader:
            plotSpHeader.append(plotSpKeyVarName)
        #Add new variable names to plotSpHeader by combining species name with attributeLabel
        for sp in newSpList:
            newName = sp + '_' + attributeLabel
            if not newName in plotSpHeader:
                plotSpHeader.append(newName)
        #Initialize plotKeyValueList
        plotList = plotSpDictAdd.keys()
        plotList.sort()
        for plot in plotList:
            #Add plotid to plotSpDict if not already in dictionary
            if not plotSpDict.has_key(plot):
                plotSpDict.update({plot:{}})
            #For each species in the newSpList add the name and value associated with each plot to plotSpDict
            for sp in newSpList:
                newName = sp + '_' + attributeLabel
                if not plotSpDictAdd[plot].has_key(newName):
                    if plotSpDictAdd[plot].has_key(sp):
                        newValue = plotSpDictAdd[plot][sp]
                    else:
                        newValue = 0.0
                    plotSpDict[plot].update({newName:newValue})
        #Cross check plotSpDict to make sure variable names and values have been assigned
        origPlotList = plotSpDict.keys()
        origPlotList.sort()
        for plot in origPlotList:
            if not plot in plotList:
                for sp in newSpList:
                    newName = sp + '_' + attributeLabel
                    plotSpDict[plot].update({newName:0})
        return plotSpHeader, plotSpDict


    def CombinePlotSumDictionariesIntoOne(self, plotSumDict = {}, plotSumHeader = [], plotSumDictAdd = {}, plotSumKeyVarNameList = ['PLOTID'], plotSumAddVarName = 'SUM', \
                                          newPlotSumVarName = ''):
        '''
        '''
        plotSumKeyVarName = plotSumKeyVarNameList[0]
        if not plotSumKeyVarName in plotSumHeader:
            plotSumHeader.append(plotSumKeyVarName)
        if not newPlotSumVarName in plotSumHeader:
            plotSumHeader.append(newPlotSumVarName)
        plotList = plotSumDictAdd.keys()
        plotList.sort()
        for plot in plotList:
            if not plotSumDict.has_key(plot):
                plotSumDict.update({plot:{}})
            newVarValue = plotSumDictAdd[plot][plotSumAddVarName]
            if not plotSumDict[plot].has_key(newPlotSumVarName):
                plotSumDict[plot].update({newPlotSumVarName: newVarValue})
        #Cross check plotSpDict to make sure variable names and values have been assigned
        origPlotList = plotSumDict.keys()
        origPlotList.sort()
        for plot in origPlotList:
            if not plot in plotList:
               plotSumDict[plot].update({newPlotSumVarName:0})
        return plotSumHeader, plotSumDict


    def SubstituteNewPspSpeciesForOldPspSpeciesNames(self, x=[]):
        '''
        Note that the tree dictionary contains a unique ID for each plot and has a list of
        trees as secondary keys.
        '''
        return
               
    def calculateLorenzIndices(self, linkDict = {}, treeDict = {}, rankVarName = '', countVarName = '', sizeVarName = ''):
        '''
        '''
            
        return
                    
    def CompileCumulativeDistributions(self, xVarName = '', minXVar = 0, maxXVar = 140, yVarName = '', yVarNameNew = '', \
                                       plotTreeDict = {},cumDistDict = {}, cumDistHeader = ['PLOTID']):
        '''
        '''
        xVarValueList = []
        #Update cumDistHeader with new variable set
        #Initialize xVarValueList
        minXVar = int(minXVar)
        maxXVar = int(round(maxXVar,0))
        #Create variable names incremented between minVar and maxVar
        for i in range(minXVar, maxXVar, 1):
            newVarName = yVarNameNew + str(i)
            if not newVarName in cumDistHeader:
                cumDistHeader.append(newVarName)
                xVarValueList.append(i)
        #print xVarValueList
        lenXVarList = len(xVarValueList)
        plotList = plotTreeDict.keys()
        plotList.sort()
        for plot in plotList:
            if not cumDistDict.has_key(plot):
                cumDistDict.update({plot:{}})
            treeList = plotTreeDict[plot].keys()
            treeList.sort()
            sumYVar = 0
            #Initialize yVarValueList
            yVarValueList = []
            for i in range(0, lenXVarList, 1):
                yVarValueList.append(0)
            for tree in treeList:
                xVarValue = plotTreeDict[plot][tree][xVarName]
                yVarValue = plotTreeDict[plot][tree][yVarName]
                #Get the sum of yVarValue
                #print plot, tree,xVarName, yVarName, xVarValue, yVarValue, sumYVar
                if xVarValue >= minXVar:
                    sumYVar = sumYVar + yVarValue
                    if xVarValue < maxXVar:
                        xVarIndex = bisect.bisect_right(xVarValueList, xVarValue)
                    else:
                        xVarIndex = lenXVarList-1
                    #print xVarValue, xVarValueList[xVarIndex]
                    for i in range(0, xVarIndex, 1):
                        #Construct a cumulative distribution
                        yVarValueList[i] = yVarValueList[i] + yVarValue
            #Convert the yVarCumulative Distribution to proportions
            #print plot, 'sum', sumYVar
            for i in range(0, lenXVarList,1):
                if not sumYVar == 0:
                    yVarValue = yVarValueList[i]/float(sumYVar)
                    yVarValueList[i] = yVarValue
                else:
                    yVarValueList[i] = 0
            #Add cumulative distribution to dictionary
            for i in range(0,lenXVarList,1):
                refNo = minXVar + i
                newVarName = yVarNameNew + str(refNo)
                yVarValue = yVarValueList[i]
                cumDistDict[plot].update({newVarName:yVarValue})
                #print plot, newVarName, refNo, yVarValue
        return cumDistHeader, cumDistDict

    def compileAttributeRanks(self, dataDict = {}, rankVarName = '', rankDict = {}, rankHeader = [], rankKeyVarNameList = ['RAVARNAME','RVARVALUE']):
        '''
        '''
        if rankHeader == []:
            rankHeader = joinOneDListBToRightOfOneDListA(rankHeader, rankKeyVarNameList)
            rankHeader = joinOneDListBToRightOfOneDListA(rankHeader, ['N', 'R', 'PR'])
        rankDict.update({rankVarName:{}})
        for plot in dataDict:
            rankVarValue = dataDict[plot][rankVarName]
            if not rankDict[rankVarName].has_key(rankVarValue):
                rankDict[rankVarName].update({rankVarValue:{'N':0,'R':0,'PR':0}})
            rankDict[rankVarName][rankVarValue]['N'] = rankDict[rankVarName][rankVarValue]['N'] + 1
        varValueList = rankDict[rankVarName].keys()
        varValueList.sort()
        if not 0 in varValueList:
            varValueList.insert(0,0)
            rankDict[rankVarName].update({0:{'N':0,'R':0,'PR':0}})
        rankList = [0]
        rank = 0
        for varValue in varValueList:
            if varValue == 0:
                rankList.append(rank)
                n = rankDict[rankVarName][0]['N']
                rankDict[rankVarName][varValue]['R'] = 0
                rank = rank + n
            else:
                n = rankDict[rankVarName][varValue]['N']
                rank = rank + n
                if n == 1:
                    rankList.append(rank)
                    rankDict[rankVarName][varValue]['R'] = rank
                else:
                    tempRank = rank - n/float(2)
                    rankList.append(tempRank)
                    rankDict[rankVarName][varValue]['R'] = tempRank
        for varValue in varValueList:
            propRank = rankDict[rankVarName][varValue]['R'] / float(rank)
            rankDict[rankVarName][varValue]['PR'] = propRank
        return rankKeyVarNameList, rankHeader, rankDict

    def rankAdjustCumulativeDistributions(self, plotSumDict={}, rankDict={}, cumDistDict={}, minXVar=0, maxXVar=0, \
                                          adjCumDistDict = {}, adjCumDistHeader = ['PLOTID']):
        '''
        '''
        varAdjustNameList = rankDict.keys()
        plotKeyList = plotSumDict.keys()
        plotKeyList.sort()
        #Check to make sure cumDistDict has the same key set
        plotKeyFlag = True
        for plot in plotKeyList:
            if not cumDistDict.has_key(plot):
                plotKeyFlag = False
        if plotKeyFlag == False:
            print 'routineLviApplications.rankAdjustCumulativeDistributions'
            print 'plotSumDict key set does not match with those in cumDistDict'
        minXVar = int(minXVar)
        maxXVar = int(round(maxXVar,0))
        for yVar in varAdjustNameList:
            for i in range(minXVar, maxXVar):
                xVarName = yVar + str(i)
                if not xVarName in adjCumDistHeader:
                    adjCumDistHeader.append(xVarName)
            yVarList = rankDict[yVar].keys()
            yVarList.sort()
            minYVar = min(yVarList)
            maxYVar = max(yVarList)
            #print yVar, minYVar, maxYVar
            for plot in plotKeyList:
                if not adjCumDistDict.has_key(plot):
                    adjCumDistDict.update({plot:{}})
                yVarValue = plotSumDict[plot][yVar]
                if yVarValue <= minYVar:
                    yVarPRank = rankDict[yVar][minYVar]['PR']
                else:
                    if yVarValue >= maxYVar:
                        yVarPRank = rankDict[yVar][maxYVar]['PR']
                    else:
                        ulYVarIndex = bisect.bisect_right(yVarList, yVarValue)
                        ulYVar = yVarList[ulYVarIndex]
                        ulPRank = rankDict[yVar][ulYVar]['PR']
                        llYVar = yVarList[ulYVarIndex-1]
                        llPRank = rankDict[yVar][llYVar]['PR']
                        yVarPRank = llPRank + (ulPRank- llPRank)/float(ulYVar-llYVar)*(yVarValue-llYVar)
                for i in range(minXVar, maxXVar):
                    xVarName = yVar + str(i)
                    adjYVarValue = cumDistDict[plot][xVarName]* yVarPRank
                    adjCumDistDict[plot].update({xVarName:adjYVarValue})
        return adjCumDistHeader, adjCumDistDict

    def CalculateQmdBphSphForPlotTreeDict(self, treeDict = {}, treeDbhName = '', treeSphName = '', minDbhThreshold = 0):
        '''
        '''
        plotList = treeDict.keys()
        newPlotDict = {}
        newPlotHeader = ['PLOTID','BPH','TPH','QMD','MINDBH','NTPP']
        for plot in plotList:
            treeList = treeDict[plot].keys()
            totalBph = 0
            totalSph = 0
            nTrees = 0
            for tree in treeList:
                dbh = treeDict[plot][tree][treeDbhName]
                if dbh >= minDbhThreshold:
                    nTrees = nTrees + 1
                    sph = treeDict[plot][tree][treeSphName]
                    bpt = CalculateBpt(dbh)
                    bph = bpt*sph
                    totalBph = totalBph + bph
                    totalSph = totalSph + sph
            qmd = CalculateQmd(totalBph, totalSph)
            newPlotDict.update({plot:{'BPH':bph,'TPH':sph,'QMD':qmd, 'MINDBH':minDbhThreshold, 'NTPP':nTrees}})
        return newPlotHeader, newPlotDict

    def CalculateLoreysMeanTreeHeight(self, treeDict = {}, treeDbhName = '', treeSphName = '', treeHeightName = '', minDbhThreshold = 0):
        '''
        '''
        plotList = treeDict.keys()
        newPlotDict = {}
        newPlotHeader = ['PLOTID','BPH','TPH','HL','MINDBH','NTPP']
        for plot in plotList:
            treeList = treeDict[plot].keys()
            totalBph = 0
            totalSph = 0
            totalLorHeight = 0
            nTrees = 0
            for tree in treeList:
                dbh = treeDict[plot][tree][treeDbhName]
                if dbh >= minDbhThreshold:
                    nTrees = nTrees + 1
                    sph = treeDict[plot][tree][treeSphName]
                    treeHeight = treeDict[plot][tree][treeHeightName]
                    bpt = CalculateBpt(dbh)
                    bph = bpt*sph
                    totalBph = totalBph + bph
                    totalSph = totalSph + sph
                    totalLorHeight = totalLorHeight + bph*treeHeight
            if totalBph > 0:
                hl = totalLorHeight/float(totalBph)
            else:
                hl = 0
            newPlotDict.update({plot:{'BPH':bph,'TPH':sph,'HL':hl, 'MINDBH':minDbhThreshold, 'NTPP':nTrees}})
        return newPlotHeader, newPlotDict

    def CompileNewTreeDictToDbhThreshold(self, treeDict = {}, treeKeyVarNames = [], treeSpeciesName = 'SP', treeDbhName = 'DBH', \
                                         treeSphName = 'TPH', treeRDbhName = 'RDBH', treeBphName = 'BPH', \
                                         minDbhThreshold = 0, treeHeightName = 'NULL', treeGvolName = 'NULL', \
                                         treeMvolName = 'NULL'):
        '''
        Altered July 4 2013
        Manditory inputs
            treeDict
            treeKeyVarNames:    the names of the fields consisting (1) plotid's and (2) treeid's
            treeSpeciesName:    the name of the field containing tree species
            treeDbhName:        the name of the field containing tree dbh
            treeSphName:        the name of the field containing the numbers of stems per hectare
            treeBphName:        the name of the field to be assigned to the calculated basal area per hectare for each tree
            treeRDbhName:       the name of the filed to be assigned a calculated relative dbh (tree dbh minus quadratic mean tree diameter
            minDbhThreshold:    the minimum tree dbh to be included in the tree dataset

        Optional inputs (set = to 'NULL' if the filed is to be EXCLUDED from the tree dictionary for calculation purposes
            treeHeightVarName:  the name of the field that contains tree height
            treeGvolName:       the name of the field that contains gross tree volume per unit area
            treeMvolName:       the name of the field that contains merchantable tree volume per unit area
        '''
        plotList = treeDict.keys()
        minRDbh = 0
        maxRDbh = 0
        newTreeHeader = joinOneDListBToRightOfOneDListA(treeKeyVarNames,[treeSpeciesName, treeDbhName,treeRDbhName,treeSphName,treeBphName])
        if not treeHeightName == 'NULL':
            newTreeHeader = joinOneDListBToRightOfOneDListA(newTreeHeader,[treeHeightName])
        if not treeGvolName == 'NULL':
            newTreeHeader = joinOneDListBToRightOfOneDListA(newTreeHeader,[treeGvolName])
        if not treeMvolName == 'NULL':
            newTreeHeader = joinOneDListBToRightOfOneDListA(newTreeHeader,[treeMvolName])
        newTreeDict = {}
        for plot in plotList:
            plotHeader, plotDict = CalculateQmdBphSphForPlotTreeDict({plot:treeDict[plot]}, treeDbhName, treeSphName, minDbhThreshold)
            treeList = treeDict[plot].keys()
            qmd = plotDict[plot]['QMD']
            rDbhList  = []
            for tree in treeList:
                dbh = treeDict[plot][tree][treeDbhName]
                if dbh >= minDbhThreshold:
                    if not newTreeDict.has_key(plot):
                        newTreeDict.update({plot:{}})
                    rDbh = treeDict[plot][tree][treeDbhName]-qmd
                    #if plot == 31:
                    #     print plot, tree, dbh, rDbh, qmd
                    sph = treeDict[plot][tree][treeSphName]
                    bph = CalculateBpt(dbh)*sph
                    species = treeDict[plot][tree][treeSpeciesName]                                                                                                       
                    newTreeDict[plot].update({tree:{treeSpeciesName:species, treeDbhName:dbh,treeRDbhName:rDbh,treeSphName:sph,treeBphName:bph}})
                    if rDbh < minRDbh:
                        minRDbh = rDbh
                    if rDbh > maxRDbh:
                        maxRDbh = rDbh
                    rDbhList.append(rDbh)
                    if not treeHeightName == 'NULL':
                        ht = treeDict[plot][tree][treeHeightName]
                        newTreeDict[plot][tree].update({treeHeightName:ht})
                    if not treeGvolName == 'NULL':
                        gvol = treeDict[plot][tree][treeGvolName]
                        newTreeDict[plot][tree].update({treeGvolName:gvol})
                    if not treeMvolName == 'NULL':
                        mvol = treeDict[plot][tree][treeMvolName]
                        newTreeDict[plot][tree].update({treeMvolName:mvol})
            #meanRDbh = numpy.mean(rDbhList)
            #sdevRDbh = numpy.std(rDbhList)
            #print meanRDbh, sdevRDbh
        minRDbh = int(minRDbh)
        maxRDbh = int(round(maxRDbh,0))+1
        return newTreeDict, newTreeHeader, minRDbh, maxRDbh
             

    def CalculateBpt(self, treeDbh = 0):
        '''
        '''
        bpt = numpy.pi* (treeDbh/float(200))**2
        return bpt


    def CalculateQmd(self, bph = 0, sph = 0):
        '''
        '''
        qmd = 0
        if sph > 0:
            qmd = 200*((bph/float(sph))*(1/numpy.pi))**0.5
        return qmd

    def CompileLorenzStatistics(self, plotTreeDict = {}, dbhVarname = '', sphVarname = '', bphVarname = '', dbhInterval = 1, maxDbh=140):
        '''
        '''
        #Establish maxDbh  as an integer - this should be as large or larger than the largest tree in the dataset
        #This is used for cdi calculation
        maxDbh = int(round(maxDbh+0.5,0))
        #Initialize lorenz / gini coefficient file
        lorenzKeyVarnameList = ['PLOTID']
        lorenzHeader = ['PLOTID','LORAREA', 'LORMAX', 'GINI', 'CDI', 'NTPP']
        lorenzDict = {}
        #Initialize lorenz distribution file
        lorenzCurveHeader = ['PLOTID']
        lorenzPsphList = []
        lorenzCurveDict = {}
        #Establish standard intervals for lorenz distributions 
        for i in range(0,105,5):
            interval = i /float(100)
            lorenzPsphList.append(interval)
            lorenzCurveVarName = 'L' + str(i)
            lorenzCurveHeader.append(lorenzCurveVarName)
        #Start processing
        plotList = plotTreeDict.keys()
        plotList.sort()
        for plot in plotList:
            treeList = plotTreeDict[plot].keys()
            treeList.sort()
            dbhList = []
            sphList = []
            bphList = []
            sphDbhList = []
            for tree in treeList:
                dbh = plotTreeDict[plot][tree][dbhVarname]
                sph = plotTreeDict[plot][tree][sphVarname]
                bph = plotTreeDict[plot][tree][bphVarname]
                sphDbh = sph*dbh
                dbhList.append(dbh)
                sphList.append(sph)
                bphList.append(bph)
                sphDbhList.append(sphDbh)
            sphSortList = []
            bphSortList = []
            dbhSortList = deepcopy(dbhList)
            dbhSortList.sort()
            dbhSortList.reverse()                               #Dbh sort list large to small
            for dbh in dbhSortList:
                colIndex = dbhList.index(dbh)
                sph = sphList[colIndex]
                bph = bphList[colIndex]
                sphSortList.append(sph)                         #sph sort list given dbh sort list
                bphSortList.append(bph)                         #bph sort list given dbh sort list
            sphSum = sum(sphSortList)                           #Total stems per hectare
            bphSum = sum(bphSortList)                           #Total basal area
            nTrees = len(dbhSortList)                           #Number of trees
            if nTrees > 0:
                meanDbh = sum(sphDbhList)/float(sphSum)             #Mean tree dbh
            else:
                meanDbh = 0
            cumSphList = []
            cumBphList = []
            for i in range(0,nTrees,1):
                if i == 0:
                    sph = sphSortList[i]                        
                    bph = bphSortList[i]                        
                else:
                    sph = sphSortList[i] + cumSphList[i-1]
                    bph = bphSortList[i] + cumBphList[i-1]
                cumSphList.append(sph)                          #Cumulative sph distribution
                cumBphList.append(bph)                          #Cumulative bph distribution
            cumSphPropList = []
            cumBphPropList = []
            cumDiffPropList = []
            cumArea = 0
            maxCumDiff = 0
            gini = 0
            cdi = 0
            if nTrees > 0:
                #Compute Lorenz statistics
                for i in range(0, nTrees, 1):
                    #Covert cumulative distributions to proportions
                    if sphSum > 0:
                        cumSphPropList.append(cumSphList[i]/float(sphSum))  #Cumulation proportion of sph distribution
                    else:
                        cumSphPropList.append(0.0)
                    if bphSum > 0:
                        cumBphPropList.append(cumBphList[i]/float(bphSum))  #Cumulation proportion of bph distribution
                    else:
                        cumBphPropList.append(0.0)
                #Calculate differences between cumulative distributions in bph vs. sph 
                for i in range(0, nTrees, 1):
                    cumDiffPropList.append(cumBphPropList[i]-cumSphPropList[i])         #Cumuulative diff (propBph - propSph) distribution
                #Compute maximum cumulative distirbutions
                maxCumDiff = max(cumDiffPropList)                                       #Lorenz maximum difference
                for i in range(0, nTrees, 1):
                    if i == 0:
                        cumArea = cumArea + cumDiffPropList[i]/2 * cumSphPropList[i]    #Lorenz area
                    else:
                        cumArea = cumArea + (cumDiffPropList[i]+cumDiffPropList[i-1])/2 * (cumSphPropList[i]- cumSphPropList[i-1])
                cumArea = cumArea * 2
                #Compute CDI in 1 cm intervals
                cdi = 0
                for i in range(0,maxDbh,dbhInterval):
                    dbh = maxDbh - i
                    cumDiff = 0
                    for j in range(0,nTrees,1):
                        if dbhSortList[j] >= dbh:
                            cumDiff = cumDiffPropList[j]
                    cdi = cdi + cumDiff
                #Normalize CDI between 0 and 1
                cdi = 2*cdi*dbhInterval/float(maxDbh)
                #Comupute gini coefficient
                dbhDiff = 0
                if meanDbh > 0 and nTrees > 1:
                    for i in range(0, nTrees, 1):
                        iDbh = dbhSortList[i]
                        iSph = sphSortList[i]
                        for j in range(0, nTrees, 1):
                            jDbh = dbhSortList[j]
                            jSph = sphSortList[j]
                            dbhDiff = dbhDiff + abs(iDbh-jDbh)*(iSph*jSph)
                    gini = dbhDiff/(float(sphSum*(sphSum-1)*meanDbh)*2)                         #Calculate gini coefficient
                else:
                    gini = 0
            if not lorenzDict.has_key(plot):
                lorenzDict.update({plot:{'LORAREA':cumArea,'LORMAX':maxCumDiff,'GINI':gini, 'CDI':cdi,'NTPP':nTrees}})
                #Construct lorenz distributions
                minCumPsph = min(cumSphPropList)
                maxCumPsph = max(cumSphPropList)
                minCumPbph = min(cumBphPropList)
                maxCumPbph = max(cumBphPropList)
                lorenzCurveDict.update({plot:{}})
                for i in range (0,105,5):
                    interval = i /float(100)
                    varName = 'L' + str(i)
                    if i == 0 or i == 100 or maxCumPsph <= 0:
                        lorenzCurveDict[plot].update({varName:interval})
                    else:
                        if interval > maxCumPsph:
                            ulNumerator = 1
                            ulDenominator = 1
                            llNumerator = maxCumPbph
                            llDenominator = maxCumPsph
                        else:
                            if interval < minCumPsph:
                                ulNumerator = maxCumPbph
                                ulDenominator = maxCumPsph
                                llNumerator = 0
                                llDenominator = 0
                            else:
                                ulIndex = bisect.bisect_right(cumSphPropList, interval)
                                llIndex = ulIndex - 1
                                ulNumerator = cumBphPropList[ulIndex] 
                                ulDenominator = cumSphPropList[ulIndex]
                                llNumerator = cumBphPropList[llIndex] 
                                llDenominator = cumSphPropList[llIndex]
                        newProp = ((ulNumerator-llNumerator)/(ulDenominator - llDenominator))*(interval-llDenominator) + llNumerator
                        lorenzCurveDict[plot].update({varName:newProp})                   
        return lorenzKeyVarnameList, lorenzHeader, lorenzDict, lorenzCurveHeader, lorenzCurveDict 

    def calculateUnivariateSTVI(self, plotTreeDict = {}, dbhVarname = '', sphVarname = '', bphVarname = '', maxDbh = 140):
        '''
        '''
        stviHeader = ['PLOTID','STVI']
        stviKeyVarnameList = ['PLOTID']
        stviDict = {}
        plotList = plotTreeDict.keys()
        plotList.sort()
        Su = (maxDbh**2)/float(12)
        mStat = (maxDbh**2)/float(4)
        mStatSu = 1.1281*mStat-Su
        stvi = -1
        for plot in plotList:
            treeList = plotTreeDict[plot].keys()
            treeList.sort()
            #calculateBph and meanDbh
            sumDbhSph = 0
            sumBph = 0
            sumSph = 0
            for tree in treeList:
                dbh = plotTreeDict[plot][tree][dbhVarname]
                sph = plotTreeDict[plot][tree][sphVarname]
                sumDbhSph = sumDbhSph + dbh*sph
                sumSph = sumSph + sph
                bph = plotTreeDict[plot][tree][bphVarname]
                sumBph = sumBph + bph
            meanDbh = sumDbhSph/float(sumSph)
            sumSdbhk = 0
            for tree in treeList:
                dbh = plotTreeDict[plot][tree][dbhVarname]
                bph = plotTreeDict[plot][tree][bphVarname]
                Sdbhk = bph*((dbh-meanDbh)**2)
                sumSdbhk = sumSdbhk + Sdbhk
            Sdbhk = sumSdbhk/float(sumBph)
            if Sdbhk <= Su:
                stvi = 1-(((Su-Sdbhk)/float(Su))**2.4094)
            else:
                stvi = 1-(((Sdbhk-Su)/float(mStatSu))**0.5993)
            if stvi < 0:
                stvi = float(0)
            if stvi > 1:
                stvi = float(1)
            stviDict.update({plot:{'STVI':stvi}})
        return stviKeyVarnameList, stviHeader, stviDict 
                
        

    def ComputeNaturalLogarithMicTranformations(self, plotSumDict, plotSumHeader, preTransformVarNameList, postTransformVarNameList):
        '''
        '''
        plotList = plotSumDict.keys()
        plotList.sort()
        varnameCount = len(preTransformVarNameList)
        for newVarName in postTransformVarNameList:
            plotSumHeader.append(newVarName)
        for plot in plotList:
            for varNo in range(0,varnameCount,1):
                origVarName = preTransformVarNameList[varNo]
                newVarName = postTransformVarNameList[varNo]
                varValue = plotSumDict[plot][origVarName]
                if varValue > 0:
                    lnVarValue = numpy.log(varValue)
                else:
                    lnVarValue = 0
                plotSumDict[plot].update({newVarName:lnVarValue})
        return plotSumHeader, plotSumDict

    def innerJoinTwoDictWithSameKeysDifferentVariables(self, parentDict = {}, parentHeader = [], childDict = {}, childHeader = [], keyVarNameList =[]):
        '''
        '''
        innerJoinHeader = innerJoinDictDBs.createUniqueListFromTwoNewLists(parentHeader, childHeader)
        parentKeys = innerJoinDictDBs.getDictKeySetValuesList(parentDict, keyVarNameList)
        childKeys = innerJoinDictDBs.getDictKeySetValuesList(childDict, keyVarNameList)
        commonKeys = innerJoinDictDBs.getCommonInnerJoinKeyValueList(parentKeys, childKeys)
        innerJoinDict = innerJoinDictDBs.extractDictDBForKeySetsList(parentDict,childDict,commonKeys)       
        return innerJoinHeader, innerJoinDict

    def RemovePlotsBelowMinimumAndAboveMaximumCriteria(self, plotDict = {}, linkDict = {},  criteriaVarName = '', minCriteria = 0, maxCriteria = 10000000):
        '''
        '''
        plotList = plotDict.keys()
        plotList.sort()
        for plot in plotList:
            if plotDict[plot].has_key(criteriaVarName):
                if plotDict[plot][criteriaVarName] < minCriteria or plotDict[plot][criteriaVarName] > maxCriteria:
                    del plotDict[plot]
                    del linkDict[plot]
        return plotDict, linkDict

    def SelectCumulativeDistributionsUsingLinkDict(self, parentDict={}, selectKeysDict={}, keyVarnameList = []):
        '''
        '''
        distinctKeyValueSetList = innerJoinDictDBs.getDictKeySetValuesList(selectKeysDict, keyVarnameList)
        newDict = innerJoinDictDBs.selectRowsInKeySetsList(parentDict,distinctKeyValueSetList)
        return newDict

    def CompileAviSiteIndices(self, dataDict = {}, speciesCol = 'SPECIES', bhageCol = 'AGE', totalAgeCol = 'NULL', \
                              treeHeightCol = 'HT_MEAS', treeMeasDateCol = 'MEASDATE', measDateFormat = 'dd/mm/yyyy'):
        '''
        '''
        siDict = {}
        siDictHeader = ['SIID','SPECIES','BHAGE','TAGE', 'HT','SI','DAY','MONTH','YEAR']
        siDictKeyVarNameList = ['SIID']
        if bhageCol == 'NULL' and totalAgeCol == 'NULL':
            print 'routineLviApplications.CompileAviSiteIndices'
            print 'bhageCol and totalAgeCol both indicated as NULL'
            print 'Only one of these columns can be indicated as NULL in order to calculate site index'
        keyList = dataDict.keys()
        keyList.sort()
        for keyValue in keyList:
            species = dataDict[keyValue][speciesCol]
            treeHeight = dataDict[keyValue][treeHeightCol]
            if bhageCol == 'NULL':
                bhage, totalAge = ComputeAviBhageFromTotalAge(species, dataDict[keyValue][totalAgeCol], 0)
            else:
                bhage, totalAge = ComputeAviBhageFromTotalAge(species, 0, dataDict[keyValue][bhageCol])
            measDate = dataDict[keyValue][treeMeasDateCol]
            day, month, year = RecoverYearMonthAndDay(measDate, measDateFormat)
            siteIndex = ComputeAviSiteIndex(species, bhage, treeHeight)
            #print keyValue, species, bhage, totalAge, treeHeight, siteIndex
            siDict.update({keyValue:{'SPECIES':species,'BHAGE':bhage,'TAGE':totalAge,'HT':treeHeight,'SI':siteIndex,'DAY':day,'MONTH':month,'YEAR':year}})
        return siDictKeyVarNameList, siDictHeader, siDict


    def CompileAviSiteIndices_v2(self, dataDict = {}, speciesCol = 'SPECIES', bhageCol = 'AGE', totalAgeCol = 'NULL', \
                              treeHeightCol = 'HT_MEAS', year = 2011):
        '''
        '''
        siDict = {}
        siDictHeader = ['SIID','SPECIES','BHAGE','TAGE', 'HT','SI','YEAR']
        siDictKeyVarNameList = ['SIID']
        if bhageCol == 'NULL' and totalAgeCol == 'NULL':
            print 'routineLviApplications.CompileAviSiteIndices'
            print 'bhageCol and totalAgeCol both indicated as NULL'
            print 'Only one of these columns can be indicated as NULL in order to calculate site index'
        keyList = dataDict.keys()
        keyList.sort()
        for keyValue in keyList:
            species = dataDict[keyValue][speciesCol]
            treeHeight = dataDict[keyValue][treeHeightCol]
            if bhageCol == 'NULL':
                bhage, totalAge = ComputeAviBhageFromTotalAge(species, dataDict[keyValue][totalAgeCol], 0)
            else:
                bhage, totalAge = ComputeAviBhageFromTotalAge(species, 0, dataDict[keyValue][bhageCol])
            siteIndex = ComputeAviSiteIndex(species, bhage, treeHeight)
            #print keyValue, species, bhage, totalAge, treeHeight, siteIndex
            siDict.update({keyValue:{'SPECIES':species,'BHAGE':bhage,'TAGE':totalAge,'HT':treeHeight,'SI':siteIndex,'YEAR':year}})
        return siDictKeyVarNameList, siDictHeader, siDict


    def RecoverYearMonthAndDay(self, measDate = '', measDateFormat = 'dd/mm/yyyy'):
        '''
        '''
        day = 0
        month = 0
        year = 0
        
        measDateFormatList = measDateFormat.split('/')
        measDateList = measDate.split('/')
        end_i = len(measDateFormatList)
        end_j = len(measDateList)
        if not end_i == end_j:
            print 'routineLviApplications.RecoverYearMonthDay'
            print 'measDateFormat:', measDateFormat, 'not compaible with measDate:', measDate
        for i in range(0, end_i, 1):
            measDateAttribute = measDateFormatList[i]
            if i < end_j:
                measDateValue = measDateList[i]
            else:
                measDateValue = 0
            if measDateAttribute == 'dd' and measDateValue > 0:
                day = int(measDateValue)
            if measDateAttribute == 'mm' and measDateValue > 0:
                month = int(measDateValue)
            if measDateAttribute == 'yyyy' and measDateValue > 0:
                year = int(measDateValue)
        return day, month, year

    def ProjectHeightAndAgeGivenSiteIndices(self, siDict ={},siDictHeader=[],  \
                                            speciesColName = 'SPECIES', \
                                            bhageColName = 'BHAGE', totalAgeColName = 'TAGE', heightColName = 'HT', \
                                            siColName = 'SI', monthColName = 'MONTH', yearColName = 'YEAR', \
                                            projectionYear = 2011, siteIndexEqType = 'AVI'):
        '''
        '''
        keyVarValueList = siDict.keys()
        projBhageName = 'P'+ bhageColName
        projTotalAgeName = 'P' + totalAgeColName
        projHeightColName = 'P' + heightColName
        projYearColName = 'P' + yearColName
        newSiDictHeader = joinOneDListBToRightOfOneDListAExcludingValuesAlreadyInA(siDictHeader, [projBhageName, projTotalAgeName,\
                                                                                                  projHeightColName, projYearColName])
        for keyValue in keyVarValueList:
            treeSpecies = siDict[keyValue][speciesColName]
            bhAge = siDict[keyValue][bhageColName]
            totalAge = siDict[keyValue][totalAgeColName]
            siteIndex = siDict[keyValue][siColName]
            totalHeight = siDict[keyValue][heightColName]
            month = siDict[keyValue][monthColName]
            year = siDict[keyValue][yearColName]
            if month <= 5:
                yearIncrement = projectionYear - year + 1
            else:
                yearIncrement = projectionYear - year
            projBhage = bhAge + yearIncrement
            projTotalAge = totalAge + yearIncrement
            if siteIndexEqType == 'AVI':
                projHeight = ComputeAviSiteIndex(treeSpecies, projBhage, siteIndex)
            if siteIndexEqType == 'GYPSY':
                projHeight = ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(treeSpecies, siteIndex, projTotalAge)
            siDict[keyValue].update({projBhageName:projBhage,projTotalAgeName:projTotalAge, \
                                     projHeightColName:projHeight, projYearColName:projectionYear})
        return newSiDictHeader, siDict

    def ComputeAviSiteIndex(self, species = 'Aw', bhage = 1, treeHeight = 2):
        '''
        Site index formula's extracted from Alberta vegetation inventory interpretation
        standards. Version 2.1.1. Chapter 3 - Vegetation inventory standards and
        data model documents. March 2005. Pp. 64-65
        '''
        siteIndex = 0
        newTreeHeight = treeHeight - 1.3
        if newTreeHeight > 0 and bhage > 0:
            if species == 'Aw' or \
               species == 'Bw' or \
               species == 'Pb' or \
               species == 'A' or \
               species == 'H':
                siteIndex = 1.3 + 17.0100096 \
                                + 0.878406*(newTreeHeight) \
                                + 1.836354*numpy.log(bhage) \
                                - 1.401817*(numpy.log(bhage))**2 \
                                + 0.437430*numpy.log(newTreeHeight)/float(bhage)
            if species == 'Sw' or \
               species == 'Se' or \
               species == 'Fd' or \
               species == 'Fb' or \
               species == 'Fa':
                siteIndex = 1.3 + 10.398053 \
                                + 0.324415*(newTreeHeight) \
                                + 0.00599608*numpy.log(bhage)*bhage \
                                - 0.838036*(numpy.log(bhage))**2 \
                                + 27.487397*(newTreeHeight)/float(bhage) \
                                + 1.191405*(numpy.log(newTreeHeight))
            if species == 'P' or \
               species == 'Pl' or \
               species == 'Pj' or \
               species == 'Pa' or \
               species == 'Pf':
                siteIndex = 1.3 + 10.940796 \
                                + 1.675298 *(newTreeHeight) \
                                - 0.932222*(numpy.log(bhage))**2 \
                                + 0.005439671*numpy.log(bhage)*bhage \
                                + 8.228059*(newTreeHeight)/float(bhage) \
                                - 0.256865*(newTreeHeight)*numpy.log(newTreeHeight)
            if species == 'Sb' or \
               species == 'Lt' or \
               species == 'La' or \
               species == 'Lw' or \
               species == 'L':
                siteIndex = 1.3 + 4.903774 \
                                + 0.811817 * (newTreeHeight) \
                                - 0.363756*(numpy.log(bhage))**2 \
                                + 24.030758*(newTreeHeight)/float(bhage) \
                                - 0.102076*(newTreeHeight)*numpy.log(newTreeHeight)
        return siteIndex


    def ComputeAviBhageFromTotalAge(self, species = 'Aw', totalAge = 0, bhage = 0):
        '''
        Breast height age formula's extracted from Alberta vegetation inventory interpretation
        standards. Version 2.1.1. Chapter 3 - Vegetation inventory standards and
        data model documents. March 2005. Pp. 20.
        '''
        if species == 'Aw' or \
           species == 'Bw' or \
           species == 'Pb' or \
           species == 'A' or \
           species == 'H':
            if totalAge > 0 and bhage == 0:
                bhage = totalAge - 6
            else:
                totalAge = bhage + 6
        if species == 'Sw' or \
           species == 'Se' or \
           species == 'Fd' or \
           species == 'Fb' or \
           species == 'Fa' or \
           species == 'Lt' or \
           species == 'La' or \
           species == 'Lw' or \
           species == 'L':
            if totalAge > 0 and bhage == 0:
                bhage = totalAge - 15
            else:
                totalAge = bhage + 15
        if species == 'P' or \
           species == 'Pl' or \
           species == 'Pj' or \
           species == 'Pa' or \
           species == 'Pf':
            if totalAge > 0 and bhage == 0:
                bhage = totalAge - 10
            else:
                totalAge = bhage + 10
        if species == 'Sb':
            if totalAge > 0 and bhage == 0:
                bhage = totalAge - 20
            else:
                totalAge = bhage + 20
        if bhage < 0:
            bhage = 0
        if totalAge < 0:
            totalAge = 0
        return bhage, totalAge

    def CompileGypsySiteIndices(self, dataDict = {}, speciesCol = 'SPECIES', bhageCol = 'AGE', totalAgeCol = 'NULL', \
                              treeHeightCol = 'HT_MEAS', treeMeasDateCol = 'MEASDATE', measDateFormat = 'dd/mm/yyyy'):
        '''
        '''
        siDict = {}
        siDictHeader = ['SIID','SPECIES','BHAGE','TAGE', 'HT','SI','DAY','MONTH','YEAR']
        siDictKeyVarNameList = ['SIID']
        if bhageCol == 'NULL' and totalAgeCol == 'NULL':
            print 'routineLviApplications.CompileAviSiteIndices'
            print 'bhageCol and totalAgeCol both indicated as NULL'
            print 'Only one of these columns can be indicated as NULL in order to calculate site index'
        keyList = dataDict.keys()
        keyList.sort()
        for keyValue in keyList:
            species = dataDict[keyValue][speciesCol]
            treeHeight = dataDict[keyValue][treeHeightCol]
            if bhageCol == 'NULL':
                bhage, totalAge, siteIndex = ComputeGypsySiteIndex(species, treeHeight, 0, dataDict[keyValue][totalAgeCol])
            else:
                bhage, totalAge, siteIndex = ComputeGypsySiteIndex(species, treeHeight, dataDict[keyValue][bhageCol], 0)
            measDate = dataDict[keyValue][treeMeasDateCol]
            day, month, year = RecoverYearMonthAndDay(measDate, measDateFormat)
            #print keyValue, species, bhage, totalAge, treeHeight, siteIndex
            siDict.update({keyValue:{'SPECIES':species,'BHAGE':bhage,'TAGE':totalAge,'HT':treeHeight,'SI':siteIndex,'DAY':day,'MONTH':month,'YEAR':year}})
        return siDictKeyVarNameList, siDictHeader, siDict


    def CompileGypsySiteIndices_v2(self, dataDict = {}, speciesCol = 'SPECIES', bhageCol = 'AGE', totalAgeCol = 'NULL', \
                              treeHeightCol = 'HT_MEAS', year = 2011):
        '''
        '''
        siDict = {}
        siDictHeader = ['SIID','SPECIES','BHAGE','TAGE', 'HT','SI','YEAR']
        siDictKeyVarNameList = ['SIID']
        if bhageCol == 'NULL' and totalAgeCol == 'NULL':
            print 'routineLviApplications.CompileAviSiteIndices'
            print 'bhageCol and totalAgeCol both indicated as NULL'
            print 'Only one of these columns can be indicated as NULL in order to calculate site index'
        keyList = dataDict.keys()
        keyList.sort()
        for keyValue in keyList:
            species = dataDict[keyValue][speciesCol]
            treeHeight = dataDict[keyValue][treeHeightCol]
            if bhageCol == 'NULL':
                bhage, totalAge, siteIndex = ComputeGypsySiteIndex(species, treeHeight, 0, dataDict[keyValue][totalAgeCol])
            else:
                bhage, totalAge, siteIndex = ComputeGypsySiteIndex(species, treeHeight, dataDict[keyValue][bhageCol], 0)
            #print keyValue, species, bhage, totalAge, treeHeight, siteIndex
            siDict.update({keyValue:{'SPECIES':species,'BHAGE':bhage,'TAGE':totalAge,'HT':treeHeight,'SI':siteIndex,'YEAR':year}})
        return siDictKeyVarNameList, siDictHeader, siDict

    def ComputeGypsySiteIndex(self, species = 'Aw', totalHeight = 1.3, bhage = 0, totalAge = 0):
        '''
        Equations and logic derived from:
        Huang, S., Meng, S.X., and Yang, Y. 2009. A growth and yield projection system (GYPSY) for natural and
        post-harvest stands in Alberta. Technical Report Pb. No.:T/216. Forest Management Branch, Alberta Sustainable
        Resource Development, Edmonton, AB, CAN.  Appendix I. Pp. 21,22.
        '''
        tage = totalAge
        si0 = 0
        if totalHeight > 1.3:
            if bhage > 0 or totalAge > 0:
                if species == 'P' or \
                   species == 'Pl' or \
                   species == 'Pj' or \
                   species == 'Pa' or \
                   species == 'Pf':
                    b1 = 12.84571
                    b2 = -5.73936
                    b3 = -0.91312
                    b4 = 0.150668
                    si0 = 10
                    si1 = 0
                    while abs(si0-si1)>0.00000001:
                        k1 = numpy.exp(b1+b2*(numpy.log(50+1)**0.5) + b3*numpy.log(si0)+b4*(50**0.5))
                        k2 = si0**b3
                        k3 = ((si0)*(1+k1)/1.3-1)/(numpy.exp(b1)*numpy.exp(b4*(50**0.5))*k2)
                        y2bh = numpy.exp((numpy.log(k3)/b2)**2)-1
                        if bhage > 0 and totalAge == 0:
                            tage = bhage + y2bh
                        else:
                            #bhage = 0 and totalGe > 0
                            tage = totalAge
                            bhage = tage - y2bh
                        x10 = (1+numpy.exp(b1+b2*(numpy.log(tage+1)**0.5)+b3*numpy.log(si0)+b4*(50**0.5)))
                        x20 = (1+numpy.exp(b1+b2*(numpy.log(50+1)**0.5)+b3*numpy.log(si0)+b4*(50**0.5)))
                        si1 = totalHeight*(x10/float(x20))
                        si0 = (si0+si1)/2
                if species == 'Sw' or \
                   species == 'Se' or \
                   species == 'Fd' or \
                   species == 'Fb' or \
                   species == 'Fa':
                    b1 = 12.14943
                    b2 = -3.77051
                    b3 = -0.28534
                    b4 = 0.165483
                    si0 = 10
                    si1 = 0
                    while abs(si0-si1)>0.00000001:
                        k1 = numpy.exp(b1+b2*(numpy.log(50**2+1)**0.5) + b3*(numpy.log(si0)**2)+b4*(50**0.5))
                        k2 = si0**(b3*numpy.log(si0))
                        k3 = ((si0)*(1+k1)/1.3-1)/(numpy.exp(b1)*numpy.exp(b4*(50**0.5))*k2)
                        y2bh = (numpy.exp((numpy.log(k3)/b2)**2)-1)**0.5
                        if bhage > 0 and totalAge == 0:
                            tage = bhage + y2bh
                        else:
                            #bhage = 0 and totalGe > 0
                            tage = totalAge
                            bhage = tage - y2bh
                        x10 = (1+numpy.exp(b1+b2*(numpy.log((tage**2)+1)**0.5)+b3*(numpy.log(si0)**2)+b4*(50**0.5)))
                        x20 = (1+numpy.exp(b1+b2*(numpy.log((50**2)+1)**0.5)+b3*(numpy.log(si0)**2)+b4*(50**0.5)))
                        si1 = totalHeight*(x10/float(x20))
                        si0 = (si0+si1)/2
                if species == 'Sb' or \
                   species == 'Lt' or \
                   species == 'La' or \
                   species == 'Lw' or \
                   species == 'L':
                    b1 = 14.56236
                    b2 = -6.04705
                    b3 = -1.53715
                    b4 = 0.240174
                    si0 = 10
                    si1 = 0
                    while abs(si0-si1)>0.00000001:
                        k1 = numpy.exp(b1+b2*(numpy.log(50+1)**0.5) + b3*numpy.log(si0)+b4*(50**0.5))
                        k2 = si0**b3
                        k3 = ((si0)*(1+k1)/1.3-1)/(numpy.exp(b1)*numpy.exp(b4*(50**0.5))*k2)
                        y2bh = numpy.exp((numpy.log(k3)/b2)**2)-1
                        if bhage > 0 and totalAge == 0:
                            tage = bhage + y2bh
                        else:
                            #bhage = 0 and totalGe > 0
                            tage = totalAge
                            bhage = tage - y2bh
                        x10 = (1+numpy.exp(b1+b2*(numpy.log(tage+1)**0.5)+b3*numpy.log(si0)+b4*(50**0.5)))
                        x20 = (1+numpy.exp(b1+b2*(numpy.log(50+1)**0.5)+b3*numpy.log(si0)+b4*(50**0.5)))
                        si1 = totalHeight*(x10/float(x20))
                        si0 = (si0+si1)/2
                if species == 'Aw' or \
                   species == 'Bw' or \
                   species == 'Pb' or \
                   species == 'A' or \
                   species == 'H':
                    b1 = 9.908888
                    b2 = -3.92451
                    b3 = -0.32778
                    b4 = 0.134376
                    si0 = 10
                    si1 = 0
                    while abs(si0-si1)>0.00000001:
                        k1 = numpy.exp(b1+b2*(numpy.log(50+1)**0.5) + b3*(numpy.log(si0)**2)+b4*(50**0.5))
                        k2 = si0**(b3*numpy.log(si0))
                        k3 = ((si0)*(1+k1)/1.3-1)/(numpy.exp(b1)*numpy.exp(b4*(50**0.5))*k2)
                        y2bh = numpy.exp((numpy.log(k3)/b2)**2)-1
                        if bhage > 0 and totalAge == 0:
                            tage = bhage + y2bh
                        else:
                            #bhage = 0 and totalGe > 0
                            tage = totalAge
                            bhage = tage - y2bh
                        x10 = (1+numpy.exp(b1+b2*(numpy.log(tage+1)**0.5)+b3*(numpy.log(si0)**2)+b4*(50**0.5)))
                        x20 = (1+numpy.exp(b1+b2*(numpy.log(50+1)**0.5)+b3*(numpy.log(si0)**2)+b4*(50**0.5)))
                        si1 = totalHeight*(x10/float(x20))
                        si0 = (si0+si1)/2              
        return bhage, tage, si0 

    def ComputeGypsyTreeHeightGivenSiteIndexAndTotalAge(self, species = 'Aw', siteIndex = 1.3, totalAge = 0):
        '''
        Equations and logic derived from:
        Huang, S., Meng, S.X., and Yang, Y. 2009. A growth and yield projection system (GYPSY) for natural and
        post-harvest stands in Alberta. Technical Report Pb. No.:T/216. Forest Management Branch, Alberta Sustainable
        Resource Development, Edmonton, AB, CAN.  Appendix I. Pp. 21,22.
        '''
        tage = totalAge
        si0 = siteIndex
        treeHeight = 0
        if siteIndex > 1.3:
            if totalAge > 0:
                if species == 'P' or \
                   species == 'Pl' or \
                   species == 'Pj' or \
                   species == 'Pa' or \
                   species == 'Pf':
                    b1 = 12.84571
                    b2 = -5.73936
                    b3 = -0.91312
                    b4 = 0.150668
                    x10 = (1+numpy.exp(b1+b2*(numpy.log(50+1)**0.5)+b3*numpy.log(si0)+b4*(50**0.5)))
                    x20 = (1+numpy.exp(b1+b2*(numpy.log(totalAge+1)**0.5)+b3*numpy.log(si0)+b4*(50**0.5)))
                    treeHeight = siteIndex*(x10/float(x20))
                if species == 'Sw' or \
                   species == 'Se' or \
                   species == 'Fd' or \
                   species == 'Fb' or \
                   species == 'Fa':
                    b1 = 12.14943
                    b2 = -3.77051
                    b3 = -0.28534
                    b4 = 0.165483
                    x10 = (1+numpy.exp(b1+b2*(numpy.log((50**2)+1)**0.5)+b3*(numpy.log(si0)**2)+b4*(50**0.5)))
                    x20 = (1+numpy.exp(b1+b2*(numpy.log((totalAge**2)+1)**0.5)+b3*(numpy.log(si0)**2)+b4*(50**0.5)))
                    treeHeight = siteIndex*(x10/float(x20))
                if species == 'Sb' or \
                   species == 'Lt' or \
                   species == 'La' or \
                   species == 'Lw' or \
                   species == 'L':
                    b1 = 14.56236
                    b2 = -6.04705
                    b3 = -1.53715
                    b4 = 0.240174
                    x10 = (1+numpy.exp(b1+b2*(numpy.log(50+1)**0.5)+b3*numpy.log(si0)+b4*(50**0.5)))
                    x20 = (1+numpy.exp(b1+b2*(numpy.log(totalAge+1)**0.5)+b3*numpy.log(si0)+b4*(50**0.5)))
                    treeHeight = siteIndex*(x10/float(x20))
                if species == 'Aw' or \
                   species == 'Bw' or \
                   species == 'Pb' or \
                   species == 'A' or \
                   species == 'H':
                    b1 = 9.908888
                    b2 = -3.92451
                    b3 = -0.32778
                    b4 = 0.134376
                    x10 = (1+numpy.exp(b1+b2*(numpy.log(50+1)**0.5)+b3*(numpy.log(si0)**2)+b4*(50**0.5)))
                    x20 = (1+numpy.exp(b1+b2*(numpy.log(totalAge+1)**0.5)+b3*(numpy.log(si0)**2)+b4*(50**0.5)))
                    treeHeight = siteIndex*(x10/float(x20))
        return treeHeight 

    def calculateStandAgeFromDateOfOrigin(self, dataDict = {}, dataDictHeader = [], originVarName = 'IGB_ORIGIN', invYearVarName = 'IGB_INV_YEAR', \
                                          inventoryYear = 2011, ageVarName = 'IGB_TAGE'):
        '''
        '''
        keyVarList = dataDict.keys()
        keyVarList.sort()
        #Check header to ensure it includes inventory year and age variables
        if not invYearVarName in dataDictHeader:
            dataDictHeader.append(invYearVarName)
        if not ageVarName in dataDictHeader:
            dataDictHeader.append(ageVarName)
        if not originVarName in dataDictHeader:
            dataDictHeader.append(originVarName)
        #Get key list from 1 level dictionary
        for keyVar in keyVarList:
            #Check for data dictionary origin data
            #If no origin date in dictionary set origin to year 0 and update dictionary
            if dataDict[keyVar].has_key(originVarName):
                origin = dataDict[keyVar][originVarName]
            else:
                origin = 0
                dataDict[keyVar].update({originVarName:origin})
            #Check dictionary for inventory year
            #If no inventory year use default provided as input into routine and update dataDictionary
            if dataDict[keyVar].has_key(invYearVarName):
                invYear = dataDict[keyVar][invYearVarName]
            else:
                invYear = inventoryYear
                dataDict[keyVar].update({invYearVarName:invYear})
            #If there is no origin date then there is no age - set age equal to -1 and update dictionary
            #Otherwise calculate age
            if origin == 0 or origin == '':
                age = 0
            else:
                age = invYear - origin
                #Origin date cannot exceed inventory year
                if age < 0:
                    age = 0
            dataDict[keyVar].update({ageVarName:age})
        return dataDictHeader, dataDict


    def compileAlbertaTimberProductivityRating(self, spSiDict = {}, spSiDictHeader = [], spVarName = 'SPECIES', siVarName = 'SI'):
        '''
        '''
        if 'TPR' not in spSiDictHeader:
            spSiDictHeader.append('TPR')
        for key0 in spSiDict:
            sp = ''
            si = 0
            tpr = ''
            if spSiDict[key0].has_key(spVarName):
                sp = spSiDict[key0][spVarName]
            if spSiDict[key0].has_key(siVarName):
                si = spSiDict[key0][siVarName]
            if not sp == '' and si > 0:
                tpr = computeTimberProductivityRatingFromSiteIndex(sp, si)
            spSiDict[key0].update({'TPR':tpr})
        return spSiDictHeader, spSiDict

    def computeTimberProductivityRatingFromSiteIndex(self, treeSpecies = '', siteIndex = 0):
        '''
        Timber Productivity Ratings (TPR) extracted from Alberta vegetation inventory interpretation
        standards. Version 2.1.1. Chapter 3 - Vegetation inventory standards and
        data model documents. March 2005. Pp. 64-65
        '''
        tpr = ''
        
        if treeSpecies == 'Aw' or \
           treeSpecies == 'Bw' or \
           treeSpecies == 'Pb' or \
           treeSpecies == 'A':
            if siteIndex >= 5 and siteIndex <= 10.05:
                tpr = 'U'
            else:
                if siteIndex > 10.05 and siteIndex <= 14.05:
                    tpr = 'F'
                else:
                    if siteIndex > 14.05 and siteIndex <= 18.05:
                        tpr = 'M'
                    else:
                        if siteIndex > 18.05 and siteIndex <= 30:
                            tpr = 'G'
                        else:
                            print 'Species', treeSpecies, 'site index', siteIndex, 'exceeds 30 m height at 50 years breast height age'
                            tpr = 'G'
                            
        if treeSpecies == 'Sw' or \
           treeSpecies == 'Se' or \
           treeSpecies == 'Fd' or \
           treeSpecies == 'Fb' or \
           treeSpecies == 'Fa':
            if siteIndex >= 3 and siteIndex <= 6.05:
                tpr = 'U'
            else:
                if siteIndex > 6.05 and siteIndex <= 10.05:
                    tpr = 'F'
                else:
                    if siteIndex > 10.05 and siteIndex <= 15.55:
                        tpr = 'M'
                    else:
                        if siteIndex > 15.55 and siteIndex <= 25:
                            tpr = 'G'
                        else:
                            print 'Species', treeSpecies, 'site index', siteIndex, 'exceeds 25 m height at 50 years breast height age'
                            tpr = 'G'

        if treeSpecies == 'P' or \
           treeSpecies == 'Pl' or \
           treeSpecies == 'Pj' or \
           treeSpecies == 'Pa' or \
           treeSpecies == 'Pf':
            if siteIndex >= 3 and siteIndex <= 7.05:
                tpr = 'U'
            else:
                if siteIndex > 7.05 and siteIndex <= 12.05:
                    tpr = 'F'
                else:
                    if siteIndex > 12.05 and siteIndex <= 16.05:
                        tpr = 'M'
                    else:
                        if siteIndex > 16.05 and siteIndex <= 25:
                            tpr = 'G'
                        else:
                            print 'Species', treeSpecies, 'site index', siteIndex, 'exceeds 25 m height at 50 years breast height age'
                            tpr = 'G'

        if treeSpecies == 'Sb' or \
           treeSpecies == 'Lt':
            if siteIndex >= 1 and siteIndex <= 6.05:
                tpr = 'U'
            else:
                if siteIndex > 6.05 and siteIndex <= 7.05:
                    tpr = 'F'
                else:
                    if siteIndex > 7.05 and siteIndex <= 10.05:
                        tpr = 'M'
                    else:
                        if siteIndex > 10.05 and siteIndex <= 20:
                            tpr = 'G'
                        else:
                            print 'Species', treeSpecies, 'site index', siteIndex, 'exceeds 20 m height at 50 years breast height age'
                            tpr = 'G'
        return tpr

    def ExtractPhotoInterpreterSpeciesRecognition(self, photoInterpDict = {}, photoInterpKeyVarNames = [], photoInterpreterList = [], speciesNameList = []):
        '''
        This function ensures that there is a complete record of species proportions for each interpreter
        and for each plot and that the species proportions always add up to 1.  This includes an accounting
        for conditions where one interpreter may not have assigned any species to a plot provided
        that the speciesNameList includes a species as '' or 'NULL' or 'NONE' or ''.  
        '''
        newPlotInterpDict = {}
        newPlotInterpHeader = joinOneDListBToRightOfOneDListA(photoInterpKeyVarNames, speciesNameList)
        newPlotInterpKeyVarNames = deepcopy(photoInterpKeyVarNames)
        nInterpreter = len(photoInterpreterList)
        nSpecies = len(speciesNameList)
        for plot in photoInterpDict:
            #print 'PLOT:', plot
            newPlotInterpDict.update({plot:{}})
            #Compile the species percentages associated with each interpreter
            #in the order listed in the photoInterpreterList and in the order of species
            #as listed in the speciesNameList
            for interpreter in photoInterpreterList:
                newPlotInterpDict[plot].update({interpreter:{}})
                if photoInterpDict[plot].has_key(interpreter):
                    for sp in speciesNameList:
                        if photoInterpDict[plot][interpreter].has_key(sp):
                            spPcnt = photoInterpDict[plot][interpreter][sp]
                            if spPcnt == '':
                                spPcnt = 0
                        else:
                            spPcnt = 0
                        newPlotInterpDict[plot][interpreter].update({sp:spPcnt})
                else:
                    for sp in speciesNameList:
                        newPlotInterpDict[plot][interpreter].update({sp:0})
            #Check to make sure interpreter percentages add up to 1
            for intepreter in photoInterpreterList:
                interpSum = 0
                for sp in speciesNameList:
                    interpSum = interpSum + newPlotInterpDict[plot][interpreter][sp]
                if not interpSum == 1: 
                    if interpSum == 0:
                        #If the sum is 0 then assign a 1 to species label 'NA'
                        if 'NULL' in speciesNameList:
                            newPlotInterpDict[plot][interpreter]['NULL'] = float(1)
                        else:
                            if 'NONE' in speciesNameList:
                                naIndex = speciesNameList.index('NONE')
                                newPlotInterpDict[plot][interpreter]['NONE'] = float(1)
                            else:
                                if '' in speciesNameList:
                                    naIndex = speciesNameList.index('')
                                    newPlotInterpDict[plot][interpreter][''] = float(1)
                    else:
                        #interpSum greater than 0 but not equal to 1
                        for sp in speciesNameList:
                            newPlotInterpDict[plot][interpreter][sp] = newPlotInterpDict[plot][interpreter][sp] / float(interpSum)
        return newPlotInterpKeyVarNames, newPlotInterpHeader, newPlotInterpDict 

    def CrossTabulateInterpeterSpeciesRecognition(self, plotInterpDict = {},piCtabKeyVarName = 'NPLOTID',photoInterpreterList = [],speciesNameList = []):
        '''
        Need to get the frequency distributions - presence or absence - of a given species associated with each fromInterpreter
        These are to then be converted into a probablility distribution and the probability distributions multiplied by the
        respective from rows p-values to get a correct conversion, i.e. there are cases where a from species occurs but
        is not transferred to a specific to species; once this is corrected for the matrices from-to (e.g.  should be the same  
        
        so that the proportions can be 
        '''
        piInterpDict = {}
        piInterpHeader = [piCtabKeyVarName,'TOINTERP','FRINTERP','TOSP','FRSP','P']
        piKeyVarNames = [piCtabKeyVarName,'TOINTERP','FRINTERP','TOSP','FRSP']
        piSumHeader = ['TOINTERP','FRINTERP','TOSP','FRSP','SUMP','N','P', 'PPPLOTS', 'PPPSP']
        piSumKeyVarNames = ['TOINTERP','FRINTERP','TOSP','FRSP']
        nInterpreters = len(photoInterpreterList)
        nSpecies = len(speciesNameList)
        plotKeyList = plotInterpDict.keys()
        plotKeyList.sort()
        nPlotTotal = len(plotKeyList)
        interpSpKeyVarNames = ['INTERP','FRSP']
        interpSpHeader = ['INTERP','FRSP', 'NPLOTS', 'PPLOTS', 'SPPSUM', 'SPP']
        #Initialize piSumDict and dummyDict to initialize each plot in piInterpDict
        dummyDict = {}
        piSumDict = {}
        interpSpDict = {}
        #This routine should be rewritten to a more generalized dictionary initialization routine
        for i in range(0,nInterpreters,1):
            #rows
            toInterp = photoInterpreterList[i] 
            if not piSumDict.has_key(toInterp):
                piSumDict.update({toInterp:{}})
                dummyDict.update({toInterp:{}})
            for j in range(0, nInterpreters,1):
                #columns 
                fromInterp = photoInterpreterList[j]
                if not piSumDict[toInterp].has_key(fromInterp):
                    piSumDict[toInterp].update({fromInterp:{}})
                    dummyDict[toInterp].update({fromInterp:{}})
                if not interpSpDict.has_key(fromInterp):
                    interpSpDict.update({fromInterp:{}})
                for k in range(0,nSpecies,1):
                    #rows
                    toSp = speciesNameList[k]
                    if not piSumDict[toInterp][fromInterp].has_key(toSp):
                        piSumDict[toInterp][fromInterp].update({toSp:{}})
                        dummyDict[toInterp][fromInterp].update({toSp:{}})
                    for l in range(0,nSpecies,1):
                        fromSp = speciesNameList[l]
                        if not piSumDict[toInterp][fromInterp][toSp].has_key(fromSp):
                            piSumDict[toInterp][fromInterp][toSp].update({fromSp:{'SUMP':0,'N':0,'P':0, 'PPPLOTS':0, 'PPPSP':0}})
                            dummyDict[toInterp][fromInterp][toSp].update({fromSp:{'P':0}})
                        if not interpSpDict[fromInterp].has_key(fromSp):
                            interpSpDict[fromInterp].update({fromSp:{'NPLOTS':0, 'PPLOTS':0, 'SPPSUM':0, 'SPP':0}})
        #Compile transition probabilities from species in interpreter j to species in interpreter i
        for plot in plotKeyList:
            if not piInterpDict.has_key(plot):
                piInterpDict.update({plot:dummyDict})
            for i in range(0,nInterpreters,1):
                toInterp = photoInterpreterList[i]
                for j in range(0, nInterpreters,1):
                    fromInterp = photoInterpreterList[j]    
                    speciesDifferenceList = []
                    for k in range(0,nSpecies):
                        sp = speciesNameList[k]
                        diff = plotInterpDict[plot][toInterp][sp]-plotInterpDict[plot][fromInterp][sp]
                        speciesDifferenceList.append(diff)
                    fromVector = []
                    toVector = []
                    for k in range(0,nSpecies,1):
                        sp = speciesNameList[k]
                        if speciesDifferenceList[k] == 0:
                            fromVector.append(0)
                            toVector.append(0)
                        else:
                            if speciesDifferenceList[k] < 0:
                                #Species moved from species k in observer j
                                #The proportions moved from j are relative to the abundance of species k initialy
                                #assigned by interpeter j
                                #print sp, jInterp, speciesDifferenceList[k], plotInterpDict[plot][jInterp][sp]
                                prop = abs(speciesDifferenceList[k]/float(plotInterpDict[plot][fromInterp][sp]))
                                fromVector.append(prop)
                                toVector.append(0)
                                nplots = interpSpDict[fromInterp][sp]['NPLOTS'] + 1
                                pplots = nplots/float(nPlotTotal)
                                sppsum = interpSpDict[fromInterp][sp]['SPPSUM'] + plotInterpDict[plot][fromInterp][sp]
                                interpSpDict[fromInterp][sp].update({'NPLOTS':nplots,'PPLOTS':pplots, 'SPPSUM':sppsum})
                            else:
                                if speciesDifferenceList[k] > 0:
                                    #Species moved to species k in observer i
                                    fromVector.append(0)
                                    toVector.append(speciesDifferenceList[k])
                    #Ensure that the toVector proportions moved to interpreter i sum to 1
                    #The total amount moved is relative to the proportions moved from interpreter j
                    toVectorSum = float(numpy.sum(toVector))
                    if toVectorSum > 0:
                        for k in range(0, nSpecies,1):
                            toVector[k] = toVector[k]/toVectorSum
                    outerProduct = MATRIX_MAN.matrix_multiply_outer_product(toVector, fromVector)
                    #print plot, toInterp, fromInterp, toVectorSum
                    #print speciesNameList
                    #print fromVector
                    #print toVector
                    #Update Dictionaries
                    for k in range(0, nSpecies,1):
                        pTot = numpy.sum(outerProduct[k])
                        toSp = speciesNameList[k]
                        for l in range(0, nSpecies,1):
                            fromSp = speciesNameList[l]                               
                            p = float(outerProduct[k][l])
                            piInterpDict[plot][toInterp][fromInterp][toSp][fromSp]['P'] = p
                            if p > 0:
                                sumP = piSumDict[toInterp][fromInterp][toSp][fromSp]['SUMP'] + p
                                piSumDict[toInterp][fromInterp][toSp][fromSp]['SUMP'] = sumP
                                nCount = piSumDict[toInterp][fromInterp][toSp][fromSp]['N'] + 1
                                piSumDict[toInterp][fromInterp][toSp][fromSp]['N'] = nCount


        
        
        #Calculate proportions
        for i in range(0,nInterpreters,1):
            toInterp = photoInterpreterList[i]
            for j in range(0, nInterpreters,1):
                fromInterp = photoInterpreterList[j]
                totalSpSum = 0
                for k in range(0, nSpecies,1):
                    #pTot = numpy.sum(outerProduct[k])
                    fromSp = speciesNameList[k]
                    totalSpSum = totalSpSum + interpSpDict[fromInterp][fromSp]['SPPSUM']
                for k in range(0, nSpecies,1):
                    #pTot = numpy.sum(outerProduct[k])
                    toSp = speciesNameList[k]
                    for l in range(0, nSpecies,1):
                        fromSp = speciesNameList[l]
                        nCount = piSumDict[toInterp][fromInterp][toSp][fromSp]['N']
                        if nCount > 0:
                            sumP = piSumDict[toInterp][fromInterp][toSp][fromSp]['SUMP']
                            nCount = piSumDict[toInterp][fromInterp][toSp][fromSp]['N']
                            p = sumP/float(nCount)
                            nplots = interpSpDict[fromInterp][fromSp]['NPLOTS']
                            piSumDict[toInterp][fromInterp][toSp][fromSp]['P'] = p
                            ppplots =  p * nCount/float(nplots)
                            piSumDict[toInterp][fromInterp][toSp][fromSp]['PPPLOTS'] = ppplots
                            #piSumDict[toInterp][fromInterp][toSp][fromSp]['PPPSP'] = ppplots * interpSpDict[fromInterp][fromSp]['PPLOTS']
                            #if interpSpDict[toInterp][toSp]['PPLOTS'] > 0:
                            piSumDict[toInterp][fromInterp][toSp][fromSp]['PPPSP'] = p * nCount/float(nPlotTotal)
                            interpSpDict[fromInterp][fromSp]['SPP'] = interpSpDict[fromInterp][fromSp]['SPPSUM']/float(totalSpSum)
                            #piSumDict[toInterp][fromInterp][toSp][fromSp]['PPPSP'] = ppplots * (interpSpDict[fromInterp][fromSp]['PPLOTS']/interpSpDict[toInterp][toSp]['PPLOTS'])
                            #print plot, toInterp, fromInterp, toSp, fromSp, p, piSumDict[toInterp][fromInterp][toSp][fromSp]['SUMP'], piSumDict[toInterp][fromInterp][toSp][fromSp]['N']
                                            
        return piKeyVarNames, piInterpHeader, piInterpDict, piSumKeyVarNames, piSumHeader, piSumDict, interpSpKeyVarNames, interpSpHeader, interpSpDict

    def combinedDictionariesWithCommonKeyStructure(self, dataDictA = {}, dataDictB = {}, keyVarNames = [], dataHeader = [], keyLevelMatch = 1):
        '''
        inner join conditional on matching keys down to a specified level in the hierarchy
        '''
        nKeys = len(keyVarNames)
        varNameList = removeItemsInOneDListBFromOneDListA(dataHeader, keyVarNames)
        newDict = {}
        if nKeys > 0:
            keyListA0 = dataDictA.keys()
            keyListB0 = dataDictB.keys()
            if keyLevelMatch >= 1:
                #Get overlapping set from keyListA and keyListB
                keyList0 = list(set.intersection(set(keyListA0),set(keyListB0)))
            else:
                #Add keyListB to keyListA excluding those items already in keyListA 
                keyList0 = joinOneDListBToRightOfOneDListAExcludingValuesAlreadyInA(keyListA0, keyListB0)
            for key0 in keyList0:
                newDict.update({key0:{}})
                if nKeys == 1:
                    if dataDictA.has_key(key0):
                        for varName in varNameList:
                            if dataDictA[key0].has_key(varName):
                                newDict[key0].update({varName:dataDictA[key0][varName]})
                    if dataDictB.has_key(key0):
                        for varName in varNameList:
                            if dataDictB[key0].has_key(varName):
                                if not newDict[key0].has_key(varName):
                                    newDict[key0].update({varName:dataDictB[key0][varName]})
                    for varName in varNameList:
                        if not newDict[key0].has_key(varName):
                            newDict[key0].update({varName:''})
                else:
                    #Two keys
                    keyListA1 = dataDictA[key0].keys()
                    keyListB1 = dataDictB[key0].keys()
                    if keyLevelMatch >= 2:
                        #Get overlapping set from keyListA and keyListB
                        keyList1 = list(set.intersection(set(keyListA1),set(keyListA2)))
                    else:
                        #Add keyListB to keyListA excluding those items already in keyListA 
                        keyList1 = joinOneDListBToRightOfOneDListAExcludingValuesAlreadyInA(keyListA1, keyListB1)
                        for key1 in keyList1:
                            newDict[key0].update({key1:{}})
                            if nKeys == 2:
                                if dataDictA[key0].has_key(key1):
                                    for varName in varNameList:
                                        if dataDictA[key0][key1].has_key(varName):
                                            newDict[key0][key1].update({varName:dataDictA[key0][key1][varName]})
                                if dataDictB[key0].has_key(key1):
                                    for varName in varNameList:
                                        if dataDictB[key0][key1].has_key(varName):
                                            if not newDict[key0][key1].has_key(varName):
                                                newDict[key0][key1].update({varName:dataDictB[key0][key1][varName]})
                                for varName in varNameList:
                                    if not newDict[key0][key1].has_key(varName):
                                        newDict[key0][key1].update({varName:''})
        return newDict

    def compileStageSlopeAspectElevTransformationsAndAddToData(self, dataDict={},keyVarNameList = [], slopeVarName = 'SLOPE', elevationVarName = 'ELEV', aspectVarName = 'ASP', \
                                                               varNameList = ['ELEV2','SLOPELEV2','SLOPCASP','SLOPSASP','SLNELEV','SLNELEVCA',\
                                                                'SLNELEVSA','SE2CA','SE2SA']):
        '''
        This routine derived a new set of variables based on transofmration
        of slope, aspect, and elevation that are based on the work of Al Stage
        as follows:

        Stage, A.B., and Salas, C. 2007. Interaction of elevation, aspect, and slope
        in models of forest species composition and productivity.
        Forest Science 53(4): 486-492.

        The following variable transforms are computed:
        ASP = aspect(degrees)
        SLOP = slope (degrees)
        ELEV = Elevation (m) 
        ELEV2 = ELEV**2
        SLOPELEV2 = SLOP*ELELV2
        SLOPCASP = SLOP*cosine(ASP)
        SLOPSASP = SLOP*sine(ASP)
        SLNELEV = SLOP*ln(ELEV+1)
        SLNELEVCA = SLNELEV*SLOPCASP
        SLNELEVSA = SLNELEV*SLOPSASP
        SE2CA = SLOPELEV2*cosine(ASP)
        SE2SA = SLOPELEV2*sin(ASP)
        '''
        oldVarNameList = [slopeVarName, elevationVarName, aspectVarName]
        newVarNameList = joinOneDListBToRightOfOneDListA(oldVarNameList, varNameList)
        newHeader = joinOneDListBToRightOfOneDListA(keyVarNameList, newVarNameList)
        newDict = {}
        primaryKeyList = dataDict.keys()
        varCount = 12
        for primaryKey in primaryKeyList:
            slope = dataDict[primaryKey][slopeVarName]
            aspect = dataDict[primaryKey][aspectVarName]
            elev = dataDict[primaryKey][elevationVarName]
            elev2 = elev**2
            slopelev2 = elev2 * slope
            slopcasp = slope*math.cos(math.radians(aspect))
            slopsasp = slope*math.sin(math.radians(aspect))
            slnelev = slope*math.log(elev+1)
            slnelevca = slnelev*math.cos(math.radians(aspect))
            slnelevsa = slnelev*math.sin(math.radians(aspect))
            se2ca = slopelev2*math.cos(math.radians(aspect))
            se2sa = slopelev2*math.sin(math.radians(aspect))
            varValuesList = [slope, elev, aspect, elev2,slopelev2,slopcasp, \
                                         slopsasp,slnelev,slnelevca, \
                                         slnelevsa,se2ca,se2ca]
            newDict.update({primaryKey:{}})
            for i in range(0,varCount,1):
                varName = newVarNameList[i]
                varValue = varValuesList[i]
                newDict[primaryKey].update({varName:varValue})     
        return newHeader, newDict

