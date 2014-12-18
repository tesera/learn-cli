'''
'''
import sys

print 'Running COMBINE_EVALUATION_DATASETS.py'

#Identify code directory and data directory
adminPath = 'D:\\Rwd\\Python\\Admin\\'
inputDataPath = 'D:\\Rwd\\'
readErrorFilePath = 'D:\\Rwd\\Python\\PyReadError\\'
dictFilePath = 'D:\\Rwd\\Python\\DATDICT\\'
sys.path.append(adminPath)
sys.path.append(inputDataPath)
printFilePath = inputDataPath + 'ASSESS.csv'

import makeDD
import dictionaryDBUtilities
import readCSV
import typeDataset
import PRINTv1
import innerJoinDictDBs

#Get Data Dictionary
filename = 'PyRDataDict'
fileExtension = '.csv'
originalDict, newDict = makeDD.dataDictionaryType_21(dictFilePath,filename, fileExtension)

#Get CTABSUM 
ctabTableName = 'CTABSUM'
errorFilePath = readErrorFilePath + 'ERROR-CHECK-COMBINE1.txt'
ctabKeyVarnames = ['VARSET']
fileExtension = '.csv'
ctabStringList = readCSV.read_csv_text_file_v2(inputDataPath, ctabTableName, fileExtension)
ctabTypedList = typeDataset.typeDataset_v2(ctabStringList, originalDict, ctabTableName, errorFilePath)
#Create CTABSUM data dictionary
ctabDict = {}
ctabHeader = ctabTypedList[0]
ctabDict = dictionaryDBUtilities.additive_nested_key_multiple_item_dictionary(ctabDict,ctabKeyVarnames,ctabTypedList)
ctabDictUniqueKeyList = innerJoinDictDBs.getDictKeySetValuesList(ctabDict, ctabKeyVarnames)
#
#Get MinMaxCorr
corrTableName = 'MINMAXCOR'
errorFilePath = readErrorFilePath + 'ERROR-CHECK-COMBINE2.txt'
corrKeyVarnames = ['VARSET']
fileExtension = '.csv'
corrStringList = readCSV.read_csv_text_file_v2(inputDataPath, corrTableName, fileExtension)
corrTypedList = typeDataset.typeDataset_v2(corrStringList, originalDict, corrTableName, errorFilePath)
#Create CTABSUM data dictionary
corrDict = {}
corrHeader = corrTypedList[0]
corrDict = dictionaryDBUtilities.additive_nested_key_multiple_item_dictionary(corrDict,corrKeyVarnames,corrTypedList)
corrDictUniqueKeyList = innerJoinDictDBs.getDictKeySetValuesList(corrDict, corrKeyVarnames)
#
#Joining ctabDict and corrDict
innerJoinKeyValues = innerJoinDictDBs.getCommonInnerJoinKeyValueList(corrDictUniqueKeyList, ctabDictUniqueKeyList)
combDict = innerJoinDictDBs.extractDictDBForKeySetsList(corrDict,ctabDict,innerJoinKeyValues)
combHeader = innerJoinDictDBs.createUniqueListFromTwoNewLists(corrHeader,ctabHeader)
#
#Get POSTERIOR 
postTableName = 'POSTERIOR'
errorFilePath = readErrorFilePath + 'ERROR-CHECK-COMBINE3.txt'
postKeyVarnames = ['VARSET']
fileExtension = '.csv'
postStringList = readCSV.read_csv_text_file_v2(inputDataPath, postTableName, fileExtension)
postTypedList = typeDataset.typeDataset_v2(postStringList, originalDict, postTableName, errorFilePath)
#Create POSTERIOR data dictionary
postDict = {}
postHeader = postTypedList[0]
postDict = dictionaryDBUtilities.additive_nested_key_multiple_item_dictionary(postDict,postKeyVarnames,postTypedList)
postDictUniqueKeyList = innerJoinDictDBs.getDictKeySetValuesList(postDict, postKeyVarnames)
#
#Joining combDict and postDict
innerJoinKeyValues = innerJoinDictDBs.getCommonInnerJoinKeyValueList(innerJoinKeyValues, postDictUniqueKeyList)
combDict = innerJoinDictDBs.extractDictDBForKeySetsList(combDict,postDict,innerJoinKeyValues)
combHeader = innerJoinDictDBs.createUniqueListFromTwoNewLists(combHeader,postHeader)
#
#Get XVARSELV with blank dictionary
xvarTableName = 'XVARSELV'
errorFilePath = readErrorFilePath + 'ERROR-CHECK-COMBINE4.txt'
xvarKeyVarnames = ['VARSET']
fileExtension = '.csv'
xvarStringList = readCSV.read_csv_text_file_v2(inputDataPath, xvarTableName, fileExtension)
#Create a new data dictionary
xvarDataDict = makeDD. makeNewDataDictionaryFromDataStringFile(xvarTableName, xvarStringList, {})
xvarTypedList = typeDataset.typeDataset_v2(xvarStringList, xvarDataDict, xvarTableName, errorFilePath)
#Create XVARSELV data dictionary
xvarDict = {}
xvarHeader = xvarTypedList[0]
xvarDict = dictionaryDBUtilities.additive_nested_key_multiple_item_dictionary(xvarDict,xvarKeyVarnames,xvarTypedList)
xvarDictUniqueKeyList = innerJoinDictDBs.getDictKeySetValuesList(xvarDict, xvarKeyVarnames)
#
#Joining combDict and xvarDict
innerJoinKeyValues = innerJoinDictDBs.getCommonInnerJoinKeyValueList(innerJoinKeyValues, xvarDictUniqueKeyList)
combDict = innerJoinDictDBs.extractDictDBForKeySetsList(combDict,xvarDict,innerJoinKeyValues)
combHeader = innerJoinDictDBs.createUniqueListFromTwoNewLists(combHeader,xvarHeader)
assessDictKeyVarnames = ['VARSET']
#
#Print ASSESS
PRINTv1.initialize_header(combHeader,printFilePath)
PRINTv1.print_to_nested_dictionary(assessDictKeyVarnames,combHeader,combDict, printFilePath)

print 'Created Summary Statistic File: ASSESS.csv'

raw_input("\n Press ENTER to Close This Session ... ")
