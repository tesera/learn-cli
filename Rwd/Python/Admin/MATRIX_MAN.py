'''
'''
import sys

import BASE

import bisect
from math import *
from random import *
import numpy
import scipy
from scipy import linalg
import time


def get_id_list(distList):
    standidDict = {}
    end_i = len(distList)
    #print end_i
    for i in range(0,end_i,1):
        #print i
        a = distList[i][0]
        b = distList[i][1]
        standidDict.update({i:{'STANDID':a}})
        del distList[i][0:1]
    return (standidDict, distList)


def get_means_vector_from_transposed_array(newArray):
    meansVector = []
    end_array = len(newArray)
    for num in range(0,end_array,1):
        meanValue = numpy.mean(newArray[num])
        meansVector.append(meanValue)
    return meansVector

def get_standard_deviation_vector_from_transposed_array(newArray):
    stdevVector = []
    end_array = len(newArray)
    for num in range(0,end_array,1):
        stdevValue = numpy.std(newArray[num])
        stdevVector.append(stdevValue)
    return stdevVector

def transpose_varList(varList):
    newArray = numpy.transpose(varList)
    return newArray

def get_row_numbers_with_zero_standard_deviation(xVector):
    zeroVector = []
    end_vector = len(xVector)
    for num in range(0,end_vector):
        if xVector[num] == 0:
            zeroVector.append(num)
    return zeroVector

def get_new_varList(xList):
    newList = []
    end_x = len(xList)
    for x in range(1, end_x,1):
        name = xList[x]
        newList.append(name)
    return newList

def delete_vectors_in_array_with_zero_stdev(xArray,zeroList):
    newVarArray = []
    end_x = len(xArray)
    for x in range(0,end_x,1):
        if not x in zeroList:
            newVarArray.append(xArray[x])
    return newVarArray
    
def check_vector_lengths(xArray,mVector,stdVector,vList):
    end_x = len(xArray)
    if not end_x == len(mVector):
        print 'varArray is', end_x, 'rows; mVector is', len(mVector), 'rows'
    if not end_x == len(stdVector):
        print 'varArray is', end_x, 'rows; stdVector is', len(stdVector), 'rows'
    if not end_x == len(vList):
        print 'varArray is', end_x, 'rows; vList is', len(vList), 'rows'
    return

def subtract_means_from_array_values(xArray,xmVector):
    newArray = []
    end_x = len(xArray)
    for x in range(0,end_x,1):
        varMean = xmVector[x]
        end_y = len(xArray[x])
        newArray.append([])
        for y in range(0,end_y,1):
            newVarValue = xArray[x][y] - varMean
            newArray[x].append(newVarValue)
    return newArray
            
def divide_array_values_by_standard_deviations(xArray,xsVector):
    newArray = []
    end_x = len(xArray)
    n = len(xArray)
    #correction = 1/sqrt(n-1)
    for x in range(0,end_x,1):
        varStdev = xsVector[x]
        end_y = len(xArray[x])
        newArray.append([])
        for y in range(0,end_y,1):
            #newVarValue = correction*(xArray[x][y]/ float(varStdev))
            newVarValue = (xArray[x][y]/ float(varStdev))
            newArray[x].append(newVarValue)
    return newArray

def get_select_list_variables(logitVarNames, distList, distHeader):
    newList = []
    end_y = len(distHeader)
    end_x = len(distList)
    for x in range(0,end_x,1):
        newList.append([])
        for y in range(0,end_y,1):
            varName = distHeader[y]
            if varName in logitVarNames:
                varValue = distList[x][y]
                newList[x].append(y)
    return newList

def exctract_new_array_from_dictionary(keyList,varNames,aDict):
    newArray = []
    i = 0
    for keyName in keyList:
        newArray.append([])
        j = 0
        for varN in varNames:
            newVarValue = aDict[keyName][varN]
            newArray[i].append(newVarValue)
        i = i + 1
    return newArray

def join_two_varNameLists(finalList,appendList):
    end_i = len(appendList)
    for i in range(0,end_i,1):
        varValue = appendList[i]
        finalList.append(varValue)
    return finalList

def get_xx_or_yy_correlation_matrix(varArray1):
    '''
    Array has variables listed in rows
    and observations in columns
    '''
    corrArray = scipy.corrcoef(varArray1)
    return corrArray

def get_xx_or_yy_covariance_matrix(varArray1):
    '''
    Array has variables listed in rows
    and observations in columns
    '''
    varArrayT = np.transpose(varArray1)
    covArray = np.cov(varArrayT)
    return covArray


def get_xy_or_yx_correlation_matrix(varArray1,varArray2):
    '''
    Array has variables listed in rows
    and observations in columns; varArray1 variables
    will be listed in the first set of rows and columns;
    varArray2 Variables will be listed in the rows and columns
    after the varArray1 variables. 
    '''
    corrArray = scipy.corrcoef(varArray1,varArray2)
    return corrArray

def get_array_inverse(varArray1):
    inverseArray = linalg.inv(varArray1)
    return inverseArray

def matrix_multiply_inner_product(varArray1, varArray2):
    innerProductArray = numpy.inner(varArray1,varArray2)
    return innerProductArray

def matrix_multiply_outer_product(varArray1, varArray2):
    outerProductArray = numpy.outer(varArray1,varArray2)
    return outerProductArray

def get_determinant_of_symmetrical_matrix(myMatrix):
    varValue = linalg.det(myMatrix)
    return varValue

def get_inverse_of_matrix(myMatrix):
    varValue = linalg.inv(myMatrix)
    return varValue

def get_transpose_of_matrix(myMatrix):
    arrayTranspose = numpy.transpose(myMatrix)
    return arrayTranspose

def extract_array_partition_from_symmetric_array(arrayHeader,extractRowNames, extractColNames, extractArray):
    newArray = []
    end_row = len(arrayHeader)
    end_col = len(extractArray)
    if not end_col == end_row:
        print 'Extract arrayHeader a different length from extractHeader'
    i = 0
    for rowName in extractRowNames:
        rowNo = arrayHeader.index(rowName)
        newArray.append([])
        for colName in extractColNames:
            colNo = arrayHeader.index(colName)
            varValue = extractArray[rowNo][colNo]
            newArray[i].append(varValue)
        i = i + 1
    return newArray

def add_two_two_dimensional_arrays_of_same_dimensions(varArray1, varArray2):
    newArray = []
    end_i = len(varArray1)
    end_j = len(varArray1[0])
    for i in range(0,end_i,1):
        newArray.append([])
        for j in range(0,end_j,1):
            newVarValue = varArray1[i][j] + varArray2[i][j]
            newArray[i].append(newVarValue)
    return newArray
