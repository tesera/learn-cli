'''
'''
import routineLviApplications
dataTableName = 'TOLKOLORTREE'
printTypes = 'YES'
oldDict, newDict = routineLviApplications.createNewDataDictionaryFromFile(dataTableName, printTypes, nLines = 1000)
readErrorFileName = 'ERROR_TOLKOLORENZ'
#keyTreeVarNameList = ['PLOTID', 'TREEID']
keyTreeVarNameList = ['NPLOTID', 'TREEID']
treeHeader, treeDict = routineLviApplications.ReadCsvDataFileAndTransformIntoDictionaryFormat_v2(oldDict, newDict, dataTableName, readErrorFileName, keyTreeVarNameList)
minDbhThreshold = 0
treeDictColName = 'DBH'
treeDict = routineLviApplications.SelectTreesAboveMinimumThrehsold(treeDict, treeDictColName, minDbhThreshold)

treeDbhName = 'DBH'
treeSphName = 'TPH'
treeSpeciesName = 'SPECIES'
treeRDbhName = 'RDBH'
treeBphName = 'BPH'
minDbhThreshold = 0
#Compile new tree dictionary
treeDict, treeDictHeader, minRDbh, maxRDbh = routineLviApplications.CompileNewTreeDictToDbhThreshold(treeDict, keyTreeVarNameList, treeSpeciesName, treeDbhName, \
                                     treeSphName, treeRDbhName, treeBphName,  \
                                     minDbhThreshold)

#Compile species composition
spColNamesList = ['SPECIES']
spTableName = 'SPDICT'
dataDictType = 'TWOKEY'
spDictKeyList, spDictHeader, spDict, newSpList = routineLviApplications.GetSpeciesCodesFromFileOrAssigneNewSpeciesCodes(treeDict, spColNamesList, spTableName, dataDictType)
#Replace tree species in treeDict with new species
treeDict = routineLviApplications.ReplaceTreeSpeciesInPlotDataWithNewSpecies(treeDict,spDict, spColNamesList)
#for tree in treeDict[32]:
#    print tree, treeDict[32][tree]['DBH']

#Compile basal area and stems per hectare and volumes per hectare and percentages by species for each plot
spVarValuesNamesList = ['BPH']
baphPlotKeyVarnameList, baphPlotHeader, baphPlotDict = routineLviApplications.CompilePerHectarePlotLevelStatisticsBySpeciesFromTreeLists(treeDict, spColNamesList, newSpList, spVarValuesNamesList)
baphSumPlotKeyVarnameList, baphSumPlotHeader, baphSumPlotDict = routineLviApplications.CompilePerHectarePlotLevelStatisticsFromTreeLists(treeDict, spVarValuesNamesList)
baphPcntDict = routineLviApplications.CompilePlotLevelSpeciesPercentages(baphPlotDict,newSpList)

#Compile species dominance dictionary using baphPcntDict
spDomKeyVarList,spDomHeader,spDomDict = routineLviApplications.compileSpeciesDominance(baphPcntDict, newSpList)

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
plotSumHeader = []
plotSumDict = {}
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
spVarValuesNamesList = ['TPH']
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
#Lorey's mean tree heaight
#Compile quadratic mean tree diameters
qmdDictKeyVarnameList, qmdHeader, qmdDict = routineLviApplications.CompilePlotQuadraticMeanTreeDiameters(baphSumPlotDict, sphSumPlotDict)

#Compile total plot statistics - qmd
originalVarName = 'DG'
newVarName = 'DG'
plotSumHeader, plotSumDict = routineLviApplications.CombinePlotSumDictionariesIntoOne(plotSumDict, plotSumHeader, qmdDict, qmdDictKeyVarnameList, originalVarName, \
                                      newVarName)
#Lorenz Area and Index
dbhVarname = 'DBH'
sphVarname = 'TPH'
bphVarname = 'BPH'
dbhInterval = 1
maxDbh = 140

lorenzKeyVarnameList, lorenzHeader, lorenzDict, lorenzCurveHeader, lorenzCurveDict = routineLviApplications.CompileLorenzStatistics(treeDict, \
                                                                        dbhVarname, sphVarname, bphVarname, dbhInterval, maxDbh)

#Print Lorenz Distributions
tableName = 'LCDISTR'
routineLviApplications.printNestedDictionary(lorenzKeyVarnameList, lorenzCurveHeader, lorenzCurveDict, tableName)

#Calculate STVI
stviKeyVarnameList, stviHeader, stviDict = routineLviApplications.calculateUnivariateSTVI(treeDict, dbhVarname, sphVarname, bphVarname, maxDbh)

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

originalVarName = 'CDI'
newVarName = 'CDI'
plotSumHeader, plotSumDict = routineLviApplications.CombinePlotSumDictionariesIntoOne(plotSumDict, plotSumHeader, lorenzDict, lorenzKeyVarnameList, originalVarName, \
                                      newVarName)

originalVarName = 'STVI'
newVarName = 'STVI'
plotSumHeader, plotSumDict = routineLviApplications.CombinePlotSumDictionariesIntoOne(plotSumDict, plotSumHeader, stviDict, stviKeyVarnameList, originalVarName, \
                                      newVarName)

