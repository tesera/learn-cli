'''
'''
import sys

#Set paths
#adminpath = r'E:\Python25\Admin'
#filepath = 'E:\\Python25\\DISTANCE\\'
#inputFileDictionary = 'TOLKO-DISTR-DICT'
#inputFileDictionary = 'DM_DICT'

#inputFile1 = 'TOLKO_DISTR_OUT'
#inputFile1 = 'DISTANCE_MATRIX_TOLKO'
#inputFile2 = ''
#printFile = '' 
#printFileDict 


#targetGroupNo = 17


#sys.path.append(adminpath)
#sys.path.append(filepath)

#import PRINTv1
#import READv1
#import MAN
#import BASE
#import MATRIX_MAN
#import bisect
from math import *
#from random import *
import numpy
import scipy
import scipy.spatial
#import time
import asaMVA
import dataMachete
from copy import deepcopy

def runFuzzyCMeansClassification(dataKeyVarNameList = [],dataKeyList = [], dataSelectVarNameList = [],dataTypedSubsetList = [[]]):
    '''
    '''
    #
    fuzzyInit = readCSV.read_csv_text_file_v2(filePath, 'FUZZYC_INITIALIZATION', '.csv')
    m_value = int(fuzzyInit[1][2])
    minError = float(fuzzyInit[2][2])
    classificationType = fuzzyInit[3][2]
    llNclass = int(fuzzyInit[4][2])
    ulNclass = int(fuzzyInit[5][2]) + 1
    if llNclass < 2:
        llNclass = 2
    if ulNclass < llNclass:
        ulNclass = llNclass + 1
    nGroupList = []
    for i in range(llNclass,ulNclass,1):
        nGroupList.append(i)
    lenNGroups = len(nGroupList)
    classListHeader = ['CID','CLASS']
    centroidHeader = joinOneDListBToRightOfOneDListA(['NCLASSES','CLASSNO'], dataSelectVarNameList)
    newCentroidList = []
    for nG in range(0, lenNGroups, 1):
        nGroups = nGroupList[nG]
        #If classification type is Fuzzy C-Means - Euclidean Distances
        if classificationType == 'FCM_E':
            classList, centroidList = fuzzyC_v2.run_fuzzy_c_means_euclidean(m_value,nGroups,dataTypedSubsetList, minError)
        #If classification type is Fuzzy C-Means - Censored Euclidean Distances - ignore zeros in determining distances
        if classificationType == 'FCM_CE':
            classList, centroidList = fuzzyC_v2.run_censored_fuzzy_c_means_euclidean(m_value,nGroups,dataTypedSubsetList, minError)
        #If classification type is Fuzzy C-Means - Mahalanobis (Note that this needs review)
        if classificationType == 'FCM_M':
            classList, centroidList, covMatrix = fuzzyC_v2.run_fuzzy_c_means_mahalonobis(m_value,nGroups,dataTypedSubsetList, minError)
        #Get a list of only the classifications in column 1 of the classList that includes record id in column 0
        newClassList = createNewListFromSelectColumnNumbersIn2DList(classList, [1])
        #compile newClassListHeader by adding the number of groups to the end of 'CLASS'
        newClassLabel = 'CLASS' + str(nGroups)
        if nG == 0:
            #Combine the lviKeyList with the classes - Include ID's produced by Fuzzy C-means algorithm in the first instance
            #Also initialize classification header and join with keyVarNames 
            classListHeader = ['CID',newClassLabel]
            updatedHeader = joinOneDListBToRightOfOneDListA(dataKeyVarNameList, classListHeader)
            classDataList = joinTwoDListBToRightOfTwoDListA(dataKeyList, classList)    
        else:
            #Get only the class assignments, not the FUZZYC id's. 
            newClassList = createNewListFromSelectColumnNumbersIn2DList(classList, [1])
            classListHeader = [newClassLabel]
            updatedHeader = joinOneDListBToRightOfOneDListA(updatedHeader, classListHeader)
            classDataList = joinTwoDListBToRightOfTwoDListA(classDataList, newClassList)
        centroidList = addIndexToRowsOnLeftSideOfArray(centroidList)
        centroidList = addListOfNumbersToLeftSideOfArray(centroidList, [nGroups])
        newCentroidList = appendListB2DToBottomOfListA2D(newCentroidList, centroidList)
    
    finalClassList = addHeaderListToDataList(updatedHeader, classDataList)
    finalCentroidList = addHeaderListToDataList(centroidHeader, newCentroidList)

    #printFilePathClass = filePath + 'FCLASS.csv'
    #addToDataMachette20121026.printList2D(finalClassList,printFilePathClass,'OVERWRITE')
    #printFilePathCentroid = filePath + 'FCENTROID.csv'
    #addToDataMachette20121026.printList2D(finalCentroidList,printFilePathCentroid,'OVERWRITE')
    return finalClassList, finalCentroidList

def runFuzzyCMeansClassification_v2(dataKeyVarNameList = [],dataKeyList = [[]], dataSelectVarNameList = [],dataTypedSubsetList = [[]]):
    '''
    '''
    #
    
    m_value = 2
    print '\n Fuzzy c-means m-value default is equal to 2.'
    print '\n Enter Y if you wish to change the m-value and then press ENTER, otherwise press ENTER'
    flag = raw_input("\n ... ")
    if flag == 'Y' or flag == 'y' or flag == 'Yes' or flag == 'yes':
        print ' \n m-value should be greater than or equal to 1'
        m_value = input("\n Enter new m-value and then press ENTER ... ")
        if m_value < 1:
            m_value = 1
    minError = 0.01
    print '\n Fuzzy c-means acceptable error default is equal to 0.01'
    print '\n Enter Y if you wish to change the acceptable error and then press ENTER, otherwise press ENTER'
    flag = raw_input("\n ... ")
    if flag == 'Y' or flag == 'y' or flag == 'Yes' or flag == 'yes':
        print '\n Acceptable error should be less than 0.1'
        minError = input("\n Enter new error threshold and then press ENTER ... ")
        if minError > 0.1:
            minError = 0.1
    classificationType = 'FCM_E'
    print '\n Enter the lower limit in number of classes within classification'
    llNclass = input("\n ... ")
    print '\n Enter the upper limit in number of classes within classification'
    ulNclass = input("\n ... ")
    ulNclass = ulNclass + 1
    if llNclass < 2:
        llNclass = 2
    if ulNclass < llNclass:
        ulNclass = llNclass + 1
    nGroupList = []
    for i in range(llNclass,ulNclass,1):
        nGroupList.append(i)
    lenNGroups = len(nGroupList)
    classListHeader = ['CID','CLASS']
    centroidHeader = dataMachete.join1DListBToRightOf1DListA(['NCLASSES','CLASSNO'], dataSelectVarNameList)
    newCentroidList = []
    membershipList = []
    for nG in range(0, lenNGroups, 1):
        nGroups = nGroupList[nG]
        #If classification type is Fuzzy C-Means - Euclidean Distances
        if classificationType == 'FCM_E':
            classList, centroidList, membershipMatrix = run_fuzzy_c_means_euclidean(m_value,nGroups,dataTypedSubsetList, minError)
        #If classification type is Fuzzy C-Means - Censored Euclidean Distances - ignore zeros in determining distances
        if classificationType == 'FCM_CE':
            classList, centroidList, membershipMatrix = run_censored_fuzzy_c_means_euclidean(m_value,nGroups,dataTypedSubsetList, minError)
        #If classification type is Fuzzy C-Means - Mahalanobis (Note that this needs review)
        if classificationType == 'FCM_M':
            classList, centroidList, covMatrix, membershipMatrix = run_fuzzy_c_means_mahalonobis(m_value,nGroups,dataTypedSubsetList, minError)
        #Get a list of only the classifications in column 1 of the classList that includes record id in column 0
        newClassList = dataMachete.createNewListFromSelectColumnNumbersIn2DList(classList, [1])
        #compile newClassListHeader by adding the number of groups to the end of 'CLASS'
        newClassLabel = 'CLASS' + str(nGroups)
        if nG == 0:
            #Combine the lviKeyList with the classes - Include ID's produced by Fuzzy C-means algorithm in the first instance
            #Also initialize classification header and join with keyVarNames 
            classListHeader = ['CID',newClassLabel]
            updatedHeader = dataMachete.join1DListBToRightOf1DListA(dataKeyVarNameList, classListHeader)
            classDataList = dataMachete.join2DListBToRightOf2DListA(dataKeyList, classList)
            membershipList = [[]]
            membershipList = updateMembershipList(dataKeyVarNameList,ulNclass, dataKeyList, membershipList, membershipMatrix, nGroups)
        else:
            #Get only the class assignments, not the FUZZYC id's.
            classListHeader = [newClassLabel]
            updatedHeader = dataMachete.join1DListBToRightOf1DListA(updatedHeader, classListHeader)
            classDataList = dataMachete.join2DListBToRightOf2DListA(classDataList, newClassList)
            membershipList = updateMembershipList(dataKeyVarNameList,ulNclass, dataKeyList, membershipList, membershipMatrix, nGroups)
        centroidList = dataMachete.addIndexToRowsOnLeftSideOfArray(centroidList)
        centroidList = dataMachete.addListOfNumbersToLeftSideOfArray(centroidList, [nGroups])
        newCentroidList = dataMachete.appendRowsFrom2DListBTo2DListA(centroidList, newCentroidList)
        
    finalClassList = dataMachete.addHeaderListToDataList(updatedHeader, classDataList)
    finalCentroidList = dataMachete.addHeaderListToDataList(centroidHeader, newCentroidList)

    #printFilePathClass = filePath + 'FCLASS.csv'
    #addToDataMachette20121026.printList2D(finalClassList,printFilePathClass,'OVERWRITE')
    #printFilePathCentroid = filePath + 'FCENTROID.csv'
    #addToDataMachette20121026.printList2D(finalCentroidList,printFilePathCentroid,'OVERWRITE')
    return finalClassList, finalCentroidList, membershipList

