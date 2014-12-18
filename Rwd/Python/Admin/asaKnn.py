'''
'''
#import RESET_SYS_PATH
#import sys
#sys.path.append('C:\\Anaconda\\Lib\\site-packages\\')
import numpy
from scipy import spatial
import dataMachete
import asaMVA
import miniApp
from copy import deepcopy

def getNearestNeighbours(refData =[[]],targData=[[]], kNearestNeighbours =1, eps=0, minkowski=2, \
                         keyRefValueList=[[]], keyTargValueList=[[]]):
    '''
    '''
    distList, kNN = compileNearestNeighbours(refData,targData,kNearestNeighbours,eps,minkowski)
    kNNKeyValuesList = substituteAcualListItemsInBForListItemNumebrsInA(kNN,keyRefValueList)
    knnHeader, knnComboList = joinKNNDistAndKNNObsFileAnadAssignNewHeader(distList,kNNKeyValuesList)
    knnHeader, knnComboList = joinTargetKeyValueList(['TARGOBS'], keyTargValueList, knnHeader, knnComboList)
    knnComboList = convertKnnKeyVarValuesToIntegersAndDistValuesToFloat(knnHeader,['TARGOBS'],knnComboList, kNearestNeighbours)
    knnComboList = insertHeaderAtTopOfList(knnHeader,knnComboList)
    return knnComboList

def getNearestNeighbours_v2(refData =[[]],targData=[[]], kNearestNeighbours =1, eps=0, minkowski=2, \
                         keyRefValueList=[[]], keyTargValueList=[[]], newVarSet=0):
    '''
    '''
    distList, kNN = compileNearestNeighbours(refData,targData,kNearestNeighbours,eps,minkowski)
    kNNKeyValuesList = substituteAcualListItemsInBForListItemNumebrsInA(kNN,keyRefValueList)
    knnHeader, knnComboList = joinKNNDistAndKNNObsFileAnadAssignNewHeader(distList,kNNKeyValuesList)
    knnHeader, knnComboList = joinTargetKeyValueList_v2(['TARGOBS','VARSET'], newVarSet, keyTargValueList, knnHeader, knnComboList)
    knnComboList = convertKnnKeyVarValuesToIntegersAndDistValuesToFloat(knnHeader,['TARGOBS'],knnComboList, kNearestNeighbours)
    knnComboList = insertHeaderAtTopOfList(knnHeader,knnComboList)
    return knnComboList



def compileNearestNeighbours(refData=[[]], targData = [[]], k=1, eps=0,p=2):
    '''
    Input Data
        refData     Reference data: The data from which nearest neighbours are to be selected from
        targDate    Target data: The data to which nearest neighbours are to be assigned
        k           The number of nearest neighbours to be assigned in order of nearest to farthest
        eps         Returns approximate nearest neighbours no further than (1+eps) times the distance
                        from the real kth nearest neighbours
        p           Is the minkowski distance equal to euclidean if p=2;
                        If p='infinity' this is equal to the maximum coordinate difference distance
                
    Output data
        distances   A list of distances from nearest to farthest for each observation k nearest neighbours
        kNN         A list of observation numbers from nearest to farthest for each observation k nearest neighbours

    Note
        1. All data sets are in 2D list format without the variable names (header; top row) and without the keyy ID
        2. The variable sets include all of the variables to be used in kNN and no others   
    '''
    #Create a tree for representing the ref data
    tree = spatial.KDTree(refData, 2)
    distances, kNN = tree.query(targData, k, eps, p)
    distances = distances.tolist()
    kNN = kNN.tolist()
    return distances, kNN

def getReferenceAndTargetSelectedVariableSets(refVarSelect = [], targVarSelect=[], refDataList = [[]], targDataList=[[]]):
    '''
    '''
    refVarValueSelList = getSelectedVariableSet(refVarSelect, refDataList)
    targVarValueSelList = getSelectedVariableSet(targVarSelect, targDataList)
    return refVarValueSelList, targVarValueSelList

def getSelectedVariableSet(varSelect = [], dataTypedList = [[]]):
    '''
    '''
    subsetIntegrity = True
    uniqueSubset = True
    uniqueCompleteSet = True
    printDiagnostics = True
    #Get list of reference and target of key values
    varValueSelect = dataMachete.createNewListFromSelectVariableList(varSelect, dataTypedList, \
                                                 subsetIntegrity, uniqueSubset, uniqueCompleteSet, printDiagnostics)
    return varValueSelect

