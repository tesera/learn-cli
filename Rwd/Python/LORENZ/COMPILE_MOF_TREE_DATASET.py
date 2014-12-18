'''
1. Note Check input files si_eqn_meth1 and si_eqn+meth2
    to ensure that no commas are included.

'''
import routineLviApplications

xvarSelHeader = ['TVID','VARNAME','XVARSEL']
xvarKeyVarName = ['TVID']
print '\n Enter source TREE file name without .csv extension, then press ENTER to continue.'
myTreeDataTableName = raw_input(" ... ")
readTreeErrorFileName = 'ERROR_' + myTreeDataTableName
nLines = 10000
oldTreeDict, newTreeDict = routineLviApplications.ReadStandardDataDictionary('TREEDICT')        #Get standard data dictionary
oldTreeDict = routineLviApplications.UpdateDataDictionaryWithNewTableName(oldTreeDict, 'TREE', myTreeDataTableName) #Assign ec=xiting data dictionary to new table name
newTreeDict = routineLviApplications.UpdateDataDictionaryWithNewTableName(newTreeDict, 'TREE', myTreeDataTableName) #Assign ec=xiting data dictionary to new table name
keyTreeVarNameList = ['SAMP_ID','plot_no','meas_no','tree_no']
treeHeader, treeDict = routineLviApplications.ReadCsvDataFileAndTransformIntoDictionaryFormat_v2(oldTreeDict, newTreeDict, myTreeDataTableName, readTreeErrorFileName, keyTreeVarNameList)
#
#print '\n Enter source PLOT file name without .csv extension, then press ENTER to continue.'
#myPlotDataTableName = raw_input(" ... ")
#readPlotErrorFileName = 'ERROR_' + myPlotDataTableName
#nLines = 10000
#oldPlotDict, newPlotDict = routineLviApplications.createNewDataDictionaryFromFile(myPlotDataTableName, 'YES', nLines)
#keyPlotVarNameList = ['SAMP_ID','meas_no']
#plotHeader, plotDict = routineLviApplications.ReadCsvDataFileAndTransformIntoDictionaryFormat_v2(oldPlotDict, newPlotDict, myPlotDataTableName, readPlotErrorFileName, keyPlotVarNameList)
#
keyLinkVarNameList = ['SAMP_ID','plot_no','meas_no']
linkHeader, linkKeyVarNamesList, linkDict = routineLviApplications.createUniqueIdLinkTable(keyLinkVarNameList, treeDict)
#Print key link table
tableName = 'PSPLINK'
routineLviApplications.printNestedDictionary(linkKeyVarNamesList, linkHeader, linkDict, tableName)
#Remove plots numbers equal to 0 from linkDict and update UID's
linkDict = routineLviApplications.removeMoFPspPlotNameBlankAndReestablishKeys(linkDict)
#Collapse treeDict keys to unique id from linkDict to represent each plot (plot numbers equal to 0 removed)
mismatchNotification = 'Yes'
treeDict = routineLviApplications.collapseDictKeysUsingLinkTableData(treeDict, linkDict, keyLinkVarNameList, mismatchNotification, myTreeDataTableName)
#Need also to get new header for tree Dict
newTreeKeyVarNameList = ['LINKID','tree_no']
newTreeHeader = routineLviApplications.removeItemsInOneDListBFromOneDListA(treeHeader, newTreeKeyVarNameList)
newTreeHeader = routineLviApplications.joinItemsInOneDListBExcludingThoseInOneDListCToOneDListA(newTreeKeyVarNameList, newTreeHeader, keyLinkVarNameList)
#Extract new treeDict with live trees only
treeDictColName = 'tree_cls'
treeAttrList = [1,2,5]
treeDict = routineLviApplications.SelectCertainTreeClassesForPSPTreeLists(treeDict, treeDictColName, treeAttrList)
#Compile species composition
spColNamesList = ['species']
spTableName = 'SPDICT'
dataDictType = 'TWOKEY'
spDictKeyList, spDictHeader, spDict, newSpList = routineLviApplications.GetSpeciesCodesFromFileOrAssigneNewSpeciesCodes(treeDict, spColNamesList, spTableName, dataDictType)
#Replace tree species in treeDict with new species
treeDict = routineLviApplications.ReplaceTreeSpeciesInPlotDataWithNewSpecies(treeDict,spDict, spColNamesList)
#Compile basal area and stems per hectare and volumes per hectare and percentages by species for each plot
spVarValuesNamesList = ['baha']
baphPlotKeyVarnameList, baphPlotHeader, baphPlotDict = routineLviApplications.CompilePerHectarePlotLevelStatisticsBySpeciesFromTreeLists(treeDict, spColNamesList, newSpList, spVarValuesNamesList)
baphSumPlotKeyVarnameList, baphSumPlotHeader, baphSumPlotDict = routineLviApplications.CompilePerHectarePlotLevelStatisticsFromTreeLists(treeDict, spVarValuesNamesList)
baphPcntDict = routineLviApplications.CompilePlotLevelSpeciesPercentages(baphPlotDict,newSpList)
#Compile global species data
attributeLabel = 'G'
plotSpHeader = []
plotSpDict = {}
plotSpHeader, plotSpDict = routineLviApplications.CompileSpeciesPlotStatisticsIntoOneDictionary(plotSpDict, baphPlotDict, plotSpHeader, baphPlotKeyVarnameList, \
                                                  newSpList, attributeLabel)
