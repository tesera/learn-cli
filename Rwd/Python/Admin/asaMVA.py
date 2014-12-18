#!/usr/bin/env python
"""
asaPlot: ported from Ian Moss module dataTransforms_20120926_Ian
to work with TSIAnalytics. Original modules (c) Ian Moss 2006-2012

CurrentRevisionDate:20121119


Author(s): Ian Moss
Contact: ian.moss@tesera.com
collated by: Mishtu Banerjee, mishtu.banerjee@tesera.com

Copyright: The Author(s)
License: Distributed under MIT License
    [http://opensource.org/licenses/mit-license.html]



Dependencies:
    Python interpreter and base libraries, matplotlib
    
""" 
import numpy 
import scipy
from scipy import linalg
from scipy import stats
from math import *
from random import *
from copy import deepcopy

# The imports below from MATRIX_MAN do not appear to be used
#import sys
#import bisect
#import time
#import BASE 
# ---------- Multivariate Analysis Basics: Correlation and Regression ----------


def linear_regression():
    slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
    print 'Slope Coefficient:', slope
    print 'Intercept:', intercept
    print 'Rsq:', r_value**2
    print 'p Value:', p_value
    print 'Standard Error:', std_err
    return
    
def multiple_linear_regression(x=[], Y=[], intercept = 'Y'):
    '''
    Matrix Algebra based on:
    
    Neter, J, Kutner, M.H., Nachtsheim, C.J., and Wasserman, W. 1996.
    Applied linear statistical models. Fourth Edition. Pp. 225-231.
    McGraw-Hill, Boston, MA,US.

    Inputs:
    intercept is indicated as 'Y' if an intercept is to be included or 'N' if not
        The default value is 'Y'
    x is a a matrix of x values with each variable represented by
        a separate list or vector (in rows) and the different observations represented
        in the same order (in columns). If there is only 1 x-Variable then this is in
        a single vector, not in 2 or more vectors embedded within a list format
    Y is a single list of Y observeations of the smae length (number of observations) as the X variables

    At the moment there is no provision to deal with missing observations

    Matrices:
    b is a matrix of slope coefficients
    X is matrix that includes a column of ones in the first column if intercept = 'Y'
        otherwise it is equal to x if intercept = 'N'
    J is a s square matrix of ones with the numbre of rows and columns equal to the number of observations

    Outputs:
    b slope coefficients
    SSR is the sums of squares regression
    RDF is regression degrees of freedom - equal to the number of variables minus one.
    MSR is the mean sums of squares regression = SSR/RDF
    SSE is the sums of squares error
    EDF is the error degrees of freedom - equal to the number of observations minus the number of variables
    MSE is the mean sums of squares error - equal to SSE/EDF
    SST is the total sums of squares
    TDF is the total degrees of freedome - equal to the number of observations minus 1
    F   is the Fisher statistic
    R2  is the r-squared value - equal to SSR/SST
    R2ADJ is the adjusted r-squared vale - equal to 1 - (TDF/EDF * SSE/SST)
    SIGNIFICANCE is the significance of the f-statistic generated using scipy.stats.f.cdf(F,RDF,EDF)
        This was tested using (0.667,1,2) to produce a p-value of 0.5 which is correct based on the table on p 1340 in Neter et al.1996.
        
    Here is a usage example in a python workflow script:
    #Test multiple linear regression
    x = [1,2,3,4]
    y = [12,14,16,18]
    b, SSR, RDF, MSR, SSE, EDF, MSE, SST, TDF, F, R2, R2ADJ, SIGNIFICANCE = dataTransforms.multiple_linear_regression(x, y,'Y')
    #Bring in new dataset to test regression module
    regressDataDictName = 'REGRESS_DICT'
    regressDataDict = dataMachete.getDataDictionary(dataFilePath, regressDataDictName)
    regressDataTableName = 'REGRESS'
    regressDataStringList = dataMachete.getListarray(dataFilePath, regressDataTableName)
    regressDataTypedList = dataMachete.typeDataset(regressDataStringList, regressDataDict, regressDataTableName, errorFilePath)
    regressDataHeader = regressDataTypedList[0]
    regressKeyVariableNameList = ['NPLOTID']
    regressDataTypeDict = {}
    regressDataTypedDict = dataMachete.createDictDB(regressDataTypeDict,regressKeyVariableNameList,regressDataTypedList)
    regressDistinctValueList = regressDataTypedDict.keys()
    regressDistinctValueList.sort()
    '''
    if intercept == 'Y':
        X = add_column_of_ones_to_array(x)
    else:
        X = x
    #Number of observations
    nObs = len(Y)
    invN = 1/float(nObs)
    #Number of variables including ones if present
    pVariables = len(X)
    #Regression degrees of freedom
    RDF = pVariables-1
    #Error degrees of freedom
    EDF = nObs - pVariables
    #Total degrees of freedom
    TDF = nObs-1
    XX=matrix_multiply_inner_product(X,X)
    #Note singularity can cause the inverse to be blown out of proportion 
    InverseXX = get_array_inverse(XX)
    XY=matrix_multiply_inner_product(X,Y)
    #Calculate slope coefficients.
    b = matrix_multiply_inner_product(InverseXX,XY)
    #Produce a J matrix or n x n matrix of ones
    J = produce_a_matrix_of_ones_with_nrows_ncolumns(nObs, nObs, 1)
    #Calculate the sums of square and mean sums of square regression  
    JY = matrix_multiply_inner_product(J,Y)
    YJY = matrix_multiply_inner_product(Y,JY)
    invNYJY = matrix_multiply_inner_product(invN,YJY)
    bXY = matrix_multiply_inner_product(b,XY)
    SSR = bXY - invNYJY
    MSR = SSR/float(RDF)
    #Calculate the sums of squared and mean sums of squared error
    YY = matrix_multiply_inner_product(Y,Y)
    SSE = YY-bXY
    MSE = SSE/float(EDF)
    #Calculate total sums of squared error
    SST = YY-invNYJY
    F = MSR/MSE
    R2 = SSR/SST
    R2ADJ = 1 - (TDF/EDF) * (SSE/SST)
    SIGNIFICANCE = stats.f.cdf(F,RDF,EDF)
    return b, SSR, RDF, MSR, SSE, EDF, MSE, SST, TDF, F, R2, R2ADJ, SIGNIFICANCE


