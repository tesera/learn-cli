'''
Compile the new Discriminant Function X-Variable datasets

Inputs
    LVINEW.csv
    DFUNCT.csv
    BWRATIO
    PyRDataDict.csv

Outputs (\\Rwd\\ Directory)
    NNZDICT.csv
    ZSCORE.csv
    ZNSCORE.csv
    ZSTAT.csv
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
                                                                                      'ERROR-CHECK-LVUNZ', lviKeyVarNameList)

#Read Y-variable selection
varSelTableName = 'XVARSELV1'
varSelKeyVarNameList = ['TVID']
varSelHeader, varSelTypedDict = routineLviApplications.ReadCsvDataFileAndTransformIntoDictionaryFormat(newDict, varSelTableName, \
                                                                                      'ERROR-CHECK-VSELZ', varSelKeyVarNameList)

#Read DFUNCT into list format
dfuncTableName = 'DFUNCT'
dfuncTypedList = routineLviApplications.ReadCsvDataFile(newDict, dfuncTableName, 'ERROR-CHECK-DFUNC')

#Read BWRATIO
bwrTableName = 'BWRATIO'
bwrKeyVarNameList = ['VARSET4','FUNCLABEL4']
bwrHeader, bwrTypedDict = routineLviApplications.ReadCsvDataFileAndTransformIntoDictionaryFormat(newDict, bwrTableName, \
                                                                                      'ERROR-CHECK-BWR', bwrKeyVarNameList)
#Read DFUNCT into dictionary format
dfuncKeyVarNameList = ['VARSET3','FUNCLABEL3', 'VARNAMES3']
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
    print 'Batch Number:', batchNo + 1
    for setNo in range(0,nVarSetsPerBatch,1):
        if setCount < nVarSets:
            dfuncKeyValue = dfuncKeyValueList[setCount]
            newKeyList.append(dfuncKeyValue)
            dfuncTypedDict.update({dfuncKeyValue: completeDfuncTypedDict[dfuncKeyValue]})
        setCount = setCount + 1
    if len(newKeyList) > 0:
        #Get Initial Zscores and Unique set of discriminant function names spanning all variable sets
        columnNo = 2                #Z discriminant function names are in column 2 of the dfuncTypedList
        fileName = 'ZSCORE.csv'     #This is the name of the file that contains the untransformed discriminant function Z-variables assigned to each observation within a variable set
        zvarKeyVarNames, zvarHeader, zvarDict = routineLviApplications.assignVariableSetZscoresToObservations(dfuncTypedList, dfuncTypedDict, lviTypedDict, columnNo, fileName, batchNo, printFlag)
        zstatKeyVarNames = ['VARSET3','FUNCLABEL3']
        zstatHeader = ['VARSET3','FUNCLABEL3','MEAN','SDEV']
        fileNames = ['ZNSCORE.csv','ZSTAT.csv']
        #Calculate Mean and Standard Devations for varSet Functions and Normalize Zscores
        zvarNormDict, zvarStatDict = routineLviApplications.normalizeZscores(dfuncTypedDict, zvarDict, zvarHeader, zvarKeyVarNames,zstatKeyVarNames, zstatHeader, fileNames, batchNo, printFlag)

        #This statement must not be changed
        zscores = True
        #These options can be changed when running this module
        inputVarWeights = False
        squareWeights = False
        inverseWeights = False
        constrainWeightsToAddToOne = False
        #
        #Get X-var nearest neighbours
        fileNameModifier = 'Z'
        nnADict, nnEDict, nnMDict, zcovDict = routineLviApplications.getNearestNeighboursInReferenceDataset(zvarNormDict, zvarStatDict, bwrTypedDict, kNN, zscores, inputVarWeights, squareWeights, inverseWeights, constrainWeightsToAddToOne, fileNameModifier, batchNo, printFlag)
        #fileNames = ['ZERROR.csv','ZRMSE.csv']
        fileNameModifier = 'ZM'
        rule = 'M'
        rmseMDict = routineLviApplications.getZNearestNeighbourRMSE(nnMDict, varSelTypedDict, lviTypedDict, kNN, fileNameModifier, rule, batchNo, printFlag)
        fileNameModifier = 'ZE'
        rule = 'E'
        rmseEDict = routineLviApplications.getZNearestNeighbourRMSE(nnEDict, varSelTypedDict, lviTypedDict, kNN, fileNameModifier, rule, batchNo, printFlag)
        fileNameModifier = 'ZA'
        rule = 'A'
        rmseADict = routineLviApplications.getZNearestNeighbourRMSE(nnADict, varSelTypedDict, lviTypedDict, kNN, fileNameModifier, rule, batchNo, printFlag)

print 'Finished processing Z-Variable Sets', time.ctime()
                
raw_input(" Press Enter to Close This Session ... ")          
        





                      
        
   


    




                                                            
