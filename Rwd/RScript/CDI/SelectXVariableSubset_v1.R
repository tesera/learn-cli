#Select X-variable data subset from original file
#load  a csv text file, named XVARSELV1.txt to select X-variables
fileName <- "D:\\Rwd\\XVARSELV1.csv"	#Set file name for variable selection input
xVarSel <- read.csv(fileName,header=T,row.names=1, stringsAsFactors=FALSE, 
	strip.white=TRUE, na.strings = c("NA",""))
#
attach(xVarSel)				#Make variable names accessible during session by attaching the variable names
nRows <- length(xVarSel[,1])		#Get the number of rows or X-variables in xVarSel
varNameList <- xVarSel[,1]		#Get potential list of xVariables
DUMMY <- rep(0,nCdiRows)		#Create a DUMMY vector of zeros the same length as the lvi (initial) dataset dataset
xDataset <- data.frame(DUMMY)		#Initialize a new dataframe using the DUMMY variable to establish the correct number of rows
#
#Get the list of elgible x and y variables and put them in a vector
for (i in 1:nRows) {
	if (xVarSel[i,2]== "X")
	xDataset[,varNameList[i]] <- get(varNameList[[i]])
	}
#
xDataset$DUMMY <- NULL			#Delete the initial DUMMY variable from the dataframe
xNames <- names(xDataset)		#Create a vector of xDataset names


