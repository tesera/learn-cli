#Make variable names accessible during session
#load  a csv text file, named lvinew
#wellFileName <- "D:\\Rwd\\Rdata\\WELLS\\welldatatable.txt"		#Enter file name and address for lvi dataset 
wellFileName <- "D:\\Rwd\\Rdata\\WELLS\\IrisDatacsvnospace.txt"
wells <- read.csv(wellFileName,header=T,row.names=1)			#Read file and put in R dataframe lvinew
attach(wells)									#Attach variable names to each of the columns
wellsVarNames <- names(wells)							#Print variable names in interpreter
nWellsRows <- length(wells[,1])						#Count the number of rows or observations (for use in extracting variable subsets)