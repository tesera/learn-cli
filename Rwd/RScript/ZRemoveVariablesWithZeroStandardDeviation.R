#Remove variables from xDataset
DUMMY <- rep(0,nLviRows)
newXData <- data.frame(DUMMY)
for (i in 1:length(xNames)) {
	sdev <- sd(xDataset[,xNames[i]])
	if (sdev>0) {
		newXData[,xNames[i]]<- xDataset[,xNames[i]]
		}
	} 
newXData$DUMMY<-NULL
xDataset<-newXData
xNames <- names(xDataset) 
flog.info("Variables with 0 standard deviation have been removed from the xDataset")
xVarCount <- length(xDataset)
flog.info("The following number of variables remain selected: %s", xVarCount)
