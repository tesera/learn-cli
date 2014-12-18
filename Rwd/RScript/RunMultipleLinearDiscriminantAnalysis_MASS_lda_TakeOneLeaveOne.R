#Run take-one-leave-one discriminant analysis on multiple datasets
#CLASSIFICATION previously entered and defined as Factor
#priorDistribution defined using previous previous script.
#CV=TRUE produces results using leave-one-out-cross-validation.
#Package MASS has already been loaded prior to running this script.
#SelectXVariableSubset_v2.1.R has already been run
#
#lda output statistics for CV = TRUE
#lvi.lda$class containins the predicted class
#lvi.lad$posterior contains the posterior probability assigned to each class-observation combination
#
#Get the list of elgible x variables and select the variables from the datafile 
#and put them in a vector, each vector to be analyzed in turn
xDataset <- data.frame(DUMMY)										#Initialize a new xDataset
#
REFCLASS <- c()
PREDCLASS <- c()
CTAB <- c()
VARSET <- c()
UERROR <- c()
EVARSET <- c()
NVAR <- c()
for (i in 1:nRows) {
	#print(i)
	totalError <- 0												#Print run number
	nVariables <- 0
	end_k = length(xDataset)									#Get number of columns
	xDataset[1:end_k] <- list(NULL) 								#Clear the columns to start with a new dataset
	xDataset <- data.frame(DUMMY)									#Initialize the length of the dataset with a dummy variables
	for (j in 4:nCols) {
		if (!xVarSel[i,j] == "N") {								#If not xVarSel[i,j] == "N"
			nVariables = nVariables + 1
			xDataset[,xVarSel[i,j]] <- lvinew[,xVarSel[i,j]]				#Add the variable of name xVarSel[i,j] to the xDataset
			}}				
	xDataset$DUMMY <- NULL										#Remove the DUMMY variable
	lvi.lda = lda(xDataset,CLASSIFICATION,prior = priorDistribution, CV=TRUE)	#Run discriminant analysis
	class.pred = lvi.lda$class									#Get classification prediction table	
	class.table = table(CLASSIFICATION,class.pred)						#Develop contingency table (rows = Actual; columns = predicted
	for (m in 1:nClasses) {
		for (n in 1: nClasses) {
			VARSET <- c(VARSET, as.integer(i))
			REFCLASS <- c(REFCLASS, classNumberList[m])
			PREDCLASS <- c(PREDCLASS, classNumberList[n])
			CTAB <- c(CTAB,class.table[m,n]) 
			}}
	for  (q in 1:nLviRows) {
		totalError = totalError + max(lvi.lda$posterior[q,])
		}
	totalError <- 1 - totalError/nLviRows
	UERROR <- c(UERROR,totalError)
	EVARSET <- c(EVARSET,as.integer(i))
	NVAR <- c(NVAR, nVariables) 
	#print (class.table)										#Print predicted (columns) vs. actual (rows) results
	}
CTABULATION <- cbind(VARSET,REFCLASS,PREDCLASS,CTAB)
POSTERIOR <- cbind(VARSET = EVARSET,NVAR, UERROR)
