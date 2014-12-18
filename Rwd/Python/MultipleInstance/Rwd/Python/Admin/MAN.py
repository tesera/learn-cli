'''
The purpose of this module is to store standard conversion routines:
e.g.

1. Produce a new list from an original list so that a change in
the new list is not replicated in the original list.

2. Make a list from a dictionary given the variable names.

'''

from types import *
from numpy import *

def append_list_items(list1,list2):
    for item in list2:
        list1.append(item)
    return list1

def get_list_from_dictionary(varNames, someDict):
    '''
    The dictionary is in the following format:
    {'variable':value,...}
    The varNames are as follows:
    ['variable1','variable2',...]   
    '''
    newList = []
    for variable in varNames:
        newVar = someDict[variable]
        newList.append(newVar)
    return newList

def extract_dictionary_items_in_list_and_put_in_new_dictionary(list1, someDict):
    aNewDict = {}
    for item in list1:
        if someDict.has_key(item):
            aNewDict.update({item:someDict[item]})
    return aNewDict

def get_species_list(invSpeciesCodeList, spDict, varName):
    '''
    This subroutine does a species conversion where the list contains
    the key variables in the spDict (e.g. spDict[keyVariable]) and
    the varName refers to a specific variable name in the dictionary
    (e.g. spDict[keyVariable][varName].  The output is a new a species
    list relating to a specific application.
    '''
    newList = []
    for species in invSpeciesCodeList:
        if not species == '':
            newSpecies = spDict[species][varName]
        else:
            newSpecies = ''
        newList.append(newSpecies)
    return newList

def format_printline_to_specific_column_widths_plus_intervening_spaces(attribute, colWidth):
    '''
    If typeIndicator is string then left justify, otherwise right justify.
    '''
    attrLength = len(str(attribute))
    #If variable is floating point type
    if type(attribute) == FloatType:
        if attrLength > colWidth:
            newVarList = str(attribute).split('.')
            preDecimal = len(newVarList[0])+1
            if colWidth - preDecimal < 0:
                print 'Error in Man.format_printline_'
                print 'floating point variable too large (before decimal point) for column width', attribute
            else:
                newVar = str(round(attribute, colWidth - preDecimal))
                newVar = add_zeros_to_end_of_float_printVariable(newVar, colWidth)
        else:
            newVar = str(attribute)
            newVar = add_zeros_to_end_of_float_printVariable(newVar, colWidth)
    #If variable is integer type
    if type(attribute) == IntType:
        if attrLength > colWidth:
            print 'Error in Man.format_printline_'
            print 'integer variable too large for column width', attribute
        else:
            newVar = str(attribute)
            newVar = add_blanks_to_start_of_integer_or_float_printVariable(newVar, colWidth)
    #If attribute is string type
    if type(attribute) == StringType:
        if attrLength > colWidth:
            print 'Error in Man.format_printline_'
            print 'string variable too large for column width', attribute
        else:
            newVar = attribute
            newVar = add_blanks_to_end_of_string_printVariable(newVar, colWidth)
    return newVar

def format_printline_with_decimal_points_to_specific_column_widths_plus_intervening_spaces(attribute, colWidth, decimalPoints):
    '''
    If typeIndicator is string then left justify, otherwise right justify.
    '''
    attrLength = len(str(attribute))
    #If variable is floating point type
    if type(attribute) == FloatType:
        decimalIndicator = '%0.' + str(decimalPoints) + 'f'
        newVar = decimalIndicator % attribute
        attrLength = len(newVar)
        if attrLength > colWidth:
            print 'Error in Man.format_printline_with_decimal_points'
            print 'fixed decimal floating point variable too large for column width', attribute, 'col width:', colWidth
        else:
            if attrLength < colWidth:
                newVar = add_blanks_to_start_of_integer_or_float_printVariable(newVar, colWidth)
    #If variable is integer type
    if type(attribute) == IntType:
        if attrLength > colWidth:
            print 'Error in Man.format_printline_with_decimal_points'
            print 'integer variable too large for column width', attribute, 'col width:', colWidth
        else:
            newVar = str(attribute)
            newVar = add_blanks_to_start_of_integer_or_float_printVariable(newVar, colWidth)
    #If attribute is string type
    if type(attribute) == StringType:
        if attrLength > colWidth:
            print 'Error in Man.format_printline_with_decimal_points'
            print 'string variable too large for column width', attribute, 'colWidth:', colWidth
        else:
            newVar = attribute
            newVar = add_blanks_to_end_of_string_printVariable(newVar, colWidth)
    return newVar

