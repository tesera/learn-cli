'''
'''

import routineLviApplications
import time

print ' Start Processing X-Variable Sets', time.ctime()
kNN = input("\n Please indicate the integer value for the maximum k in kNN for this session and then press ENTER: ... ")
print '\n It is recommended that no more than 50 variable sets be processed at a time.'
print ' Processing a lesser number of variable sets in each batch will result in more frequent additions to each file.'
nVarSetsPerBatch = input("\n Please indicate the number of variable sets to be processed in a single batch: ... ")
if nVarSetsPerBatch > 50:
    nVarSetsPerBatch = 50
    print ' The number of variable sets to be processed in a single batch has been to reduced to the maximum of 50'
printFlag = raw_input("\n Do you wish to see when files are being created and written to: Yes or No ... ")
print '\n'

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

nBatches = int(round(nVarSets/float(nVarSetsPerBatch),0))
if nBatches < 1 or nBatches > nVarSets:
    nBatches = 1
    
setCount = 0
for batchNo in range(0, nBatches, 1):
    dfuncTypedDict = {}
    newKeyList = []
    print ' Batch Number:', batchNo + 1
    for setNo in range(0,nVarSetsPerBatch,1):
        if setCount < nVarSets:
            dfuncKeyValue = dfuncKeyValueList[setCount]
            newKeyList.append(dfuncKeyValue)
            dfuncTypedDict.update({dfuncKeyValue: completeDfuncTypedDict[dfuncKeyValue]})
        setCount = setCount + 1
    if len(newKeyList) > 0:
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
        
        #These options can NOT be changed when running this module
        bwrTypedDict = {}
        zscores = False
        inputVarWeights = False
        squareWeights = False
        inverseWeights = False
        constrainWeightsToAddToOne = False
        #
        #Get X-var nearest neighbours
        fileNameModifier = 'X'
        nnADict, nnEDict, nnMDict, zcovDict = routineLviApplications.getNearestNeighboursInReferenceDataset(xvarNormDict, xvarStatDict, bwrTypedDict, kNN, zscores, inputVarWeights, squareWeights, inverseWeights, constrainWeightsToAddToOne, fileNameModifier, batchNo, printFlag)
        #fileNames = ['ZERROR.csv','ZRMSE.csv']
        fileNameModifier = 'XM'
        rule = 'M'
        rmseMDict = routineLviApplications.getZNearestNeighbourRMSE(nnMDict, varSelTypedDict, lviTypedDict, kNN, fileNameModifier, rule, batchNo, printFlag)
        fileNameModifier = 'XE'
        rule = 'E'
        rmseEDict = routineLviApplications.getZNearestNeighbourRMSE(nnEDict, varSelTypedDict, lviTypedDict, kNN, fileNameModifier, rule, batchNo, printFlag)
        fileNameModifier = 'XA'
        rule = 'A'
        rmseADict = routineLviApplications.getZNearestNeighbourRMSE(nnADict, varSelTypedDict, lviTypedDict, kNN, fileNameModifier, rule, batchNo, printFlag)
#
print ' Finished processing X-Variable Sets', time.ctime()
    
raw_input(" Press ENTER to Close This Session ... ")    