def runFuzzyCMeansClassification_v3(dataKeyVarNameList = [],dataKeyList = [[]], dataSelectVarNameList = [], \
                                    dataTypedSubsetList = [[]], m_value = 2, minError = 0.01, llNclass = 2, \
                                    ulNclass = 2, classificationType = 'FCM_E', classBaseName = 'CLASS'):
    '''
    '''
    #
    
    #flag = raw_input("\n ... ")
    if m_value < 1:
        m_value = 1
    if minError > 0.1:
        minError = 0.1
    #classificationType = 'FCM_E'
    ulNclass = ulNclass + 1
    if llNclass < 2:
        llNclass = 2
    if ulNclass < llNclass:
        ulNclass = llNclass + 1
    nGroupList = []
    for i in range(llNclass,ulNclass,1):
        nGroupList.append(i)
    lenNGroups = len(nGroupList)
    classListHeader = ['CID',classBaseName]
    centroidHeader = dataMachete.join1DListBToRightOf1DListA(['NCLASSES','CLASSNO'], dataSelectVarNameList)
    newCentroidList = []
    membershipList = []
    for nG in range(0, lenNGroups, 1):
        nGroups = nGroupList[nG]
        #If classification type is Fuzzy C-Means - Euclidean Distances
        if classificationType == 'FCM_E':
            classList, centroidList, membershipMatrix = run_fuzzy_c_means_euclidean(m_value,nGroups,dataTypedSubsetList, minError)
        #If classification type is Fuzzy C-Means - Censored Euclidean Distances - ignore zeros in determining distances
        if classificationType == 'FCM_CE':
            classList, centroidList, membershipMatrix = run_censored_fuzzy_c_means_euclidean(m_value,nGroups,dataTypedSubsetList, minError)
        #If classification type is Fuzzy C-Means - Mahalanobis (Note that this needs review)
        if classificationType == 'FCM_M':
            classList, centroidList, covMatrix, membershipMatrix = run_fuzzy_c_means_mahalonobis(m_value,nGroups,dataTypedSubsetList, minError)
        #Get a list of only the classifications in column 1 of the classList that includes record id in column 0
        newClassList = dataMachete.createNewListFromSelectColumnNumbersIn2DList(classList, [1])
        #compile newClassListHeader by adding the number of groups to the end of 'CLASS'
        newClassLabel = classBaseName + str(nGroups)
        if nG == 0:
            #Combine the lviKeyList with the classes - Include ID's produced by Fuzzy C-means algorithm in the first instance
            #Also initialize classification header and join with keyVarNames 
            classListHeader = ['CID',newClassLabel]
            updatedHeader = dataMachete.join1DListBToRightOf1DListA(dataKeyVarNameList, classListHeader)
            classDataList = dataMachete.join2DListBToRightOf2DListA(dataKeyList, classList)
            membershipList = [[]]
            membershipList = updateMembershipList(dataKeyVarNameList,ulNclass, dataKeyList, membershipList, membershipMatrix, nGroups)
        else:
            #Get only the class assignments, not the FUZZYC id's.
            classListHeader = [newClassLabel]
            updatedHeader = dataMachete.join1DListBToRightOf1DListA(updatedHeader, classListHeader)
            classDataList = dataMachete.join2DListBToRightOf2DListA(classDataList, newClassList)
            membershipList = updateMembershipList(dataKeyVarNameList,ulNclass, dataKeyList, membershipList, membershipMatrix, nGroups)
        centroidList = dataMachete.addIndexToRowsOnLeftSideOfArray(centroidList)
        centroidList = dataMachete.addListOfNumbersToLeftSideOfArray(centroidList, [nGroups])
        newCentroidList = dataMachete.appendRowsFrom2DListBTo2DListA(centroidList, newCentroidList)
        
    finalClassList = dataMachete.addHeaderListToDataList(updatedHeader, classDataList)
    finalCentroidList = dataMachete.addHeaderListToDataList(centroidHeader, newCentroidList)

    #printFilePathClass = filePath + 'FCLASS.csv'
    #addToDataMachette20121026.printList2D(finalClassList,printFilePathClass,'OVERWRITE')
    #printFilePathCentroid = filePath + 'FCENTROID.csv'
    #addToDataMachette20121026.printList2D(finalCentroidList,printFilePathCentroid,'OVERWRITE')
    return finalClassList, finalCentroidList, membershipList

def applyExistingFuzzyCMeansClassification_v3(dataKeyVarNameList = [],dataSelectVarNameList = [], dataKeyList = [[]], dataTypedSubsetList = [[]], \
                                    centroidKeyVarNameList = [], centroidTypedList = [[]], m_value = 2, printNclasses = 'YES', classBaseName = 'CLASS', \
                                    classificationType = 'FCM_E'):
    '''
    '''
    #
    
    #flag = raw_input("\n ... ")
    if m_value < 1:
        m_value = 1
    nGroupList = []
    #Get number of Groups
    nplotIdColIndex = centroidTypedList[0].index('NCLASSES')
    nCentroidRows = len(centroidTypedList)
    nCentroidCols = len(centroidTypedList[0])
    for centroid in range(1,nCentroidRows,1):
        nClasses = centroidTypedList[centroid][nplotIdColIndex]
        if not nClasses in nGroupList:
            nGroupList.append(nClasses)
    nGroupList.sort()
    ulNclass = max(nGroupList) + 1
    lenNGroups = len(nGroupList)
    classListHeader = ['CID',classBaseName]
    centroidHeader = deepcopy(centroidTypedList)
    membershipList = []
    for nG in range(0, lenNGroups, 1):
        nGroups = nGroupList[nG]
        newCentroidList = []
        rowCount = 0
        for centroid in range(1,nCentroidRows,1):
            nClasses = centroidTypedList[centroid][nplotIdColIndex]
            if nClasses == nGroups:
                newCentroidList.append([])
                for varNo in range(0,nCentroidCols):
                    varName = centroidTypedList[0][varNo]
                    if not varName in centroidKeyVarNameList:
                        varValue = centroidTypedList[centroid][varNo]
                        newCentroidList[rowCount].append(varValue)
                rowCount = rowCount + 1
        #If classification type is Fuzzy C-Means - Euclidean Distances
        if classificationType == 'FCM_E' :
            classList, membershipMatrix = apply_fuzzy_c_means_euclidean(m_value,nGroups,dataTypedSubsetList, newCentroidList, printNclasses)
        #If classification type is Fuzzy C-Means - Censored Euclidean Distances - ignore zeros in determining distances
        #if classificationType == 'FCM_CE':
        #    classList, centroidList, membershipMatrix = run_censored_fuzzy_c_means_euclidean(m_value,nGroups,dataTypedSubsetList, minError)
        #If classification type is Fuzzy C-Means - Mahalanobis (Note that this needs review)
        #if classificationType == 'FCM_M':
        #    classList, centroidList, covMatrix, membershipMatrix = run_fuzzy_c_means_mahalonobis(m_value,nGroups,dataTypedSubsetList, minError)
        #Get a list of only the classifications in column 1 of the classList that includes record id in column 0
        newClassList = dataMachete.createNewListFromSelectColumnNumbersIn2DList(classList, [1])
        #compile newClassListHeader by adding the number of groups to the end of 'CLASS'
        newClassLabel = classBaseName + str(nGroups)
        if nG == 0:
            #Combine the lviKeyList with the classes - Include ID's produced by Fuzzy C-means algorithm in the first instance
            #Also initialize classification header and join with keyVarNames 
            classListHeader = ['CID',newClassLabel]
            updatedHeader = dataMachete.join1DListBToRightOf1DListA(dataKeyVarNameList, classListHeader)
            classDataList = dataMachete.join2DListBToRightOf2DListA(dataKeyList, classList)
            membershipList = [[]]
            membershipList = updateMembershipList(dataKeyVarNameList,ulNclass, dataKeyList, membershipList, membershipMatrix, nGroups)
        else:
            #Get only the class assignments, not the FUZZYC id's.
            classListHeader = [newClassLabel]
            updatedHeader = dataMachete.join1DListBToRightOf1DListA(updatedHeader, classListHeader)
            classDataList = dataMachete.join2DListBToRightOf2DListA(classDataList, newClassList)
            membershipList = updateMembershipList(dataKeyVarNameList,ulNclass, dataKeyList, membershipList, membershipMatrix, nGroups)
    finalClassList = dataMachete.addHeaderListToDataList(updatedHeader, classDataList)
    
    #printFilePathClass = filePath + 'FCLASS.csv'
    #addToDataMachette20121026.printList2D(finalClassList,printFilePathClass,'OVERWRITE')
    #printFilePathCentroid = filePath + 'FCENTROID.csv'
    #addToDataMachette20121026.printList2D(finalCentroidList,printFilePathCentroid,'OVERWRITE')
    return finalClassList, membershipList

def updateMembershipList(dataKeyVarNameList = [],ulNclass = 0, dataKeyList = [[]], membershipList = [[]], membershipMatrix = [[]], nGroups = 2):
    '''
    '''
    membRowCount = len(membershipList[0])           #If the first row is an empty list then a new header is created below   
    keyCount = len(dataKeyList)                     #Count the number of keys in the original data
    row = len(membershipList)                       #Row to start with appending new values
    if not len(dataKeyList) == len(membershipMatrix):
        print 'asaClassifiers.updateMembershipList'
        print 'membership matrix length:', len(membershipMatrix), '\n not equal to keyList length:', len(dataKeyList)
    if membRowCount == 0:
        membershipList[0] = ['NCLASSES']            #The number of classes in a given classification is a primary key
        for keyVarName in dataKeyVarNameList:       #The keys associated with the unique identification of each record are primary keys
            newVar = keyVarName                     
            membershipList[0].append(newVar)            
        for classNo in range(0, ulNclass-1, 1):       #The class numbers used in each row range from 0 up to the upper limit number of classes 
            membershipList[0].append(classNo)
    for keyNo in range(0,keyCount,1):
        membershipList.append([nGroups])                 #Assign the number of classes identified in the classification
        for keyVarValue in dataKeyList[keyNo]:
            membershipList[row].append(keyVarValue)
        for classNo in range(0,nGroups,1):                      #Assign the memberships for each class in the classification
            membershipValue = membershipMatrix[keyNo][classNo]
            membershipList[row].append(membershipValue)
        for classNo in range(nGroups,ulNclass-1,1):               #Assign zero's to the remaining classes for which there are no memberships up to the upper limit
            membershipList[row].append(0)
        row = row + 1
    return membershipList


def initialize_distMatrix_old(distKeyList,distDict):
    distMatrix = []
    i = 0
    for primaryKey in distKeyList:
        distMatrix.append([])
        j = 0
        for secondaryKey in distKeyList:
            distMatrix[i].append(distDict[primaryKey][secondaryKey]['TD'])
        i = i + 1
    return distMatrix

def initialize_distMatrix_new(distDict):
    distMatrix = []
    i = 0
    uidKeyList = distDict.keys()
    uidKeyList.sort()
    for uid in uidKeyList:
        distMatrix.append([])
        dbhKeyList = distDict[uid].keys()
        dbhKeyList.sort()
        for dbh in dbhKeyList:
            distMatrix[i].append(distDict[uid][dbh]['LBPH'])
        for dbh in dbhKeyList:
            distMatrix[i].append(distDict[uid][dbh]['LTPH'])
        i = i + 1
    return distMatrix

def initialize_mahalanobis_v2_standard_deviations(varMatrix):
    '''
    varMatrix is the inputData nClasses is equal to nGroups
    
    This subroutine initializes the standard deviations for the input data
    where variables are in the columns.  A standard deviation
    is calculated for each variable.

    The output of this function are standard deviations by variable (in the columns).
    '''
    nVariables = len(varMatrix[0])
    varMatrixT = transpose_varList(varMatrix)
    varStdev = get_standard_deviation_vector_from_transposed_array(varMatrixT)    
    return varStdev