#Delete species baph Dictionary
del baphPlotDict
del baphPlotHeader

#Compile total plot statistics - baph
plotSumDict = {}
plotSumHeader = []
originalVarName = 'SUM'
newVarName = 'G'
plotSumHeader, plotSumDict = routineLviApplications.CombinePlotSumDictionariesIntoOne(plotSumDict, plotSumHeader, baphSumPlotDict, baphSumPlotKeyVarnameList, originalVarName, \
                                      newVarName)

#Add species percentages to global species data
attributeLabel = 'PCT'
plotSpHeader, plotSpDict = routineLviApplications.CompileSpeciesPlotStatisticsIntoOneDictionary(plotSpDict, baphPcntDict, plotSpHeader, baphPlotKeyVarnameList, \
                                                  newSpList, attributeLabel)
#Delete dictionary with species percentages
del baphPcntDict

#Compile species sph dictionary
spVarValuesNamesList = ['phf_tree']
sphPlotKeyVarnameList, sphPlotHeader, sphPlotDict = routineLviApplications.CompilePerHectarePlotLevelStatisticsBySpeciesFromTreeLists(treeDict, spColNamesList, newSpList, spVarValuesNamesList)
sphSumPlotKeyVarnameList, sphSumPlotHeader, sphSumPlotDict = routineLviApplications.CompilePerHectarePlotLevelStatisticsFromTreeLists(treeDict, spVarValuesNamesList)
#Add dictionary with stems per hectare by species to global species data
attributeLabel = 'N'
plotSpHeader, plotSpDict = routineLviApplications.CompileSpeciesPlotStatisticsIntoOneDictionary(plotSpDict, sphPlotDict, plotSpHeader, baphPlotKeyVarnameList, \
                                                  newSpList, attributeLabel)
#Delete sphPlotDict
del sphPlotDict
del sphPlotHeader

#Compile total plot statistics - sph
originalVarName = 'SUM'
newVarName = 'N'
plotSumHeader, plotSumDict = routineLviApplications.CombinePlotSumDictionariesIntoOne(plotSumDict, plotSumHeader, sphSumPlotDict, baphSumPlotKeyVarnameList, originalVarName, \
                                      newVarName)

#Compile species whole stem volume statistics
spVarValuesNamesList = ['wsvha']
wsvPlotKeyVarnameList, wsvPlotHeader, wsvPlotDict = routineLviApplications.CompilePerHectarePlotLevelStatisticsBySpeciesFromTreeLists(treeDict, spColNamesList, newSpList, spVarValuesNamesList)
wsvSumPlotKeyVarnameList, wsvSumPlotHeader, wsvSumPlotDict = routineLviApplications.CompilePerHectarePlotLevelStatisticsFromTreeLists(treeDict, spVarValuesNamesList)

#Add whole stem volume by species to global species dictionary
attributeLabel = 'WSV'
plotSpHeader, plotSpDict = routineLviApplications.CompileSpeciesPlotStatisticsIntoOneDictionary(plotSpDict, wsvPlotDict, plotSpHeader, baphPlotKeyVarnameList, \
                                                  newSpList, attributeLabel)
#Delete wsvPlotDict
del wsvPlotDict
del wsvPlotHeader

#Compile total plot statistics - wsvph
originalVarName = 'SUM'
newVarName = 'WSV'
plotSumHeader, plotSumDict = routineLviApplications.CombinePlotSumDictionariesIntoOne(plotSumDict, plotSumHeader, wsvSumPlotDict, wsvSumPlotKeyVarnameList, originalVarName, \
                                      newVarName)
#Delete total wsv dictionary
del wsvSumPlotDict
del wsvSumPlotHeader

#Print Global Species Statistics
#tableName = 'PSPSPSTAT'
#routineLviApplications.printNestedDictionary(baphPlotKeyVarnameList, plotSpHeader, plotSpDict, tableName)

#Lorey's mean tree heaight
#Compile quadratic mean tree diameters
qmdDictKeyVarnameList, qmdHeader, qmdDict = routineLviApplications.CompilePlotQuadraticMeanTreeDiameters(baphSumPlotDict, sphSumPlotDict)

