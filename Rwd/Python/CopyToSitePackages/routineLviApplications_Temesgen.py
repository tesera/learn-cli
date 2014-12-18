'''
Set file paths
'''
import sys

#Identify admin code directory
adminPath = '/shared/GitHub/Tesera/Rwd/Python/Admin/'
filePath = '/shared/GitHub/Tesera/Rwd/'
dataFilePath = '/shared/GitHub/Tesera/Rwd/'
dictFilePath = '/shared/GitHub/Tesera/Rwd/Python/DATDICT/'
fileExtension = '.csv'
readErrorFilePath = '/shared/GitHub/Tesera/Rwd/Python/PyReadError/'

#Add directory to sys.path 
sys.path.append(adminPath)

import makeDD
import readCSV
import typeDataset
import fuzzyC_v2
import PRINTv1
import addToDataMachette20121026
import dictionaryDBUtilities
import innerJoinDictDBs
import fileUtilities
from copy import deepcopy
import numpy
import time
import datetime
from dbfpy import dbf
from types import *
import os
from scipy import linalg


def ReadLviDataDictionary(filename = 'PyRDataDict'):
    '''
    Read LVI data dictionary contained in
    /Rwd/Python/DATDICT/ ... directory with filename
    PyRDataDict.csv

    Note that this dictionary estblishes variable names and types. 
    '''
    originalDict, newDict = makeDD.dataDictionaryType_21(dictFilePath,filename, fileExtension)
    return originalDict, newDict

def ReadStandardDataDictionary(filename = ''):
    '''
    Read Standard data dictionary contained in
    /Rwd/ ... directory with filename
    PyRDataDict.csv

    Note that this dictionary estblishes variable names and types. 
    '''
    originalDict, newDict = makeDD.dataDictionaryType_21(dataFilePath,filename, fileExtension)
    return originalDict, newDict

def UpdateDataDictionaryWithNewTableName(myDataDict={}, oldTableName = '', newTableName = ''):
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


def GetNewHeader(originalDataDict = {}, dataStringList=[[]], dataTableName = ''):
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

def ReadCsvDataFile(dataDict = {}, dataTableName = '', readErrorFileName = ''):
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
    dataStringList = readCSV.read_csv_text_file_v2(filePath, dataTableName, fileExtension)
    dataTypedList = typeDataset.typeDataset_v2(dataStringList, dataDict, dataTableName, dataErrorFilePath)
    return dataTypedList

def ReadFirstNlinesInCsvDataFile_v2(originalDataDict = {}, newDataDict = {}, dataTableName = '', readErrorFileName = '', nLines = 1):
    '''
    '''
    dataErrorFilePath = readErrorFilePath + readErrorFileName + '.txt'
    PRINTv1.deleteFileIfItExists(dataErrorFilePath)
    dataStringList = readCSV.read_first_nLines_csv_text_file_v2(filePath, dataTableName, fileExtension, nLines)
    if originalDataDict == {} and newDataDict == {}:
        originalDataDict = makeDD.makeNewDataDictionaryFromDataStringFile(dataTableName , dataStringList, oldDict = {})
        newDataDict = originalDataDict
    oldHeader = dataStringList[0]
    newHeader = GetNewHeader(originalDataDict, dataStringList, dataTableName)
    dataStringList[0] = newHeader
    dataTypedList = typeDataset.typeDataset_v2(dataStringList, newDataDict, dataTableName, dataErrorFilePath)
    return dataTypedList
                                    


def ReadCsvDataFile_v2(originalDataDict = {}, newDataDict = {}, dataTableName = '', readErrorFileName = ''):
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
    dataStringList = readCSV.read_csv_text_file_v2(filePath, dataTableName, fileExtension)
    if originalDataDict == {} and newDataDict == {}:
        originalDataDict = makeDD.makeNewDataDictionaryFromDataStringFile(dataTableName , dataStringList, oldDict = {})
        newDataDict = originalDataDict
    oldHeader = dataStringList[0]
    newHeader = GetNewHeader(originalDataDict, dataStringList, dataTableName)
    dataStringList[0] = newHeader
    dataTypedList = typeDataset.typeDataset_v2(dataStringList, newDataDict, dataTableName, dataErrorFilePath)
    return dataTypedList