# ---------- Matrix Manipulations for Multivariate ----------


def add_column_of_ones_to_array(xArray):
    '''
    A column of ones is added
    '''
    newArray = []
    newOneVector = []
    arrayLength = len(xArray)
    flag = True
    if arrayLength > 0:
        if type(xArray[0])==type([]):
            #Two dimensional array, i.e. a list of lists
            newArrayLength = len(xArray[0])
            for i in range(1,arrayLength,1):
                #Check to ensure that all vectors inside array are
                #also in the list format; if not print error message
                if not type(xArray[i]) == type([]) \
                   and not len(xArray[i]) == newArrayLength:
                    flag = False
                    print 'xArray is in wrong format'
                    break
                for j in range(0,newArrayLength,1):
                    #Check to ensure that values inside each of the vectors
                    #are either integer or float; if not print error message
                    if not type(xArray[i][j]) == type(1) and not type(xArray[i][j]) == type(1.1):
                        flag = False
                        print 'xArray vector(s) have values that are neither integer or float'
                        break
            if flag == True:
                #Data is in 2D array and vectors are all the same length
                for i in range(0,newArrayLength,1):
                    newOneVector.append(1)
                newArray.append(newOneVector)
                for i in range(0,arrayLength,1):
                    newArray.append(xArray[i])
        if type(xArray[0]) == type(1) or type(xArray[0]) == type(1.1):
            #One dimensional array containing either integer of float format numbers or both
            #If not print error message
            for i in range(1,arrayLength,1):
                if not type(xArray[i]) == type(1) and not type(xArray[i]) == type(1.1):
                    flag = False
                    print 'xArray as single vector has values that are neither integer or float'
                    break
            #Make new array with vector of 1's followed by the xArray vector
            if flag == True:
                for i in range(0,arrayLength,1):
                    newOneVector.append(1)
                newArray.append(newOneVector)
                newArray.append(xArray)
    if newArray == []:
        print 'newArray is empty. No vector of ones appended and values of xArray appended'
    return newArray

def produce_a_matrix_of_ones_with_nrows_ncolumns(nrows = 0, ncolumns = 0, varValue = 1):
    newMatrix = []
    i = 1
    if nrows > 0 and ncolumns > 0:
        for row in range(0,nrows,1):
            newMatrix.append([])
            for column in range(0, ncolumns, 1):
                newMatrix[row].append(1)
    return newMatrix

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

def extract_new_array_from_dictionary(keyList,varNames,aDict):
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

def computeZscores(zParamList = [[]], xVarValueList = [[]]):
    '''
    '''
    zScore = []
    for vector in zParamList:
        zScoreArray = sum(numpy.transpose(numpy.multiply(vector, xVarValueList)))
        #print len(zScoreVector)
        zScore.append(zScoreArray.tolist())
        #print len(zScore)
    zScore = numpy.transpose(zScore)
    zScore = zScore.tolist()
    #print len(zScore)
    return zScore

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

