'''
'''
import routineLviApplications

#interactiveMode = 'YES'
interactiveMode = 'NO'

myDataDictName = 'PyRDataDict'

#Open Dictionary
originalDict, newDict = routineLviApplications.ReadLviDataDictionary(myDataDictName)

#Open LVINEW with Y-Variable Dataset
lvinewTableName = 'LVINEW'
readErrorFileName = 'ERROR_LVINEW'
keyVarNameList = ['LVI_FCOID']
lvinewHeader, lvinewTypedDict = routineLviApplications.ReadCsvDataFileAndTransformIntoDictionaryFormat_v2(originalDict, newDict, lvinewTableName, \
                                                                                     readErrorFileName, keyVarNameList)
#
#Read Y-variable selection
varSelTableName = 'XVARSELV1'
varSelKeyVarNameList = ['TVID']
readErrorFileName = 'ERROR-CHECK-VSEL'
varSelHeader, varSelTypedDict = routineLviApplications.ReadCsvDataFileAndTransformIntoDictionaryFormat_v2(originalDict, newDict, varSelTableName, \
                                                                                      readErrorFileName, varSelKeyVarNameList)

#Get selected Y- variable list
varSelectCriteria = 'Y'
yVarNameList = routineLviApplications.createSelectVariableListFromXvarselv1TypedDict(varSelTypedDict, varSelectCriteria)

myDataDictName = {}
print "\n The demo NNTARGET filename is 'NNTARGET64'"
nnTargetTableNo = raw_input("\n Input the NNTARGET file no, e.g. '64' without the '', the press ENTER ...")
nnTargetTableName = 'NNTARGET' + nnTargetTableNo
readErrorFileName = 'ERROR_NNTARGET'
keyVarNameList = ['TARGOBS']

if not myDataDictName == {}:
    origDict2, newDict2 = routineLviApplications.ReadLviDataDictionary(myDataDictName)
else:
    origDict2 = {}
    newDict2 = {}
    
targetHeader, targetTypedDict = routineLviApplications.ReadCsvDataFileAndTransformIntoDictionaryFormat_v2(origDict2, newDict2, nnTargetTableName, \
                                                                                     readErrorFileName, keyVarNameList)

targStatHeader,targStatKeyVarNameList,targStatDict = routineLviApplications.compileTargetNearestNeighbourYStatistics(targetHeader, targetTypedDict, lvinewTypedDict, yVarNameList, nnTargetTableNo)

print "\n Done"        
    

