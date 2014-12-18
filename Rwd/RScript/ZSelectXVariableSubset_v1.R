xVarSel <- read.csv(xVarSelectFileName,header=T,row.names=1, stringsAsFactors=FALSE, 
	strip.white=TRUE, na.strings = c("NA",""))
#
attach(xVarSel)				#Make variable names accessible during session by attaching the variable names
nRows <- length(xVarSel[,1])		#Get the number of rows or X-variables in xVarSel
varNameList <- xVarSel[,1]		#Get potential list of xVariables
DUMMY <- rep(0,nLviRows)		#Create a DUMMY vector of zeros the same length as the lvi (initial) dataset dataset
xDataset <- data.frame(DUMMY)		#Initialize a new dataframe using the DUMMY variable to establish the correct number of rows
#
#Get the list of elgible x and y variables and put them in a vector
for (i in 1:nRows) {
	if (xVarSel[i,2]== xVarSelectCriteria)
	xDataset[,varNameList[i]] <- lvinew[varNameList[i]]
	}
#
xDataset$DUMMY <- NULL			#Delete the initial DUMMY variable from the dataframe
xNames <- names(xDataset)		#Create a vector of xDataset names
xVarCount = length(xDataset)
cat(" A new data frame, xDataset, has been created\n") 
cat(" The following number of variables have been selected: ", xVarCount)
