xVarNames <- names(xDataset)
yVarNames <- names(yDataset)
xDataLength <- length(xVarNames)
yDataLength <- length(yVarNames)
#myCount = 0
for (i in 1:xDataLength) {
	for (j in 1: yDataLength)	{
		#The following statements establish a pause between each graph
		old.par <- par(no.readonly = TRUE)
		on.exit(par(old.par))
		par("ask"=TRUE)
		plot(xDataset[,i],yDataset[,j], main = "Pairwise Scatter Plots",
		xlab = xVarNames[i], ylab = yVarNames[j], pch = 10)
		abline(lm(yDataset[,j]~xDataset[,i]), col = "red")	#regression line (y~x)
		lines(lowess(xDataset[,i],yDataset[,j]),col = "blue")	#lowess line (x,y)
		#myCount = myCount + 1
		}
	}
	 
