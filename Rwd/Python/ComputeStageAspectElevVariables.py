'''
This routine derived a new set of variables based on transofmration
of slope, aspect, and elevation that are based on the work of Al Stage
as follows:

Stage, A.B., and Salas, C. 2007. Interaction of elevation, aspect, and slope
in models of forest species composition and productivity.
Forest Science 53(4): 486-492.

The following variable transforms are computed:
ASP = aspect(degrees)
SLOP = slope (degrees)
ELEV = Elevation (m) 
ELEV2 = ELEV**2
SLOPELEV2 = SLOP*ELELV2
SLOPCASP = SLOP*cosine(ASP)
SLOPSASP = SLOP*sine(ASP)
SLNELEV = SLOP*ln(ELEV+1)
SLNELEVCA = SLNELEV*SLOPCASP
SLNELEVSA = SLNELEV*SLOPSASP
SE2CA = SLOPELEV2*cosine(ASP)
SE2SA = SLOPELEV2*sin(ASP)
'''

import RESET_SYS_PATH
import miniCli
import dataMachete
import routineLviApplications

#Initialize configuration settings
configName = 'stageTerrainConfig.txt'
configdefpath = '/Rwd/Python/Config/'
configaltpath = '/Rwd/Python/Config/'
pathkeyslist=['dataInPath', 'dataOutPath', 'readErrorFilePath']
configKeyList = ['dataInFileName','dataPrimaryKeyVariableName','dataOutFileName','slopeVarName','elevationVarName','aspectVarName']
#Get Information About Configuration File 
configInfoName = 'stageTerrainConfigInfo.txt'
config = miniCli.getConfig(configName, configdefpath, configaltpath, pathkeyslist, configKeyList, configInfoName)
dataInPath = config['dataInPath'][0]
dataOutPath = config['dataOutPath'][0]
myDataTableName = config['dataInFileName'][0]
dataOutFileName = config['dataOutFileName'][0]
readErrorFilePath = config['readErrorFilePath'][0]
slopeVarName = config['slopeVarName'][0]
elevationVarName = config['elevationVarName'][0]
aspectVarName = config['aspectVarName'][0]
varNameList = config['outputVarNameList']
dataKeyVarNameList = config['dataPrimaryKey']
readLineIncrement = int(config['largeDatasetReadLines'][0])
printFilePath = dataOutPath + dataOutFileName
#Infer data dictionary
printTypes = 'YES'
readErrorFileName = 'ERROR_' + myDataTableName
fileExtension = ''
oldDict, newDict = dataMachete.inferDataDictionary_v2(myDataTableName, dataInPath, fileExtension, printTypes, readLineIncrement)
# Initialize large dataset processing
startReadLine = 0
endOfFile = False
batch = 0
while endOfFile == False:
    batch = batch + 1
    print '\n Processing batch number:', batch
    endReadLine = startReadLine + readLineIncrement + 1
    dataTypedList, dataTypedDict = dataMachete.getLargeDatasetListArrayAndDictDB(myDataTableName, dataInPath, \
                        readErrorFilePath, dataKeyVarNameList, oldDict, newDict, fileExtension,
                        printTypes, startReadLine, endReadLine)

    #Check to see if endOfFile
    readLineCount = len(dataTypedList)
    if readLineCount == 1 or readLineCount == 0:
        break
    else:       
        if readLineCount < readLineIncrement:
            endOfFile = True
        stageHeader, stageDict = routineLviApplications.compileStageSlopeAspectElevTransformationsAndAddToData(dataTypedDict,dataKeyVarNameList, slopeVarName, \
                                                            elevationVarName, aspectVarName, \
                                                            varNameList)
        if startReadLine == 0:
            dataMachete.initializeVariableHeader(stageHeader,printFilePath)
        dataMachete.saveDictDB(dataKeyVarNameList,stageHeader,stageDict,printFilePath)
        startReadLine = endReadLine
print '\n Finished generating Stage Terrain indices'
    
        
 


