'''
'''
#import MAN
#import BASE
import MATRIX_MAN
#import random
#import bisect
from math import *
from random import *
import numpy
#import time

def initialize_mahalanobis_v3_standard_deviations(varMatrix, nObs):
    '''
    varMatrix is the inputData nClasses is equal to nGroups
    
    This subroutine initializes the standard deviations for the input data
    where variables are in the columns.  A standard deviation
    is calculated for each variable.

    The output of this function are standard deviations by variable (in the columns).
    '''
    
    varMatrixT = MATRIX_MAN.get_transpose_of_matrix(varMatrix)
    varCovariance = MATRIX_MAN.matrix_multiply_inner_product(varMatrixT, varMatrixT)
    varCovariance = (1/float(nObs))*varCovariance
    return varCovariance

def initialize_centroid_matrix_max_min_rule(distList, k_centroids):
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
                dikValue = dikValue + (distMatrix[i][k]- newCentroidMatrix[j][k])**2
            dikMatrix[i][j] = dikValue
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
            xMatrix = MATRIX_MAN.matrix_multiply_inner_product(invCovMatrix,dikVector)
            xDist = MATRIX_MAN.matrix_multiply_inner_product(dikVector,xMatrix)
            dikMatrix[i][j] = xDist
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


def run_fuzzy_c_means_euclidean(m_value,nGroups,inputData, minError):
    print nGroups
    distMatrix = inputData
    classAssignments = []
    m = m_value
    if m <= 1:
        m = 2
    #initialCentroidMatrix = initialize_centroid_matrix(distMatrix, nGroups)
    initialCentroidMatrix = initialize_centroid_matrix_max_min_rule(distMatrix, nGroups)
    dikMatrix = get_dik_matrix(distMatrix, initialCentroidMatrix, m)
    #membershipMatrix = get_membership_matrix(dikMatrix, m)
    membershipMatrix = get_membership_matrix_version2(dikMatrix, m)
    updateCentroidMatrix = update_centroid_matrix(distMatrix,membershipMatrix, m)
    newError = check_for_error(initialCentroidMatrix, updateCentroidMatrix)
    #print newError
    while newError > minError:
        initialCentroidMatrix = replace_initialCentroidMatrix_with_updateCentroidMatrix(updateCentroidMatrix)
        dikMatrix = get_dik_matrix(distMatrix, initialCentroidMatrix, m)
        #membershipMatrix = get_membership_matrix(dikMatrix, m)
        membershipMatrix = get_membership_matrix_version2(dikMatrix, m)
        updateCentroidMatrix = update_centroid_matrix(distMatrix,membershipMatrix, m)
        newError = check_for_error(initialCentroidMatrix, updateCentroidMatrix)
        #print newError
    end_ii = len(membershipMatrix)
    for i in range(0,end_ii,1):
        newClass = dikMatrix[i].index(min(dikMatrix[i]))
        classAssignments.append([i,newClass])
        #print i, newClass
    return classAssignments,updateCentroidMatrix

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
    initialCentroidMatrix = initialize_centroid_matrix_max_min_rule(distMatrix, nGroups)
    dikMatrix = get_censored_dik_matrix(distMatrix, initialCentroidMatrix, m)
    #membershipMatrix = get_membership_matrix(dikMatrix, m)
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
    return classAssignments,updateCentroidMatrix

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

    Note that I rean into a situation where the error decreased to a minimum
    and then started to increase before crossing the minimum error criteria.
    Also there are some improvements that can be made based on the work of
    Liu et al. 2008.

    
    
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
    invCovMatrix = MATRIX_MAN.get_inverse_of_matrix(covMatrix)    
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
        oldError = newError
        initialCentroidMatrix = replace_initialCentroidMatrix_with_updateCentroidMatrix(updateCentroidMatrix)
        dikMatrix = get_covariance_normalized_dik_matrix(distMatrix, invCovMatrix, initialCentroidMatrix, m)
        membershipMatrix = get_membership_matrix_version2(dikMatrix, m)
        #Need to keep old membership matrix 
        updateCentroidMatrix = update_centroid_matrix(distMatrix,membershipMatrix, m)
        #need to keep old centroid matrix 
        newError = check_for_error(initialCentroidMatrix, updateCentroidMatrix)
        if newError > oldError:
            #Use previous centroid matrix
            break
        print newError
    end_ii = len(membershipMatrix)
    for i in range(0,end_ii,1):
        newClass = dikMatrix[i].index(min(dikMatrix[i]))
        classAssignments.append([i,newClass])
        #print i, newClass
    return classAssignments,updateCentroidMatrix, covMatrix
