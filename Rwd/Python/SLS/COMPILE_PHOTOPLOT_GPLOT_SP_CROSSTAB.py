import routineLviApplications
#Get data dictionary
dictName = 'SLSDATDICT'
oldDict, newDict = routineLviApplications.ReadLviDataDictionary(dictName)
#Update old and new data dictionaries to reflect change in tableNames
oldTableName = 'Interpreters_Groundplot_Boundaries'
dataTableName = 'GPHOTO'
oldDict = routineLviApplications.UpdateDataDictionaryWithNewTableName(oldDict, oldTableName, dataTableName)
newDict = routineLviApplications.UpdateDataDictionaryWithNewTableName(newDict, oldTableName, dataTableName)
#Read photo plot data file and change variable names to those in new dictionary
readErrorFileName = 'ERROR_' + dataTableName
keyVarNameList = ['IPG_PKEY']
photoKeyVarNameList = ['INTERP_GP_ID']
photoHeader, photoDict = routineLviApplications.ReadCsvDataFileAndTransformIntoDictionaryFormat_v2(oldDict, newDict, \
                                                                                   dataTableName, readErrorFileName, photoKeyVarNameList)

#Read in ground plot data
#gyTableName = 'PSPSUMSEL'
#gyTableName = 'PSPSUMSEL2'
#gyTableName = 'PSPSUMSEL3'
gyTableName = 'PSPSUMSELCAL'    #Photo calibration plots removed
printTypes = 'YES'
nLines = 10000
oldGyDict, newGyDict = routineLviApplications.createNewDataDictionaryFromFile(gyTableName, printTypes, nLines)
readErrorFileName = 'ERROR_' + dataTableName
gyKeyVarNameList = ['MEASPLOTID']
gyHeader, gyDict = routineLviApplications.ReadCsvDataFileAndTransformIntoDictionaryFormat_v2(oldGyDict, newGyDict, gyTableName, \
                                                                                             readErrorFileName, gyKeyVarNameList)



#Check Species List
#Note species that are identified as blank should be changed to 'NA'
spColNamesList = ['IGB_SP1', 'IGB_SP2', 'IGB_SP3', 'IGB_SP4', 'IGB_SP5', 'IGB_USP1', 'IGB_USP2','IGB_USP3','IGB_USP4','IGB_USP5']
spTableName = 'SPDICT'
dataDictType = 'ONEKEY'
spDictKeyList, spDictHeader, spDict, newSpList = routineLviApplications.GetSpeciesCodesFromFileOrAssigneNewSpeciesCodes(photoDict, spColNamesList, spTableName, dataDictType)
#Replace tree species in photoDict with new species
photoDict = routineLviApplications.ReplaceTreeSpeciesInOneKeyDataWithNewSpecies(photoDict,spDict, spColNamesList)

#Check for species from gyTable
print '\n Now Check For Species in Ground Plot Data'
spColNamesList = ['SP1', 'SP2', 'SP3', 'SP4', 'SP5', 'SP6', 'SP7','SP8','SP9','SP10']
spTableName = 'SPDICT'
dataDictType = 'ONEKEY'
spDictKeyList, spDictHeader, spDict, newSpList = routineLviApplications.GetSpeciesCodesFromFileOrAssigneNewSpeciesCodes(gyDict, spColNamesList, spTableName, dataDictType)
#Replace tree speecies in gyDict with new species
gyDict = routineLviApplications.ReplaceTreeSpeciesInOneKeyDataWithNewSpecies(gyDict,spDict, spColNamesList)


#Compile Photo Plot Level Species Percentages
spColNameList = ['IGB_SP1', 'IGB_SP2','IGB_SP3','IGB_SP4','IGB_SP5']
spPcntNameList = ['IGB_SP1_PER','IGB_SP2_PER','IGB_SP3_PER','IGB_SP4_PER','IGB_SP5_PER']
spPropHeader, spPropDict = routineLviApplications.CompilePlotLevelSpeciesProportions(photoDict, photoKeyVarNameList, newSpList, \
                                                                       spColNameList, spPcntNameList)