def substituteAcualListItemsInBForListItemNumebrsInA(itemRowNumbers = [[]], itemRowNumberValues = [[]]):
    '''
    Inputs
        itemRowNumbers contains lists of row numbers in which the actual value cane be found
        itemRowNumber values contains lists of actual values that can be found in a given row number

    Note:

    itemRowNo's is in the following format: [[1,2,3, ...],[3,2,4, ...]] where each of the subsets
    contains a list of row numbers referring to those row numbers in itemRowNumber values that contain
    the key variable values originally associated with a given dataset - that were removed for the purpose
    of doing data analysis.  There may be one or more key variable values assigned to a given row
    within the itemRowNumberValues, but it is recommended (preferred) that there be only 1 unique identifier.
    For example it is recommended that the itemRowNumberValues has the following format:
        [[1634],[213],[3156], ...] instead of [[1634,312,514],[5413,216,719],...]
    The format will return a List2D=[[]] file whereas the latter will return a List3D = [[[]]] file.
    
    
    '''
    noActualValuesPerSet = len(itemRowNumberValues[0])
    if not noActualValuesPerSet == 1:
        print ' asaKnn.substituteAcualListItemsInBForListItemNumebrsInA()'
        print ' Each row in the original reference dataset has more or less than 1 key value'
        print ' Ean row has:', noActualValuesPerSet, 'key values'
        print ' Processing will continue but this will cause the program to fail'
    noItemSets = len(itemRowNumbers)
    noRowNosPerItem = len(itemRowNumbers[0])
    newListOfActualValues = []
    for itemNo in range(0,noItemSets,):
        newListOfActualValues.append([])
        for rowNo in range(0,noRowNosPerItem,1):
            itemRowNo = itemRowNumbers[itemNo][rowNo]
            if noActualValuesPerSet == 1:
                #Return a List2D file
                actualValue = itemRowNumberValues[itemRowNo][0]
            else:
                
                #Return a List3D file
                actualValue = itemRowNumberValues[itemRowNo]
            newListOfActualValues[itemNo].append(actualValue)
    return newListOfActualValues


def joinKNNDistAndKNNObsFileAnadAssignNewHeader(distList=[[]],kNNKeyValuesList = [[]]):
    '''
    '''
    noDist = len(distList[0])
    noKeySubSets = len(kNNKeyValuesList[0])
    nTargObs = len(distList)   
    knnHeader = []
    knnDistComboList = []
    if not noDist == noKeySubSets:
        print ' asaKnn.joinKNNDistAndKNNObsFileAnadAssignNewHeader()'
        print ' Each row in the original reference dataset has more or less than 1 key value'
        print ' Ean row has:', noKeySubsets, 'key values'
        print ' This will cause the program to fail'
    else:
        for i in range(0,noDist,1):
            nnName = 'NN' + str(i+1)
            knnHeader.append(nnName)
        for i in range(0,noDist,1):
            nnName = 'DIST' + str(i+1)
            knnHeader.append(nnName)
        #Concatenate the second list to the first list by row 
        knnDistComboList = numpy.hstack((kNNKeyValuesList,distList))
    return knnHeader, knnDistComboList

def joinTargetKeyValueList(targKeyVarNames=['TARGOBS'], keyTargValueList = [[]], knnHeader = [], knnComboList = []):
    '''
    '''
    newHeader = numpy.concatenate((targKeyVarNames,knnHeader))
    knnComboList = numpy.hstack((keyTargValueList,knnComboList))
    newHeader = newHeader.tolist()
    knnComboList = knnComboList.tolist()
    return newHeader, knnComboList

def joinTargetKeyValueList_v2(targKeyVarNames=['TARGOBS','VARSET'], newVarSet = 0, keyTargValueList = [[]], knnHeader = [], knnComboList = []):
    '''
    '''
    newHeader = numpy.concatenate((targKeyVarNames,knnHeader))
    varSetList = numpy.transpose([[newVarSet]*len(keyTargValueList)])
    #print numpy.shape(varSetList)
    #print numpy.shape(keyTargValueList)
    knnLabelList = numpy.hstack((keyTargValueList,varSetList))
    knnComboList = numpy.hstack((knnLabelList,knnComboList))
    newHeader = newHeader.tolist()
    knnComboList = knnComboList.tolist()
    return newHeader, knnComboList

