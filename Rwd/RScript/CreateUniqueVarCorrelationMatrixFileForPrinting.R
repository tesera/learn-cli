#Create Correlation Matrix File for Printing
VARNAME1 <- c()
VARNAME2 <- c()
CORCOEF <- c()
nnCols <- length(correlationMatrix[1,])
nnRows <- nnCols
varNames <- names(xDataset)
#
for (i in 1:nnCols) {	
	for (j in 1:nnRows)	{
		VARNAME1 <- c(VARNAME1, varNames[i])
		VARNAME2 <- c(VARNAME2, varNames[j])
		CORCOEF <- c(CORCOEF, correlationMatrix[j,i]) 
		}
	}
UCORCOEF <- cbind.data.frame(VARNAME1,VARNAME2,CORCOEF)
