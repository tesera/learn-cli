'''
'''
import routineLviApplications

#interactiveMode = 'YES'
interactiveMode = 'NO'

#Get Species Report
#Notify user as to location of data dictionary for new dataset

if interactiveMode == 'YES':
    print ' A new standard data dictionary for new dataset \n identifying variable names and data types \n should be located in the: \\Rwd\\Python\\DATDICT\\ file path'
    raw_input(" Press ENTER to continue ... ")
    #Ask user to input name of data dictionary without .csv extension and then read data dictionary
    myDataDict = raw_input("\n Input name of DICTIONARY without .csv extension\n and press ENTER to continue ... ")
    raw_input("\n The .csv DATA file should be in the top of the \\Rwd\\ directory\n press ENTER to continue ... ")
    newDataFileName = raw_input("\n Input name of DATA file without .csv extension\n and press ENTER to continue ... ")
    keyVarNameList = raw_input("\n Input list of the KEY VARIABLE NAMES (NEWVARNAME in DICTIONARY)\n in square parenthesis, [], in the order that they occur separated by commas\n and press ENTER to continue ... ")
    print '\n If there are errors in the data dictionary regarding declaration\n of data types then these will be printed to the\n \\Rwd\\Pthon\\PyReadError\\ERROR-CHECK-RSP.csv file'
else:
    myDataDict = 'LVIDICT'
    originalDict, newDict = routineLviApplications.ReadLviDataDictionary(myDataDict)
    #Get name of the file containing the actual data
    newDataTableName = 'DCS_ATT_SPECTRAL'
    readErrorFileName = 'ERROR-CHECK-RSP'
    keyVarNameList = ['VRI_FCOID']
    varSelHeader, varSelTypedDict = routineLviApplications.ReadCsvDataFileAndTransformIntoDictionaryFormat_v2(originalDict, newDict, newDataTableName, \
                                                                                      readErrorFileName, keyVarNameList)