def convertKnnKeyVarValuesToIntegersAndDistValuesToFloat(knnHeader = [],knnComboKeyVarname = [], knnComboList = [[]], kNearestNeighbours = 1):
    '''
    '''
    #First column is target observation ID to be converted to integer
    nnColIndexList = []
    #distColIndexList = []
    if len(knnComboKeyVarname) == 1:
        if knnComboKeyVarname[0] in knnHeader:
            keyColIndex = knnHeader.index(knnComboKeyVarname[0])
            nnColIndexList.append(keyColIndex)    
    nRows = len(knnComboList)
    for i in range(0, kNearestNeighbours,1):
        k = i + 1
        nnName = 'NN' + str(k)
        if nnName in knnHeader:
            nnColIndex = knnHeader.index(nnName)
            nnColIndexList.append(nnColIndex)
        #distName = 'DIST' +  str(k)
        #if distName in knnHeader:
        #    distColIndex = knnHeader.index(distName)
        #    distColIndexList.append(distColIndex)
    for rowNo in range(0,nRows,1):
        for nnColNo in nnColIndexList:
            knnComboList[rowNo][nnColNo]=int(knnComboList[rowNo][nnColNo])
        #for distColNo in distColIndexList:
        #    knnComboList[rowNo][distColNo]=float(knnComboList[rowNo][distColNo])
    return knnComboList
                    
def insertHeaderAtTopOfList(knnHeader=[[]],knnComboList=[[]]):
    '''
    '''
    knnComboList.insert(0,knnHeader)
    return knnComboList

def extractDfuncVarnamesAndValuesLists(varSet=0, dfuncTypedDict={}):
    '''
    '''
    dfuncVarNameList = []
    dfuncCoefList = []
    if not dfuncTypedDict.has_key(varSet):
        print 'lviWorkFlow.extractDfuncVarnamesAndValuesLists()'
        print 'dfuncTypedDict does not have variable set number:', varSet
        print 'returning empty dfuncVarNameList and dfuncVarCoefList'
    else:
        varFuncList = dfuncTypedDict[varSet].keys()
        nFunc = len(varFuncList)
        dfuncVarNameList = dfuncTypedDict[varSet][varFuncList[0]].keys()
        for i in range(0,nFunc,1):
            dfuncCoefList.append([])
            for varName in dfuncVarNameList:
                newCoef = dfuncTypedDict[varSet][varFuncList[i]][varName]['DFCOEF3']
                dfuncCoefList[i].append(newCoef)      
    return dfuncVarNameList, dfuncCoefList

        
