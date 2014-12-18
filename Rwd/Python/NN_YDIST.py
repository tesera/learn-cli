'''
'''
import routineLviApplications
import time

print 'Start Processing Y-Variable Sets', time.ctime()
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
                                                                                      'ERROR-CHECK-LVUN', lviKeyVarNameList)
#Read Y-variable selection
varSelTableName = 'XVARSELV1'
varSelKeyVarNameList = ['TVID']
varSelHeader, varSelTypedDict = routineLviApplications.ReadCsvDataFileAndTransformIntoDictionaryFormat(newDict, varSelTableName, \
                                                                                      'ERROR-CHECK-VSEL', varSelKeyVarNameList)

#Get selected Y- variable list
varSelectCriteria = 'Y'
varNameList = routineLviApplications.createSelectVariableListFromXvarselv1TypedDict(varSelTypedDict, varSelectCriteria)
varSetNo = 0
ystatHeader, ystatKeys, yvarStatDict = routineLviApplications.getSelectVariableMeanAndSdev(varSetNo, varNameList, lviTypedDict)

#Get Normalized and Non Normalized Y-statistics
yvarKeyVarNames, yvarHeader, yvarDict, yvarNormDict = routineLviApplications.getNormalizedAndNonNormalizedVariableStatistics(varSetNo, varNameList, lviTypedDict, yvarStatDict)

#This statement must not be changed
bwrTypedDict = {}
zscores = False
#These options can be changed when running this module
inputVarWeights = False
squareWeights = False
inverseWeights = False
constrainWeightsToAddToOne = False
#
kNN = 1
print 'k = 1 for kNN based on Y-Variable Set'
batchNo = 0
#Get X-var nearest neighbours
fileNameModifier = 'Y'
nnADict, nnEDict, nnMDict, zcovDict = routineLviApplications.getNearestNeighboursInReferenceDataset(yvarNormDict, yvarStatDict, bwrTypedDict, kNN, zscores, inputVarWeights, squareWeights, inverseWeights, constrainWeightsToAddToOne, fileNameModifier, batchNo, printFlag)
#fileNames = ['ZERROR.csv','ZRMSE.csv']
fileNameModifier = 'YM'
rule = 'M'
rmseMDict = routineLviApplications.getZNearestNeighbourRMSE(nnMDict, varSelTypedDict, lviTypedDict, kNN, fileNameModifier, rule, batchNo, printFlag)
fileNameModifier = 'YE'
rule = 'E'
rmseEDict = routineLviApplications.getZNearestNeighbourRMSE(nnEDict, varSelTypedDict, lviTypedDict, kNN, fileNameModifier, rule, batchNo, printFlag)
fileNameModifier = 'YA'
rule = 'A'
rmseADict = routineLviApplications.getZNearestNeighbourRMSE(nnADict, varSelTypedDict, lviTypedDict, kNN, fileNameModifier, rule, batchNo, printFlag)

print 'Finished processing Y-Variable Sets', time.ctime()

        
raw_input(" Press Enter to Close This Session ... ")


        
