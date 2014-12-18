'''
'''
from types import *
import numpy
import os
from operator import concat

def new_file_path(filepath, filename):
    FileKind = '.txt'
    newFilename = concat(filename, FileKind)
    newFilePath = concat(filepath, newFilename)
    return newFilePath

def initialize_header(header,printFilepath):
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

def print_to_nested_dictionary(keyList,header,myFile, printFilepath):
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
            print_nested_dictionary_printline(keyList,keyVar,header,remainingVar,printFile)
            break
        else:
            if numberOfKeys == 1:
                remainingVar = myFile[key0]
                keyVar = [key0]
                print_nested_dictionary_printline(keyList,keyVar,header,remainingVar,printFile)
            else:
                for key1 in myFile[key0]:
                    if numberOfKeys == 2:
                        remainingVar = myFile[key0][key1]
                        keyVar = [key0,key1]
                        print_nested_dictionary_printline(keyList,keyVar,header,remainingVar,printFile)
                    else:
                        for key2 in myFile[key0][key1]:
                            if numberOfKeys == 3:
                                remainingVar = myFile[key0][key1][key2]
                                keyVar = [key0,key1,key2]
                                print_nested_dictionary_printline(keyList,keyVar,header,remainingVar,printFile)
                            else:
                                for key3 in myFile[key0][key1][key2]:
                                    if numberOfKeys == 4:
                                        remainingVar = myFile[key0][key1][key2][key3]
                                        keyVar = [key0,key1,key2,key3]
                                        print_nested_dictionary_printline(keyList,keyVar,header,remainingVar,printFile)
                                    else:
                                        for key4 in myFile[key0][key1][key2][key3]:
                                            if numberOfKeys == 5:
                                                remainingVar = myFile[key0][key1][key2][key3][key4]
                                                keyVar = [key0,key1,key2,key3,key4]
                                                print_nested_dictionary_printline(keyList,keyVar,header,remainingVar,printFile)
                                            else:
                                                for key5 in myFile[key0][key1][key2][key3][key4]:
                                                    if numberOfKeys == 6:
                                                        remainingVar = myFile[key0][key1][key2][key3][key4][key5]
                                                        keyVar = [key0,key1,key2,key3,key4,key5]
                                                        print_nested_dictionary_printline(keyList,keyVar,header,remainingVar,printFile)
                                                    else:
                                                        for key6 in myFile[key0][key1][key2][key3][key4][key5]:
                                                            if numberOfKeys == 7:
                                                                remainingVar = file[key0][key1][key2][key3][key4][key5][key6]
                                                                keyVar = [key0,key1,key2,key3,key4,key5,key6]
                                                                print_nested_dictionary_printline(keyList,keyVar,header,remainingVar,printFile)
                                                            else:
                                                                print 'The number of keys in print_to_nested_dictionary is exceeded'
                                                                print 'number of keys:', numberOfKeys
    printFile.close()
    return

def print_nested_dictionary_printline(keyVarnames,keyVar,header,remainingVar,printFile):
    printline = ''
    floatFormat = '%0.3f,'
    end_i = len(keyVar)
    for varName in header:
        flag = 'False'
        if remainingVar.has_key(varName):
            varValue = remainingVar[varName]
            printline = update_printline(varValue, printline, floatFormat, varName)
            flag = 'True'
        else:
            for i in range(0,end_i):
                if varName == keyVarnames[i]:
                    varValue = keyVar[i]
                    printline = update_printline(varValue, printline, floatFormat, varName)
                    flag = 'True'
                    break
            if flag == 'False':
                print 'varName:', varName, 'not found in keyVarnames or header in print_nested_dictionary_printline'
                print 'keyVarnames or header:', keyVarnames, 'keyVarValues:', keyVar
    printline = printline.rstrip(',')
    print >> printFile, printline
    return

def update_printline(varValue, printline, floatFormat, varName):
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
            else:
                if varType == numpy.int32:
                    printline = printline + '%i' % varValue
                else:
                    if varType == FloatType or varType == numpy.float64:
                        printline = printline + floatFormat% varValue
                    else:
                        print 'type of variable varName', varName, 'with value:', varValue, 'is:', varType,
                        print 'no such type provided for in update_printline'
    return printline

def check_for_filepath_then_print(filepath,keyList,fileHeader,dictionaryName):
    '''
    This subroutine checks a filepath to see if it exists. If not it creates
    a new file with the first line as the fiel header. In any event it writes
    the data in the nested dictionary file (dictionaryName) to the file in
    the appropriate format.
    '''
    if os.path.exists(filepath):
        print_to_nested_dictionary(keyList,fileHeader,dictionaryName,filepath)
    else:
        initialize_header(fileHeader,filepath)
        print_to_nested_dictionary(keyList,fileHeader,dictionaryName,filepath)
    return

def createCommaDelimmitedPrintLine(printStringList):
    '''
    This function takes a list of variables - all strings -
    and combines them into a single, comma delimitted string
    suitable for printig to a text (.txt) file.

    Nov 10, 2006
    Ian S Moss
    '''
    j = 0
    for item in printStringList:
        end_j = len(printStringList)-1
        if j == 0 :
            printLine = item +','
            j=j+1
        else:
            if j == end_j:
                printLine = printLine + item
            else:
                printLine = printLine + item + ','
            j = j + 1
            
    printLine.rstrip(',')
    return printLine

def deleteFileIfItExists(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)
    return

def print_printline_to_file(printLineString,printFilepath):
    '''
    This function takes a preformated printline, opens a pre-existing file
    and writes the line to the file.
    '''
    newFile = open(printFilepath,'a')
    print >> newFile, printLineString
    newFile.close()
    return

def convert_dictionary_to_list_format_and_generate_print_line(header, simpleDict, floatFormat, printFilepath):
    printList = []
    printline = ''
    for keyVar in header:
        if simpleDict.has_key(keyVar):
            printList.append(simpleDict[keyVar])
        else:
            print 'Variable Name', keyVar, 'could not be found when converting dictionary to list format in PRINT module'
    printline = update_printline(printList, printline, floatFormat, 'vaName in printList')
    print_printline_to_file(printline,printFilepath)
    return

def convert_varmapDict_to_ordinary_varDict_and_print_to_VARDICT(filepath, varmapDict, newTableName):
    table_name = 'VARDICT'
    file_path = new_file_path(filepath, table_name)
    temp_file =open (file_path,'w')
    header = 'Variable,Table,Type,Description'
    print >> temp_file, header
    keyVarList = varmapDict.keys()
    for newKey in keyVarList:
        variableName = newKey
        variableType = varmapDict[newKey]['TYPE']
        variableDefinition = varmapDict[newKey]['DEFINITION']
        printLine = '%s,%s,%s,%s' % (variableName, newTableName, variableType, variableDefinition)
        print >> temp_file, printLine
    temp_file.close()
    return

def convert_varmapDict_to_ordinary_varDict_and_print_to_VARDICT_v2(filepath, varmapDict, newTableName, new_dict_name):
    '''
    This function uses the PROGVAR key varmapDict as input to developint the new_dict_name
    '''
    file_path = new_file_path(filepath, new_dict_name)
    temp_file =open (file_path,'w')
    header = 'Variable,Table,Type,Description'
    print >> temp_file, header
    keyVarList = varmapDict.keys()
    for newKey in keyVarList:
        variableName = newKey
        variableType = varmapDict[newKey]['TYPE']
        variableDefinition = varmapDict[newKey]['DEFINITION']
        printLine = '%s,%s,%s,%s' % (variableName, newTableName, variableType, variableDefinition)
        print >> temp_file, printLine
    temp_file.close()
    return
