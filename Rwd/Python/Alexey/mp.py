'''
'''

from multiprocessing import Pool

import routineLviApplications
import time

def process(dfuncTypedDict, batchNo):
    #XVariables to be extracted from Dfunc
    #Yvariables to be extracted from XVARSELV1
    #Nearest neighbours - absolute distance, euclidean distance, mahalanobis distance to be extracted for X and Y variable dataset
    #Root mean squared errors to be calculated for nearest neighbours based on Y-variable dataset 

    #Get Initial Xvalues and Unique set of variable names spanning all variable sets 
    columnNo = 1                #X variable names are in column 1 of the dfuncTypedList
    fileName = 'XSCORE.csv'     #This is the name of the file that contains the untransformed X-variables assigned to each observation within a variable set
    xvarKeyVarNames, xvarHeader, xvarDict = routineLviApplications.assignVariableSetZscoresToObservations(dfuncTypedList, dfuncTypedDict, lviTypedDict, columnNo, fileName, batchNo, printFlag)

    #Calculate Mean and Standard Devations for varSet Functions and Normalize Zscores
    xstatKeyVarNames = ['VARSET3','VARNAMES3']
    xstatHeader = ['VARSET3','VARNAMES3','MEAN','SDEV']
    fileNames = ['XNSCORE.csv','XSTAT.csv']
    xvarNormDict, xvarStatDict = routineLviApplications.normalizeZscores(dfuncTypedDict, xvarDict, xvarHeader, xvarKeyVarNames, xstatKeyVarNames, xstatHeader, fileNames, batchNo, printFlag)
        
    #Get X-var nearest neighbours
    fileNameModifier = 'X'
    nnADict, nnEDict, nnMDict, zcovDict = routineLviApplications.getNearestNeighboursInReferenceDataset(xvarNormDict, xvarStatDict, bwrTypedDict, kNN, zscores, inputVarWeights, squareWeights, inverseWeights, constrainWeightsToAddToOne, fileNameModifier, batchNo, printFlag)
    #fileNames = ['ZERROR.csv','ZRMSE.csv']
    for fileNameModifier, rule, nnDict in [('XM', 'M', nnMDict), ('XE', 'E', nnEDict), ('XA', 'A', nnADict)]:
        routineLviApplications.getZNearestNeighbourRMSE(nnADict, varSelTypedDict, lviTypedDict, kNN, fileNameModifier, rule, batchNo, printFlag)

split = lambda num, lst: [lst[:num]] + split(num, lst[num:]) if len(lst) > num else [lst]

def worker(payload):
    batchNo, varSets = payload
    dfuncTypedDict = {}
    for c in varSets:
        dfuncTypedDict.update({c: completeDfuncTypedDict[c]})
    process(dfuncTypedDict, batchNo)

if __name__ == '__main__':
    kNN = 5
    nVarSetsPerBatch = 5
    printFlag = 'Yes'

    #Get data dictionary
    #filePath = routineLviApplications.SetDataFilePath()
    originalDict, newDict = routineLviApplications.ReadLviDataDictionary()
    #
    #Read lvinew into dictionary format
    lviTableName = 'LVINEW'
    lviKeyVarNameList = ['LVI_FCOID']
    lviHeader, lviTypedDict = routineLviApplications.ReadCsvDataFileAndTransformIntoDictionaryFormat(newDict, lviTableName, \
                                                                                      'ERROR-CHECK-LVUNX', lviKeyVarNameList)
    uidList = lviTypedDict.keys()
    uidList.sort()

    #Read Y-variable selection
    varSelTableName = 'XVARSELV1'
    varSelKeyVarNameList = ['TVID']
    varSelHeader, varSelTypedDict = routineLviApplications.ReadCsvDataFileAndTransformIntoDictionaryFormat(newDict, varSelTableName, \
                                                                                      'ERROR-CHECK-VSELX', varSelKeyVarNameList)
    #Read DFUNCT into list format
    dfuncTableName = 'DFUNCT'
    dfuncTypedList = routineLviApplications.ReadCsvDataFile(newDict, dfuncTableName, 'ERROR-CHECK-DFUNCX')

    #Read DFUNCT into dictionary format
    dfuncKeyVarNameList = ['VARSET3','VARNAMES3', 'FUNCLABEL3']     #Note for NN_ZDIST the order of the key variable names is different from this one
    newDfuncHeader, completeDfuncTypedDict = routineLviApplications.TransformDataTypedListIntoDictionaryFormat(dfuncKeyVarNameList, dfuncTypedList)
    dfuncKeyValueList = completeDfuncTypedDict.keys()
    dfuncKeyValueList.sort()
    nVarSets = len(dfuncKeyValueList)

    #These options can NOT be changed when running this module
    bwrTypedDict = {}
    zscores = False
    inputVarWeights = False
    squareWeights = False
    inverseWeights = False
    constrainWeightsToAddToOne = False
    #

    # split data in batches
    sets = split(nVarSetsPerBatch, dfuncKeyValueList)
    data = zip(range(0, len(sets)), sets)

    # sequential execution
    #map(worker, data)

    # parallel execution
    pool = Pool(5)
    pool.map(worker, data)
