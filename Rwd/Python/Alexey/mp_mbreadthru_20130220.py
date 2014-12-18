'''
'''

from multiprocessing import Pool

import routineLviApplications #MB -- this is a module built by Ian?
import time

def process(dfuncTypedDict, batchNo):
    #XVariables to be extracted from Dfunc
    #Yvariables to be extracted from XVARSELV1
    #Nearest neighbours - absolute distance, euclidean distance, mahalanobis distance to be extracted for X and Y variable dataset
    #Root mean squared errors to be calculated for nearest neighbours based on Y-variable dataset 
    #MB -- what is dfunctTypedDict -- Ian's usual dictionary type?

    #Get Initial Xvalues and Unique set of variable names spanning all variable sets 
    columnNo = 1                #X variable names are in column 1 of the dfuncTypedList
    fileName = 'XSCORE.csv'     #This is the name of the file that contains the untransformed X-variables assigned to each observation within a variable set
    xvarKeyVarNames, xvarHeader, xvarDict = routineLviApplications.assignVariableSetZscoresToObservations(dfuncTypedList, dfuncTypedDict, lviTypedDict, columnNo, fileName, batchNo, printFlag)

    #Calculate Mean and Standard Devations for varSet Functions and Normalize Zscores
    xstatKeyVarNames = ['VARSET3','VARNAMES3']
    xstatHeader = ['VARSET3','VARNAMES3','MEAN','SDEV']
    fileNames = ['XNSCORE.csv','XSTAT.csv']
    xvarNormDict, xvarStatDict = routineLviApplications.normalizeZscores(dfuncTypedDict, xvarDict, xvarHeader, xvarKeyVarNames, xstatKeyVarNames, xstatHeader, fileNames, batchNo, printFlag)
      
#MB -- So far just seems to be calling functions from routineLviApplications. 

    #Get X-var nearest neighbours
    fileNameModifier = 'X'
    nnADict, nnEDict, nnMDict, zcovDict = routineLviApplications.getNearestNeighboursInReferenceDataset(xvarNormDict, xvarStatDict, bwrTypedDict, kNN, zscores, inputVarWeights, squareWeights, inverseWeights, constrainWeightsToAddToOne, fileNameModifier, batchNo, printFlag)
    #fileNames = ['ZERROR.csv','ZRMSE.csv']
    for fileNameModifier, rule, nnDict in [('XM', 'M', nnMDict), ('XE', 'E', nnEDict), ('XA', 'A', nnADict)]:
        routineLviApplications.getZNearestNeighbourRMSE(nnADict, varSelTypedDict, lviTypedDict, kNN, fileNameModifier, rule, batchNo, printFlag)
#MB If finds the correct keys in the dicts, wlll runn the NN algorithm's RMSE fn. 

split = lambda num, lst: [lst[:num]] + split(num, lst[num:]) if len(lst) > num else [lst]#
#lst[:num] is  
#MB easier to understand if a normal fn rather than lambda 1 liner
#MB  split before and after num index if list > num

def worker(payload): #What is done to each batch? Look at multiproccessing module
    batchNo, varSets = payload
    dfuncTypedDict = {}
    for c in varSets:
        dfuncTypedDict.update({c: completeDfuncTypedDict[c]})
    process(dfuncTypedDict, batchNo)
    
#MB /why is payload assigned to both batchNo and varSets?
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

    # split data in batches - a set of sets
    sets = split(nVarSetsPerBatch, dfuncKeyValueList)
    #Produces an index (range for 0 to length of sets, and then the list of sets
    data = zip(range(0, len(sets)), sets)
    #MB uses the split variable, assigned via a lambda fn to break up key value lists
    #MB I think creates tuples where first item is the set number, and 2nd item is the set (of key values)

    # sequential execution
    #map(worker, data)

    # parallel execution; data is a list of keys
    pool = Pool(5)
    # map is a method in pool
    #data is the set of sets - ISM
    pool.map(worker, data)
    #MB Sending out batches of 5 sets
