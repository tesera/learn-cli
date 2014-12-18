#Get a subset of observations
cdiData <- subset(cdiData, SP1=="FD"|SP1=="PL")
attach(cdiData)
nCdiRows <- length(cdiData[,1])
nCdiRows