preTransformVarNameList = ['G','N','DG','LORMAX','LORAREA','CDI','GINI']
postTransformVarNameList = ['LNG','LNN','LNDG','LNLMAX','LNLAREA','LNCDI','LNGINI']
plotSumHeader, plotSumDict = routineLviApplications.ComputeNaturalLogarithMicTranformations(plotSumDict, plotSumHeader, preTransformVarNameList, postTransformVarNameList)

#Add the plotSpDict to the plotSumDict - innerJoin
plotSumHeader, plotSumDict = routineLviApplications.innerJoinTwoDictWithSameKeysDifferentVariables(plotSumDict, plotSumHeader, plotSpDict, plotSpHeader, baphPlotKeyVarnameList)

#Add Species Dominance Dictionary to plotSumDict
plotSumHeader, plotSumDict = routineLviApplications.innerJoinTwoDictWithSameKeysDifferentVariables(plotSumDict, plotSumHeader, spDomDict, spDomHeader, spDomKeyVarList)

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
#delete species dominance dictionary
del spDomDict
del spDomHeader


#Cumulative Level 2 Distributions in Stems Per Hectare
xVarName = 'DBH'
minXVar = 0
maxXVar = 140
yVarName = 'TPH'
yVarNameNew = 'N'
cumDistDict = {}
#cumDistKeyVarnameList = ['PLOTID']
#cumDistHeader = ['PLOTID']
cumDistKeyVarnameList = ['NPLOTID']
cumDistHeader = ['NPLOTID']
cumDistHeader, cumDistDict = routineLviApplications.CompileCumulativeDistributions(xVarName, minXVar, maxXVar, yVarName, yVarNameNew, \
                                   treeDict, cumDistDict, cumDistHeader)

#Cumulative Level 2 Distributions in basal area using DBH
yVarName = 'BPH'
yVarNameNew = 'G'
cumDistHeader, cumDistDict = routineLviApplications.CompileCumulativeDistributions(xVarName, minXVar, maxXVar, yVarName, yVarNameNew, \
                                   treeDict, cumDistDict, cumDistHeader)

#Print cumDistDict
tableName = 'CDISTR'
routineLviApplications.printNestedDictionary(cumDistKeyVarnameList, cumDistHeader, cumDistDict, tableName)

##############################################################################################
# Produce Rank adjusted cumulative distributions
#Assign a proportional rank for N and G to each plot id

rankVarName = 'G'
rankDict = {}
rankHeader = []
rankKeyVarNameList = ['RVARNAME', 'RVARVALUE']
rankKeyVarNameList, rankHeader, rankDict = routineLviApplications.compileAttributeRanks(plotSumDict, rankVarName, rankDict, rankHeader, rankKeyVarNameList)
rankVarName = 'N'
rankKeyVarNameList, rankHeader, rankDict = routineLviApplications.compileAttributeRanks(plotSumDict, rankVarName, rankDict, rankHeader, rankKeyVarNameList)
rankTableName = 'RANKGN'
routineLviApplications.printNestedDictionary(rankKeyVarNameList, rankHeader, rankDict, rankTableName)

#Cumpute rank adjusted cumulative distributions
adjCumDistDict = {}
adjCumDistHeader = ['NPLOTID']
adjCumDistHeader, adjCumDistDict = routineLviApplications.rankAdjustCumulativeDistributions(plotSumDict, rankDict, cumDistDict, minXVar, maxXVar, adjCumDistDict, adjCumDistHeader)
#Print adjusted cumulative distributions
tableName = 'ACDISTR'
routineLviApplications.printNestedDictionary(cumDistKeyVarnameList, adjCumDistHeader, adjCumDistDict, tableName)

#Update tree disctionary with relatative tree dbh equal to tree dbh minus qmd
treeDbhName = 'DBH'
treeSphName = 'TPH'


#Create cumulative level 3 distributions using RDBH
xVarName = 'RDBH'
minXVar = minRDbh
maxXVar = maxRDbh +1
yVarName = 'TPH'
yVarNameNew = 'N'
cumDistDict = {}
#cumDistKeyVarnameList = ['PLOTID']
#cumDistHeader = ['PLOTID']
cumDistKeyVarnameList = ['NPLOTID']
cumDistHeader = ['NPLOTID']
cumDistHeader, cumDistDict = routineLviApplications.CompileCumulativeDistributions(xVarName, minXVar, maxXVar, yVarName, yVarNameNew, \
                                   treeDict, cumDistDict, cumDistHeader)

#Cumulative Level 3 Distributions in basal area
yVarName = 'BPH'
yVarNameNew = 'G'
cumDistHeader, cumDistDict = routineLviApplications.CompileCumulativeDistributions(xVarName, minXVar, maxXVar, yVarName, yVarNameNew, \
                                   treeDict, cumDistDict, cumDistHeader)

#Print cumDistDict
tableName = 'RCDISTR'
routineLviApplications.printNestedDictionary(cumDistKeyVarnameList, cumDistHeader, cumDistDict, tableName)