def getMeanAndStandardDeviationFor2DList(statsTableName = '', varNameList = [], dataTypedList = [[]], \
                                         statsDict = {}):
    '''

    Explanation
        This function extracts means and standard deviations for variables dataTypedList corresponding
        with the variable names identified in the varNameList.  Each variable is added to the statsDict
        under an associated statsTableName with the corresponding means('MEN') and standard deviations
        ('SDEV'). A non empty statsDict will contain information for a number of statsTableNames.

    Inputs
        statsTableName      The name of the table associated with different variables.
        varNameList         A list of variable names corresponding with those in the top
                            row of the dataTypedList for which means and standard deviations are required
                            and included in the statsDict.
        dataTypedList       A 2D list of data where the top row ioncludes the a list of all the variable
                            names associated with varaibale values in each of the rows below. This list
                            does not include a header (list of variable names in the first line) and it
                            does not include any primary keys - it only contains the variables that are
                            to be directly analyzed.
        stasDict            A data dictionary that is empty or corresponds to the following format:

                            TABLENAME   The name of the table with associated variable names.
                            VARNAME     Variable names associated with a given table names.
                            MEAN        The mean value associated with a given variable name
                            SDEV        The standard deviation associated with a given variable name.

                            

    Outputs
        statsHeader         The header = ['TABLENAME','VARNAME','MEAN','SDEV']
        statsKeyVarNameList The key variables in order of priority = ['TABLENAME','VARNAME']
        statDict            See Inputs above for table format

    Ian Moss
    July 31 2013
    '''
    #Scenario 1: fails
    #Scenario 2: Default - Header and a varNameList (use variname list to select columns according to header)
    #Convert scenarios 3 and 4  below to saitisfy default conditions
    #
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

def getMeanAndStandardDeviationFor2DListNumpy(statsTableName = '', varNameList = [], dataTypedList = [[]], \
                                         statsDict = {}, excludeZeros = False):
    '''

    Explanation
        This function extracts means and standard deviations for variables dataTypedList corresponding
        with the variable names identified in the varNameList.  Each variable is added to the statsDict
        under an associated statsTableName with the corresponding means('MEN') and standard deviations
        ('SDEV'). A non empty statsDict will contain information for a number of statsTableNames.

    Inputs
        statsTableName      The name of the table associated with different variables.
        varNameList         A list of variable names corresponding with those in the top
                            row of the dataTypedList for which means and standard deviations are required
                            and included in the statsDict.
        dataTypedList       A 2D list of data where the top row ioncludes the a list of all the variable
                            names associated with varaibale values in each of the rows below. This list
                            does not include a header (list of variable names in the first line) and it
                            does not include any primary keys - it only contains the variables that are
                            to be directly analyzed.
        stasDict            A data dictionary that is empty or corresponds to the following format:

                            TABLENAME   The name of the table with associated variable names.
                            VARNAME     Variable names associated with a given table names.
                            MEAN        The mean value associated with a given variable name
                            SDEV        The standard deviation associated with a given variable name.

                            

    Outputs
        statsHeader         The header = ['TABLENAME','VARNAME','MEAN','SDEV']
        statsKeyVarNameList The key variables in order of priority = ['TABLENAME','VARNAME']
        statDict            See Inputs above for table format

    Ian Moss
    July 31 2013
    '''
    #Scenario 1: fails
    #Scenario 2: Default - Header and a varNameList (use variname list to select columns according to header)
    #Convert scenarios 3 and 4  below to saitisfy default conditions
    #
    statsHeader = ['TABLENAME','VARNAME','MEAN','SDEV']
    statsKeyVarNameList = ['TABLENAME','VARNAME']
    numberOfVariables = len(varNameList)
    statsDict.update({statsTableName:{}})
    dataTypedListTranspose = deepcopy(numpy.transpose(dataTypedList))
    for varNo in range(0,numberOfVariables,1):
        varName = varNameList[varNo]
        if excludeZeros == True:
            newList = []
            for varValue in dataTypedListTranspose[varNo]:
                if varValue <> 0:
                    newList.append(varValue)
        else:
            newList = list(dataTypedListTranspose[varNo])
        
        if len(newList)==0:
            meanValue = 0
            sdevValue = 0
        else:            
            meanValue = numpy.mean(newList)
            sdevValue = numpy.std(newList)
        statsDict[statsTableName].update({varName:{'MEAN':meanValue,'SDEV':sdevValue}})
    return statsHeader, statsKeyVarNameList, statsDict

def computeMeanFor2DListByColumn(List2D=[[]]):
    '''
    Observations in rows, variables in columns
    '''
    meanVector = numpy.mean(List2D,0)
    meanVector = meanVector.tolist()
    return meanVector


