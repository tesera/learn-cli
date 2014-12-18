'''
'''
import routineLviApplications

#interactiveMode = 'YES'
interactiveMode = 'NO'

#Get Species Report
#Notify user as to location of data dictionary for new dataset

if interactiveMode == 'YES':
    myDataDictName, newDataTableName, keyVarNameList, readErrorFileName = routineLviApplications.GetStandardDataInputFiles()
    spColumnNames = routineLviApplications.GetSpeciesColumnNames()
    spPcntColumnNames = routineLviApplications.GetSpeciesPercentColumnNames()
else:
    myDataDictName = 'LVIDICT'
    readErrorFileName = 'ERROR_CHK_SPECTRAL'
    #Get name of the file containing the actual data
    newDataTableName = 'DCS_ATT_SPECTRAL'
    keyVarNameList = ['LVI_FCOID']
    spColumnNames = ['LVI_SP1','LVI_SP2','LVI_SP3','LVI_SP4']
    spPcntColumnNames = ['LVI_PCT1','LVI_PCT2','LVI_PCT3','LVI_PCT4']
    
#Open Dictionary
originalDict, newDict = routineLviApplications.ReadLviDataDictionary(myDataDictName)    
varSelHeader, varSelTypedDict = routineLviApplications.ReadCsvDataFileAndTransformIntoDictionaryFormat_v2(originalDict, newDict, newDataTableName, \
                                                                                     readErrorFileName, keyVarNameList)
# GetTreeSpeciesList
spList = routineLviApplications.GetSpeciesList(varSelTypedDict,spColumnNames)
spDict = routineLviApplications.AssignNewSpeciesCodes(spList)



 
        
    