def add_blanks_to_start_of_integer_or_float_printVariable(newVar, colWidth):
    newLength = len(newVar)
    newWidth = colWidth - newLength
    newString = ''
    if newWidth > 0:
        for i in range(1,newWidth +1, 1):
            newString = newString + ' '
        newString = newString + newVar
    else:
        newString = newVar
    return newString

def add_blanks_to_end_of_string_printVariable(initialVar, colWidth):
    newLength = len(initialVar)
    newWidth = colWidth - newLength
    newVar = initialVar
    if newWidth > 0:
        for i in range(1,newWidth +1, 1):
            newVar = newVar + ' '
    return newVar

def add_zeros_to_end_of_float_printVariable(initialVar, colWidth):
    newLength = len(initialVar)
    newWidth = colWidth - newLength
    newVar = initialVar
    if newWidth > 0:
        for i in range(1,newWidth +1, 1):
            newVar = newVar + '0'
    return newVar

def add_characters_to_start_of_string(targetStringLength,newCharachter,currentString):
    newString = ''
    lenCurrentString = len(currentString)
    newCount = targetStringLength - lenCurrentString
    for i in range(0,newCount):
        newString = newString + newCharachter
    newString = newString + currentString
    newLength = len(newString)
    if not newLength == targetStringLength:
        print 'newLength not equal to targetStringLength in MAN.add_charachters_to_start_of_string'
        print 'newString:',newString
    return newString


def create_space_delimited_printline_from_list_of_string_variables(varList):
    end_i = len(varList)
    printLine = ''
    for i in range(0,end_i-1,1):
        printLine = printLine + varList[i] + ' '
    printLine = printLine + varList[end_i-1]
    return printLine

def create_printline_from_variableList_and_column_width_list(varList,colWidthList):
    newList = []
    newVar = ''
    printLine = ''
    end_i = len(varList)
    for i in range(0, end_i,1):
        newVar = format_printline_to_specific_column_widths_plus_intervening_spaces(varList[i], colWidthList[i])
        newList.append(newVar)
    printLine = create_space_delimited_printline_from_list_of_string_variables(newList)     
    return printLine

def convert_list_of_float_variables_to_integers(varList):
    newList = []
    for item in varList:
        newVar = int(item)
        newList.append(newVar)
    return newList

def open_file_remove_header_rows_resave_close(readFilepath, writeFilepath, nRowsDelete):
    readFile = open(readFilepath, 'r')
    writeFile = open(writeFilepath, 'w')
    i = 0
    rowCount = 20000
    for line in readFile:
        newLine = ''
        if not i < nRowsDelete:
            #Remove '\n' linefeed characters
            end_l = len(line)
            for l in range(0,end_l-1,1):
                newLine = newLine + line[l]
            print >> writeFile, newLine
        i = i + 1
        if i == rowCount:
            print rowCount
            rowCount = rowCount + 20000
    print i
    readFile.close()
    writeFile.close()
    return
            
def compute_weighted_statistics(varNameList, someDict, wt):
    newDict = {}
    for varName in varNameList:
        newVarValue = someDict[varName] * wt
        newDict.update({varName:newVarValue})
    return newDict

def sum_up_weighted_dictionary_items(initDict,tempDict):
    newKeys = tempDict.keys()
    for keyVarName in newKeys:
        varValue = tempDict[keyVarName]
        if not initDict.has_key(keyVarName):
            initDict.update({keyVarName:varValue})
        else:
            previousValue = initDict[keyVarName]
            initDict[keyVarName] = previousValue + varValue
    return initDict

def divide_total_weighted_items_by_sum_of_weights(totDict, wt, varNameList):
    for varName in varNameList:
        if wt <= 0:
            totDict[varName] = 0
        else:
            previousValue = totDict[varName]
            totDict[varName] = previousValue/float(wt)
    return totDict

