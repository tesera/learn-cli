#This script takes output from mdaVariableSubselect.R and 
#creates a new dataframe withh all of the variable names 
#Inupt array is a 3 dimensional array
#Where rows are lda solutions from 1 to m number of variables
#Columns are variable names from 1 ("Var.1") to x ("Var.x")
arrayDim <- dim(lviVariableSets$subsets)
maxSolutions <- arrayDim[1]
maxVariables <- arrayDim[2]
maxSolutionTypes <- arrayDim[3]
SOLTYPE <- c()
SOLNUM <- c()
VARNAME <- c()
VARNUM <- c()
KVAR <- c()
MODELID <- c()
UID <- c()
mindex = 0
uid <- 0
for (k in 1:maxSolutionTypes){
	for (i in 1: maxSolutions) {
		mindex <- mindex + 1
		for (j in 1:maxVariables){
			if (lviVariableSets$subsets[i,j,k] > 0) {
				uid <- uid + 1
				UID <- c(UID, uid)
				MODELID <- c(MODELID, mindex)
				SOLTYPE <- c(SOLTYPE,k)
				SOLNUM <- c(SOLNUM,i)
				VARNUM <- c(VARNUM,lviVariableSets$subsets[i,j,k])
				VARNAME <- c(VARNAME,xNames[lviVariableSets$subsets[i,j,k]])
				KVAR <- c(KVAR,j)
			}	
		}
	}
}
SOLSUM <- cbind(UID,MODELID,SOLTYPE,SOLNUM,KVAR,VARNUM,VARNAME)				

    
			
