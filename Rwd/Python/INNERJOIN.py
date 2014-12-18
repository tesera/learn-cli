'''
This routine completes a one-to-one inner join for two datasets
with the same set of keys ranging from a single primary key variable name
to nested sets of keys wherein the key variable names are identical
in both datasets.  The routine has been developed for both large and small
datasets.  The user defines a left and right table and the key variable names
by way of the innerJoinConfig file.  The user also defines the number of lines
in the left and right tables that will be processed in a batch (left) or subBatch (right).
The routine processes each batch in memory by looking in each successive subBatch
for the keys that match in each subBatch.  Where matches are found a join is made
and the new data is placed in a master dictionary.  When all joins are completed
for a given batch the batch is written to a file (defined by the user in the innerJoinConfig
file) and the next batch is loaded into memory and the process is started
all over again by way of comparison of each subBatch in the right table.  Some diagnostics
are printed to the screen to help the user verify whether or not the process is
being correctly applied.
'''

import miniCli
import dataMachete
import innerJoinDictDBs
import readCSV
#import os
#import inspect
#import sys
import time

#print os.path.dirname(inspect.getfile(dataMachete))
#print sys.path

# Input original LVI data
print '\n This routine joins two tables, the left and right table based on \n matching unique keys according to a single unique key variable name'
print '\n The routine completes a one-to-one join; it does not complete a one to many join.'
print '\n The routine requires that the same set of names of one or more key \n variables be identified in both the left and right tables.'
print '\n This routine can be used for large or small datasets'

