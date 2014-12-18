'''
This is a program to convert a dbf file into a csv file format.
It uses dbf.py in site tools to recover the original data.
It assumes that the first field in each record is a unique ID and
that the remaining fields are associated with that unique ID. It then


'''
import sys
import datetime
from dbfpy import dbf
from types import *

adminpath = 'D:\\Rwd\\Python\\Admin\\'
filepath = 'D:\\Rwd\\'
printFilepath= r'E:\Rwd\MyDbfFile.txt'
printDictionaryFilepath = r'E:\Rwd\MyDbfFileDictionary.txt'

sys.path.append(adminpath)
sys.path.append(filepath)

import PRINTv1
import READv1

#Delete MyDbfFile.txt and MyDbfFileDictionary.txt either one of them exist
#in the chosen directories (printFilepath and printDictionaryFilepath).
PRINTv1.deleteFileIfItExists(printFilepath)
PRINTv1.deleteFileIfItExists(printDictionaryFilepath)

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
        
dbf = dbf.Dbf('D:\\Rwd\\LVIVRI_out.dbf', True)
header = ['NEWID']
keyList = ['NEWID']
NewDict = {}
#Initialize NewDict Dictionary
DictionaryHeader = ['variable','table', 'type']
DictionaryKeyList = ['table','variable']
NewDictDictionary = {'NewTable':{}}
printCount = 1000
i = 1
for rec in dbf:
    #print rec
    j = 1
    #Update MewDict with key variable NEWID = i
    NewDict.update({i:{}})
    for fldName in dbf.fieldNames:
        if i == 1:
            NewType = ''
            #Create NewDict Header
            header.append(fldName)
            #Create NewDict Dictionary
            NewType = getNewType(rec[fldName])
            NewDictDictionary['NewTable'].update({fldName:{'type':NewType}})
        #Get Key Variable Value             
        NewVarValue = rec[fldName]
        NewDict[i].update({fldName:NewVarValue})
        j = j + 1
    i = i + 1
    #if i == 2: break
    if i == printCount:
        print printCount
        printCount = printCount + 1000
        #Print NewDict
        PRINTv1.check_for_filepath_then_print(printFilepath,keyList,header,NewDict)
        NewDict = {}
#Print NewDictDictionary
PRINTv1.check_for_filepath_then_print(printDictionaryFilepath,DictionaryKeyList,DictionaryHeader,NewDictDictionary)
#Print blast remaining records in NewDict
PRINTv1.check_for_filepath_then_print(printFilepath,keyList,header,NewDict)
#Print number of records
print i-1
        