def get_printline_with_fixed_decimal_foating_point_variables(varHeader, varDict, colWidthList, decimalPointList):
    '''
    This module creates a fixed format printline that includes float variables with fixed decimal point formats.
    The varHeader, colWidthList and decimalPointList must all be of the same length.
    The integer and float variables will be right justified.
    The string variables will be left justified.
    '''
    printLine = ''
    varList = get_list_from_dictionary(varHeader, varDict)
    end_i = len(varList)
    for i in range(0,end_i,1):
        varValue = varList[i]
        colWidth = colWidthList[i]
        decimalPoints = decimalPointList[i]
        newStringVar = format_printline_with_decimal_points_to_specific_column_widths_plus_intervening_spaces(varValue, colWidth, decimalPoints)
        if i < end_i-1:
            printLine = printLine + newStringVar + ' '
        else:
            #No blank column separator at the end of the line
            printLine = printLine + newStringVar
    return printLine

def find_item_in_mutilevel_dictionary(someDict, KeyVarValueList, VarName):
    '''
    The KeyVarValueList must have the var values listed in the same order as the keys in someDict.
    The VarName must be in a string format and is the name of the variable to be found.
    The main advantage of this function is that it checks for the variable names in the
    KeyVarValueList and prints an error statement if it can not be found in someDict.
    June 5, 2008
    '''
    varValue = ''
    newDict = {}
    end_i = len(KeyVarValueList)
    for i in range(0,end_i,1):
        if i == 0:
            Key0 = KeyVarValueList[0]
            if someDict.has_key(Key0):
                if someDict[Key0].has_key(VarName):
                    varValue = someDict[Key0][VarName]
                    break
            else:
                print 'someDict in MAN.sum_up_dictionary_items_given_dictionary_keys_and_key_var_name'
                print ' missing Key0, KeyVarValueList:'
                print KeyVarValueList
        else:
            if i == 1:
                Key1 = KeyVarValueList[1]
                if someDict[Key0].has_key(Key1):
                    if someDict[Key0][Key1].has_key(VarName):
                        varValue = someDict[Key0][Key1][VarName]
                        break
                else:
                    print 'someDict in MAN.sum_up_dictionary_items_given_dictionary_keys_and_key_var_name'
                    print ' missing Key1, KeyVarValueList:'
                    print KeyVarValueList
            else:
                if i == 2:
                    Key2 = KeyVarValueList[2]
                    if someDict[Key0][Key1].has_key(Key2):
                        if someDict[Key0][Key1][Key2].has_key(VarName):
                            varValue = someDict[Key0][Key1][Key2][VarName]
                            break
                    else:
                        print 'someDict in MAN.sum_up_dictionary_items_given_dictionary_keys_and_key_var_name'
                        print ' missing Key2, KeyVarValueList:'
                        print KeyVarValueList
                else:
                    if i == 3:
                        Key3 = KeyVarValueList[3]
                        if someDict[Key0][Key1][Key2].has_key(Key3):
                            if someDict[Key0][Key1][Key2][Key3].has_key(VarName):
                                varValue = someDict[Key0][Key1][Key2][Key3][VarName]
                                break
                        else:
                            print 'someDict in MAN.sum_up_dictionary_items_given_dictionary_keys_and_key_var_name'
                            print ' missing Key3, KeyVarValueList:'
                            print KeyVarValueList
                    else:
                        if i == 4:
                            Key4 = KeyVarValueList[4]
                            if someDict[Key0][Key1][Key2][Key3].has_key(Key4):
                                if someDict[Key0][Key1][Key2][Key3][Key4].has_key(VarName):
                                    varValue = someDict[Key0][Key1][Key2][Key3][Key4][VarName]
                                    break
                            else:
                                print 'someDict in MAN.sum_up_dictionary_items_given_dictionary_keys_and_key_var_name'
                                print ' missing Key4, KeyVarValueList:'
                                print KeyVarValueList
                        else:
                            if i == 5:
                                Key4 = KeyVarValueList[5]
                                if someDict[Key0][Key1][Key2][Key3][Key4].has_key(Key5):
                                    if someDict[Key0][Key1][Key2][Key3][Key4][Key5].has_key(VarName):
                                        varValue = someDict[Key0][Key1][Key2][Key3][Key4][Key5][VarName]
                                        break
                                else:
                                    print 'someDict in MAN.sum_up_dictionary_items_given_dictionary_keys_and_key_var_name'
                                    print ' missing Key5, KeyVarValueList:'
                                    print KeyVarValueList
                            else:
                                if i == 6:
                                    Key6 = KeyVarValueList[6]
                                    if someDict[Key0][Key1][Key2][Key3][Key4][Key5].has_key(Key6):
                                        if someDict[Key0][Key1][Key2][Key3][Key4][Key5].has_key(VarName):
                                            varValue = someDict[Key0][Key1][Key2][Key3][Key4][Key5][VarName]
                                            break
                                else:
                                    print 'someDict in MAN.sum_up_dictionary_items_given_dictionary_keys_and_key_var_name'
                                    print ' missing Key6, KeyVarValueList:'
                                    print KeyVarValueList
                                            
    return varValue

