'''

'''
import sys

print ' Running COHENS_KHAT'

#Identify code directory and data directory
adminPath = 'D:\\Rwd\\Python\\Admin\\'
inputDataPath = 'D:\\Rwd\\'
errorFilePath = 'D:\\Rwd\\Python\\PyReadError\\'
sys.path.append(adminPath)
sys.path.append(inputDataPath)
printFilePath = inputDataPath + 'CTABSUM.csv'

import makeDD
import dictionaryDBUtilities
import readCSV
import typeDataset
import fileUtilities
import PRINTv1

#Get Data Dictionary
dictFilePath = 'D:\\Rwd\\Python\\DATDICT\\'
filename = 'PyRDataDict'
fileExtension = '.csv'
originalDict, newDict = makeDD.dataDictionaryType_21(dictFilePath,filename, fileExtension)

#Get LVI dataFile Non normalized data
#dataTableName = 'LVINEW'
ctabTableName = 'CTABULATION'
ctabErrorFilePath = errorFilePath + 'ERROR-CHECK-CTABULATION.txt'
ctabKeyVarnames = ['VARSET','REFCLASS', 'PREDCLASS']
fileExtension = '.csv'
ctabStringList = readCSV.read_csv_text_file_v2(inputDataPath, ctabTableName, fileExtension)
ctabTypedList = typeDataset.typeDataset(ctabStringList, originalDict, ctabTableName, ctabErrorFilePath)
#Create a data dictionary
ctabDict = {}
ctabHeader = ctabTypedList[0]
ctabDict = dictionaryDBUtilities.additive_nested_key_multiple_item_dictionary(ctabDict,ctabKeyVarnames,ctabTypedList)
#Build matrices
varsetKeyList = ctabDict.keys()
varsetKeyList.sort()
#Initialize CTAB SUMMARY DICTIONARY
ctabSumDict = {}
ctabSumDictHeader = ['VARSET', 'OA','KHAT','MINPA','MAXPA','MINUA','MAXUA']
ctabSumDictKeyVarnames = ['VARSET']
for varset in varsetKeyList:
    newArray = []
    refclassKeyList = ctabDict[varset].keys()
    refclassKeyList.sort()
    lengthRef = len(refclassKeyList)
    for i in range(0,lengthRef,1):
        newArray.append([])
        refclass = refclassKeyList[i]
        predclassKeyList = ctabDict[varset][refclass].keys()
        predclassKeyList.sort()
        lengthPred = len(predclassKeyList)
        if not lengthRef == lengthPred:
            print 'COHENS_KHAT: Differeint number of classes'
            print 'Varset:', varset, 'Reference class N:', lengthRef, 'Predicted class N:', lengthPred
        for j in range(0,lengthPred,1):
            predclass = predclassKeyList[j]
            nObs = ctabDict[varset][refclass][predclass]['CTAB']
            newArray[i].append(nObs)
    #Compute total number of observations
    totalObs = 0
    traceVector = []
    rowSums = []
    userAccuracy = []
    #For each row get row sum and trace elements
    for i in range(0,lengthRef,1):
        rowSum = sum(newArray[i])
        totalObs = totalObs + rowSum
        rowSums.append(rowSum)
        traceN = newArray[i][i]
        traceVector.append(traceN)
        userAccuracy.append(traceN/float(rowSum))
    #Get Column Sums
    columnSums = []
    producerAccuracy = []
    for j in range(0, lengthPred,1):
        colSum = 0
        for i in range(0,lengthRef,1):
            colSum = colSum + newArray[i][j]
        columnSums.append(colSum)
        if not colSum == 0:
            producerAccuracy.append(traceVector[j]/float(colSum))
        else:
            producerAccuracy.append(0)
    #Overall Accuracy
    totalTrace = sum(traceVector)
    overallAccuracy = totalTrace/float(totalObs)
    #Get sum of corresponding row multiplied by column totals
    sumRC = 0
    for i in range(0,lengthRef,1):
        sumRC = sumRC + rowSums[i]*columnSums[i]
    kNumerator = (totalObs*totalTrace) - sumRC
    kDenominator = (totalObs**2) - sumRC
    kHat = kNumerator/float(kDenominator)
    minUser = min(userAccuracy)
    maxUser = max(userAccuracy)
    minProd = min(producerAccuracy)
    maxProd = max(producerAccuracy)
    #Update ctabSumDict
    ctabSumDict.update({int(varset):{'OA':overallAccuracy,'KHAT':kHat,'MINUA':minUser,'MAXUA':maxUser,'MINPA':minProd,'MAXPA':maxProd}})
    #print varset, overallAccuracy, kHat, minUser, maxUser, minProd, maxProd
    PRINTv1.initialize_header(ctabSumDictHeader,printFilePath)
    PRINTv1.print_to_nested_dictionary(ctabSumDictKeyVarnames,ctabSumDictHeader,ctabSumDict, printFilePath)

print ' New File Created CTABSUM.csv'
print '\n Now run COMBINE_EVALUATION_DATASETS.py'

#raw_input("\n Press ENTER to Close This Session ... ")            
        


        
    
