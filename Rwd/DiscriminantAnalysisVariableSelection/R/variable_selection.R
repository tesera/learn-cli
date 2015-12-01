library('futile.logger')
library('subselect')

vs.IdentifyAndOrganizeUniqueVariableSets <- function(lviFileName, xVarSelectFileName, xVarSelectOutFile) {
	flog.info('Reading lviFileName %s and xVarSelectFileName %s', lviFileName, xVarSelectFileName)
	xVarSel <<- read.csv(xVarSelectFileName, header=T, row.names=1, stringsAsFactors=FALSE, strip.white=TRUE, na.strings = c("NA",""))
	attach(xVarSel)

	vs.LoadDatasetAndAttachVariableNames(lviFileName)
	vs.ExcludeRowsWithCertainVariableValues()
	vs.DeclareClassificationVariableAsFactor()
	vs.SelectXVariableSubset()
	vs.RemoveVariablesWithZeroStandardDeviation()
	vs.RunLinearDiscriminantAnalysis()
	vs.VariableSelectionImprove()
	vs.ExtractVariableNameSubsets()
	vs.WriteVariableSelectFileToCsvFile(xVarSelectOutFile)

	detach(lvinew)
	detach(xVarSel)
}

vs.CompleteVariableSelectionPlusRemoveCorrelationVariables <- function(lviFileName, uniqueVarFilePath, xVarSelectOutFile) {
	vs.LoadDatasetAndAttachVariableNames(lviFileName)
	vs.ExcludeRowsWithCertainVariableValues()
	vs.SelectUniqueXVariableSubset(uniqueVarFilePath)
	vs.CompileUniqueXVariableCorrelationMatrixSubset()
	vs.CreateUniqueVarCorrelationMatrixFileForPrinting()
	vs.WriteUniqueVarCorrelationMatrix(xVarSelectOutFile)

	detach(lvinew)		
}

vs.LoadDatasetAndAttachVariableNames <- function(lviFileName) { 
	flog.info(paste("Step:", match.call()[[1]]))
	lvinew <<- read.csv(lviFileName, header=T, row.names=1)
	attach(lvinew)		

	lviVarNamesv <<- names(lvinew)					
	nLviRows <<- length(lvinew[,1])
	flog.info('lvinew has the following number of rows: %s', nLviRows)
}

# Exclude rows with excludeRowValue associated with excludeRowVarName
vs.ExcludeRowsWithCertainVariableValues <- function() {
	flog.info(paste("Step:", match.call()[[1]]))
	if (excludeRowVarName %in% names(lvinew)) {
		if (excludeRowValue %in% lvinew[,excludeRowVarName]) {
			flog.info('Deleting selected rows from variable.')
			sel <<- lvinew[excludeRowVarName]== excludeRowValue
			lvinew <<- lvinew[!sel,]
			nLviRows <<- length(lvinew[,1])
			flog.info('Remaining number of rows in dataframe: %s', nLviRows)
		}
	}
}

# Declare classification variable as Factor (i.e. identify variable as classification variable)
vs.DeclareClassificationVariableAsFactor <- function() {
	flog.info(paste("Step:", match.call()[[1]]))
	newClass <<- unlist(lvinew[classVariableName])
	CLASSIFICATION <<- factor(newClass)
	nclassObs <<- length(CLASSIFICATION)
	# Get unique list of class names and sort them in order
	uniqueClasses <<- sort(unique(CLASSIFICATION))
	# Convert factors back into a list of numbers
	classNumberList <<- as.numeric(levels(uniqueClasses)[uniqueClasses])	
	# Count the number of classes
	nClasses <<- length(uniqueClasses)							
	flog.info("There are the following number of classes in the classification: %s", nClasses)
	flog.info("There are the following number of factor observations: %s", nclassObs)
}

# Variable Selection using xVarSelectFileName (XVARSELV1.csv) according to criteria xVarSelectCriteria ("X")
vs.SelectXVariableSubset <- function() {
	flog.info(paste("Step:", match.call()[[1]]))
	# Get the number of rows or X-variables in xVarSel
	nRows <<- length(xVarSel[,1])	
	# Get potential list of xVariables	
	varNameList <<- xVarSel[,1]
	# Create a DUMMY vector of zeros the same length as the lvi (initial) dataset dataset
	DUMMY <<- rep(0,nLviRows)		
	# Initialize a new dataframe using the DUMMY variable to establish the correct number of rows
	xDataset <<- data.frame(DUMMY)		
	
	# Get the list of elgible x and y variables and put them in a vector
	for (i in 1:nRows) {
		if (xVarSel[i,2]== xVarSelectCriteria) {
			xDataset[,varNameList[i]] <<- lvinew[varNameList[i]]
		}
	}

	# Delete the initial DUMMY variable from the dataframe
	xDataset$DUMMY <<- NULL			
	# Create a vector of xDataset names
	xNames <<- names(xDataset)		
	xVarCount = length(xDataset)
	flog.info("A new data frame, xDataset, has been created") 
	flog.info("The following number of variables have been selected: %s", xVarCount)
}

