'''
'''
import routineLviApplications

myDataDictName = 'PyRDataDict'

#Open Dictionary
originalDict, newDict = routineLviApplications.ReadLviDataDictionary(myDataDictName)

#Open Disctiminant Functions
#These functions are used to derive Z-Scores for the target dataset
dfunctTableName = 'DFUNCT'
readErrorFileName = 'ERROR_DFINCT'
keyVarNameList = ['VARSET3','FUNCLABEL3','VARNAMES3']
dfuncHeader, dfuncTypedDict = routineLviApplications.ReadCsvDataFileAndTransformIntoDictionaryFormat_v2(originalDict, newDict, dfunctTableName, \
                                                                                     readErrorFileName, keyVarNameList)
#
#Open Reference Dataset
#This is the dataset from which nearest neighbors are obtained
refTableName = 'LVINEW'
readErrorFileName = 'ERROR_REF'
keyVarNameList = ['LVI_FCOID']
#refHeader, refTypedDict = routineLviApplications.ReadCsvDataFileAndTransformIntoDictionaryFormat_v2(originalDict, newDict, refTableName, \
#                                                                                     readErrorFileName, keyVarNameList)
refTypedList = routineLviApplications.ReadCsvDataFile_v2(originalDict, newDict, refTableName, readErrorFileName)
#
#Open QTARGET dataset
#This is the dataset to which nearest neighbours are applied
targetTableName = 'QTARGET'
readErrorFileName = 'ERROR_TARGET'
keyVarNameList = ['TFCOID']
#targetHeader, targetTypedDict = routineLviApplications.ReadCsvDataFileAndTransformIntoDictionaryFormat_v2(originalDict, newDict, targetTableName, \
#                                                                                     readErrorFileName, keyVarNameList)
targetTypedList = routineLviApplications.ReadCsvDataFile_v2(originalDict, newDict, targetTableName, readErrorFileName)


maxKNN = 5
print '\n The default is to identify up to 5 nearest neighbours'
maxKNNFlag = raw_input("\n Enter 'Yes' without '' if you wish to change the default, then press ENTER ... ")
if maxKNNFlag == 'Yes' or maxKNNFlag == 'YES' or maxKNNFlag == 'yes' or maxKNNFlag == 'Y' or maxKNNFlag == 'y' :
    maxKNN = raw_input("\n Enter the maximum number of k nearest neighbours, then press ENTER ...")
    maxKNN = int(maxKNN)                   
zNorm = 'YES'
varSetList = [64]
print '\n The demo varSetList = [64], referring to VARSET in XVARSELV.csv'
varSetList = input("\n List the variable sets to be included in this analysis, e.g. [64,65,66], then press ENTER ...")

#1. Extract 


#routineLviApplications.getTargetDatasetNearestNeighboursForManyVarsets(maxKNN, varSetList, targetTypedDict, targetHeader, \
#                                                                       refTypedDict, refHeader, dfuncTypedDict, zNorm)
print '\n TARGET NEAREST NEIGHBOUR ANALYSIS COMPLETED'

raw_input(" Press Enter to Close This Session ... ")  
        