def convert_two_lists_into_one(List1, List2):
    newList = []
    for item in List1:
        newList.append(item)
    for item in List2:
        newList.append(item)
    return newList
    
def remove_items_in_first_list_from_second_list(List1,List2):
    newList = []
    for item in List2:
        newList.append(item)
    for item in List1:
        if item in newList:
            i = newList.index(item)
            del newList[i]
    return newList

def find_list_of_items_in_zero_level_dictionary(someDict,varNameList):
    newList = []
    for name in varNameList:
        varValue = someDict[name]
        newList.append(varValue)
    return newList

def compute_euclidean_distance_between_two_lists_in_list_object(twinList):
    diff = 0
    end_i = len(twinList[0])
    for i in range(0,end_i):
        a = float(twinList[0][i])
        b = float(twinList[1][i])
        diff = diff + (a - b)**2
    diff = diff**(0.5)
    return diff

def generate_array(otherDict, varHeader):
    '''
    Note that is function generates a square matrix
    with Eclidean distances. varHeader contains a list
    of variable names in smpnDict that are to be used to
    establish the differences.  smpnDict is a dictionary
    of observations each identified by a unique id. The
    number of observations in the dictionary corresponds
    to the array order that is calculated below.

    June 2008
    '''
    print 'creating array'
    #Initialize newArray
    arrayOrder = len(otherDict)
    newArray = resize(array((0,0)),(arrayOrder,arrayOrder))
    count = 100
    
    for i in range(0,arrayOrder):
        varList = []
        firstList =(find_list_of_items_in_zero_level_dictionary(otherDict[i],varHeader))
        for j in range(i,arrayOrder):
            varList = [firstList]
            varList.append(find_list_of_items_in_zero_level_dictionary(otherDict[j],varHeader))
            diff = compute_euclidean_distance_between_two_lists_in_list_object(varList)
            newArray[i][j] = diff
            newArray[j][i] = diff
    print 'finished creating array', i, 'observations'
    return newArray

def get_statistics_from_square_matrix_given_list_of_items(someList, distMatrix):
    '''
    Note the list contains matrix rows and columns that correspond to a distance
    in each matrix and correspond to either a column or row in a data table.
    '''
    newList = []
    sumSquares = 0
    nObs = len(someList)
    for i in range(0,nObs,1):
        if i+1 == nObs:
            break
        else:
            for j in range(i+1,nObs,1):
                newList.append(distMatrix[i][j])
    newLen = len(newList)
    if newLen > 1:
        average = mean(newList)
        variance = var(newList)
        for i in range(0,newLen,1):
            sumSquares = sumSquares + ((newList[i]-average)**2)
    else:
        average = 0
        variance = 0
        sumSquares = 0
    newDict = {'nobs':nObs,'mean':average,'var':variance,'sumOfSquares':sumSquares}
    return newDict

