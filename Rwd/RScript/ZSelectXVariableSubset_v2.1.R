#Select X-variable data subset from original file
#load  a csv text file, named XVARSELV.csv to select X-variables
fileName <- xVarSelectFileName	#Set file name for variable selection input
xVarSel <- read.csv(fileName,header=T,row.names=1,stringsAsFactors=FALSE, 
	strip.white=TRUE, na.strings = c("NA",""))
#
attach(xVarSel)				#Make variable names accessible during session by attaching the variable names
nRows <- length(xVarSel[,1])		#Get the number of rows or X-variables in xVarSel
varNameList <- names(xVarSel)		#Get potential list of xVariables
nCols <- length(varNameList)		#Get number of columns in data frame
DUMMY <- rep(0,nLviRows)		#Create a DUMMY vector of zeros of length 1 (initial) dataset dataset
cat ("\n A DUMMY vector has been created with the following\n number of nLviRows: ", nLviRows) 