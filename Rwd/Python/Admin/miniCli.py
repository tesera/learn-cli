'''

'''
import miniApp
import dataMachete
import miniGraph
import random
import shutil
from copy import deepcopy

def reviewAndChangeConfigSettings(configKeyList = [], appConfig = {}, decisionCriteriaList = [],  appConfigInfo={}):
    '''
    '''
    for keyValue in configKeyList:
        print '\n ', keyValue, ':' , appConfig[keyValue]
        decisionValue = raw_input(' ... ')
        if decisionValue in decisionCriteriaList:
            if not appConfigInfo == {}:
                if appConfigInfo.has_key(keyValue):
                    print '\n keyValue >>', keyValue,'\n :',appConfigInfo[keyValue][0]
            #print '\n Enter new:', keyValue, ' criteria without [] \n and without quotation marks, then press ENTER'
            newValue = raw_input('\n ... ')
            #print newValue
            newValue.strip("")
            #print newValue
            newValueList = newValue.split(',')
            #+print newValueList
            appConfig.update({keyValue:newValueList})
    return appConfig

def writeConfigFileToInterpreter(configKeyList = [], appConfig = {}):
    print ' The config file has been reset to the following:\n'
    writeConfig = {}
    appConfigKeyList = appConfig.keys()
    for keyValue in appConfigKeyList:
        if not keyValue in configKeyList:
            configAttribute = []
            for varValue in appConfig[keyValue]:
                newValueList = varValue.split(':')
                nthValue = len(newValueList)-1
                configAttribute.append(newValueList[nthValue])
            writeConfig.update({keyValue: deepcopy(configAttribute)})
    for keyValue in configKeyList:
        configAttribute = []
        for varValue in appConfig[keyValue]:
            newValueList = varValue.split(':')
            nthValue = len(newValueList)-1
            configAttribute.append(newValueList[nthValue])
        writeConfig.update({keyValue: deepcopy(configAttribute)})
        print '', keyValue, ':' , configAttribute
    #print writeConfig
    return writeConfig
    

def getConfig(configName='', configdefpath = '', configaltpath = '', pathKeyList = [], configKeyList = [], configInfoName = ''):
    '''
    1. Looks for a standard config file; if found reads it
    2. Notifies user if config file is / is not found
    Scenario 1. Config file found:
    1. Do you want to use this config file as is?
    1.1. If yes: then program executes.
    1.2.1. If no:
        backup previous file
        cycle through each line in the config file and asks user to accept or change
       Accept = leave blank and press ENTER
       Reject = enter new infomration and press ENTER
    1.2.2. Once at the end the file is reprinted and user is asked if it is ok or not
        If not returns to processing every line again - 1.2.1.
        If yes proceed to 1.2.3.
    1.2.3. Overwrites config file - completes process
    
    Inputs
        configName      config file name e.g. cmeansConfig.txt
        configdefpath   directory where configName can be found, e.g. '/apps/TSIAnalytics/Config/'
        configaltpath   alternative directory where configName can be found, e.g. '/Users/Maxine/Documents/TSIAnalytics/Config/'
        pathKeyList     data in and data out paths in that order, e.g. ['cmeansDataInPath', 'cmeansDataOutPath']
        configKeyList   optional: list of config key names in the order that they are to be presented to the user
                        if left blank then it will be the same order as identified in the appConfig file using the .keys() command
        configInfoName  Optional - if not blank then information as to how the keys in the configName file are to be interpreted
                        i.e., what they mean.
    '''
            
    configPathAddress = configdefpath + configName
    fileExists = dataMachete.checkFileIfItExists(configPathAddress)
    if fileExists == 0:
        #Config file does not exist - try alternative file path
        configPathAddress = configaltpath + configName
        fileExists = dataMachete.checkFileIfItExists(configPathAddress)
    if fileExists == 0:
        #Config file does not exist
        print ' miniCli.py'
        print ' config filename', configName, 'not found'
    else:
        #fileExists = 1
        print ' config file:', configName, 'found'
        appConfig = miniApp.getConfig(filename=configName, defpath=configdefpath, altpath=configaltpath, pathkeyslist=pathKeyList)  #read config file
        print '\n Do you wish to change the original config file settings?'  
        rejectFile = raw_input(' Type YES if you do, otherwise press ENTER ... ')
        if rejectFile == 'YES' or rejectFile == 'Y' or rejectFile == 'Yes' or rejectFile == 'yes' or rejectFile == 'y':
            #Try to find file with configInfoName if not left blank
            if not configInfoName == '':
                configInfoPathAddress = configdefpath + configInfoName
                fileExists = dataMachete.checkFileIfItExists(configInfoPathAddress)
            if fileExists == 0:
                configInfoPathAddress = configaltpath + configInfoName
                fileExists = dataMachete.checkFileIfItExists(configInfoPathAddress)
            if fileExists == 0:
                appConfigInfo = {}
            else:
                print '\n Application configuration information file found: \n ', configInfoPathAddress
                print '\n Do you want to use the application configuration \n information to help decide if changes are needed?'
                acceptFile = raw_input('\n Type YES if you do, otherwise press ENTER ... ')
                if acceptFile == 'YES' or acceptFile == 'Y' or acceptFile == 'Yes' or acceptFile == 'yes' or acceptFile == 'y':
                    appConfigInfo = miniApp.getConfig(filename=configInfoName, defpath=configdefpath, altpath=configaltpath, pathkeyslist=[])
                else:
                    appConfigInfo = {}
           
            #make backup of old file
            rejectFile = 'YES'
            randomNo = int(1000*random.random())
            #Strip .txt from end of original file and add .bak to same file; then save
            newFilePathList = configPathAddress.split('.')
            newFilePath = newFilePathList[0] + str(randomNo) + '.bak'
            print '\n Original configure file backed up @', newFilePath
            shutil.copy2(configPathAddress,newFilePath)
            if configKeyList == []:                 #If configuration key list is blank populate list with appConfig keys
                configKeyList = appConfig.keys()
            while rejectFile == 'YES':
                print '\n For each item in the configuration file enter NO to make a change,\n otherwise press ENTER to accept'
                appConfig = reviewAndChangeConfigSettings(configKeyList, appConfig, ['NO','N','No','n','no'], appConfigInfo)
                writeConfig = writeConfigFileToInterpreter(configKeyList, appConfig)
                print '\n Enter YES if you wish to accept these configuration settings, \n otherwise press ENTER to make further changes'
                acceptFile = raw_input('\n ... ')
                if acceptFile == 'YES' or acceptFile == 'Yes' or acceptFile == 'Y' or acceptFile == 'yes' or acceptFile == 'y':
                    rejectFile = 'NO'
                    #Save new file
                    #print writeConfig 
                    miniGraph.writeGraph(writeConfig, configPathAddress, append=0)
            print '\n New configuration file created and processing continued'
        return appConfig
    return
            
        
            
            
            
            
        