def getkNNUsingDiscriminantFunctions(varSet = 0, dfuncTypedDict = {}, keyRefValueList =[[]],keyTargValueList=[[]], \
                                     refTypedList = [[]], targTypedList =[[]], kNearestNeighbours = 1,  \
                                     eps = 0, minkowski = 2, useDfuncVarCoef = 'Yes', normalizeFlag = 'Yes'):
    '''
    '''
    subsetIntegrity = True
    uniqueSubset = True
    uniqueCompleteSet = True
    printDiagnostics = True
    #compute nearest neighbours for each variable set
    newVarSet = int(varSet)
    dfuncVarNameList, dfuncCoefList = extractDfuncVarnamesAndValuesLists(newVarSet, dfuncTypedDict)
    #Get reference variable set that correspond with selected DFUNC variable set
    selRefValueList = dataMachete.createNewListFromSelectVariableList(dfuncVarNameList, refTypedList, \
                                                 subsetIntegrity, uniqueSubset, uniqueCompleteSet, printDiagnostics)
        
    #normalize reference data by subtracting mean and multiplying by inverse oif covariance matrix
    #Extract selected DFUNC variables from target dataset
    selTargValueList = dataMachete.createNewListFromSelectVariableList(dfuncVarNameList, targTypedList, \
                                                 subsetIntegrity, uniqueSubset, uniqueCompleteSet, printDiagnostics)
    if useDfuncVarCoef == 'Yes' or useDfuncVarCoef == 'YES' or useDfuncVarCoef == 'yes':
        #Use Zscore variable coefficients
        #Get reference set Z-scores using discriminant functions - dfuncCoefList
        selRefZScores = asaMVA.computeZscores(dfuncCoefList, selRefValueList)
        #Compute target data zscore
        selTargZScores = asaMVA.computeZscores(dfuncCoefList, selTargValueList)
    else:
        #Don't use Zscore variable coeficients; use original X-Variable set insead
        selRefZScores = selRefValueList
        selTargZScores = selTargValueList
    if normalizeFlag == 'Yes' or normalizeFlag == 'YES' or normalizeFlag == 'yes':
        #Normalize reference and target data using reference data means and covariance matrix
        #retrieve vraible means and inverse covariance matrix to normalize target dataset
        meanVector, covMatrix, invCovMatrix, refNormData = asaMVA.normalizeDataset_ReturnListMeanVectorInvCovMatrix(selRefZScores)
        targNormData = asaMVA.normalizeDatasetUsingMeanVectorPlusCovarianceMatrix(selTargZScores, meanVector, invCovMatrix)
    else:
        #Use non-normalized dataset
        refNormData = selRefZScores
        targNormData = selTargZScores
    #Normalization allows for use of euclidean distances
    knnComboList = getNearestNeighbours_v2(refNormData,targNormData, kNearestNeighbours, eps, minkowski, \
                         keyRefValueList, keyTargValueList, newVarSet)
    #distList, kNN = compileNearestNeighbours(refNormData, targNormData, kNearestNeighbours, eps, minkowski)
    #kNNKeyValuesList = substituteAcualListItemsInBForListItemNumebrsInA(kNN,keyRefValueList)
    #knnHeader, knnComboList = joinKNNDistAndKNNObsFileAnadAssignNewHeader(distList,kNNKeyValuesList)
    #knnHeader, knnComboList = joinTargetKeyValueList(['TARGOBS'], keyTargValueList, knnHeader, knnComboList)
    #knnComboList = convertKnnKeyVarValuesToIntegersAndDistValuesToFloat(knnHeader,['TARGOBS'],knnComboList, kNearestNeighbours)
    #knnComboList = insertHeaderAtTopOfList(knnHeader,knnComboList)
    return knnComboList


def getkNNUsingXVARSELV1(xvarselvTypedList = [[]], keyRefValueList =[[]],keyTargValueList=[[]], \
                                     refTypedList = [[]], targTypedList =[[]], kNearestNeighbours = 1,  \
                                     eps = 0, minkowski = 2, normalizeFlag = 'Yes'):
    '''
    '''
    subsetIntegrity = True
    uniqueSubset = True
    uniqueCompleteSet = True
    printDiagnostics = True
    #compute nearest neighbours for each variable set
    varSelCriteria = 'X'
    xVariableList = miniApp.selectAnalysisVariables(varSelCriteria, xvarselvTypedList)
    #Get reference variable set that correspond with selected DFUNC variable set
    selRefValueList = dataMachete.createNewListFromSelectVariableList(xVariableList, refTypedList, \
                                                 subsetIntegrity, uniqueSubset, uniqueCompleteSet, printDiagnostics)
        
    #normalize reference data by subtracting mean and multiplying by inverse oif covariance matrix
    #Extract selected DFUNC variables from target dataset
    selTargValueList = dataMachete.createNewListFromSelectVariableList(xVariableList, targTypedList, \
                                                 subsetIntegrity, uniqueSubset, uniqueCompleteSet, printDiagnostics)
    if normalizeFlag == 'Yes' or normalizeFlag == 'YES' or normalizeFlag == 'yes':
        #Normalize reference and target data using reference data means and covariance matrix
        #retrieve vraible means and inverse covariance matrix to normalize target dataset
        meanVector, covMatrix, invCovMatrix, refNormData = asaMVA.normalizeDataset_ReturnListMeanVectorInvCovMatrix(selRefValueList)
        targNormData = asaMVA.normalizeDatasetUsingMeanVectorPlusCovarianceMatrix(selTargValueList, meanVector, invCovMatrix)
    else:
        #Use non-normalized dataset
        refNormData = selRefValueList
        targNormData = selTargValueList
        
    knnComboList = getNearestNeighbours(refNormData,targNormData, kNearestNeighbours, eps, minkowski, \
                         keyRefValueList, keyTargValueList)
   
    return knnComboList

