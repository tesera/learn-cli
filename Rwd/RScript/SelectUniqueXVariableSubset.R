#Select Unique X-variable data subset from original file
#load  a csv text file, named UNIQUEVAR.txt to select X-variables
fileName <- "D:\\Rwd\\UNIQUEVAR.csv"	#Set file name for variable selection input
xVarSel <- read.csv(fileName,header=T,row.names=1,stringsAsFactors=FALSE, 
	strip.white=TRUE, na.strings = c("NA",""))

nCols <- length(xVarSel)
DUMMY <- rep(0,nLviRows)		#Create a DUMMY vector of zeros of length 1 (initial) dataset dataset
xDataset <- data.frame(DUMMY)
for (j in 1:nCols) {
	xDataset[,xVarSel[1,j]] <- get(xVarSel[1,j])
	}
xDataset$DUMMY <- NULL