def ReadCsvDataFileAndTransformIntoDictionaryFormat(dataDict = {}, dataTableName = '', readErrorFileName = '', keyVarNameList = []):
    '''
    Inputs
        dataDict is the dictionary containing table name, variable name and variable types (i.e. originalDict or newDict
        dataPath is the file path 
        dataTableName must be a string variable without any file extension but referring to a CSV file
        keyVarNameList is a list of key variable names in string format starting with Primary, Secondary, Tertiary ... keys
        readErrorFilePath is the read error file path relating to the use of the data dictionary to establish a variable type
        readErrorFileName is the dsired name of the read error file without any extension
        fileExtension refers to the type of file, e.g. .txt or .csv

        Note that this version does not adequately account for transition from old to new variable names.
        To correct for this problem ReadCsvDataFileAndTransformIntoDictionaryFormat_v2 as created instead
    '''
    newDict = {}
    dataTypedList = ReadCsvDataFile(dataDict, dataTableName, readErrorFileName)
    newHeader = dataTypedList[0]
    newDict = dictionaryDBUtilities.additive_nested_key_multiple_item_dictionary(newDict,keyVarNameList,dataTypedList)
    return newHeader, newDict

def ReadCsvDataFileAndTransformIntoDictionaryFormat_v2(originalDataDict = {}, newDataDict = {}, dataTableName = '', readErrorFileName = '', keyVarNameList = []):
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
    dataTypedList = ReadCsvDataFile_v2(originalDataDict, newDataDict, dataTableName, readErrorFileName)
    newHeader = dataTypedList[0]
    newDict = dictionaryDBUtilities.additive_nested_key_multiple_item_dictionary(newDict,keyVarNameList,dataTypedList)
    return newHeader, newDict

def TransformDataTypedListIntoDictionaryFormat(keyVarNameList = [], dataTypedList = [], newDict = {}):
    '''
    Inputs
        newDict is an existing dataset already in a dictionary format - usually assumed to be empty to begin with
        dataTypedList is a dataset that has been brought into the Python environment with variables transformed into the correct data types
        keyVarNameList is a list of key variable names in string format starting with Primary, Secondary, Tertiary ... keys
    '''
    newHeader = dataTypedList[0]
    newDict = dictionaryDBUtilities.additive_nested_key_multiple_item_dictionary(newDict,keyVarNameList,dataTypedList)
    return newHeader, newDict



def ReadXVarSelv1XorYVariableList(dataDict = {}, varSelCriteria = 'Y', dataTableName = 'XVARSELV1', readErrorFileName = 'ERROR-CHECK-XVARSELV1'):
    '''
    '''
    varSelvTypedList = ReadCsvDataFile(dataDict, dataTableName, readErrorFileName)
    end_i = len(varSelvTypedList)
    varSelList = []
    for i in range(0,end_i,1):
        if varSelvTypedList[i][2] == varSelCriteria:
            newVar = varSelvTypedList[i][1]
            varSelList.append(newVar)   
    return varSelList

def createNewListFromSelectVariableListAndIdList(keyVarNameList = [], selectVarList = [], typedList = []):
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

def createSelectVariableListFromXvarselv1TypedDict(varSelTypedDict = {}, varSelectCriteria = 'Y'):
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


def getSelectVariableMeanAndSdev(varSetNo = 0, varNameList = [], lviTypedDict = {}):
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


def getNormalizedAndNonNormalizedVariableStatistics(varSetNo = 0, varNameList = [], lviTypedDict = {}, ystatsDict = {}):
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


def getVariableNameColumnNumbers(selectNameList=[], header = []):
    newColumnNumberList = []
    for selName in selectNameList:
        colNo = header.index(selName)
        newColumnNumberList.append(colNo)
    return newColumnNumberList

def checkForMissingVariableNameInVariableList(sourceList=[], newList=[]):
    '''
    '''
    for varName in newList:
        if not varName in sourceList:
            print 'variable name', varName, 'missing from sourceList'
    return

def joinOneDListBToRightOfOneDListA(listA1D = [], listB1D = []):
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

