varNames <- names(xDataset)
xDataLength <- length(varNames)
#myCount = 0
for (i in 1:xDataLength) {
	k = i + 1
	if (!(k > xDataLength))	{
		for (j in k:xDataLength)	{
			#The following statements establish a pause between each graph
			old.par <- par(no.readonly = TRUE)
			on.exit(par(old.par))
			par("ask"=TRUE)
			plot(xDataset[,i],xDataset[,j], main = "Pairwise Scatter Plots",
			xlab = varNames[i], ylab = varNames[j], pch = 10)
			abline(lm(xDataset[,j]~xDataset[,i]), col = "red")	#regression line (y~x)
			lines(lowess(xDataset[,i],xDataset[,j]),col = "blue")	#lowess line (x,y)
			#myCount = myCount + 1
			}
		}
	}
	 