#Compile Ground Plot Level Species Percentages
gySpColNameList = ['SP1', 'SP2', 'SP3', 'SP4', 'SP5', 'SP6', 'SP7','SP8','SP9','SP10']
gySpPcntNameList = ['SP_PCT1','SP_PCT2','SP_PCT3','SP_PCT4','SP_PCT5', 'SP_PCT6', 'SP_PCT7', 'SP_PCT8', 'SP_PCT9', 'SP_PCT10']
gySpPropHeader, gySpPropDict = routineLviApplications.CompilePlotLevelSpeciesProportions(gyDict, gyKeyVarNameList, newSpList, \
                                                                       gySpColNameList, gySpPcntNameList)

#Need to Extract species percentages by Interprter for each NPLOTID
nplotidKeyVarNames = ['NPLOTID','IGB_INITIALS']
#Define variable subsets to be extracted from photoDict and spPropDict
#Make a deepcopy of the spPropDict header
nplotidHeader = routineLviApplications.DeepCopyList(spPropHeader)
#Remove the old keyVarNames, e.g. ['INTERP_GP_ID'], in both nplotidHeader

spNameList = routineLviApplications.removeItemsInOneDListBFromOneDListA(nplotidHeader, photoKeyVarNameList)
#Add new keyVarNames, e.g. ['NPLOTID', 'IGB_INIYIALS'] as the first two rows of nplotidHeader
nplotidHeader = routineLviApplications.joinOneDListBToRightOfOneDListA(nplotidKeyVarNames, spNameList)
#Complete inner join of photoDict and spPropDict and extract desired variable subset
nplotidDataList = routineLviApplications.InnerJoinDictAAndDictBAndExtractVariableSubset(photoDict, photoKeyVarNameList, \
                                                                                        spPropDict, nplotidHeader)
#Complete inner join of gyDict and gySpPropDict and extract desired variable subset
gyNplotidDataList = routineLviApplications.InnerJoinDictAAndDictBAndExtractVariableSubset(gyDict, gyKeyVarNameList, \
                                                                                        spPropDict, nplotidHeader)

#Get photo interpreters list
photoInterpreterList = routineLviApplications.identifyUniqueValuesForAGivenListOfVariableNamesInRow0(nplotidDataList,['IGB_INITIALS'])
gyInterpreterList = routineLviApplications.identifyUniqueValuesForAGivenListOfVariableNamesInRow0(gyNplotidDataList,['IGB_INITIALS'])
#Convert plotid - phto interpreter table back into dictionary format
nplotidHeader, nplotidDict = routineLviApplications.TransformDataTypedListIntoDictionaryFormat(nplotidKeyVarNames, nplotidDataList, {})
gyNplotidHeader, gyNplotidDict = routineLviApplications.TransformDataTypedListIntoDictionaryFormat(nplotidKeyVarNames, gyNplotidDataList, {})

#Combine gyNplotDict with nplotidDict with requirement that Level 1 keys match
keyLevelMatch = 1
nplotidDict = routineLviApplications.combinedDictionariesWithCommonKeyStructure(nplotidDict, gyNplotidDict, nplotidKeyVarNames, nplotidHeader, keyLevelMatch) 
photoInterpreterList = routineLviApplications.joinOneDListBToRightOfOneDListAExcludingValuesAlreadyInA(photoInterpreterList, gyInterpreterList)

#Cross tabulate photo interpeter results
plotInterpKeyVarNames, plotInterpHeader, plotInterpDict = routineLviApplications.ExtractPhotoInterpreterSpeciesRecognition(nplotidDict, nplotidKeyVarNames, photoInterpreterList, spNameList)
#Initialize prinary key variable name cor cross tabulations in string format
piCtabKeyVarName = 'NPLOTID'
piKeyVarNames, piInterpHeader, piInterpDict, piSumKeyVarNames, piSumHeader, piSumDict, interpSpKeyVarNames, interpSpHeader, interpSpDict = routineLviApplications.CrossTabulateInterpeterSpeciesRecognition(plotInterpDict, piCtabKeyVarName, photoInterpreterList, spNameList)
#Print interpreter data
tableName = 'SPINTERP'
routineLviApplications.printNestedDictionary(piKeyVarNames, piInterpHeader, piInterpDict, tableName)
tableName = 'INTERPCTAB'
routineLviApplications.printNestedDictionary(piSumKeyVarNames, piSumHeader, piSumDict, tableName)
tableName = 'SPDISTINTERP'
routineLviApplications.printNestedDictionary(interpSpKeyVarNames, interpSpHeader, interpSpDict, tableName)