def print_rectangular_matrix_in_columnar_format(newMatrix, thisPrintFilePath, floatFormat):
    '''
    The format describes the number of decimal places to be included
    in reporting the distance, e.g. '%0.3f' indicates floating point
    with 3 decimal places.
    '''
    newFile = open(thisPrintFilePath, 'w')
    nColumn = len(newMatrix[0])
    matrixHeader = 'ROWNO,COLNO,DIST'
    print >> newFile, matrixHeader
    i = 1
    for rowObs in newMatrix:
        j = 1
        for colNo in newMatrix[i-1]:
            printLine = '%i,%i' % (i,j)
            printLine = printLine + ',' + floatFormat % newMatrix[i-1][j-1]
            print >> newFile, printLine
            j = j + 1
        i = i + 1
    newFile.close()
    return
def find_list_of_items_in_dictionary_and_create_new_dictionary(someDict,itemList):
    '''
    someDict is a dictionary containing all of the items (key variable names) in
    the list and more.  It is a single level, 1-line dictionary.  The variable
    names in the item list are used to transfer the desired sumbset of data to
    someOtherDict that is then returned to the main dataset. 
    '''
    someOtherDict = {}
    for varName in itemList:
        if someDict.has_key(varName):
            somOtherDict.update({varName:someDict[varName]})
        else:
            'WARNING: MAN.find_list_of_items_in_dictionary_and_create_new_dictionary'
            'Unable to find variable name:', varName, 'in someDict'
            'Unable to create complete subset of data'
    return someOtherDict

def initialize_differential_row_and_column_zero_matrix(numberOfRows,numberOfColumns, startNumber):
    '''
    This function creates an array of startNumbers in each row
    and column of dimensions equal to the numberOfRows and
    numberOfColumns
    '''
    newArray = resize(array((startNumber,startNumber)),(numberOfRows,numberOfColumns))
    return newArray

def compute_expected_proportions_of_boxes_filled(numberOfBoxes,numberOfObs):
    if numberOfObs == 0:
        EPf = 0
        Pfmax = 0
        Pfmin = 0
    else:
        EPf = (1-(1-(1/float(numberOfBoxes)))**numberOfObs)
        Pfmax = min(numberOfBoxes, numberOfObs)/float(numberOfBoxes)
        Pfmin = 1/float(numberOfBoxes)
    PfDict = {'EPF':EPf, 'PFMAX':Pfmax, 'PFMIN':Pfmin}
    return PfDict

def compute_box_distributions_indicator(countBoxesFull, numberOfBoxes, PfDict):
    '''
    This routine updates PfDict.
    It estimates the actual number of boxes full and compares it
    with the expected boxes full using the indiacatorRatio. A ratio
    of 1 indicates a random distribution. A ratio of 0.5 indicates
    a completely random distribution. A ratio > 0.5 indicates a distribution
    that is more uniform than random - located in more boxes than expected
    as a result of a random distribution, up to a maximum of 1, and a ratio
    < 0.5 indicates a more clumpy distribution, down to a minimum of 0,
    indicating that all of the observations are in 1 box.
    '''
    pBoxesFull = countBoxesFull/float(numberOfBoxes)
    if PfDict['PFMAX'] == PfDict['PFMIN']:
        indicatorRatio = 0.5
    else:
        if pBoxesFull > PfDict['EPF']:
            indicatorRatio = 0.5 + 0.5 * float(pBoxesFull - PfDict['EPF'])/float(PfDict['PFMAX']-PfDict['EPF'])
        else:
            indicatorRatio = 0.5 - 0.5 * float(PfDict['EPF']- pBoxesFull)/float(PfDict['EPF']- PfDict['PFMIN'])
    PfDict.update({'APF':pBoxesFull,'IR':indicatorRatio})
    return PfDict

def initialize_row_vector(numberOfColumns,startValue):
    rowVector = []
    for i in range(0,numberOfColumns):
        rowVector.append(startValue)
    return rowVector

def interpolate(UBnum,LBnum,UBden,LBden, MIDden):
    if UBden - LBden == 0:
        newVal = (UBnum + LBnum)/2
    else:
        newVal = LBnum +((UBnum-LBnum)/(UBden-LBden)) *(MIDden-LBden)
    return newVal