def initialize_mahalanobis_v3_standard_deviations(varMatrix, nObs):
    '''
    varMatrix is the inputData nClasses is equal to nGroups
    
    This subroutine initializes the standard deviations for the input data
    where variables are in the columns.  A standard deviation
    is calculated for each variable.

    The output of this function are standard deviations by variable (in the columns).
    '''
    
    #varMatrixT = MATRIX_MAN.get_transpose_of_matrix(varMatrix)
    varMatrixT = asaMVA.get_transpose_of_matrix(varMatrix)
    #varCovariance = MATRIX_MAN.matrix_multiply_inner_product(varMatrixT, varMatrixT)
    varCovariance = asaMVA.matrix_multiply_inner_product(varMatrixT, varMatrixT)
    varCovariance = (1/float(nObs))*varCovariance
    return varCovariance

def initialize_centroid_matrix(distMatrix, k_centroids):
    #The number of variables representing each observation
    #is computed in terms of end_i
    #Number of observations
    end_i = len(distMatrix)
    #Number of variables
    end_j = len(distMatrix[0])
    initialCentroidMatrix = []
    centroidRatio = 1/float(k_centroids + 1)
    centroidIncrement = centroidRatio
    centroidIndexList = []
    #initialize centroid indices
    for k in range(0, k_centroids,1):
        centroidIndex = int(centroidRatio * end_j)
        centroidIndexList.append(centroidIndex)
        centroidRatio = centroidRatio + centroidIncrement
    for k in range(0,k_centroids,1):
        initialCentroidMatrix.append([])
        centroidIndex = centroidIndexList[k]
        for j in range(0, end_j,1):
            #print i, centroidIndex
            centroidValue = distMatrix[centroidIndex][j]
            #Don't allow centroids with values == 0
            if centroidValue == 0:
                centroidValue = 1
            initialCentroidMatrix[k].append(centroidValue)
    return initialCentroidMatrix

def initialize_centroid_matrix_max_min_rule(distList, k_centroids):
    '''
    This routine finds the two most polar opposite pairs and establishes these as initial
    centroids.  It then finds successive polar opposite observations from the previously
    selected centroids and adds these as centroids until k_centroids are selected.
    '''
    initial_centroid_matrix = []
    end_i = len(distList)
    end_k = len(distList[0])
    maxDist = 0
    maxPairs = []
    for i in range(0,end_i,1):
        #newDict.update({i:{}})
        for j in range(0,end_i,1):
            diffSum = 0
            for k in range(0,end_k,1):
                diffSum = diffSum + (distList[i][k]-distList[j][k])**2
            diffSum = sqrt(diffSum)
            if diffSum > maxDist:
                maxDist = diffSum
                maxPairs = [i,j]
    #print maxPairs
    #print maxDist
    #Iterate until the i number of groups is obtained
    for i in range(2,k_centroids,1):
        maxDist = -1
        maxObs = -1
        end_l = len(maxPairs)
        #For all j observations
        for j in range(0,end_i,1):
            if not j in maxPairs:
                #For each observation number l, obsNo in maxPairs
                diffList = []
                for l in range(0,end_l,1):
                    obsNo = maxPairs[l]
                    #for each variable
                    for k in range(0,end_k,1):
                        diffSum = diffSum + (distList[j][k]-distList[obsNo][k])**2
                    diffSum = sqrt(diffSum)
                    diffList.append(diffSum)
                #If the difference between the two is greater than maxDist
                #Make that observation, j, the next one in the maxPairs list
                #diffSum = numpy.mean(diffList)
                diffSum = min(diffList)
                if diffSum > maxDist:
                    maxDist = diffSum
                    maxObs = j
        maxPairs.append(maxObs)
    for i in range(0,k_centroids,1):
        initial_centroid_matrix.append([])
        obsNo = maxPairs[i]
        for k in range(0,end_k,1):
            varValue = distList[obsNo][k]
            initial_centroid_matrix[i].append(varValue)
    return initial_centroid_matrix

def initialize_centroid_matrix_max_min_rule_numpy(distList, k_centroids):
    '''
    This routine finds the two most polar opposite pairs and establishes these as initial
    centroids.  It then finds successive polar opposite observations from the previously
    selected centroids and adds these as centroids until k_centroids are selected.
    '''
    initial_centroid_matrix = []
    end_i = len(distList)
    end_k = len(distList[0])
    maxDist = 0
    maxPairs = []
    #get distance matrix
    distMatrix = scipy.spatial.distance.cdist(distList, distList, 'euclidean')
    maxPairArrayIndices = numpy.where(distMatrix==numpy.amax(distMatrix))
    maxRow = maxPairArrayIndices[0][0]
    maxCol = maxPairArrayIndices[0][1]
    maxPairs.append(maxRow)
    maxPairs.append(maxCol)
    distMatrix[maxRow,maxCol] = 0
    distMatrix[maxCol,maxRow] = 0
    #Array is symmetric
    #print maxPairs
    #print maxDist
    #Iterate until the i number of groups is obtained
    for i in range(2,k_centroids,1):
        end_j = len(maxPairs)
        newDistVector = [0]*end_i
        for j in range(0,end_j,1):
            newDistVector = numpy.add(newDistVector,distMatrix[maxPairs[j]])
        maxPairArrayIndices = numpy.where(newDistVector==numpy.amax(newDistVector))
        nextObs = maxPairArrayIndices[0][0]
        for j in range(0,end_j,1):
            distMatrix[maxPairs[j],nextObs] = 0
            distMatrix[nextObs, maxPairs[j]] = 0
        maxPairs.append(nextObs)               
    for i in range(0,k_centroids,1):
        initial_centroid_matrix.append(deepcopy(distList[maxPairs[i]]))
    return initial_centroid_matrix

def initialize_centroid_matrix_ibc_rule(distMatrix, nGroups, initialDateDict):
    end_i = len(distMatrix)
    end_k = len(distMatrix[0])
    maxDist = 0
    maxDisti = -1
    maxDistj = -1
    newDistMatrix = []
    newCentroid = []
    candidateMatrix = []
    for i in range(0,1000,1):
        newPick = int(numpy.random.uniform()*end_i)
        newVector = distMatrix[newPick]
        candidateMatrix.append(newVector)
    end_i = len(candidateMatrix)
    #initialize distance matrix
    for i in range(0,end_i,1):
        newDistMatrix.append([])
        for j in range(0, end_i, 1):
            newDistMatrix[i].append(0)
    #Get distances
    #print 'Initialize Distances'
    for i in range(0,end_i-1,1):
        #print i
        #myCount = myCount + i
        for j in range(i, end_i, 1):
            flagi = False
            flagj = False
            newDist = 0
            #Only accept distances based on data after
            #first event has occurred in both cases
            myCount = 0
            for k in range(0,end_k,1):
                if candidateMatrix[i][k] == 1:
                    flagi = True
                if candidateMatrix[j][k] == 1:
                    flagj = True
                if flagi == True and flagj == True:
                    newDist = newDist + abs(candidateMatrix[i][k]-candidateMatrix[j][k])
                    myCount = myCount + 1
            #newDist = (newDist / float(myCount)) * end_k
            if newDist > maxDist:
                maxDist = newDist
                maxDisti = i
                maxDistj = j
            newDistMatrix[i][j] = newDist
            newDistMatrix[j][i] = newDist
    #print 'Found Maximum Distance'
    centroidList = [maxDisti,maxDistj]
    if nGroups > 2:
        for n in range(3, nGroups+1):
            maxDist = 0
            maxCentroid = -1
            for i in range(0,end_i,1):
                for centroid in centroidList:
                    newDist = 0
                    newDist = newDist + newDistMatrix[i][centroid]
                if newDist > maxDist:
                    if not i in centroidList:
                        maxDist = newDist
                        maxCentroid = i
            centroidList.append(maxCentroid)
    i = 0
    for centroid in centroidList:
        newCentroid.append([])
        for k in range(0, end_k,1):
            newVarValue = candidateMatrix[centroid][k]
            newCentroid[i].append(newVarValue)
        i = i + 1
    return newCentroid    

def initialize_centroid_matrix_known_classification(distMatrix, nGroups, classDict, classDictKeyList):
    '''
    Calculate the mean variable values for each group in known classification
    '''
    #Initialize
    initial_centroid_matrix = []
    obsCountList = []
    end_i = len(distMatrix)
    end_j = len(distMatrix[0])
    for k in range(0,nGroups,1):
        initial_centroid_matrix.append([])
        obsCountList.append(0)
        for j in range(0,end_j,1):
            initial_centroid_matrix[k].append(0)
    for i in range(0,end_i,1):
        obsNo = classDictKeyList[i]
        classNo = classDict[obsNo]['CMCLASS']
        obsCountList[classNo] = obsCountList[classNo] + 1
        for j in range(0,end_j,1):
            initial_centroid_matrix[classNo][j] = initial_centroid_matrix[classNo][j] + distMatrix[i][k]
    for k in range(0,nGroups,1):
        nObs = obsCountList[k]
        for j in range(0,end_j,1):
            initial_centroid_matrix[k][j] = initial_centroid_matrix[k][j] / nObs
    return initial_centroid_matrix


def get_dik_matrix(distMatrix, newCentroidMatrix,m):
    '''
    Centroid matrix has centroids in rows and variables in columns
    dikMatrix has observations in rows and variables in columns
    '''
    dikMatrix = []
    #the number of observations
    end_i = len(distMatrix)
    #the number of centroids
    end_j = len(newCentroidMatrix)
    for i in range(0, end_i,1):
        dikMatrix.append([])
        for j in range(0, end_j, 1):
            dikMatrix[i].append(0)
    #for each observation in dist matrix
    for i in range(0,end_i,1):
        #for each centroid
        for j in range(0,end_j,1):
            #and for each variable
            end_k = len(distMatrix[i])
            dikValue = 0
            for k in range(0,end_k,1):
                dikValue = dikValue + (distMatrix[i][k]- newCentroidMatrix[j][k])**2        #Euclidean distance squared / Bezdek
            dikMatrix[i][j] = dikValue
    return dikMatrix

def get_dik_matrix_numpy(distMatrix, newCentroidMatrix,m):
    '''
    Centroid matrix has centroids in rows and variables in columns
    dikMatrix has observations in rows and variables in columns
    '''
    dikMatrix = []
    #the number of observations
    end_i = len(distMatrix)
    #the number of centroids
    end_j = len(newCentroidMatrix)
    #for each observation in dist matrix
    for i in range(0,end_i,1):
        #for each centroid
        newList = list(sum(numpy.transpose(numpy.subtract(distMatrix[i],newCentroidMatrix)**2)))
        dikMatrix.append(deepcopy(newList))
    return dikMatrix


