#Select Unique X-variable data subset from original file
#load  a csv text file, named UNIQUEVAR.txt to select X-variables
xVarSel <- read.csv(uniqueVarPath,header=T,row.names=1,stringsAsFactors=FALSE, 
	strip.white=TRUE, na.strings = c("NA",""))

nCols <- length(xVarSel)
DUMMY <- rep(0,nLviRows)		#Create a DUMMY vector of zeros of length 1 (initial) dataset dataset
xDataset <- data.frame(DUMMY)
for (j in 1:nCols) {
	xDataset[,xVarSel[1,j]] <- lvinew[,xVarSel[1,j]]
	}
xDataset$DUMMY <- NULL