def readDFUNCTFile(dfuncTableName ='', dataOutPath='', errorDiagnosticPath='', dfuncKeyVarNames=[],\
                                 originalDict={}, newDict={}, fileExtension='.txt'):
    '''
    '''
    #Open discriminant function file name
    readErrorFileName = 'ERROR_DFUNCT.txt'
    errorPath = errorDiagnosticPath + readErrorFileName
    fileExtension = ''        
    dfuncTypedList, dfuncTypedDict = dataMachete.getListArrayAndDictDB(dfuncTableName,dataOutPath, errorPath, dfuncKeyVarNames, \
                                                                                originalDict, newDict, fileExtension)
    return dfuncTypedDict

def readXVARSELV1File(xVarSelectTableName ='', dataInPath='', errorDiagnosticPath='', xVarKeyVarNames=[],\
                                 originalDict={}, newDict={}, fileExtension='.txt'):
    '''
    '''
    #Open XVARSELV1.csv
    readErrorFileName = 'ERROR_XVARSELV.txt'
    errorPath = errorDiagnosticPath + readErrorFileName
    fileExtension = ''
    xvarselvTypedList, xvarselvTypedDict = dataMachete.getListArrayAndDictDB(xVarSelectTableName,dataInPath, errorPath, xVarKeyVarNames, \
                                                                                originalDict, newDict, fileExtension)
    #Get candidate x-variable set (note that this set must apply to both reference and target datasets)
    return xvarselvTypedList

def compileKnnVariableSelectionLists(knnMax = 0, knnHeader = ['TARGOBS','VARSET','NN1','NN2','DIST1','DIST2']):
    '''
    '''
    knnVarSelect = []
    for i in range(0,knnMax+1,1):
        nnName = 'NN' + str(i)
        if nnName in knnHeader:
            knnVarSelect.append(nnName)
    distVarSelect = []
    for i in range(0,knnMax+1,1):
        nnName = 'DIST' + str(i)
        if nnName in knnHeader:
            distVarSelect.append(nnName)
    return knnVarSelect, distVarSelect

def checkNearestNeighbourCriteria(refVarValue, listOfExcludedValues = [], minIncludeValue = '', maxIncludeValue = ''):
    '''
    '''
    flag = True
    if not listOfExcludedValues == []:
        if refVarValue in listOfExcludedValues:
            flag = False
    if not minIncludeValue == '':
        if refVarValue < minIncludeValue:
            flag = False
    if not maxIncludeValue == '':
        if refVarValue > maxIncludeValue:
            flag = False
    return flag

def initializeTargetObsStatSets(keyList = [], nKNN = 1, stat ='MEAN',varSelList = [], uid = 1):
    '''
    '''
    newStatList = []
    for NN in range(0,nKNN):
        newStatList.append([uid])
        uid = uid + 1
        for keyValue in keyList:
            newStatList[NN].append(keyValue)
        newStatList[NN].append(NN+1)
        newStatList[NN].append(stat)
        for varName in varSelList:
            newStatList[NN].append(0)
    return newStatList, uid