def get_ibc_dik_matrix(distMatrix, initialCentroidMatrix, m):
    '''
    Centroid matrix has centroids in rows and variables in columns
    dikMatrix has observations in rows and variables in columns
    In this distance measure no observations count before the earliest
    observation in the distMatrix (i.e. data) is equal to 1 since
    the data is ordered in time from earliest to latest.  This allows short
    chains being joined to long chains (e.g. dna with different lengths).
    '''
    dikMatrix = []
    #the number of observations
    end_i = len(distMatrix)
    #the number of centroids
    end_j = len(initialCentroidMatrix)
    #Initialize observation-x-centroid distance matrix
    for i in range(0, end_i,1):
        dikMatrix.append([])
        for j in range(0, end_j, 1):
            dikMatrix[i].append(0)
    #for each observation in dist matrix
    for i in range(0,end_i,1):
        #for each centroid
        for j in range(0,end_j,1):
            #and for each variable
            end_k = len(distMatrix[i])
            dikValue = 0
            Flag = False
            myCount = 0
            for k in range(0,end_k,1):
                if distMatrix[i][k]==1:
                    Flag = True
                if Flag == True:
                    myCount = myCount + 1
                    dikValue = dikValue + (distMatrix[i][k]- initialCentroidMatrix[j][k])**2
            #dikValue = dikValue/float(myCount)*end_k
            dikMatrix[i][j] = dikValue
    return dikMatrix

def get_normalized_dik_matrix(distMatrix, stdDev, initialCentroidMatrix, m):
    '''
    Centroid matrix has centroids in rows and variables in columns
    dikMatrix has observations in rows and variables in columns
    '''
    dikMatrix = []
    #the number of observations
    end_i = len(distMatrix)
    #the number of centroids
    end_j = len(initialCentroidMatrix)
    for i in range(0, end_i,1):
        dikMatrix.append([])
        for j in range(0, end_j, 1):
            dikMatrix[i].append(0)
    #for each observation in dist matrix
    for i in range(0,end_i,1):
        #for each centroid
        for j in range(0,end_j,1):
            #and for each variable
            end_k = len(distMatrix[i])
            dikValue = 0
            for k in range(0,end_k,1):
                dikValue = dikValue + ((distMatrix[i][k]- initialCentroidMatrix[j][k])/stdDev[k])**2
            dikMatrix[i][j] = dikValue
    return dikMatrix

def get_covariance_normalized_dik_matrix(distMatrix, invCovMatrix, initialCentroidMatrix, m):
    '''
    Centroid matrix has centroids in rows and variables in columns
    dikMatrix has observations in rows and variables in columns
    '''
    dikMatrix = []
    #the number of observations
    end_i = len(distMatrix)
    #the number of centroids
    end_j = len(initialCentroidMatrix)
    for i in range(0, end_i,1):
        dikMatrix.append([])
        for j in range(0, end_j, 1):
            dikMatrix[i].append(0)
    #for each observation in dist matrix
    for i in range(0,end_i,1):
        #for each centroid
        for j in range(0,end_j,1):
            #and for each variable
            end_k = len(distMatrix[i])
            dikVector = []
            for k in range(0,end_k,1):
                dikValue = distMatrix[i][k]- initialCentroidMatrix[j][k]
                dikVector.append(dikValue)
            #xMatrix = MATRIX_MAN.matrix_multiply_inner_product(invCovMatrix,dikVector)
            xMatrix = asaMVA.matrix_multiply_inner_product(invCovMatrix,dikVector)
            #xDist = MATRIX_MAN.matrix_multiply_inner_product(dikVector,xMatrix)
            xDist = asaMVA.matrix_multiply_inner_product(dikVector,xMatrix)
            dikMatrix[i][j] = xDist
    return dikMatrix

def get_censored_dik_matrix(distMatrix, newCentroidMatrix,m):
    '''
    Centroid matrix has centroids in rows and variables in columns
    dikMatrix has observations in rows and variables in columns

    A sensored difference matrix includes only non-zero values
    in the observation (versus centroid) set to compute distances
    
    '''
    dikMatrix = []
    #the number of observations
    end_i = len(distMatrix)
    #the number of centroids
    end_j = len(newCentroidMatrix)
    for i in range(0, end_i,1):
        dikMatrix.append([])
        for j in range(0, end_j, 1):
            dikMatrix[i].append(0)
    #for each observation in dist matrix
    for i in range(0,end_i,1):
        #for each centroid
        for j in range(0,end_j,1):
            #and for each variable
            end_k = len(distMatrix[i])
            dikValue = 0
            for k in range(0,end_k,1):
                #Apply restriction that the distance must be greater than zero
                #in observation set
                if distMatrix[i][k] > 0:
                    dikValue = dikValue + (distMatrix[i][k]- newCentroidMatrix[j][k])**2
            dikMatrix[i][j] = dikValue
    return dikMatrix

def get_covariance_dik_matrix(distMatrix,centMatrix,scatterNorms):
    '''
    This routine weights the distances in a manner consistent
    with the use of 
    
    '''
    dikMatrix = []
    #the number of observations
    end_i = len(distMatrix)
    #the number of centroids
    end_j = len(centMatrix)
    for i in range(0, end_i,1):
        dikMatrix.append([])
        for j in range(0, end_j, 1):
            dikMatrix[i].append(0)
    #for each observation in dist matrix
    for i in range(0,end_i,1):
        #for each centroid
        for j in range(0,end_j,1):
            #and for each variable
            end_k = len(distMatrix[i])
            dikValue = 0
            newVector = []
            newNorm = scatterNorms[j]
            for k in range(0,end_k,1):
                dikValue = (distMatrix[i][k]- centMatrix[j][k])
                newVector.append(dikValue)
            #xMatrix = MATRIX_MAN.matrix_multiply_inner_product(newNorm,newVector)
            xMatrix = asaMVA.matrix_multiply_inner_product(newNorm,newVector)
            #xDist = MATRIX_MAN.matrix_multiply_inner_product(newVector,xMatrix)
            xDist = asaMVA.matrix_multiply_inner_product(newVector,xMatrix)
            dikMatrix[i][j] = xDist
    return dikMatrix




def get_logit_dik_matrix(distMatrix, newCentroidMatrix,m, coefMatrix):
    '''
    Centroid matrix has centroids in rows and variables in columns
    dikMatrix has observations in rows and variables in columns

    Logit distance matrix generated for LiDAR data
    Variables : [F4,F7, F12, 'L4]

    Distanes originally generated using BLOM-NN.py
    Absolute distances were used.
    '''
    dikMatrix = []
    #the number of observations
    end_i = len(distMatrix)
    #the number of centroids
    end_j = len(newCentroidMatrix)
    for i in range(0, end_i,1):
        dikMatrix.append([])
        for j in range(0, end_j, 1):
            dikMatrix[i].append(0)
    #for each observation in dist matrix
    for i in range(0,end_i,1):
        #for each centroid
        dikMultiplier = 0
        for j in range(0,end_j,1):
            #and for each variable
            end_k = len(distMatrix[i])
            dikValue = 0
            for k in range(0,end_k,1):
                #print i,j, k
                dikValue = dikValue + (coefMatrix[k]* abs(distMatrix[i][k]- newCentroidMatrix[j][k]))
            dikMatrix[i][j] = 1 - exp(dikValue)
    return dikMatrix

def get_membership_matrix_version2(dikMatrix, m):
    '''
    This version produces correct results
    The output represents observations in rows and centroids
    in columns.
    '''
    newMembershipMatrix = []
    #Number of observations
    end_i = len(dikMatrix)
    #Number of Centroids
    end_j = len(dikMatrix[0])
    for i in range(0,end_i,1):
        newMembershipMatrix.append([])
        for j in range(0,end_j):
            newMembershipMatrix[i].append(0)
    for i in range(0, end_i, 1):
        #If the distance is zero then membership is
        #is 1 in that centroid and 0 in all other centroids.
        flag = False
        for j in range(0,end_j, 1):
            if dikMatrix[i][j] == 0:
                newMembershipMatrix[i][j] = 1
                flag = True
                for l in range(0,end_j,1):
                    if not l == j:
                        newMembershipMatrix[i][l] = 0
                break
        #If no distance was found to be the zero then flag is False
        if flag == False:
            for j in range(0, end_j,1):
                newNumeratorValue = dikMatrix[i][j]
                membershipValue = 0
                #The membership values must add up to 1 for each observation
                for k in range(0, end_j,1):
                    newDenominatorValue = dikMatrix[i][k]
                    #print i, j
                    if not newDenominatorValue == 0:
                        membershipValue = membershipValue + (newNumeratorValue/float(newDenominatorValue))**(2/(m-1))
                if not membershipValue == 0:
                    membershipValue = 1/float(membershipValue)
                newMembershipMatrix[i][j] = membershipValue
    #check_membership_values(newMembershipMatrix)
    return newMembershipMatrix

def get_membership_matrix_version2_numpy(dikMatrix, m):
    '''
    This version produces correct results
    The output represents observations in rows and centroids
    in columns.
    '''
    newMembershipMatrix = []
    #Number of observations
    end_i = len(dikMatrix)
    #Number of Centroids
    end_j = len(dikMatrix[0])
    for i in range(0, end_i, 1):
        #If the distance is zero then membership is
        #is 1 in that centroid and 0 in all other centroids.
        minMembership = min(dikMatrix[i])
        if minMembership <= 0:
            minMembIndex = dikMatrix[i].index(minMembership)
            newMembershipMatrix.append([0]*end_j)
            newMembershipMatrix[i][minMembIndex] = 1
        else:
            newMembershipMatrix.append([0]*end_j) 
            for j in range(0, end_j,1):
                newNumeratorValue = dikMatrix[i][j]
                membershipValue = 0
                #The membership values must add up to 1 for each observation
                for k in range(0, end_j,1):
                    newDenominatorValue = dikMatrix[i][k]
                    #print i, j
                    if not newDenominatorValue == 0:
                        membershipValue = membershipValue + (newNumeratorValue/float(newDenominatorValue))**(2/(m-1))
                if not membershipValue == 0:
                    membershipValue = 1/float(membershipValue)
                newMembershipMatrix[i][j] = membershipValue
    return newMembershipMatrix

def initialize_membership_matrix(distMatrix, nGroups):
    newMatrix = []
    end_i = len(distMatrix)
    initialMembership = 1/float(nGroups)
    for i in range(0, end_i,1):
        newMatrix.append([])
        for j in range(0,nGroups,1):
            newMatrix[i].append(initialMembership)
    return newMatrix

