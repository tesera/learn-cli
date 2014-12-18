'''
This routine convers a .dbf file to a . csv file.
1. The user enters the dbf file name in the Rwd directory without the .dbf file extension.
2. A new csv file is created in the Rwd directory called TAREGETDATA.csv.
3. A data dictionary is also created for the TARGETDATA file called TARGETDICT.csv.
4. When processing is complete the user must manually update the NEWVARNAME field in the TARGETDICT
    to ensure that the NEWVARNAMES in the target dataset match with those in LVINEW. 
'''
import routineLviApplications

print ' If the dbf file is not in the top of the Rwd directory please put it there now.'
print raw_input(" Press ENTER to continue ... ")
dbfFileName = raw_input("\n Enter the dbf fileName without the .dbf extension then press ENTER ... ")
printLine = " The dbf filename:" + dbfFileName + '.dbf' + " will be converted to a .csv file. Press ENTER ... "
newCsvFileName = 'TARGETDBF'
#newCsvFileName = raw_input("\n Enter the new csv data fileName without the .csv extension then press ENTER ... ")
printLine = " The new csv filename: TARGETDBF.csv will be printed to the Rwd directory. Press ENTER ... "
raw_input(printLine)
newDataDictFileName = 'TARGETDBFDICT'
printLine = " The new csv data dictionary filename: TARGETDBFDICT.csv will be printed to the Rwd directory. Press ENTER ... "
raw_input(printLine)
routineLviApplications.convertDbfFileToCsvFile(dbfFileName, newCsvFileName, newDataDictFileName)
raw_input(" File conversion complete. Press ENTER to continue ... ")
raw_input(" Manually Assign NEWVARNAME in TARGETDATA.csv to ensure match with Reference Dataset, LVINEW. Press ENTER ... ")
raw_input(" Press ENTER to exit program ... ")          
