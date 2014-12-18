#Select X-variable data subset from original file
#load  a csv text file, named VARSELXNEW.csv to select X-variables
fileName <- "XVARSELV2.csv"	#Set file name for variable selection input
xVarSel <- read.csv(fileName,header=T,row.names=1,stringsAsFactors=FALSE, 
	strip.white=TRUE, na.strings = c("NA",""))
#
attach(xVarSel)				#Make variable names accessible during session by attaching the variable names
nRows <- length(xVarSel[,1])		#Get the number of rows or X-variables in xVarSel
varNameList <- names(xVarSel)		#Get potential list of xVariables
nCols <- length(varNameList)		#Get number of columns in data frame
DUMMY <- rep(0,nIbcRows)		#Create a DUMMY vector of zeros of length 1 (initial) dataset dataset

#Get the list of elgible x variables and select the variables from the datafile 
#and put them in a vector, each vector to be analyzed in turn
for (i in 1:nRows) {
	xDataset <- data.frame(DUMMY)						#Start a new xDataset
	for (j in 4:nCols) {
		#print (xVarSel[i,j])
		if (!(xVarSel[i,j] == "N"))	{				#If not xVarSel[i,j] == "N"
			xDataset[,xVarSel[i,j]] <- get(xVarSel[i,j])	#Add the variable of name xVarSel[i,j] to the xDataset
			}
		}
	xDataset$DUMMY <- NULL							#Remove the DUMMY variable
	#print(i)									#Use this to check that the right number of varibale sets are being produced	
	#print(names(xDataset))							#Use this to check that each set of variables is being correctly compiled into xDataset 
	}	