def get_logit_membership_matrix_version2(dikMatrix, m):
    '''
    This version produces correct results
    '''
    newMembershipMatrix = []
    #Number of observations
    end_i = len(dikMatrix)
    #Number of Centroids
    end_j = len(dikMatrix[0])
    for i in range(0,end_i,1):
        newMembershipMatrix.append([])
        for j in range(0,end_j):
            newMembershipMatrix[i].append(0)
    for i in range(0, end_i, 1):
        #If the distance is zero then membership is
        #is 1 in that centroid and 0 in all other centroids.
        flag = False
        for j in range(0,end_j, 1):
            if dikMatrix[i][j] == 0:
                newMembershipMatrix[i][j] = 1
                flag = True
                for l in range(0,end_j,1):
                    if not l == j:
                        newMembershipMatrix[i][l] = 0
                break
        #If no distance was found to be the zero then flag is False
        if flag == False:
            for j in range(0, end_j,1):
                newNumeratorValue = dikMatrix[i][j]
                membershipValue = 0
                #The membership values must add up to 1 for each observation
                for k in range(0, end_j,1):
                    newDenominatorValue = dikMatrix[i][k]
                    #print i, j
                    if not newDenominatorValue == 0:
                        membershipValue = membershipValue + (newNumeratorValue/float(newDenominatorValue))**(2/(m-1))
                if not membershipValue == 0:
                    membershipValue = 1/float(membershipValue)
                newMembershipMatrix[i][j] = membershipValue
    #check_membership_values(newMembershipMatrix)
    return newMembershipMatrix

def check_membership_values(newMembershipMatrix):
    #Number of Observations
    end_i = len(newMembershipMatrix)
    #Number of centroids
    end_j = len(newMembershipMatrix[0])
    for j in range(0,end_j,1):
        membershipSum = 0
        for i in range(0,end_i,1):
            membershipSum = membershipSum + newMembershipMatrix[i][j]
        print j, membershipSum
    return

def check_membership_values_observations(newMembershipMatrix):
    #Number of Observations
    end_i = len(newMembershipMatrix)
    #Number of centroids
    end_j = len(newMembershipMatrix[0])
    for i in range(0,end_i,1):
        membershipSum = 0
        for j in range(0,end_j,1):
            membershipSum = membershipSum + newMembershipMatrix[i][j]
        print i, j, membershipSum
    return

def update_centroid_matrix(distMatrix,membershipMatrix, m):
    '''
    For a given centroid, sum up all of the associated
    observation memberships, multiplied by a given
    variable value - and then divide by the sum of all
    the memberships
    '''
    nextCentroidMatrix = []
    #Number of observations
    end_i = len(distMatrix)
    #Number of variables
    end_k = len(distMatrix[0])
    #Number of centroids
    end_j = len(membershipMatrix[0])
    #for a given centroid
    for j in range(0, end_j,1):
        nextCentroidMatrix.append([])
        #for a given variable
        for k in range(0,end_k,1):
            sumMembership = 0
            newCentroidValue = 0
            #for a given observation the membership values must add up to 1
            for i in range(0,end_i,1):
                newMembershipValue = (membershipMatrix[i][j])**m
                sumMembership = sumMembership + newMembershipValue
                newCentroidValue = newCentroidValue + newMembershipValue * distMatrix[i][k]
            newCentroidValue = newCentroidValue / float(sumMembership)
            nextCentroidMatrix[j].append(newCentroidValue)
    return nextCentroidMatrix

def update_centroid_matrix_numpy(distMatrix,membershipMatrix, m):
    '''
    For a given centroid, sum up all of the associated
    observation memberships, multiplied by a given
    variable value - and then divide by the sum of all
    the memberships
    '''
    nextCentroidMatrix = []
    #Number of observations
    end_i = len(distMatrix)
    #Number of variables
    end_k = len(distMatrix[0])
    distMatrixTranspose = numpy.transpose(distMatrix)
    #Number of centroids
    end_j = len(membershipMatrix[0])
    #Transpose membership matrix to put centroid memberships in rows
    membershipMatrixTranspose = list(numpy.transpose(membershipMatrix))
    for j in range(0, end_j,1):
        nextCentroidMatrix.append([])
        sumMembership = sum(membershipMatrixTranspose[j])
        centroidValueMatrix = numpy.multiply(distMatrixTranspose,membershipMatrixTranspose[j])
        for k in range(0,end_k,1):
            newCentroidValue = sum(centroidValueMatrix[k])/float(sumMembership)
            nextCentroidMatrix[j].append(newCentroidValue)
    return nextCentroidMatrix


def get_initial_ibc_date(distMatrix):
    end_i = len(distMatrix)
    end_k = len(distMatrix[0])
    newDict = {}
    for i in range(0,end_i,1):
        newDict.update({i:-1})
        for k in range(0,end_k,1):
            if distMatrix[i][k]== 1 and newDict[i] < 0:
                newDict[i] = k
                break         
    return newDict

def update_ibc_centroid_matrix(distMatrix,membershipMatrix, m, initialDateDict):
    '''
    For a given centroid, sum up all of the associated
    observation memberships, multiplied by a given
    variable value - and then divide by the sum of all
    the memberships

    Note that for IBC updates diatnces prior to first event
    are not included in determining the centroid
    '''
    nextCentroidMatrix = []
    #Number of observations
    end_i = len(distMatrix)
    #Number of variables
    end_k = len(distMatrix[0])
    #Number of centroids
    end_j = len(membershipMatrix[0])
    #for a given centroid
    for j in range(0, end_j,1):
        #print 'centroidNo', j
        nextCentroidMatrix.append([])
        #for a given variable
        centroidInclusionList = []
        for k in range(0,end_k,1):
            sumMembership = 0
            newCentroidValue = 0
            #for a given observation the membership values must add up to 1
            for i in range(0,end_i,1):
                #If k is greater than or equal to the time of the first claim
                if k >= initialDateDict[i]:
                    newMembershipValue = (membershipMatrix[i][j])**m
                    sumMembership = sumMembership + newMembershipValue
                    newCentroidValue = newCentroidValue + newMembershipValue * distMatrix[i][k]
            if sumMembership > 0:
                newCentroidValue = newCentroidValue / float(sumMembership)
            nextCentroidMatrix[j].append(newCentroidValue)
    return nextCentroidMatrix

def update_centroid_matrix_of_known_classification(distMatrix,membershipMatrix, m, classDict, classDictKeyList):
    '''
    For a given centroid, sum up all of the associated
    observation memberships, multiplied by a given
    variable value - and then divide by the sum of all
    the memberships
    '''
    nextCentroidMatrix = []
    #Number of observations
    end_i = len(distMatrix)
    #Number of variables
    end_k = len(distMatrix[0])
    #Number of centroids
    end_j = len(membershipMatrix[0])
    #for a given centroid
    for j in range(0, end_j,1):
        nextCentroidMatrix.append([])
        #for a given variable
        for k in range(0,end_k,1):
            sumMembership = 0
            newCentroidValue = 0
            #for a given observation the membership values must add up to 1
            for i in range(0,end_i,1):
                #Centroid adjustments are constrained to only those observations
                #that are in the known class. Greater weight are given to those that are
                #most different from the other classes; less weight to those that are more
                #similar in an effort to maximize the differences between the classes
                obsNo = classDictKeyList[i]
                classNo = classDict[obsNo]['CMCLASS']
                if classNo == j:
                    newMembershipValue = (membershipMatrix[i][j])**m
                    sumMembership = sumMembership + newMembershipValue
                    newCentroidValue = newCentroidValue + newMembershipValue * distMatrix[i][k]
            newCentroidValue = newCentroidValue / float(sumMembership)
            nextCentroidMatrix[j].append(newCentroidValue)
    return nextCentroidMatrix

def update_censored_centroid_matrix(distMatrix,membershipMatrix, m):
    '''
    For a given centroid, sum up all of the associated
    observation memberships, multiplied by a given
    variable value - and then divide by the sum of all
    the memberships

    A censored centroid matrix uses only those obeservations
    with variable values greater than zero.  This is particularly
    useful for vegetation data where most species are absent from any
    one plot.
    
    '''
    nextCentroidMatrix = []
    #Number of observations
    end_i = len(distMatrix)
    #Number of variables
    end_k = len(distMatrix[0])
    #Number of centroids
    end_j = len(membershipMatrix[0])
    #for a given centroid
    for j in range(0, end_j,1):
        nextCentroidMatrix.append([])
        #for a given variable
        for k in range(0,end_k,1):
            sumMembership = 0
            newCentroidValue = 0
            #for a given observation the membership values must add up to 1
            for i in range(0,end_i,1):
                #Censored membership: only include members where the input (distMatrix)
                #observation has a value > 0; i.e. do not include 0's as a contribution
                #to determining the centroid
                if distMatrix[i][k] > 0:
                    newMembershipValue = (membershipMatrix[i][j])**m
                    sumMembership = sumMembership + newMembershipValue
                    newCentroidValue = newCentroidValue + newMembershipValue * distMatrix[i][k]
            newCentroidValue = newCentroidValue / float(sumMembership)
            nextCentroidMatrix[j].append(newCentroidValue)
    return nextCentroidMatrix


def check_for_error_version2(initialCentroidMatrix, updateCentroidMatrix):
    error = 0
    end_i = len(initialCentroidMatrix)
    end_j = len(initialCentroidMatrix[0])
    for i in range(0,end_i,1):
        for j in range(0,end_j,1):
            diff = (initialCentroidMatrix[i][j] - updateCentroidMatrix[i][j])**2
            if diff > error:
                error = diff
    return error

def check_for_error(initialCentroidMatrix, updateCentroidMatrix):
    error = 0
    end_i = len(initialCentroidMatrix)
    end_j = len(initialCentroidMatrix[0])
    for i in range(0,end_i,1):
        for j in range(0,end_j,1):
            diff = (initialCentroidMatrix[i][j] - updateCentroidMatrix[i][j])**2
            error = error + diff
    error = (error)**0.5
    return error

def check_for_error_numpy(initialCentroidMatrix, updateCentroidMatrix):
    error = (sum(sum(numpy.subtract(initialCentroidMatrix,updateCentroidMatrix)**2)))**0.5
    return error


def replace_initialCentroidMatrix_with_updateCentroidMatrix(updateCentroidMatrix):
    funnyNewMatrix = []
    end_i = len(updateCentroidMatrix)
    end_j = len(updateCentroidMatrix[0])
    for i in range(0,end_i,1):
        funnyNewMatrix.append([])
        for j in range(0,end_j,1):
            newVarValue = updateCentroidMatrix[i][j]
            funnyNewMatrix[i].append(newVarValue)
    return funnyNewMatrix

def replace_initialCentroidMatrix_with_updateCentroidMatrix_numpy(updateCentroidMatrix):
    funnyNewMatrix = deepcopy(updateCentroidMatrix)
    return funnyNewMatrix


def transpose_varList(varList):
    newArray = numpy.transpose(varList)
    return newArray

def get_standard_deviation_vector_from_transposed_array(newArray):
    stdevVector = []
    end_array = len(newArray)
    for num in range(0,end_array,1):
        stdevValue = numpy.std(newArray[num])
        stdevVector.append(stdevValue)
    return stdevVector

