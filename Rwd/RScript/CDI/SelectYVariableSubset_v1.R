#Select X-variable data subset from original file
#load  a csv text file, named XVARSELV1.csv to select Y-variables
fileName <- "D:\\Rwd\\XVARSELV1.csv"	#Set file name for variable selection input
yVarSel <- read.csv(fileName,header=T,row.names=1, stringsAsFactors=FALSE, 
	strip.white=TRUE, na.strings = c("NA",""))
#
attach(yVarSel)				#Make variable names accessible during session by attaching the variable names
nRows <- length(yVarSel[,1])		#Get the number of rows or X-variables in xVarSel
varNameList <- yVarSel[,1]		#Get potential list of xVariables
DUMMY <- rep(0,nCdiRows)		#Create a DUMMY vector of zeros the same length as the lvi (initial) dataset dataset
yDataset <- data.frame(DUMMY)		#Initialize a new dataframe using the DUMMY variable to establish the correct number of rows
#
#Get the list of elgible x and y variables and put them in a vector
for (i in 1:nRows) {
	if (yVarSel[i,2]== "Y")
	yDataset[,varNameList[i]] <- get(varNameList[[i]])
	}
#
yDataset$DUMMY <- NULL			#Delete the initial DUMMY variable from the dataframe
yNames <- names(yDataset)		#Create a vector of xDataset names