def removeItemsInOneDListBFromOneDListA(listA1D=[], listB1D=[]):
    '''
    '''
    newListA1D = deepcopy(listA1D)
    for item in listB1D:
        if item in newListA1D:
            itemNo = newListA1D.index(item)
            del newListA1D[itemNo]
    return newListA1D

def joinItemsInOneDListBExcludingThoseInOneDListCToOneDListA(listA1D = [], listB1D = [], listC1D = []):
    '''
    '''
    newListB1D = removeItemsInOneDListBFromOneDListA(listB1D, listC1D)
    newListA1D = joinOneDListBToRightOfOneDListA(listA1D, newListB1D)
    return newListB1D

def joinTwoDListBToRightOfTwoDListA(listA2D = [[]], listB2D = [[]]):
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

def createNewListFromSelectColumnNumbersIn2DList(originalList = [[]], selectColList = []):
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

def addIndexToRowsOnLeftSideOfArray(xArray = [[]]):
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

def appendListB2DToBottomOfListA2D(listA2D = [], listB2D = []):
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

def addHeaderListToDataList(myHeader, myData):
    newList = [myHeader]
    for lineItem in myData:
        newList.append(lineItem)
    return newList

def identifyUniqueValuesInAColumnofNumbers(dataList = [[]], colNo = 0):
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

def makeACopyOfD2List(D2List = [[]]):
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

def makeACopyOfD1List(D1List = []):
    '''
    '''
    myNewList = []
    end_i = len(D1List)
    for i in range(0,end_i,1):
        newVarValue = D1List[i]
        myNewList.append(newVarValue)
    return myNewList
            
def calculateVariableWeights(varSet = 0, bwrTypedDict = {}, inputVarWeights = False, squareWeights = False, inverseWeights = False, constrainWeightsToAddToOne = False):
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

def applyWeights(weightList = [],variableArray = [[]]):
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


def calculateVariableWeights_v2(varSet=0, zvarStatDict = {}, zvarDict = {}, uidList = []):
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

def getNewType(variable):
    NewType = ''
    if type(variable) == IntType:
        NewType = 'integer'
    else:
        if type(variable) == FloatType:
            NewType = 'float'
        else:
            NewType = 'string'
    return NewType


def runFuzzyCMeansClassification(dataKeyVarNameList = [],dataKeyList = [], dataSelectVarNameList = [],dataTypedSubsetList = [[]]):
    '''
    '''
    #
    fuzzyInit = readCSV.read_csv_text_file_v2(filePath, 'FUZZYC_INITIALIZATION', '.csv')
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

    printFilePathClass = filePath + 'FCLASS.csv'
    addToDataMachette20121026.printList2D(finalClassList,printFilePathClass,'OVERWRITE')
    printFilePathCentroid = filePath + 'FCENTROID.csv'
    addToDataMachette20121026.printList2D(finalCentroidList,printFilePathCentroid,'OVERWRITE')
    return

def runFuzzyCMeansClassification_v2(dataKeyVarNameList = [],dataKeyList = [], dataSelectVarNameList = [],dataTypedSubsetList = [[]]):
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
        minError = input("\n Enter new m-value and then press ENTER ... ")
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
            newClassList = createNewListFromSelectColumnNumbersIn2DList(classList, [1])
            classListHeader = [newClassLabel]
            updatedHeader = joinOneDListBToRightOfOneDListA(updatedHeader, classListHeader)
            classDataList = joinTwoDListBToRightOfTwoDListA(classDataList, newClassList)
        centroidList = addIndexToRowsOnLeftSideOfArray(centroidList)
        centroidList = addListOfNumbersToLeftSideOfArray(centroidList, [nGroups])
        newCentroidList = appendListB2DToBottomOfListA2D(newCentroidList, centroidList)
    
    finalClassList = addHeaderListToDataList(updatedHeader, classDataList)
    finalCentroidList = addHeaderListToDataList(centroidHeader, newCentroidList)

    printFilePathClass = filePath + 'FCLASS.csv'
    addToDataMachette20121026.printList2D(finalClassList,printFilePathClass,'OVERWRITE')
    printFilePathCentroid = filePath + 'FCENTROID.csv'
    addToDataMachette20121026.printList2D(finalCentroidList,printFilePathCentroid,'OVERWRITE')
    return


