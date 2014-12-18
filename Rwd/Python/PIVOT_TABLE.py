'''
'''
import routineLviApplications

#interactiveMode = 'YES'
interactiveMode = 'NO'

print "\n The demo TNNSTATS filename is 'TNNSTATS64'"
nnTargetTableNo = input("\n Input the TNNSTATS file no, e.g. '64' without the '', the press ENTER ... ")
myDataTableName = 'TNNSTATS'
myDataTableName = myDataTableName + str(nnTargetTableNo)

readErrorFileName = 'ERROR_TNNSTATS'
keyRowVarNameList = ['TARGOBS','KNN']   #The columns that contain combinations of values that uniquely describe each row
keyColVarName = 'VARNAME'               #The column that contains the names of variables to represented as columns in a new table (nominal variable)
varSelName = 'MEAN'                     #The column containing the values to be assigned to each of the keyColVarNames
nTargObs = 1000                         #The number of target observations to processed before printing

#Create dictionary    
oldDict, newDict = routineLviApplications.createNewDataDictionaryFromFile(myDataTableName, 'YES', 1000)

print '\n Start compiling and printing MEAN pivot table.'
#Print MEAN Pivot Table
colNamesList = routineLviApplications.createPivotTable(myDataTableName, oldDict, keyRowVarNameList, keyColVarName, varSelName, nTargObs, nnTargetTableNo) 
#Note that this needs to be done using text file only must check for keys to ensure that an entire observation is processed

print '\n Start compiling and print SDEV pivot table.'
#Print SDEV Pivot Table
varSelName = 'SDEV'
colNamesList = routineLviApplications.createPivotTable(myDataTableName, oldDict, keyRowVarNameList, keyColVarName, varSelName, nTargObs, nnTargetTableNo)

print raw_input("\n Press ENTER to end this session ... ")