def compileNearestNeighbourStatistics(statsList=[[]], varSelList=[], refKeyValueList = [[]], \
                                            refSelValueList=[[]], knnKeyList=[[]], knnRefIdList=[[]], \
                                            knnDistList=[[]], knnMax=5, distancePower=0, \
                                            listOfExcludedValues=[], minIncludeValue = '',
                                             maxIncludeValue = '', outputMean = 'YES', outputStdev = 'YES'):
    '''
    This routine computes means and standard deviations for each target dataset observation
    given a variable set used to assign k = 1 to knnMax nearest neighbours.  The routine
    is called by compileLdataKnnStats().

    Inputs
        statsList: This is an initial output file with a header containg the following information:
            Unique Key ID (TARGOBS) relating to the target dataset.
            Unique Variable Set ID relating to the set of  X variables (VARSET) used to establish the k Nearest Neighbours
            KNN refering to the number of nearest neighbours from 1 up to a maximum of knnMax
            STAT this column is created to indicate the statistic that is being produced e.g. MEAN or standard deviation (STDEV)
            
        varSelList: This is the list of variables in the reference dataset that are used to calculate the statistics with reference
                    to the targbet dataset k-Nearest Neighbours.

        refKeyValueList: This is the list of keys associated with each reference observation and associated values in erfSelValueList.

        refSelValueList:  This is the list of variable values associated with each reference dataset observation listed in the same order
                          as the associated variable names in varSetList.

        knnKeyList:  This is a list of target observation and variable set keys associated with the identification of the k-Nearest Neighbours
                     in the target dataset.

        knnRefIdList:   This is the list of reference dataset IDs associated with k = 1 up to (<=) knnMax nearest neighbours starting at the
                        nearest neighbour, and then moving to the next nearest neighbour ... and so on. The knnRefKeyList contains the list
                        of target observation keys associated with each observation listed in the same order as they occur and containing
                        the same number of records (rows).

        knnDistList:    This contains the distances from the target observation to each of the nearest neighbours selected from the reference
                        dataset (identified in knnRefIdList).

        knnMax:         This is the maximum number of nearest neighbours listed for any one target observations; the actual number of nearest
                        neighbours associated with a given target observation must be less than or equal to this number.

        distancePower:  This is the power assigned to each distance in knnMax, i.e. knnMax**distancePower. Zero (0) gives equal weight to
                        all nearest neighbours, One (1) weights the statistics in proportion to  1/distance**1, two (2) in proportion
                        to 1/distance**2, etc.

        listOfExcludedValues:   This is a list of values that are to be excluded from the calculation of statistics associated with the k_nearest
                                neighbours.  In particular there are circumstances when zero's should not be included in the calculation of means
                                and standard deviations.  Other variables (e.g. -1; na) may be used to indiocated missing data and may be included
                                in the list.  When this is an empty list there are no values that will be excluded.

        minIncludeValue:        This is the minimum value for all of the variables that may be included in estimating the statistics.  If left blank
                                ('') then no minimum will be applied.

        maxIncludeValue:        This is the maximum value for all of the variables that may be included in estimating the statistics.  If left blank
                                ('') then no maximum will be applied. 
            
    '''
    nVarSel = len(varSelList)                   #Number of variables in variable selection list
    nTargObs = len(knnKeyList)                  #Number of target observations in combination with certain variable sets to which nearest neighbours have been assigned
    nRefObs = len(refKeyValueList)              #Number of refernce of observations
    nStatsList = len(statsList)                 #Current length of stats list
    if distancePower == '' or distancePower < 0:
        distanceWeight = 0
    if not len(knnRefIdList) == nTargObs:
        print ' asaKnn.compileNearestNeighbourStatistics()'
        print ' Number of keys in knnKeyList: ', nTargObs, '\n not equal to the number of target observations: ', len(knnRefIdList), '\n in the nearest neighbour list: knnRefIdList.'
    if not len(refSelValueList) == nRefObs:
        print ' asaKnn.compileNearestNeighbourStatistics()'
        print ' Number of keys in refKeyValueList: ', nRefObs, '\n not equal to the number of reference observations: ', len(refSelValueList), '\n in the reference variable value list: refSelValueList.'        
    #Start processing
    uid = 1     #Initialize unique ID for dataset
    for targObsNo in range(0,nTargObs,1):
        nKNN = len(knnRefIdList[targObsNo])
        #print nKNN
        #Initialize stats lists with 2DList containing one list for each k Nearest neighbours startin from 1 to nKNN; update unique ID's
        if outputMean == 'YES' or outputMean == 'Yes' or outputMean == 'yes' or outputMean == 'Y' or outputMean =='y':
            meanStatList, uid = initializeTargetObsStatSets(knnKeyList[targObsNo], nKNN, 'MEAN',varSelList, uid)
        if outputStdev == 'YES' or outputStdev == 'Yes' or outputStdev == 'yes' or outputStdev == 'Y' or outputStdev =='y':
            stdevStatList, uid = initializeTargetObsStatSets(knnKeyList[targObsNo], nKNN, 'STDEV',varSelList, uid)
        #for each variable 
        for varNo in range(0, nVarSel,1):
            varName = varSelList[varNo]                             #Get the variable name associated with the variable number
            varColIndex = statsList[0].index(varName)               #Get the column number where the variable name statistics are to be entered
            #start processing means
            valueVector = []
            weightVector = []
            varSum = 0                                              #Initlaize the sum of the values for the variable associated with a given reference observation 
            distanceSum = 0                                         #Initlaize the sum of the distances for a given target observation from a given reference observation 
            mean = 0                                                #Initialize the mean value for a given variable name associated with k nearest neighbours
            stdev = 0                                               #Initialize the standard deviation for a given variable name associated with k nearest neighbours        
            distanceCount = 0                                       #This is used in calculating standard deviation to account for loss in degrees of freedom due to calulation of the mean
            #                                                       #DistanceCount is equal to the number of nearest neighbour values included in the calculation
            for k in range(0,nKNN,1):
                refNeighbourKey = knnRefIdList[targObsNo][k]        #Identify the reference dataset ID associated with the k nearest neighbour
                if not type(refNeighbourKey)== list:
                    refNeighbourKey = [refNeighbourKey]             #If the reference dataset ID is not in a list format put it in that format
                if not refNeighbourKey in refKeyValueList:          #If the reference dataset ID is not in the refKeyValueList there is a problem
                    print ' asaKnn.compileNearestNeighbourStatistics()'
                    print ' reference key value: ', refNeighbourKey, '\n associated with nearest neighbour target observation: ', targObsNo, '\n not found in reference data key list: refKeyValueList.'                
                refRowIndex = refKeyValueList.index(refNeighbourKey)    #Get the row index containing the variable values associated with the reference dataset ID
                refVarValue = refSelValueList[refRowIndex][varNo]       #Get the variable value
                valueVector.append(refVarValue)                         #Append the reference variable value for the kth nearest neighbour to the valueVector
                distance = knnDistList[targObsNo][k]                    #Get the associated distance metric for the kTh nearest neighbour 
                distanceWeight = 1/(distance**distancePower)            #Compute the distance weight
                weightVector.append(distanceWeight)                     #Append the distance weight to the weightVector for the kth nearest neighbour
                includeFlag = checkNearestNeighbourCriteria(refVarValue, listOfExcludedValues, minIncludeValue, maxIncludeValue) #Check if the refVarValue is to be included or excluded from the calculation
                if includeFlag == True:                                 #If the refVarValue is to be included
                    distanceSum = distanceSum + distanceWeight          #Add the associated distance to the sum of distances
                    distanceCount = distanceCount + 1
                    varSum = varSum + refVarValue * distanceWeight      #Add the refVarValue weighted by the distance weight to the variable sum
                    if not distanceSum == 0:                            #If the distance sum is 0 then the mean is 0 and the stdev is 0
                        mean = varSum/distanceSum                       #If not then calculate the mean; divide the variable sum by the distance sum
                        sumOfSquares = 0                                #Initialize the (weighted) sum of squared differences from the mean 
                        for i in range(0,k,1):                          #For each nearest neighbour 0 to k considered up t this stage
                            refVarValue = valueVector[i]                #Get the refVarValue
                            includeFlag = checkNearestNeighbourCriteria(refVarValue, listOfExcludedValues, minIncludeValue, maxIncludeValue) #Check to make sure that that value is to be included in the computation
                            if includeFlag == True:                     #If the includeFlag is True then the value is to be included
                                distanceWeight = weightVector[i]        #Retrieve the associated distance based weight
                                sumOfSquares = sumOfSquares + ((refVarValue-mean)**2)*distanceWeight #Update the weighted sum of squares diatnces                               
                        if distanceCount <= 1:                          #DistanceCount is equal to the number of nearest neighbour values included in the calculation
                            stdev = 0                                   #If the variance is 0 the standard deviation is zero
                        else:
                            varCorrectionFactor = distanceSum/distanceCount  #Estimate the loss in degrees of freedom due to calculation of the mean
                            stdev = (sumOfSquares/(distanceSum-varCorrectionFactor))**0.5         #Otherwise compute the standard deviation  
                meanStatList[k][varColIndex] = mean
                stdevStatList[k][varColIndex] = stdev
        if outputMean == 'YES' or outputMean == 'Yes' or outputMean == 'yes' or outputMean == 'Y' or outputMean =='y':
            for i in range(0,nKNN):
                statsList.append(deepcopy(meanStatList[i]))
        if outputStdev == 'YES' or outputStdev == 'Yes' or outputStdev == 'yes' or outputStdev == 'Y' or outputStdev =='y':
            for i in range(0,nKNN):
                statsList.append(deepcopy(stdevStatList[i]))
    return statsList               
                
                    
                            
                
                        
            

            
                    
                
            
        