def computeXXCovarianceMatrix(varArray1):
    '''
    Array has variables listed in rows
    and observations in columns
    '''
    varArrayT = numpy.transpose(varArray1)
    covArray = numpy.cov(varArrayT)
    return covArray


def convertDbfFileToCsvFile(dbfFileName = '', newCsvFileName = '', newDataDictFileName = ''):
    '''
    This is a function to convert a dbf file into a csv file format.
    It uses dbf.py in site tools to recover the original data.
    It assumes that the first field in each record is a unique ID and
    that the remaining fields are associated with that unique ID. It then
    '''
    from dbfpy import dbf
    
    printFilePath = filePath + newCsvFileName + '.csv'
    printDictFilePath = filePath + newDataDictFileName + '.csv'
    dbfFilePath = filePath + dbfFileName + '.dbf'
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

def assignVariableSetZscoresToObservations(dfuncTypedList = [], dfuncTypedDict = {}, lviTypedDict = {}, columnNo = 0, fileName = '', batchNo = 0, printFlag = 'Yes'):
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
    #Print the file to a filePath indicated at the top of this module and to a fileName used as input into this function
    printFilePath = filePath + fileName
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


def normalizeZscores(dfuncTypedDict = {}, zvarDict = {}, zvarHeader = [], zvarKeyVarNames = [], zstatKeyVarNames = [], zstatHeader = [], fileNames = [], batchNo = 0, printFlag = 'Yes'):
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
    printFilePath1 = filePath + fileNames[0]
    printFilePath2 = filePath + fileNames[1]
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


def getNearestNeighboursInReferenceDataset(zvarDict = {}, zvarStatDict = {}, bwrTypedDict = {}, kNN = 1, zscores = False, inputVarWeights = False, squareWeights = False, inverseWeights = False, constrainWeightsToAddToOne = False, fileNameModifier = 'Z', batchNo = 0, printFlag = 'Yes'):
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
    kNNMPrintFilePath = filePath + newNNMFile                       #Mahalanobis print file path
    newNNEFile = fileNameModifier + 'NNE.csv'
    kNNEPrintFilePath = filePath + newNNEFile                       #Euclidean distance file path
    newNNAFile = fileNameModifier + 'NNA.csv'
    kNNAPrintFilePath = filePath + newNNAFile                       #Absolute distance file path
    newCOVFile = fileNameModifier + 'COV.csv'
    covPrintFileName = filePath + newCOVFile                        #Covariance Matrix file path
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

def getZNearestNeighbourRMSE(nnDict = {}, varSelTypedDict = {}, lviTypedDict = {}, kNN = 1, fileNameModifier = 'ZM', rule = 'M', batchNo = 0, printFlag = 'Yes'):
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
    rmseFilePath = filePath + newRMSEFile                           #Create the RMSE output file pathname
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

def GetSpeciesList(myTypedDict = {},spColumnNames = []):
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


def GetSpeciesListFromPlotAndTreeData(myTypedDict = {},spColNamesList = []):
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

