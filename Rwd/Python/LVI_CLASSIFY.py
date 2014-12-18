'''
This module activates the fuzzy cluster algorithm.

Inputs

1. The basic input data is LVINEW (a .csv file) with LVI_FCOID as the single primary key variable name.
2. XVARSELV1 is used to identify the Y-Variables in LVINEW to be used in building the classification.
3. FUZZYC_INITIALIZATION is used to define the type of Fuzzy C analysis, including the range in number of classes to be explored
4. PyRDataDict.csv (in \\Rwd\\Python\\DATDICT\\) contains the data dictionary identifying the variable names and types associated with LVINEW and XVARSELV1

Outputs

1. FCLASS (a .csv file) indicates the classes assigned to each observation for each classifation with N number of classes
2. FCENTROID indicates the centroid statitics for each class associated with N number of clasases for the selected set of Y-variables

'''
import routineLviApplications
#
originalDict, newDict = routineLviApplications.ReadLviDataDictionary()
dataKeyVarNameList = ['LVI_FCOID']
dataTableName = 'LVINEW'
dataTypedList = routineLviApplications.ReadCsvDataFile(newDict, dataTableName, 'ERROR-CHECK-LVUN')

#Extract Y variable classification names from XVARSELV1 
dataSelectVarNameList = routineLviApplications.ReadXVarSelv1XorYVariableList(originalDict, 'Y')
#Extract key Values in one dataList and associated selected variable values in a separate list  
dataKeyList, dataTypedSubsetList = routineLviApplications.createNewListFromSelectVariableListAndIdList(dataKeyVarNameList, dataSelectVarNameList, dataTypedList)
routineLviApplications.runFuzzyCMeansClassification(dataKeyVarNameList,dataKeyList, dataSelectVarNameList,dataTypedSubsetList)

raw_input(" Press Enter to Close This Session ... ")