def computeSdevFor2DListByColumn(List2D=[[]]):
    '''
    Observations in rows, variables in columns
    '''
    stdVector = numpy.std(List2D,0)
    stdVector = stdVector.tolist()
    return stdVector

def computeInverseVarCovarianceMatrix(List2D=[[]]):
    '''
    Observations in rows, variables in columns
    '''
    covMatrix = numpy.cov(numpy.transpose(List2D))
    invCovMatrix = linalg.inv(covMatrix)
    return invCovMatrix

def computeVarCovarianceMatrix(List2D=[[]]):
    '''
    Observations in rows, variables in columns
    '''
    covMatrix = numpy.cov(numpy.transpose(List2D))
    return covMatrix

def normalizeDataset_ReturnListMeanVectorInvCovMatrix(List2D=[[]]):
    '''
    Observations in rows, variables in columns
    Used to normalize reference data in kNN
    Normalization based on multiplying by inverse of covariance matrix
    
    '''
    #Calculate column means put in vector
    meanVector = numpy.mean(List2D,0)   
    #Compute variable covariance matrix
    covMatrix = numpy.cov(numpy.transpose(List2D))
    #Get inverse of covariance matrix
    if numpy.shape(covMatrix)==():
        invCovMatrix = 1/covMatrix
    else:
        invCovMatrix = linalg.inv(covMatrix)
    #Subtract variable means from observation values  
    transData = numpy.subtract(List2D,meanVector)
    #Compute inner product  
    normData = numpy.inner(transData,invCovMatrix)
    meanVector = meanVector.tolist()
    covMatrix = covMatrix.tolist()
    invCovMatrix = invCovMatrix.tolist()
    normData = normData.tolist()
    return meanVector, covMatrix,invCovMatrix,normData

def normalizeDatasetUsingMeanVectorPlusCovarianceMatrix(List2D=[[]], meanVector = [], invCovMatrix = [[]]):
    '''
    Observations in rows, variables in columns
    Mean vector calculated ffor reference dataset
    Used to normalize target data in kNN based on reference data means and covariances
    '''
    #Subtract variable means from observation values  
    transData = numpy.subtract(List2D,meanVector)
    #Compute inner product  
    normData = numpy.inner(transData,invCovMatrix)
    normData = normData.tolist()
    return normData


def createAnalysisDataset(varNameList = [], dataTypedList = [[]], headerFlag = False):
    '''
    This is somewhat redundant with dataMachete.createNewListFromSelectVariableListAndIdList
    This function has not been tested
    August 1 2013
    '''
    outDataList = []
    newDataList = deepcopy(dataTypedList)
    #Scenario 1: No header and no varNameList
    if varNameList == [] and headerFlag == False:
        print 'asaMVA.getMeanAndStandardDeviationFor2DList'
        print 'data list has no header and variable name list empty'
        print 'cannot proceed with calculations of means and standard deviations'
    else:
        numberOfVariables = len(varNameList)
        statsDict.update({statsTableName:{}})
        if headerFlag == True:
            header = deepcopy(dataTypedList[0])
            del dataTypedList[0]
        #Scenario 3: A varNameList and no header
        #Copy header from original data list and insert into new data list
        if numberOfVariables > 0 and headerFlag == False:
            header = deepcopy(varNameList)
        #Scenario 3: A header and no varNameList
        #Copy header into varNameList
        if numberOfVariables == 0:           
            varNameList = header
            numberOfVariables = len(varNameList)
        for observation in newDataList:
            varValueList = []
            for varNo in range(0,numberOfVariables,1):
                varName = varNameList[varNo]
                varIndex = header.index(varName)           
                varValue = observation[varIndex]
                varValueList.append(varValue)
            outDataList.append(deepcopy(varValueList))
    return varNameList, header, outDataList


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

def normalizeVariableDatasetNumpy(dataTypedList = [], varNameList =[], statsTableName = '', statsDict = {}):
    '''
    '''
    dataNormTypedArray = numpy.transpose(dataTypedList)
    nVar = len(varNameList)
    nObs = len(dataTypedList)
    for varNo in range(0,nVar,1):
        varName = varNameList[varNo]
        meanValue = statsDict[statsTableName][varName]['MEAN']
        sdevValue = statsDict[statsTableName][varName]['SDEV']
        dataNormTypedArray[varNo] = numpy.divide(numpy.subtract(dataNormTypedArray[varNo],meanValue),sdevValue)
    dataNormTypedList = list(numpy.transpose(dataNormTypedArray))
    return dataNormTypedList

