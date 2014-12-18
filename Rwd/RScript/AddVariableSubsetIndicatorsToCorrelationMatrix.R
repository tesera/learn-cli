#This script creates indicator variables to identify each subset of variables
#It also calculates the maximum absolute value of the correlation coefficient for all pairs of variables within each subset
#
nRowsCor <- length(UCORCOEF[,1])
MAXCOR <- c()
MINCOR <- c()
VARSET <- c()
VARNO <- c()
#
for (i in 1:nRows) {								#Initialize the length of the dataset with a dummy variables
	VARNAMES <- c()
	DUMMY <- c()
	maxCor <- -1
	minCor <- 1
	varNo <- 0
	colName <- gsub(" ","",paste("I",toString(i)))			#Create a variable name I1, I2 ...
	for (j in 4:nCols) {
		if (!xVarSel[i,j] == "N") {					#If not xVarSel[i,j] == "N"
			VARNAMES <- c(VARNAMES, xVarSel[i,j])		#Add the variable of name xVarSel[i,j]
			varNo <- varNo + 1
			}}
	for (k in 1:nRowsCor)	{						#If VARNAMES has variable names in columns 1 and 2 change the corresponding DUMMY variable to 1
		if (any(VARNAMES == UCORCOEF[k,1]))	{		
			if (any(VARNAMES == UCORCOEF[k,2]))	{
				DUMMY <- c(DUMMY,1)
				if (UCORCOEF[k,3] < 1)  {
					if (UCORCOEF[k,3] > maxCor) {
						maxCor <- UCORCOEF[k,3]
						}
					} 
				if (UCORCOEF[k,3] < minCor) {minCor <- UCORCOEF[k,3]}
				} else {DUMMY <- c(DUMMY, 0)}
			} else {DUMMY <- c(DUMMY, 0)} 
		}
	#if (any(DUMMY == 1)) 	{print(i)}
	UCORCOEF <- cbind.data.frame(UCORCOEF, DUMMY)					#Add DUMMY to the UCORCOEF data frame
	end_i <- length(UCORCOEF[1,])							
	names(UCORCOEF)[end_i] <- colName					#Change the column name to colName
	VARSET <- c(VARSET, i)
	MINCOR <- c(MINCOR, minCor)
	MAXCOR <- c(MAXCOR, maxCor)
	VARNO <- c(VARNO, varNo)
	}
MINMAXCOR <- cbind.data.frame(VARSET,VARNO,MAXCOR,MINCOR)

				