# Initialize configuration settings
configName = 'innerJoinConfig.txt'
configdefpath = '/Rwd/Python/Config/'
configaltpath = '/Rwd/Python/Config/'
pathkeyslist=['dataInPath', 'dataOutPath', 'readErrorFilePath']
configKeyList = ['dataInFileNameLeft','dataInFileNameRight','dataPrimaryKeyLinkName','dataOutFileName']
# Get Information About Configuration File 
configInfoName = 'innerJoinConfigInfo.txt'
config = miniCli.getConfig(configName, configdefpath, configaltpath, pathkeyslist, configKeyList, configInfoName)
dataInPath = config['dataInPath'][0]
dataOutPath = config['dataOutPath'][0]
dataInFileNameLeft = config['dataInFileNameLeft'][0]
dataInFileNameRight = config['dataInFileNameRight'][0]
dataKeyNameList = config['dataKeyNameList']
dataOutFileName = config['dataOutFileName'][0]
readErrorFilePath = config['readErrorFilePath'][0]
largeDatasetReadLines = int(config['largeDatasetReadLines'][0])
readLineIncrement = largeDatasetReadLines
#
printTypes = 'YES'
readErrorFilePathLeft = readErrorFilePath + 'ERROR_' + dataInFileNameLeft
readErrorFilePathRight = readErrorFilePath + 'ERROR_' + dataInFileNameRight
fileExtension = ''
# Generate data dictionaries on the fly
oldDictLeft, newDictLeft = dataMachete.inferDataDictionary_v2(dataInFileNameLeft, dataInPath, fileExtension, printTypes, readLineIncrement)
oldDictRight, newDictRight = dataMachete.inferDataDictionary_v2(dataInFileNameRight, dataInPath, fileExtension, printTypes, readLineIncrement)
#Initialize print file path and overwrite file using innerJoinHeader
leftHeader = readCSV.read_csv_text_file_header_v2(dataInPath,dataInFileNameLeft, '')
rightHeader = readCSV.read_csv_text_file_header_v2(dataInPath,dataInFileNameRight, '')
newFileHeader = dataMachete.joinOneDListBToRightOfOneDListAExcludingValuesAlreadyInA(leftHeader, rightHeader)
printFilepath = dataOutPath + dataOutFileName
dataMachete.initializeVariableHeader(newFileHeader,printFilepath)
# Initialize large dataset processing
startReadLineLeft = 0
endOfFileLeft = False
batch = 0
fileExtension = ''
printTypes = 'NO'
joinCount = 0
joinNo = 0
leftTableObsCount = 0
print '\n'
while endOfFileLeft == False:
    batch = batch + 1
    print ' Start processing batch number:', batch, startReadLineLeft, joinCount, time.ctime()
    endReadLineLeft = startReadLineLeft + readLineIncrement
    dataTypedDictLeft = dataMachete.getLargeDatasetListArrayAndDictDB_v2(dataInFileNameLeft, dataInPath, \
                        readErrorFilePathLeft, dataKeyNameList, oldDictLeft, newDictLeft, fileExtension,
                        printTypes, startReadLineLeft, endReadLineLeft, False, True)
    dataTypedDictLeftKeyList = innerJoinDictDBs.getDictKeySetValuesList(dataTypedDictLeft, dataKeyNameList)
    dataTypedDictLeftKeyList.sort()
    leftLineCount = len(dataTypedDictLeftKeyList)
    #Check for end of left table file
    if leftLineCount == 0:
        break
    else:       
        if leftLineCount < readLineIncrement-1:
            endOfFileLeft = True
    endOfFileRight = False
    #Start looking for matches in right table
    startReadLineRight = 0
    masterDict = {}
    masterKeyList = []
    masterKeyCount = 0
    subBatch = batch
    subBatchJoinNo = 0
    while endOfFileRight == False:
        print '  SubBatch number:', subBatch, startReadLineRight, subBatchJoinNo, time.ctime()
        endReadLineRight = startReadLineRight + readLineIncrement
        dataTypedDictRight = dataMachete.getLargeDatasetListArrayAndDictDB_v2(dataInFileNameRight, dataInPath, \
                        readErrorFilePathRight, dataKeyNameList, oldDictRight, newDictRight, fileExtension,
                        printTypes, startReadLineRight, endReadLineRight, False, True)
        dataTypedDictRightKeyList = innerJoinDictDBs.getDictKeySetValuesList(dataTypedDictRight, dataKeyNameList)
        dataTypedDictRightKeyList.sort()
        rightLineCount = len(dataTypedDictRightKeyList)
        #Check for end of right table file
        if rightLineCount == 0:
            break
        else:       
            if rightLineCount < readLineIncrement-1:
                endOfFileRight = True       
        #Get common inner join key list
        commonKeyList = innerJoinDictDBs.getCommonInnerJoinKeyValueList(dataTypedDictLeftKeyList, dataTypedDictRightKeyList)
        nJoins = len(commonKeyList)
        joinNo = joinNo + nJoins
        subBatchJoinNo = subBatchJoinNo + nJoins
        if not commonKeyList == []:
            innerJoinDict = innerJoinDictDBs.extractDictDBForKeySetsList(dataTypedDictLeft,dataTypedDictRight,commonKeyList)
            masterDict = dataMachete.appendNewDictToMasterDictionary(masterDict,innerJoinDict, dataKeyNameList)
            masterKeyList = dataMachete.appendRowsFrom2DListBTo2DListAExclusiveOfItemsAlreadyInA(masterKeyList, commonKeyList)
            masterKeyCount = len(masterKeyList)
            dataTypedDictLeftKeyList = dataMachete.removeItemsIn1DListBFrom1DListA(dataTypedDictLeftKeyList,commonKeyList)
        subBatch = subBatch + 0.001
        startReadLineRight = endReadLineRight
        #Note could write masterDict to file at certain threshold and then add new lines in the left dictionary
        #and empy masterDict; this might speed the process up
        if len(dataTypedDictLeftKeyList)==0:
            break
    if not masterDict == {}:
        dataMachete.saveDictDB(dataKeyNameList,newFileHeader,masterDict, printFilepath)
        joinCount = joinCount + masterKeyCount
        leftTableObsCount = leftTableObsCount + leftLineCount
    startReadLineLeft = endReadLineLeft
    
print '\n Completed inner join process.'
print ' There were:', leftTableObsCount, 'records in the left table:', dataInFileNameLeft
print ' There were:', joinCount, 'inner joins processed.'
print time.ctime()
raw_input("\n Press ENTER to finish session ... ")
    
    