def GetSpeciesCodesFromFileOrAssigneNewSpeciesCodes(myTreeDict = {}, spColNameslList = [], spTableName = 'SPDICT', dataDictType = 'TWOKEY'):
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
            A data file with name spTableName and file extension .csv written to dataFilePath (i.e. location of Rwd directory
            
        Variables Returned to Main Program:
            spKeyNameList   i.e. keyVariableNames associated with the species dictionary
            spHeader        i.e. list of variable names including keyVariableNames in species dictionary
            spDict          a dictionary with the original species as the primary key as follows: {origSpecies:{'NEWSP: newSp}}
            newSpList       a list containing the new species assignments

    The program was first developed with COMPILE_MOF_TREE_DATASET.py

    Ian Moss
    April 17 2013
    '''
    spTableFilePath = dataFilePath + spTableName + fileExtension                                                #Create a new file path 
    readSpErrorFileName = 'ERROR_' + spTableName                                                                #Create a read error file
    spHeader = ['ORIGSP','NEWSP']                                                                               #Species file header
    spKeyNameList = ['ORIGSP']                                                                                  #List of key variable names for constructing dictionary
    newSpList = []                                                                                              #Start a list of new species
    spDict = {}
    flag = False                                                                                                #Indicates that no species translation file exists or the old file is not going to be used
    if fileUtilities.checkFileIfItExists(spTableFilePath)== 1:
        useExistingFile = 'NO'                                                                                  #File exists - set the default for using the file to NO  
        print "\n Species translation table at filepath: ", spTableFilePath
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
            spList = GetSpeciesListFromPlotAndTreeData(myTreeDict,spColNameslList)                              #Get species list from tree dictionary
        spDict = AssignNewSpeciesCodes(spList, spDict)                                                          #Get new species dictionary
        addToDataMachette20121026.initialize_header(spHeader,spTableFilePath)
        addToDataMachette20121026.print_to_nested_dictionary(spKeyNameList, spHeader, spDict, spTableFilePath)  #Print new species dictionary to spTableFilePath
    for spOrig in spDict:                                                                                       #Make a list of new tree species
        newSp = spDict[spOrig]['NEWSP']
        if not newSp in newSpList:
            newSpList.append(newSp)
        newSpList.sort()                                                                                        #Sort the list of new tree species
    return spKeyNameList, spHeader, spDict, newSpList


def AssignNewSpeciesCodes(spList = [], spDict = {}):
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

def GetStandardDataInputFiles():
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
    newDataTableName = checkForFilePath(filePath, newDataTableName, '.csv')
    keyVarNameList = raw_input("\n Input list of the KEY VARIABLE NAMES (NEWVARNAME in DICTIONARY)\n in square parenthesis, e.g. ['KEY1','KEY2'], in the order that they occur separated by commas\n and press ENTER to continue ... ")
    print "\n A read error file is created in the Admin directory to indicate problems\n in assigning certain data dictionary data types to certain fields"  
    readErrorFileName = raw_input("\n Input that name of the read error file in case there are errors\n without .csv extensions and without '' and press ENTER ... ")
    return myDataDictName, newDataTableName, keyVarNameList, readErrorFileName

def GetSpeciesColumnNames():
    spColumnNames = raw_input("\n Enter list of species column names, e.g. ['SP1_CD','SP2_CD']\n and then press ENTER ... ")
    return spColumnNames

def GetSpeciesPercentColumnNames():
    spPcntColumnNames = raw_input("\n Enter list of species percentage column names, e.g. ['SP1_PCT','SP2_PCT']\n and then press ENTER ... ")
    return spPcntColumnNames

def checkForFilePath(filePath = '', tableName = '', fileExtension = '.txt'):
    '''
    '''
    newFilePath = filePath + tableName + fileExtension
    if os.path.exists(newFilePath):
        flag = True
    else:
        flag = False
    if flag == False:
        while flag == False:
            print '\n There is no fileName', tableName, 'in filePath', filePath, 'with file extension', fileExtension
            tableName = raw_input(' Please input new fileName without filePath or file extension and press ENTER ... ')
            newFilePath = filePath + tableName + fileExtension
            if os.path.exists(newFilePath):
                flag = True
            else:
                flag = False
        print '\n FileName', tableName, 'FOUND IN FILEPATH', filePath, 'with file extension', fileExtension
        raw_input (' Press ENTER to continue ... ')
    return tableName

 
def getTargetDatasetNearestNeighboursForManyVarsets(maxKNN = 1, varSetList = [], targetTypedDict = {}, targetHeader = [], refTypedDict = {}, \
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
        printFilePath = filePath + printFileName + str(varSet) + '.csv'
        addToDataMachette20121026.deleteFileIfItExists(printFilePath)
        nnDict, nnHeader, nnKeyNameList = getTargetDatasetNearestNeighbousForSingleVarsetsUsingZScores(maxKNN, varSet, targetTypedDict, targetHeader, refTypedDict, \
                                                     refHeader, dfuncTypedDict, zNorm, printFilePath)
    return nnDict                                                   
    

def getTargetDatasetNearestNeighbousForSingleVarsetsUsingZScores(maxKNN = 1, varSet = 1, targetTypedDict = {}, targetHeader = [], refTypedDict = {}, \
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


def assignZScoresToDictionarDataset(myTypedDict = {}, varSet = 1, dfuncTypedDict = {}):
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

def computeVariableMeansAndStandardDeviations(myDict = {}):
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

def compileTargetNearestNeighbourYStatistics(targetHeader = [], targetTypedDict = {}, lvinewTypedDict = {}, yVarNameList = [], nnTargetTableNo = '0'):
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

def initializeFilePath(newFileName = '', newFileType = '.csv'):
    newFilePath = dataFilePath + newFileName + newFileType
    return newFilePath


def initializeHeader(newFileHeader = [], newFilePath = ''):
    '''
    '''
    addToDataMachette20121026.initialize_header(newFileHeader,newFilePath)
    return

def addDataToFile(printFilePath = '', keyVarNameList = [], header=[], dataTypedDict = {}):
    addToDataMachette20121026.check_for_filepath_then_print(printFilePath, keyVarNameList, header, dataTypedDict)
    return

def readDataStringListHeader(table_name = ''):
    '''
    '''
    newHeader = readCSV.read_csv_text_file_header_v2(dataFilePath,table_name, fileExtension)
    return newHeader

def createNewDataDictionaryFromFile(dataTableName = '', printTypes = 'YES', nLines = 1000):
    '''
    This routine creates a data dictionary including a list of data types based
    on the first nLines (e.g. 1000) for the dataTableName given the filePath and
    fileExtension attached to this module.  printTypes = 'YES' provides a listing
    of the variable names in the file header and the data types assigned based on
    the first nLines in the file - as output in the IDE to enable the user to check
    that everything is ok.  This is created directly from from a file instead of a
    string table that has already been loaded into memmory for cases where the file
    size is too big to hold in  memory.
    '''
    oldDict, newDict = makeDD.makeNewDataDictionaryFromLargeDataStringFile(dataTableName, filePath, fileExtension, printTypes, nLines)
    return oldDict, newDict

def createPivotTable(dataTableName = [], dataDict = {}, keyRowVarNameList = [], keyColumnVarName = '', keyVarValueName = '', nObs = -1, nnTargetTableNo = 0):
    '''
    '''
    print '\n Start identifying column variables in pivot table'
    print '', time.ctime()
    file_path = fileUtilities.newFilePath_v2(filePath, dataTableName, fileExtension)              #Input filePath
    newDataTableName = 'TNNSTATP' + str(nnTargetTableNo)                            #Initialize print file name including target table number
    if keyVarValueName == 'MEAN':
        newDataTableName = newDataTableName + '_MEAN'
    if keyVarValueName == 'SDEV':
        newDataTableName = newDataTableName + '_SDEV'
    print '\n ', newDataTableName, '.csv file is being created in Rwd directory'
    newFilePath = fileUtilities.newFilePath_v2(filePath, newDataTableName, fileExtension)
    readErrorFileName = 'ERROR_' + dataTableName
    readErrorFilePath = fileUtilities.newFilePath_v2(filePath, readErrorFileName, fileExtension)
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
                print ' dataTableName filepath is:', file_path
                print ' keyColumnVarName:', keyColumnVarName, 'not found in header'
                print ' header:', header
                keyColNo = 'none'
            else:
                keyColNo = header.index(keyColumnVarName)
            #Get the column numbers holding the key variables to establish a unique set of rows, keyRowNoList
            for keyRowVarName in keyRowVarNameList:
                if not keyColumnVarName in header:
                    print ' Error in routineLviApplications.createPvotTable()'
                    print ' dataTableName filepath is:', file_path
                    print ' keyRowVarName:', keyRowVarName, 'not found in header'
                    print ' header:', header
                    keyRowNoList.append('none')
                else:
                    keyRowNo = header.index(keyRowVarName)
                    keyRowNoList.append(keyRowNo)
            #Get the column number, keyVarValueNo, for assigning values to each of the variable names in the keyColNo
            if not keyVarValueName in header:
                print ' Error in routineLviApplications.createPvotTable()'
                print ' dataTableName filepath is:', file_path
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
                
def assignTargetObservationsTokNearestNeighboursUsingEuclideanDistance(targetKeyVarNameList = [], targetKeyList = [[]], targetTypedSubsetList = [[]], refKeyList = [[]], refTypedSubsetList = [[]], kNN = 1):
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
            
def getMeanAndStandardDeviationFor2DList(statsTableName = '', varNameList = [], dataTypedList = [], statsDict = {}):
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
                   
def normalizeVariableDataset(dataTypedList = [], varNameList =[], statsTableName = '', statsDict = {}):
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
                                 
def printList2DWithSeparateVarNameListAndKeyVarNameListAndValues(varNameList = [], varList2D = [[]], keyVarNameList = [], keyVarValueList = [[]],  tableName = ''):
    '''
    '''
    printFilePath = dataFilePath + tableName + '.csv'
    printFile = open(printFilePath, 'w')
    newHeader = joinOneDListBToRightOfOneDListA(keyVarNameList, varNameList)
    addToDataMachette20121026.compilePrintLineFromList(newHeader, newHeader, printFile)
    nObs = len(keyVarValueList)
    for obsNo in range(0, nObs,1):
        obsList = joinOneDListBToRightOfOneDListA(keyVarValueList[obsNo], varList2D[obsNo])
        addToDataMachette20121026.compilePrintLineFromList(obsList, newHeader, printFile)
    return

def printNestedDictionary(keyVarNames = [], header = [], dataTypedDict = {}, tableName = ''):
    '''
    '''
    printFilePath = dataFilePath + tableName + '.csv'
    addToDataMachette20121026.initialize_header(header, printFilePath)
    addToDataMachette20121026.print_to_nested_dictionary(keyVarNames,header, dataTypedDict, printFilePath)
    return

def printList2DWithHeader(varList2D =[[]], tableName = ''):
    '''
    '''
    printFilePath = dataFilePath + tableName + '.csv'
    addToDataMachette20121026.printList2D(varList2D, printFilePath, printOption = 'OVERWRITE')
    return
                
def createUniqueIdLinkTable(keyVarNameList = [], myDataDict = {}):
    '''
    '''
    linkKeyComboValueList = innerJoinDictDBs.getDictKeySetValuesList(myDataDict,keyVarNameList)
    linkKeyVarNamesList, linkDict = innerJoinDictDBs.createNewLinkTableIndexFromKeyComboList(keyVarNameList, linkKeyComboValueList)
    linkHeader = joinOneDListBToRightOfOneDListA(linkKeyVarNamesList, keyVarNameList)
    return linkHeader, linkKeyVarNamesList, linkDict

def reassignDictKeysUsingLinkTable(dataDict = {}, linkDict = {}, keyVarNameList = [], mismatchNotification = 'Yes', tableName = ''):
    '''
    '''
    revisedDict = innerJoinDictDBs.extractDictDBDataUsingLinkDictTable(dataDict, linkDict, msimatchNotification, tableName)
    return revisedDict
                                   
def collapseDictKeysUsingLinkTableData(dataDict = {}, linkDict = {}, keyVarNameList = [], mismatchNotification = 'Yes', tableName = ''):
    '''
    '''
    revisedDict = innerJoinDictDBs.collapseDictKeysUsingALinkTable(dataDict, linkDict, keyVarNameList, mismatchNotification, tableName)
    return revisedDict

def removeMoFPspPlotNameBlankAndReestablishKeys(linkDict= {}):
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

def SelectCertainTreeClassesForPSPTreeLists(treeDict={}, treeDictColName = '', treeAttrList = []):
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
                
def ReplaceTreeSpeciesInPlotDataWithNewSpecies(treeDict={},spDict={}, spColNamesList=[]):
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


def CompilePerHectarePlotLevelStatisticsBySpeciesFromTreeLists(treeDict = {}, spColNamesList = [], mySpList = [], spVarValuesNamesList = []):
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

def CompilePerHectarePlotLevelStatisticsFromTreeLists(treeDict={}, spVarValuesNamesList = []):
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

def CompilePlotLevelSpeciesPercentages(plotDict = {},speciesList = []):
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


def SubstituteNewPspSpeciesForOldPspSpeciesNames(x=[]):
    '''
    Note that the tree dictionary contains a unique ID for each plot and has a list of
    trees as secondary keys.
    '''
    return
           
def calculateLorenzIndices(linkDict = {}, treeDict = {}, rankVarName = '', countVarName = '', sizeVarName = ''):
    '''
    '''
        
    return
                
            
            
        
        
        
    
    