def divide_array_values_by_standard_deviations(xArray,xsVector):
    newArray = []
    end_x = len(xArray)
    for x in range(0,end_x,1):
        varStdev = xsVector[x]
        end_y = len(xArray[x])
        newArray.append([])
        for y in range(0,end_y,1):
            newVarValue = xArray[x][y]/ float(varStdev)
            newArray[x].append(newVarValue)
    return newArray

def get_fuzzy_c_scatter_matrices(mStat, membMatrix, varMatrix, centMatrix):
    '''
    mStat is the m value used to determine membership values
    membMtrix is the membership matrix (observations in rows and classes in columns)
    varMtrix is the inputMatrix or distMatrix (observations in rows and variables in columns)
    centMatrix is the initialCentroidMatrix (classes in rows and variables in columns)

    i represents the observation number
    j represents the class number
    k represents the variable number

    Note that this procedur was modified from that presented in Bezdek according
    to the description by Graves and Pedrycz (2007) in their article on
    Fuzzy C-Means, Gustofsaon-Kessel FCM, and Kernal-Based FCM: A Comparative Study.
    In P. Melin et al. (Eds): Analy. and Des. of Intel. Sys. using SC tech., ASC 41,
    pp 140-149. Springer-Verlag.

    '''
    #Initialize class covariance vector
    outVector = []
    #Get number of observations
    end_i = len(varMatrix)
    #Get number of Classes
    end_j = len(centMatrix)
    #Get number of variables
    end_k = len(varMatrix[0])
    #for each class
    for j in range(0,end_j,1):
        #Initialize new class covariance matrix
        outVector.append([])
        for k in range(0,end_k,1):
            outVector[j].append([])
            for l in range(0,end_k,1):
                outVector[j][k].append(0) 
        #for each observation
        membSum = 0
        for i in range(0,end_i,1):
            membValue = membMatrix[i][j]
            membSum = membSum + membValue**mStat
            newVector = []
            #for each variable
            for k in range(0,end_k,1):
                varValue = varMatrix[i][k]-centMatrix[j][k]
                newVector.append(varValue)
            #outerProduct = (membValue**mStat)*MATRIX_MAN.matrix_multiply_outer_product(newVector,newVector)
            outerProduct = (membValue**mStat)*asaMVA.matrix_multiply_outer_product(newVector,newVector)
            #print 'OUTER PRODUCT'
            #print outerProduct
            #print 'OUT VECTOR jk', j, k
            #outVector[j] =  MATRIX_MAN.add_two_two_dimensional_arrays_of_same_dimensions(outVector[j],outerProduct)
            outVector[j] =  asaMVA.add_two_two_dimensional_arrays_of_same_dimensions(outVector[j],outerProduct)
        for k in range(0, end_k,1):
            for l in range(0,end_k,1):
                outVector[j][k][l]=outVector[j][k][l]/membSum
    return outVector

def get_fuzzy_c_scatter_determinants(fuzzyScatterMatrices):
    outVector = []
    end_j = len(fuzzyScatterMatrices)
    for j in range(0,end_j,1):
        #detValue = MATRIX_MAN.get_determinant_of_symmetrical_matrix(fuzzyScatterMatrices[j])
        detValue = asaMVA.get_determinant_of_symmetrical_matrix(fuzzyScatterMatrices[j])
        outVector.append(detValue)
    return outVector

def get_fuzzy_c_scatter_inverses(fuzzyScatterMatrices):
    outVector = []
    end_j = len(fuzzyScatterMatrices)
    for j in range(0,end_j,1):
        #detValue = MATRIX_MAN.get_inverse_of_matrix(fuzzyScatterMatrices[j])
        detValue = asaMVA.get_inverse_of_matrix(fuzzyScatterMatrices[j])
        outVector.append(detValue)
    return outVector

def get_fuzzy_c_scatter_norms(detVector,invVector, rhoVect,p, nClasses):
    outVector = []
    #Get number of centroids
    end_j = len(invVector)
    for j in range(0,end_j,1):
        #print rhoVect[j], detVector[j]
        invMatrix = invVector[j]
        detValue = ((rhoVect[j]*detVector[j])**(1/float(p)))
        aMatrix = detValue * invMatrix
        outVector.append(aMatrix)
    return outVector

def get_copy_of_fuzzyScatterDeterminants(fuzzyScatterMatrices):
    newVector = []
    end_j = len(fuzzyScatterMatrices)
    for j in range(0,end_j):
        varValue = fuzzyScatterMatrices[j]
        newVector.append(varValue)
    return newVector

def get_rhoDeterminants(nGroups,rhoValue):
    rhoVector = []
    for j in range(0,nGroups,1):
        rhoVector.append(rhoValue)
    return rhoVector

def run_fuzzy_c_means_euclidean(m_value=2,nGroups=2,inputData=[[]], minError=0.001):
    '''
    Bezdek J.C. 1981. Pattern recognition with fuzzy objective algorithms.
    Plenum Press, New York. Pp. 65 - 80.  
    
    let
    
    (d_ik)^2 = ||x_k - v_i||^2                                (11.1d)

    where
    
    d_ik    is distance from the ith centroid to the kth observation
    x_k     is the kth observation
    v_i     is the ith centroid
    ||.||   is an inner product norm (vector multiplactions
    
    Theorem 11.1. Assume |.| to be inner product induced: fix m in the set (1, inf.),
    let X have at least c < n distinct points (centroids) and define for all k the sets

        I_k ={i|1<=i<=c; d_ik = ||x_k - v_i|| = 0

        (i.e. i is the ith centroid for which the the sum of the differences
        across the variable set with respect to the ith centroid is equal to
        zero ... i.e. minimized)
 
        ~I_k = {1,2,...,c}- I_k

        (i.e. I tilda is the differnce in the centroids between a current set
        and the previous set)
         
    then (U,v) is in  the set set of fuzzy memberships and associated centroids
    in the combined set M_fc (a fuzzy-c partition of X) and Real numbers of
    dimension cp where c is the number of centroids and p is the number of
    variables; (U,v) may be globally minimal for J_m (objective function) only
    if:
    
    u_ik = 1/[sum((d_ik/d_jk)^(2/(m-1))] for j equals 1 to c centroids      (11.3a1}

    if 

    u_ik    is the membership of observation k in the ith centroid
    
    v_i = [sum ((u_{ik})^m) * x_k] / [sum ((u_{ik})^m)                      (11.3b)
            for k equals 1 to n observations

    Algorithm A11.1 [Fuzzy c-Means (FCM), Bezdek]

    (A11.1a)    Fix c, 2 <= c < n; choose any inner product norm metric for Real
                numbers raised to p dimensions; and fix m, 1 <= m < inf.
                Initilize U^(0) in the set M_fc. Then at step l, l = 0,1,2, ...,:

    (All.1b)    Calculate the c fuzzy cluster centers {v_i} for the lth iteration
                with 11.3b
    
    '''
    print nGroups
    distMatrix = inputData                      #Initialize data
    classAssignments = []
    m = m_value                                 #Controlls fuzziness - m = 1 produces hard classification; m = 2 is default
    if m <= 1:
        m = 2                                   
    #initialCentroidMatrix = initialize_centroid_matrix(distMatrix, nGroups)
    #initialCentroidMatrix = initialize_centroid_matrix_max_min_rule(distMatrix, nGroups)    #Ian's starting rule
    initialCentroidMatrix = initialize_centroid_matrix_max_min_rule_numpy(distMatrix, nGroups)    #Ian's starting rule
    #dikMatrix = get_dik_matrix(distMatrix, initialCentroidMatrix, m)                        #Get distance matrix
    dikMatrix = get_dik_matrix_numpy(distMatrix, initialCentroidMatrix, m)
    #membershipMatrix = get_membership_matrix(dikMatrix, m)
    membershipMatrix = get_membership_matrix_version2_numpy(dikMatrix, m)                         #Get membership matrix
    #updateCentroidMatrix = update_centroid_matrix(distMatrix,membershipMatrix, m)           #Update centroid position
    updateCentroidMatrix = update_centroid_matrix_numpy(distMatrix,membershipMatrix, m)
    #newError = check_for_error(initialCentroidMatrix, updateCentroidMatrix)                 #Calculate error: equals differences in locations of centroids
    newError = check_for_error_numpy(initialCentroidMatrix, updateCentroidMatrix)                 #Calculate error: equals differences in locations of centroids
    #print newError
    while newError > minError:
        #initialCentroidMatrix = replace_initialCentroidMatrix_with_updateCentroidMatrix(updateCentroidMatrix)
        initialCentroidMatrix = replace_initialCentroidMatrix_with_updateCentroidMatrix_numpy(updateCentroidMatrix)
        #dikMatrix = get_dik_matrix(distMatrix, initialCentroidMatrix, m)                    #Get distances observations from centroids 
        dikMatrix = get_dik_matrix_numpy(distMatrix, initialCentroidMatrix, m)
        #membershipMatrix = get_membership_matrix(dikMatrix, m)
        membershipMatrix = get_membership_matrix_version2_numpy(dikMatrix, m)                     #Get mebership values
        #updateCentroidMatrix = update_centroid_matrix(distMatrix,membershipMatrix, m)
        updateCentroidMatrix = update_centroid_matrix_numpy(distMatrix,membershipMatrix, m)
        #newError = check_for_error(initialCentroidMatrix, updateCentroidMatrix)
        newError = check_for_error_numpy(initialCentroidMatrix, updateCentroidMatrix)
        #print newError
    end_ii = len(membershipMatrix)
    for i in range(0,end_ii,1):
        newClass = dikMatrix[i].index(min(dikMatrix[i]))
        classAssignments.append([i,newClass])
        #print i, newClass
    return classAssignments,updateCentroidMatrix, membershipMatrix


def apply_fuzzy_c_means_euclidean(m_value=2,nGroups=2,inputData=[[]],centroidData = [[]], printNclasses = 'YES'):
    '''
    Bezdek J.C. 1981. Pattern recognition with fuzzy objective algorithms.
    Plenum Press, New York. Pp. 65 - 80.  
    
    '''
    if printNclasses == 'YES':
        print nGroups
    distMatrix = inputData                      #Initialize data
    classAssignments = []
    m = m_value                                 #Controlls fuzziness - m = 1 produces hard classification; m = 2 is default
    if m <= 1:
        m = 2                                   
    #dikMatrix = get_dik_matrix(distMatrix, initialCentroidMatrix, m)                        #Get distance matrix
    dikMatrix = get_dik_matrix_numpy(distMatrix, centroidData, m)
    #membershipMatrix = get_membership_matrix(dikMatrix, m)
    membershipMatrix = get_membership_matrix_version2_numpy(dikMatrix, m)                         #Get membership matrix
    #updateCentroidMatrix = update_centroid_matrix(distMatrix,membershipMatrix, m)           #Update centroid position
    end_ii = len(membershipMatrix)
    for i in range(0,end_ii,1):
        newClass = dikMatrix[i].index(min(dikMatrix[i]))
        classAssignments.append([i,newClass])
        #print i, newClass
    return classAssignments,membershipMatrix