#Compile total plot statistics - qmd
originalVarName = 'DG'
newVarName = 'DG'
plotSumHeader, plotSumDict = routineLviApplications.CombinePlotSumDictionariesIntoOne(plotSumDict, plotSumHeader, qmdDict, qmdDictKeyVarnameList, originalVarName, \
                                      newVarName)
#Lorenz Area and Index
dbhVarname = 'dbh'
sphVarname = 'phf_tree'
bphVarname = 'baha'
lorenzKeyVarnameList, lorenzHeader, lorenzDict = routineLviApplications.CompileLorenzStatistics(treeDict, dbhVarname, sphVarname, bphVarname)

#Compile total plot statistics - LORMAX
originalVarName = 'LORMAX'
newVarName = 'LORMAX'
plotSumHeader, plotSumDict = routineLviApplications.CombinePlotSumDictionariesIntoOne(plotSumDict, plotSumHeader, lorenzDict, lorenzKeyVarnameList, originalVarName, \
                                      newVarName)

originalVarName = 'LORAREA'
newVarName = 'LORAREA'
plotSumHeader, plotSumDict = routineLviApplications.CombinePlotSumDictionariesIntoOne(plotSumDict, plotSumHeader, lorenzDict, lorenzKeyVarnameList, originalVarName, \
                                      newVarName)

originalVarName = 'GINI'
newVarName = 'GINI'
plotSumHeader, plotSumDict = routineLviApplications.CombinePlotSumDictionariesIntoOne(plotSumDict, plotSumHeader, lorenzDict, lorenzKeyVarnameList, originalVarName, \
                                      newVarName)

originalVarName = 'NTPP'
newVarName = 'NTPP'
plotSumHeader, plotSumDict = routineLviApplications.CombinePlotSumDictionariesIntoOne(plotSumDict, plotSumHeader, lorenzDict, lorenzKeyVarnameList, originalVarName, \
                                      newVarName)

preTransformVarNameList = ['G','N', 'WSV','DG','LORMAX','LORAREA','GINI']
postTransformVarNameList = ['LNG','LNN','LNWSV','LNDG','LNLMAX','LNLAREA','LNGINI']
plotSumHeader, plotSumDict = routineLviApplications.ComputeNaturalLogarithMicTranformations(plotSumDict, plotSumHeader, preTransformVarNameList, postTransformVarNameList)

#Add the plotSpDict to the plotSumDict - innerJoin
plotSumHeader, plotSumDict = routineLviApplications.innerJoinTwoDictWithSameKeysDifferentVariables(plotSumDict, plotSumHeader, plotSpDict, plotSpHeader, baphPlotKeyVarnameList)

#Select plots that meet certain criteria
criteriaVarName = 'NTPP'    #Number of trees per plot
minCriteria = 10
maxCriteria = 100000000
plotSumDict, linkDict = routineLviApplications.RemovePlotsBelowMinimumAndAboveMaximumCriteria(plotSumDict, linkDict, criteriaVarName, minCriteria, maxCriteria)




#Print plotSumDict
tableName = 'PSPSUM'
routineLviApplications.printNestedDictionary(baphPlotKeyVarnameList, plotSumHeader, plotSumDict, tableName)

#Delete total qmd dictionary
del qmdDict
del qmdHeader
#Delete total sph dictionary
del sphSumPlotDict
del sphSumPlotHeader
#Delete total baph dictionary
del baphSumPlotDict
del baphSumPlotHeader
#Species / Site heights / ages/ site index / site_index method by species


#Cumulative Distributions in Stems Per Hectare
xVarName = 'dbh'
minXVar = 4
maxXVar = 140
yVarName = 'phf_tree'
yVarNameNew = 'N'
cumDistDict = {}
cumDistKeyVarnameList = ['PLOTID']
cumDistHeader = ['PLOTID']
cumDistHeader, cumDistDict = routineLviApplications.CompileCumulativeDistributions(xVarName, minXVar, maxXVar, yVarName, yVarNameNew, \
                                   treeDict, cumDistDict, cumDistHeader)

#Cumulative Distributions in basal area
yVarName = 'baha'
yVarNameNew = 'G'
cumDistHeader, cumDistDict = routineLviApplications.CompileCumulativeDistributions(xVarName, minXVar, maxXVar, yVarName, yVarNameNew, \
                                   treeDict, cumDistDict, cumDistHeader)

#Select cumulative distributions for plots remaining in linkDict
cumDistDict = routineLviApplications.SelectCumulativeDistributionsUsingLinkDict(cumDistDict, linkDict, linkKeyVarNamesList)

#Print cumDistDict
tableName = 'CDISTR'
routineLviApplications.printNestedDictionary(cumDistKeyVarnameList, cumDistHeader, cumDistDict, tableName)



#Gini Coefficient