# Remove variables with 0 standard deviation
vs.RemoveVariablesWithZeroStandardDeviation <- function() {
	flog.info(paste("Step:", match.call()[[1]]))
	DUMMY <<- rep(0,nLviRows)
	newXData <<- data.frame(DUMMY)
	for (i in 1:length(xNames)) {
		sdev <<- sd(xDataset[,xNames[i]])
		if (sdev>0) {
			newXData[,xNames[i]] <<- xDataset[,xNames[i]]
		}
	} 
	newXData$DUMMY <<- NULL
	xDataset <<- newXData
	xNames <<- names(xDataset) 
	flog.info("Variables with 0 standard deviation have been removed from the xDataset")
	xVarCount <<- length(xDataset)
	flog.info("The following number of variables remain selected: %s", xVarCount)
}

# Run the subselect linear discriminant analysis
vs.RunLinearDiscriminantAnalysis <- function() {
	flog.info(paste("Step:", match.call()[[1]]))
	lviHmat <<- ldaHmat(xDataset,CLASSIFICATION)	
}

# Run the subselect variable improvement routine
vs.VariableSelectionImprove <- function() {
	flog.info(paste("Step:", match.call()[[1]]))
	lviHmat <<- ldaHmat(xDataset,CLASSIFICATION)	# Set X and Y variables, where Y variables are classification sets
	lviVariableSets <<- improve(lviHmat$mat, kmin = minNvar, kmax = maxNvar, nsol=nSolutions, H=lviHmat$H, r=lviHmat$r, crit=criteria, force=TRUE, setseed=TRUE)
	flog.info("Results from subselect improve variable selection process: %s", lviVariableSets)
}

#  Extract variable name subsets from variable selection process
#  This script takes output from mdaVariableSubselect.R and creates a new dataframe withh all of the variable names 
#  Inupt array is a 3 dimensional array Where rows are lda solutions from 1 to m number of variables. Columns are variable names from 1 ("Var.1") to x ("Var.x")
vs.ExtractVariableNameSubsets <- function() {
	flog.info(paste("Step:", match.call()[[1]]))
	arrayDim <<- dim(lviVariableSets$subsets)
	maxSolutions <<- arrayDim[1]
	maxVariables <<- arrayDim[2]
	maxSolutionTypes <<- arrayDim[3]
	SOLTYPE <<- c()
	SOLNUM <<- c()
	VARNAME <<- c()
	VARNUM <<- c()
	KVAR <<- c()
	MODELID <<- c()
	UID <<- c()
	mindex <<- 0
	uid <<- 0
	for (k in 1:maxSolutionTypes){
		for (i in 1: maxSolutions) {
			mindex <<- mindex + 1
			for (j in 1:maxVariables){
				if (lviVariableSets$subsets[i,j,k] > 0) {
					uid <<- uid + 1
					UID <<- c(UID, uid)
					MODELID <<- c(MODELID, mindex)
					SOLTYPE <<- c(SOLTYPE,k)
					SOLNUM <<- c(SOLNUM,i)
					VARNUM <<- c(VARNUM,lviVariableSets$subsets[i,j,k])
					VARNAME <<- c(VARNAME,xNames[lviVariableSets$subsets[i,j,k]])
					KVAR <<- c(KVAR,j)
				}	
			}
		}
	}
	SOLSUM <<- cbind(UID,MODELID,SOLTYPE,SOLNUM,KVAR,VARNUM,VARNAME)		
}

vs.SelectUniqueXVariableSubset <- function(uniqueVarFilePath) {
	flog.info(paste("Step:", match.call()[[1]]))
	xVarSel <<- read.csv(uniqueVarFilePath, header=T, row.names=1, stringsAsFactors=FALSE, strip.white=TRUE, na.strings = c("NA",""))

	nCols <<- length(xVarSel)
	#Create a DUMMY vector of zeros of length 1 (initial) dataset dataset
	DUMMY <<- rep(0,nLviRows)
	xDataset <<- data.frame(DUMMY)
	for (j in 1:nCols) {
		xDataset[,xVarSel[1,j]] <<- lvinew[,xVarSel[1,j]]
	}
	xDataset$DUMMY <<- NULL
}

vs.CompileUniqueXVariableCorrelationMatrixSubset <- function() {
	flog.info(paste("Step:", match.call()[[1]]))
	correlationMatrix <<- cor(xDataset)
}

vs.CreateUniqueVarCorrelationMatrixFileForPrinting <- function() {
	flog.info(paste("Step:", match.call()[[1]]))
	#Create Correlation Matrix File for Printing
	VARNAME1 <<- c()
	VARNAME2 <<- c()
	CORCOEF <<- c()
	nnCols <<- length(correlationMatrix[1,])
	nnRows <<- nnCols
	varNames <<- names(xDataset)
	#
	for (i in 1:nnCols) {	
		for (j in 1:nnRows)	{
			VARNAME1 <<- c(VARNAME1, varNames[i])
			VARNAME2 <<- c(VARNAME2, varNames[j])
			CORCOEF <<- c(CORCOEF, correlationMatrix[j,i]) 
			}
		}
	UCORCOEF <<- cbind.data.frame(VARNAME1,VARNAME2,CORCOEF)
}

vs.WriteUniqueVarCorrelationMatrix <- function(xVarSelectOutFile) {
	flog.info(paste("Step:", match.call()[[1]]))
	flog.info("Generating %s", xVarSelectOutFile)	
	write.csv(UCORCOEF, file=xVarSelectOutFile, row.names=FALSE,na="")
}

vs.WriteVariableSelectFileToCsvFile <- function(xVarSelectOutFile) {
	flog.info(paste("Step:", match.call()[[1]]))
	flog.info("Generating %s", xVarSelectOutFile)
	write.csv(SOLSUM, file=xVarSelectOutFile, row.names=FALSE,na="")
}
