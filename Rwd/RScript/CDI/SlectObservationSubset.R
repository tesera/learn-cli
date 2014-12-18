#Get a subset of observations
cdiData <- subset(cdiData, LNMLOR < -1.5)
nCdiRows <- length(cdiData[,1])