def run_censored_fuzzy_c_means_euclidean(m_value,nGroups,inputData, minError):
    '''
    This process was designed to work with vegetation data where most species are
    absent from any one plot - resulting excessive contributions of zero values
    to defintion of the centroid.  As a result the clustering is driven by the
    presence of certain species and the strength of their cooccurrences rather
    than by the absence that otherwise dominates the determination of centroid
    values.
    '''
    print nGroups
    distMatrix = inputData
    classAssignments = []
    m = m_value
    if m <= 1:
        m = 2
    #initialCentroidMatrix = initialize_centroid_matrix(distMatrix, nGroups)
    #print '\n Get Centroid Matrix'
    initialCentroidMatrix = initialize_centroid_matrix_max_min_rule_numpy(distMatrix, nGroups)
    #print '\n Get Censored dik_matrix'
    dikMatrix = get_censored_dik_matrix(distMatrix, initialCentroidMatrix, m)
    #membershipMatrix = get_membership_matrix(dikMatrix, m)
    #print '\n Get membership matrix'
    membershipMatrix = get_membership_matrix_version2(dikMatrix, m)
    updateCentroidMatrix = update_censored_centroid_matrix(distMatrix,membershipMatrix, m)
    newError = check_for_error(initialCentroidMatrix, updateCentroidMatrix)
    #print newError
    while newError > minError:
        initialCentroidMatrix = replace_initialCentroidMatrix_with_updateCentroidMatrix(updateCentroidMatrix)
        #Get censored distance matrix where distances ar restricted to non-zero values
        dikMatrix = get_censored_dik_matrix(distMatrix, initialCentroidMatrix, m)
        #dikMatrix = get_dik_matrix(distMatrix, membershipMatrix,m)
        #membershipMatrix = get_membership_matrix(dikMatrix, m)
        membershipMatrix = get_membership_matrix_version2(dikMatrix, m)
        updateCentroidMatrix = update_censored_centroid_matrix(distMatrix,membershipMatrix, m)
        newError = check_for_error(initialCentroidMatrix, updateCentroidMatrix)
        #print newError
    end_ii = len(membershipMatrix)
    for i in range(0,end_ii,1):
        newClass = dikMatrix[i].index(min(dikMatrix[i]))
        classAssignments.append([i,newClass])
        #print i, newClass
    return classAssignments,updateCentroidMatrix, membershipMatrix

def run_fuzzy_c_means_euclidean_known_classification(m_value,nGroups,inputData, minError, classDict, classDictKeyList):
    '''
    Note that this routine finds centroids associated with a pre-existing classification of n groups
    where the classDict is as follows:  {obsNo:{'CMCLASS': classNo}}, where class numbers are 0,1,2,3,4 ...
    The obsNo's in classDict are in the same order as the rows listed in the inputData and are identified and
    listed in the same order in the classDictKeyList.  
    '''
    print nGroups
    distMatrix = inputData
    classAssignments = []
    m = m_value
    if m <= 1:
        m = 2
    #initialCentroidMatrix = initialize_centroid_matrix(distMatrix, nGroups)
    #initialCentroidMatrix = initialize_centroid_matrix_max_min_rule(distMatrix, nGroups)
    initialCentroidMatrix = initialize_centroid_matrix_known_classification(distMatrix, nGroups, classDict, classDictKeyList)
    dikMatrix = get_dik_matrix(distMatrix, initialCentroidMatrix, m)
    #membershipMatrix = get_membership_matrix(dikMatrix, m)
    membershipMatrix = get_membership_matrix_version2(dikMatrix, m) 
    updateCentroidMatrix = update_centroid_matrix_of_known_classification(distMatrix,membershipMatrix, m, classDict,classDictKeyList)
    newError = check_for_error(initialCentroidMatrix, updateCentroidMatrix)
    #print newError
    while newError > minError:
        initialCentroidMatrix = replace_initialCentroidMatrix_with_updateCentroidMatrix(updateCentroidMatrix)
        dikMatrix = get_dik_matrix(distMatrix, initialCentroidMatrix, m)
        #membershipMatrix = get_membership_matrix(dikMatrix, m)
        membershipMatrix = get_membership_matrix_version2(dikMatrix, m)
        updateCentroidMatrix = update_centroid_matrix_of_known_classification(distMatrix,membershipMatrix, m, classDict, classDictKeyList)
        newError = check_for_error(initialCentroidMatrix, updateCentroidMatrix)
        #print newError
    end_ii = len(membershipMatrix)
    for i in range(0,end_ii,1):
        newClass = dikMatrix[i].index(min(dikMatrix[i]))
        classAssignments.append([i,newClass])
        #print i, newClass
    return classAssignments,updateCentroidMatrix, membershipMatrix



def run_fuzzy_c_means_diagonal(m_value,nGroups,inputData, minError):
    '''
    This is the correct way to compute mahalanobis distances where the
    observation-x-centroid membership values are used to calculate
    a standard deviation for each variable. These weights are applied to
    the differences between the variable values for each of the centroids
    and observation combinations producing a weighted difference. The smaller
    the standard deviation the greater the weight.
    

    The classAssignments matrix produces the list of classes assigned
    to each observation.

    The updateCentroid matrix produces the variable values representing
    the centroid for each class.

    The stdevMatrix provides the weights for the differences between
    each variable with respect to each variable for all centroids. The
    difference in a variable value for a target observation versus a
    reference centroid should be multiplied by 1/weight (this being
    equivalent to dividing by a standard deviation)and then the resultant
    value squared to determine the relative distance for that variable.
    (Note that this procedure might vary if m is not equal to 2.)
    
    The procedure should be repeated for each variable and centroid
    combination and then the differences summed across all variables
    for each centroid to determine the assigned class - this being
    the one with the minimum distance.

    February 21, 2010
    
    '''
    print nGroups
    distMatrix = inputData
    classAssignments = []
    m = m_value
    if m <= 1:
        m = 2
    #initialCentroidMatrix = initialize_centroid_matrix(distMatrix, nGroups)
    initialCentroidMatrix = initialize_centroid_matrix_max_min_rule(distMatrix, nGroups)
    stdevMatrix = initialize_mahalanobis_v2_standard_deviations(distMatrix)
    #print stdevMatrix
    dikMatrix = get_normalized_dik_matrix(distMatrix, stdevMatrix, initialCentroidMatrix, m)
    #membershipMatrix = get_membership_matrix(dikMatrix, m)
    membershipMatrix = get_membership_matrix_version2(dikMatrix, m)
    updateCentroidMatrix = update_centroid_matrix(distMatrix,membershipMatrix, m)
    newError = check_for_error(initialCentroidMatrix, updateCentroidMatrix)
    #print newError
    myCount = 0
    while newError > minError:
        initialCentroidMatrix = replace_initialCentroidMatrix_with_updateCentroidMatrix(updateCentroidMatrix)
        dikMatrix = get_normalized_dik_matrix(distMatrix, stdevMatrix, initialCentroidMatrix, m)
        membershipMatrix = get_membership_matrix_version2(dikMatrix, m)
        updateCentroidMatrix = update_centroid_matrix(distMatrix,membershipMatrix, m)
        newError = check_for_error(initialCentroidMatrix, updateCentroidMatrix)
        #print newError
    end_ii = len(membershipMatrix)
    for i in range(0,end_ii,1):
        newClass = dikMatrix[i].index(min(dikMatrix[i]))
        classAssignments.append([i,newClass])
        #print i, newClass
    return [classAssignments,updateCentroidMatrix, stdevMatrix]

def run_fuzzy_c_means_mahalonobis(m_value,nGroups,inputData, minError):
    '''
    This is the correct way to compute mahalonobis distances where the
    observation-x-centroid membership values are used to calculate
    a standard deviation for each variable. These weights are applied to
    the differences between the variable values for each of the centroids
    and observation combinations producing a weighted difference. The smaller
    the standard deviation the greater the weight.
    

    The classAssignments matrix produces the list of classes assigned
    to each observation.

    The updateCentroid matrix produces the variable values representing
    the centroid for each class.

    The stdevMatrix provides the weights for the differences between
    each variable with respect to each variable for all centroids. The
    difference in a variable value for a target observation versus a
    reference centroid should be multiplied by 1/weight (this being
    equivalent to dividing by a standard deviation)and then the resultant
    value squared to determine the relative distance for that variable.
    (Note that this procedure might vary if m is not equal to 2.)
    
    The procedure should be repeated for each variable and centroid
    combination and then the differences summed across all variables
    for each centroid to determine the assigned class - this being
    the one with the minimum distance.

    February 21, 2010
    
    '''
    print nGroups
    distMatrix = inputData
    nObs = len(distMatrix)
    classAssignments = []
    m = m_value
    if m <= 1:
        m = 2
    #Initialize inverse covariance matrix
    covMatrix = initialize_mahalanobis_v3_standard_deviations(distMatrix, nObs)
    #invCovMatrix = MATRIX_MAN.get_inverse_of_matrix(covMatrix)
    invCovMatrix = asaMVA.get_inverse_of_matrix(covMatrix)    
    #initialCentroidMatrix = initialize_centroid_matrix(distMatrix, nGroups)
    initialCentroidMatrix = initialize_centroid_matrix_max_min_rule(distMatrix, nGroups)
    #print stdevMatrix
    dikMatrix = get_covariance_normalized_dik_matrix(distMatrix, invCovMatrix, initialCentroidMatrix, m)
    #membershipMatrix = get_membership_matrix(dikMatrix, m)
    membershipMatrix = get_membership_matrix_version2(dikMatrix, m)
    updateCentroidMatrix = update_centroid_matrix(distMatrix,membershipMatrix, m)
    newError = check_for_error(initialCentroidMatrix, updateCentroidMatrix)
    #print newError
    myCount = 0
    while newError > minError:
        initialCentroidMatrix = replace_initialCentroidMatrix_with_updateCentroidMatrix(updateCentroidMatrix)
        dikMatrix = get_covariance_normalized_dik_matrix(distMatrix, invCovMatrix, initialCentroidMatrix, m)
        membershipMatrix = get_membership_matrix_version2(dikMatrix, m)
        updateCentroidMatrix = update_centroid_matrix(distMatrix,membershipMatrix, m)
        newError = check_for_error(initialCentroidMatrix, updateCentroidMatrix)
        #print newError
    end_ii = len(membershipMatrix)
    for i in range(0,end_ii,1):
        newClass = dikMatrix[i].index(min(dikMatrix[i]))
        classAssignments.append([i,newClass])
        #print i, newClass
    return classAssignments,updateCentroidMatrix, covMatrix, membershipMatrix



