'''
'''
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

#Check Species List
#Note species that are identified as blank are left blank
spColNamesList = ['IGB_SP1', 'IGB_SP2', 'IGB_SP3', 'IGB_SP4', 'IGB_SP5', 'IGB_USP1', 'IGB_USP2','IGB_USP3','IGB_USP4','IGB_USP5']
spTableName = 'SPDICT'
dataDictType = 'ONEKEY'
spDictKeyList, spDictHeader, spDict, newSpList = routineLviApplications.GetSpeciesCodesFromFileOrAssigneNewSpeciesCodes(photoDict, spColNamesList, spTableName, dataDictType)
#Replace tree species in treeDict with new species
photoDict = routineLviApplications.ReplaceTreeSpeciesInOneKeyDataWithNewSpecies(photoDict,spDict, spColNamesList)

#Extract records with complete non empty tree overstory data
#Remove any plots with blank leading species
speciesCols = ['IGB_SP1']
removeVarValuesList = ['']
print 'total number of photoplots', len(photoDict.keys())
photoDict = routineLviApplications.removeRecordsFromDictWithSpecifiedValues(photoDict, speciesCols, \
                                                                            removeVarValuesList, photoKeyVarNameList) 
print 'length after blank leading species removed', len(photoDict.keys())
heightCol = 'IGB_HEIGHT'
removeVarValuesList = [0,'']
photoDict = routineLviApplications.removeRecordsFromDictWithSpecifiedValues(photoDict, heightCol, \
                                                                            removeVarValuesList, photoKeyVarNameList)
print 'length after null heights removed',len(photoDict.keys())
originCol = 'IGB_ORIGIN'
removeVarValuesList = [0,'']
photoDict = routineLviApplications.removeRecordsFromDictWithSpecifiedValues(photoDict, originCol, \
                                                                            removeVarValuesList, photoKeyVarNameList) 

print 'length after null origin removed',len(photoDict.keys())

inventoryDate = 2011
#Extract new dataset with the same key variable names and only the desired remaining variable names out of the entire set
varNameSubset = ['NPLOTID','IGB_SP1','IGB_SP1_PER','IGB_SITE_INDEX','IGB_HEIGHT','IGB_ORIGIN','IGB_TPR', 'IGB_INITIALS']
siKeyVarNamesList, siHeader, siDict = routineLviApplications.extractNewDictVariableSubset(photoDict, photoKeyVarNameList, varNameSubset)
#Calculate stand age from inventory date and year of origin
originVarName = 'IGB_ORIGIN'
invYearVarName = 'IGB_INV_YEAR'
inventoryYear = 2011
ageVarName = 'IGB_TAGE'
siHeader, siDict = routineLviApplications.calculateStandAgeFromDateOfOrigin(siDict, siHeader, originVarName, invYearVarName, inventoryYear, ageVarName)

#Write photo plot sidata input file
tableName = 'SIPHOTOIN'
routineLviApplications.printNestedDictionary(siKeyVarNamesList, siHeader, siDict, tableName)


#Calculate AVI site index
speciesCol = 'IGB_SP1'
bhageCol = 'NULL'
totalAgeCol = 'IGB_TAGE'
treeHeightCol = 'IGB_HEIGHT'
siAviDictKeyVarNameList, siAviDictHeader, siAviDict = routineLviApplications.CompileAviSiteIndices(siDict, speciesCol, bhageCol, \
                                                                                           totalAgeCol, treeHeightCol)
spVarName = 'SPECIES'
siVarName = 'SI'
siAviDictHeader, siAviDict = routineLviApplications.compileAlbertaTimberProductivityRating(siAviDict, siAviDictHeader, spVarName, siVarName)
tableName = 'SI_AVI_GPHOTO'
routineLviApplications.printNestedDictionary(siAviDictKeyVarNameList, siAviDictHeader, siAviDict, tableName)
#Write to file

