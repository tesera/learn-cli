import routineLviApplications

#Create data dictionary from data table
dataTableName = 'SITREE'
printTypes = 'YES'
nLines = 10000
oldDict, newDict = routineLviApplications.createNewDataDictionaryFromFile(dataTableName, printTypes, nLines)
#Convert dataTableToDataDictionary
readErrorFileName = 'ERROR_' + dataTableName
keyVarNameList = ['SITREEID']
treeHeader, treeDict = routineLviApplications.ReadCsvDataFileAndTransformIntoDictionaryFormat_v2(oldDict, newDict, dataTableName, readErrorFileName, keyVarNameList)
#Check species
spColNamesList = ['SPECIES']
spTableName = 'SPDICT'
dataDictType = 'ONEKEY'
spKeyNameList, spHeader, spDict, newSpList = routineLviApplications.GetSpeciesCodesFromFileOrAssigneNewSpeciesCodes(treeDict, spColNamesList, spTableName, dataDictType)
#Update species names in tree dictionary if desired
treeDict = routineLviApplications.ReplaceTreeSpeciesInOneKeyDataWithNewSpecies(treeDict, spDict, spColNamesList)
#Get AVI Inventory site indices
speciesCol = 'SPECIES'
bhageCol = 'AGE'
totalAgeCol = 'NULL'
treeHeightCol = 'HT_MEAS'
treeMeasDateCol = 'MEASDATE'
measDateFormat = 'dd/mm/yyyy'
siDictKeyVarNameList, siDictHeader, siDict = routineLviApplications.CompileAviSiteIndices(treeDict,speciesCol,bhageCol,totalAgeCol,treeHeightCol, \
                                                                                          treeMeasDateCol, measDateFormat)

siDictHeader, siDict = routineLviApplications.compileAlbertaTimberProductivityRating(siDict, siDictHeader, 'SPECIES','SI')

#Project tree heights to inventory date
totalAgeColName = 'TAGE'
bhAgeColName = 'BHAGE'
treeHeightColName = 'HT'
siColName = 'SI'
monthColName = 'MONTH'
yearColumnName = 'YEAR'
projectionYear = 2011       #Same as inventory year in this case
#siteIndexEqType = 'AVI'
#siDictHeader, siDict = routineLviApplications.ProjectHeightAndAgeGivenSiteIndices(siDict,siDictHeader,  \
#                                        speciesCol, \
#                                        bhAgeColName, totalAgeColName, treeHeightColName, \
#                                        siColName, monthColName, yearColumnName, \
#                                        projectionYear, siteIndexEqType)
#Write AVI inventory species to file
tableName = 'AVI_SI'
routineLviApplications.printNestedDictionary(siDictKeyVarNameList, siDictHeader, siDict, tableName)
#Get GYPSY site indices
totalAgeCol = 'NULL'
siDictKeyVarNameList, siDictHeader, siDict = routineLviApplications.CompileGypsySiteIndices(treeDict,speciesCol,bhageCol,totalAgeCol,treeHeightCol, \
                                                                                          treeMeasDateCol, measDateFormat)
siteIndexEqType = 'GYPSY'
siDictHeader, siDict = routineLviApplications.ProjectHeightAndAgeGivenSiteIndices(siDict,siDictHeader,  \
                                        speciesCol, \
                                        bhAgeColName, totalAgeColName, treeHeightColName, \
                                        siColName, monthColName, yearColumnName, \
                                        projectionYear, siteIndexEqType)

siDictHeader, siDict = routineLviApplications.compileAlbertaTimberProductivityRating(siDict, siDictHeader, 'SPECIES','SI')

#Write GYPSY site indices to file
tableName = 'GYPSY_SI'
routineLviApplications.printNestedDictionary(siDictKeyVarNameList, siDictHeader, siDict, tableName)