def run_fuzzy_c_means_gustafson_kessel(m_value, nGroups,inputData, rhoValue, minError):
    '''
    This process creates different shapes for each of the groups following
    Gustafson and Kessel (1979) as presented in Bezdek (1981).

    This algosithm has been modified from that described in Bezdek
    to converge properly. In particular the scatter matrix values
    must be divided by the sum of the membership values.

    The m_value is fuzzy logic and is usually set to two
    The p_value can be varied by group but it is set to 1 
    
    
    '''
    print nGroups
    distMatrix = inputData
    classAssignments = []
    m = m_value
    #p_value is set to the number of variables
    p_value = len(distMatrix[0])
    if m <= 1:
        m = 2
    #initialCentroidMatrix = initialize_centroid_matrix(distMatrix, nGroups)
    initialCentroidMatrix = initialize_centroid_matrix_max_min_rule(distMatrix, nGroups)
    #Get euclidean distance matrix
    dikMatrix = get_dik_matrix(distMatrix, initialCentroidMatrix, m)
    #Initialize membership matrix
    membershipMatrix = get_membership_matrix_version2(dikMatrix, m)
    #Calculate fuzzyScatterMatrices ie covariance matrix
    fuzzyScatterMatrices = get_fuzzy_c_scatter_matrices(m, membershipMatrix, distMatrix, initialCentroidMatrix)
    #Get covariance matrix determinants
    fuzzyScatterDeterminants = get_fuzzy_c_scatter_determinants(fuzzyScatterMatrices)
    #rhoDeterminants = get_copy_of_fuzzyScatterDeterminants(fuzzyScatterDeterminants)
    rhoDeterminants = get_rhoDeterminants(nGroups,rhoValue)
    #Get covariance matrix inverses
    fuzzyScatterInverses = get_fuzzy_c_scatter_inverses(fuzzyScatterMatrices)
    #Calculate the norm inducting matrices
    fuzzyScatterNorms = get_fuzzy_c_scatter_norms(fuzzyScatterDeterminants,fuzzyScatterInverses, rhoDeterminants, p_value, nGroups)
    normDeterminants = get_fuzzy_c_scatter_determinants(fuzzyScatterMatrices)
    #print normDeterminants
    #Get covariance distance metric
    dikMatrix = get_covariance_dik_matrix(distMatrix,initialCentroidMatrix,fuzzyScatterNorms)
    membershipMatrix = get_membership_matrix_version2(dikMatrix, m)
    updateCentroidMatrix = update_centroid_matrix(distMatrix,membershipMatrix, m)
    newError = check_for_error(initialCentroidMatrix, updateCentroidMatrix)
    #print newError
    myCount = 0
    while newError > minError:
        initialCentroidMatrix = replace_initialCentroidMatrix_with_updateCentroidMatrix(updateCentroidMatrix)
        #Calculate fuzzyScatterMatrices ie covariance matrix
        fuzzyScatterMatrices = get_fuzzy_c_scatter_matrices(m, membershipMatrix, distMatrix, initialCentroidMatrix)
        #Get covariance matrix determinants
        fuzzyScatterDeterminants = get_fuzzy_c_scatter_determinants(fuzzyScatterMatrices)
        #print fuzzyScatterDeterminants
        #Get covariance matrix inverses
        fuzzyScatterInverses = get_fuzzy_c_scatter_inverses(fuzzyScatterMatrices)
        #Calculate the norm inducting matrices
        fuzzyScatterNorms = get_fuzzy_c_scatter_norms(fuzzyScatterDeterminants,fuzzyScatterInverses, rhoDeterminants, p_value, nGroups)
        normDeterminants = get_fuzzy_c_scatter_determinants(fuzzyScatterMatrices)
        print normDeterminants
        #Get covariance distance metric
        dikMatrix = get_covariance_dik_matrix(distMatrix,initialCentroidMatrix,fuzzyScatterNorms)
        membershipMatrix = get_membership_matrix_version2(dikMatrix, m)
        updateCentroidMatrix = update_centroid_matrix(distMatrix,membershipMatrix, m)
        newError = check_for_error_version2(initialCentroidMatrix, updateCentroidMatrix)
        #print newError
    end_ii = len(membershipMatrix)
    for i in range(0,end_ii,1):
        newClass = dikMatrix[i].index(min(dikMatrix[i]))
        classAssignments.append([i,newClass])
        #print i, newClass
    return [classAssignments,updateCentroidMatrix, fuzzyScatterMatrices]



def run_fuzzy_c_means_logit(m_value,nGroups,inputData, minError):
    '''
    Change metric to form
    distance = 1-exp(-1.290*F4-0.608*F7-1.690*F12-1.808*L4)
    Drop constraint that membership must add up to 1 for
    each observation
    Essentially the distance is the membership value
    '''
    print nGroups
    distMatrix = inputData
    classAssignments = []
    m = m_value
    if m <= 1:
        m = 2
    coefMatrix = [-1.290,-0.608,-1.690,-1.808]
    #initialCentroidMatrix = initialize_centroid_matrix(distMatrix, nGroups)
    initialCentroidMatrix = initialize_centroid_matrix_max_min_rule(distMatrix, nGroups)
    dikMatrix = get_logit_dik_matrix(distMatrix, initialCentroidMatrix, m, coefMatrix)
    membershipMatrix = get_membership_matrix_version2(dikMatrix, m)
    updateCentroidMatrix = update_centroid_matrix(distMatrix,membershipMatrix, m)
    newError = check_for_error(initialCentroidMatrix, updateCentroidMatrix)
    #print newError
    while newError > minError:
        initialCentroidMatrix = replace_initialCentroidMatrix_with_updateCentroidMatrix(updateCentroidMatrix)
        dikMatrix = get_logit_dik_matrix(distMatrix, initialCentroidMatrix, m, coefMatrix)
        membershipMatrix = get_membership_matrix_version2(dikMatrix, m)
        updateCentroidMatrix = update_centroid_matrix(distMatrix,membershipMatrix, m)
        newError = check_for_error(initialCentroidMatrix, updateCentroidMatrix)
        print newError
    end_ii = len(membershipMatrix)
    for i in range(0,end_ii,1):
        newClass = dikMatrix[i].index(min(dikMatrix[i]))
        classAssignments.append([i,newClass])
        #print i, newClass
    return [classAssignments,updateCentroidMatrix]

def run_fuzzy_c_means_ibc_claims(m_value,nGroups,inputData, minError):
    print nGroups
    distMatrix = inputData
    classAssignments = []
    m = m_value
    if m <= 1:
        m = 2
    #ibc rule
    initialDateDict = get_initial_ibc_date(distMatrix) 
    initialCentroidMatrix = initialize_centroid_matrix_ibc_rule(distMatrix, nGroups, initialDateDict)
    dikMatrix = get_ibc_dik_matrix(distMatrix, initialCentroidMatrix, m)
    #print 'initialize membership matrix'
    membershipMatrix = get_membership_matrix_version2(dikMatrix, m)
    #print 'membership matrix initialized'
    updateCentroidMatrix = update_ibc_centroid_matrix(distMatrix,membershipMatrix, m, initialDateDict)
    newError = check_for_error(initialCentroidMatrix, updateCentroidMatrix)
    #end of ibc rule
    #Euclidean rule
    #dikMatrix = get_dik_matrix(distMatrix, initialCentroidMatrix, m)
    #membershipMatrix = get_membership_matrix_version2(dikMatrix, m)
    #updateCentroidMatrix = update_centroid_matrix(distMatrix,membershipMatrix, m)
    #newError = check_for_error(initialCentroidMatrix, updateCentroidMatrix)
    #End Euclidean Rule
    #Start Censored Euclidean Rule
    #dikMatrix = get_censored_dik_matrix(distMatrix, initialCentroidMatrix, m)
    #membershipMatrix = get_membership_matrix_version2(dikMatrix, m)
    #updateCentroidMatrix = update_censored_centroid_matrix(distMatrix,membershipMatrix, m)
    #newError = check_for_error(initialCentroidMatrix, updateCentroidMatrix)
    #End Censored Euclidean Rule
    print newError
    while newError > minError:
        #ibc rule
        initialCentroidMatrix = replace_initialCentroidMatrix_with_updateCentroidMatrix(updateCentroidMatrix)
        dikMatrix = get_ibc_dik_matrix(distMatrix, initialCentroidMatrix, m)
        membershipMatrix = get_membership_matrix_version2(dikMatrix, m)
        updateCentroidMatrix = update_ibc_centroid_matrix(distMatrix,membershipMatrix, m, initialDateDict)
        newError = check_for_error(initialCentroidMatrix, updateCentroidMatrix)
        #end of ibc rule
        #start Euclidean rule
        #initialCentroidMatrix = replace_initialCentroidMatrix_with_updateCentroidMatrix(updateCentroidMatrix)
        #dikMatrix = get_dik_matrix(distMatrix, initialCentroidMatrix, m)
        #membershipMatrix = get_membership_matrix_version2(dikMatrix, m)
        #updateCentroidMatrix = update_centroid_matrix(distMatrix,membershipMatrix, m)
        #newError = check_for_error(initialCentroidMatrix, updateCentroidMatrix)
        #End Of Euclidean rule
        #Start Censored Euclidean Rule
        #initialCentroidMatrix = replace_initialCentroidMatrix_with_updateCentroidMatrix(updateCentroidMatrix)
        #dikMatrix = get_censored_dik_matrix(distMatrix, initialCentroidMatrix, m)
        #membershipMatrix = get_membership_matrix_version2(dikMatrix, m)
        #updateCentroidMatrix = update_censored_centroid_matrix(distMatrix,membershipMatrix, m)
        #End Censored Euclidean Rule
        print newError
    end_ii = len(membershipMatrix)
    for i in range(0,end_ii,1):
        newClass = dikMatrix[i].index(min(dikMatrix[i]))
        classAssignments.append([i,newClass])
        #print i, newClass
    return [classAssignments,updateCentroidMatrix]


def getExistingFuzzyCMeansCentroids(centroidDict = {}, centroidHeader = [], classificationNo = 2, xVariableList = []):
    '''
    '''
    newHeader = deepcopy(centroidHeader)
    centroidList = [newHeader]
    nVariables = len(xVariableList)
    if not centroidDict.has_key(classificationNo):
        print ' asaClassifiers.getExistingFuzzyCMeansCentroids()'
        print ' centroidDictionary does not contain classification with:', classificationNo, 'number of classes'
        print ' can not retrieve existing centroids'
    else:
        groupNumberList = centroidDict[classificationNo].keys()
        groupNumberList.sort()
        i = 0
        for groupNo in groupNumberList:
            i = i + 1
            centroidList.append([classificationNo,groupNo])
            for j in range(0,nVariables,1):
                varValue = centroidDict[classificationNo][groupNo][xVariableList[j]]
                centroidList[i].append(varValue)
    return centroidList
     
    

    
    
    
    
        
         
     

