'''
Set file paths
'''
import sys

#Identify admin code directory
adminPath = 'D:\\Rwd\\Python\\Admin\\'
filePath = 'D:\\Rwd\\'
dataFilePath = 'D:\\Rwd\\'
dictFilePath = 'D:\\Rwd\\Python\\DATDICT\\'
fileExtension = '.csv'
readErrorFilePath = 'D:\\Rwd\\Python\\PyReadError\\'

#Add directory to sys.path 
sys.path.append(adminPath)


import makeDD
import readCSV
import typeDataset
import fuzzyC_v2
import PRINTv1
import addToDataMachette20121026
import dictionaryDBUtilities
import numpy
import time
import datetime
from dbfpy import dbf
from types import *

from scipy import linalg


def ReadLviDataDictionary(filename = 'PyRDataDict'):
    '''
    Read LVI data dictionary contained in
    \\Rwd\\Python\\DATDICT\\ ... directory with filename
    PyRDataDict.csv

    Note that this dictionary estblishes variable names and types. 
    '''
    originalDict, newDict = makeDD.dataDictionaryType_21(dictFilePath,filename, fileExtension)
    return originalDict, newDict

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
    '''
    newDict = {}
    dataTypedList = ReadCsvDataFile(dataDict, dataTableName, readErrorFileName)
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
