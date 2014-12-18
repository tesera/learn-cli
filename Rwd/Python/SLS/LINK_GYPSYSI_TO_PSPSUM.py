'''
'''
import routineLviApplications

#Create data dictionary from PSPSUM data table and read PSPSUM
dataTableName = 'PSPSUM'
printTypes = 'YES'
nLines = 10000
oldDict, newDict = routineLviApplications.createNewDataDictionaryFromFile(dataTableName, printTypes, nLines)
readErrorFileName = 'ERROR_PSPSUM'
pspKeyVarNameList = ['PLOTID']         #Same as 'MEASPLOTID'
pspHeader, pspDict = routineLviApplications.ReadCsvDataFileAndTransformIntoDictionaryFormat_v2(oldDict, newDict, dataTableName, readErrorFileName, pspKeyVarNameList)
#Get MEASPLOTID Cross References to NPLOTID and SITREEIDs
dataTableName = 'IDXREF'
printTypes = 'YES'
nLines = 10000
oldDict, newDict = routineLviApplications.createNewDataDictionaryFromFile(dataTableName, printTypes, nLines)
readErrorFileName = 'ERROR_IDXREF'
idKeyTreeVarNameList = ['MEASPLOTID','NPLOTID','SITREEID']         
idXrefHeader, idXrefDict = routineLviApplications.ReadCsvDataFileAndTransformIntoDictionaryFormat_v2(oldDict, newDict, dataTableName, readErrorFileName, idKeyTreeVarNameList)
idXrefMeasPlotIdList = idXrefDict.keys()
idXrefMeasPlotIdList.sort()
#Get GYPSY_SI
dataTableName = 'GYPSY_SI'
printTypes = 'YES'
nLines = 10000
oldDict, newDict = routineLviApplications.createNewDataDictionaryFromFile(dataTableName, printTypes, nLines)
readErrorFileName = 'ERROR_GYPSY_SI'
keyTreeVarNameList = ['SIID']         
siHeader, siDict = routineLviApplications.ReadCsvDataFileAndTransformIntoDictionaryFormat_v2(oldDict, newDict, dataTableName, readErrorFileName, keyTreeVarNameList)
#Compile species composition
spColNamesList = ['SP1','SP2']
spTableName = 'SPDICT'
dataDictType = 'ONEKEY'
spDictKeyList, spDictHeader, spDict, newSpList = routineLviApplications.GetSpeciesCodesFromFileOrAssigneNewSpeciesCodes(pspDict, spColNamesList, spTableName, dataDictType)
pspDict = routineLviApplications.ReplaceTreeSpeciesInOneKeyDataWithNewSpecies(pspDict, spDict, spColNamesList, dataDictType)
spColNamesList = ['SPECIES']
spDictKeyList, spDictHeader, spDict, newSpList = routineLviApplications.GetSpeciesCodesFromFileOrAssigneNewSpeciesCodes(siDict, spColNamesList, spTableName, dataDictType)
siDict = routineLviApplications.ReplaceTreeSpeciesInOneKeyDataWithNewSpecies(siDict, spDict, spColNamesList, dataDictType)
#Replace tree species in treeDict with new species


#
pspKeyValueList = pspDict.keys()
pspKeyValueList.sort()
newVarNameList = ['NPLOTID','SIID1','SISP1','SI1','PTAGE1','PHT1','PYEAR1','SIID1','SISP2','SI2','PTAGE2','PHT2','PYEAR2','SIID2']
newPspHeader = routineLviApplications.joinOneDListBToRightOfOneDListA(pspHeader, newVarNameList)
for measPlotId in pspKeyValueList:
    pspSpecies1 = pspDict[measPlotId]['SP1']
    pspSpecies2 = pspDict[measPlotId]['SP2']
    nplotid = 0
    siid1 = 0
    siid1List = []
    sisp1 = 'NA'
    si1 = 0
    ptage1 = 0
    pht1 = 0
    pyear1 = 0
    siid2 = 0
    siid2List = []
    sisp2 = 'NA'
    si2 = 0
    ptage2 = 0
    pht2 = 0
    pyear2 = 0
    if measPlotId in idXrefMeasPlotIdList:
        if not measPlotId == 0:
            nplotidList = idXrefDict[measPlotId].keys()
            nplotid = nplotidList[0]    #There is only one unique nplotid associated with each measPlotId
            siTreeIdList = idXrefDict[measPlotId][nplotid].keys()
            siTreeIdList.sort()
            for siTreeId in siTreeIdList:
                if siTreeId in siDict:
                    sisp = siDict[siTreeId]['SPECIES']
                    if sisp == pspSpecies1:
                        siid1List.append(siTreeId)
                    if sisp == pspSpecies2:
                        siid2List.append(siTreeId)
            siid1Count = len(siid1List)
            if siid1Count == 1:
                siid1 = siid1List[0]
            else:
                if siid1Count > 1:              
                    maxYear = 0
                    for siid in siid1List:
                        year = siDict[siid]['YEAR']
                        if year > maxYear:
                            maxYear = year
                            siid1 = siid
            siid2Count = len(siid2List)
            if siid2Count == 1:
                siid2 = siid2List[0]
            else:
                if siid2Count > 1:              
                    maxYear = 0
                    for siid in siid2List:
                        year = siDict[siid]['YEAR']
                        if year > maxYear:
                            maxYear = year
                            siid1 = siid
            if siid1 > 0:
                sisp1 = siDict[siid1]['SPECIES']
                ptage1 = siDict[siid1]['PTAGE']
                pht1 = siDict[siid1]['PHT']
                pyear1 = siDict[siid1]['PYEAR']
                si1 = siDict[siid1]['SI']
            if siid2 > 0:
                sisp2 = siDict[siid2]['SPECIES']
                ptage2 = siDict[siid2]['PTAGE']
                pht2 = siDict[siid2]['PHT']
                pyear2 = siDict[siid2]['PYEAR']
                si2 = siDict[siid2]['SI']
    pspDict[measPlotId].update({'NPLOTID':nplotid,'SIID1':siid1,'SISP1':sisp1,'SI1':si1,'PTAGE1':ptage1,'PHT1':pht1,'PYEAR1':pyear1,\
                                'SIID2':siid2,'SISP2':sisp2,'SI2':si2,'PTAGE2':ptage2,'PHT2':pht2,'PYEAR2':pyear2})
    
tableName = 'PSPSUMSI'
routineLviApplications.printNestedDictionary(pspKeyVarNameList, newPspHeader, pspDict, tableName)
            
