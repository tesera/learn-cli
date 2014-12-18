#Run full dataset discriminant analysis on multiple datasets
#CLASSIFICATION previously entered and defined as Factor
#priorDistribution defined using previous previous script.
#CV=FALSE produces using all of the data in the calibration dataset.
#Package MASS has already been loaded prior to running this script.
#SelectXVariableSubset_v2.1.R has already been run
#
#lda output statistics for CV = FALSE
#
#Get the list of elgible x variables and select the variables from the datafile 
#and put them in a vector, each vector to be analyzed in turn
xDataset <- data.frame(DUMMY)										#Initialize a new xDataset
#
REFCLASS <- c()												#Initialize vectors necessary to create print files
PREDCLASS <- c()
CTAB <- c()
VARSET <- c()
VARSET2 <- c()
CLASS2 <- c()
VARNAMES2 <- c()
MEANS2 <- c()
VARSET3 <- c()
DFCOEF3 <- c()
VARNAMES3 <- c()
FUNCLABEL3 <- c()
VARSET4 <- c()
FUNCLABEL4 <- c()
BTWTWCR4 <- c()
for (i in 1:nRows) {
	#print(i)												#Print run number
	end_k = length(xDataset)									#Get number of columns
	xDataset[1:end_k] <- list(NULL) 								#Initialize an empty dataset
	xDataset <- data.frame(DUMMY)									#Initialize the length of the dataset with a dummy variables
	for (j in 4:nCols) {
		if (!xVarSel[i,j] == "N") {								#If not xVarSel[i,j] == "N"
			xDataset[,xVarSel[i,j]] <- lvinew[,xVarSel[i,j]]				#Add the variable of name xVarSel[i,j] to the xDataset
			}
		}				
	xDataset$DUMMY <- NULL										#Remove the DUMMY variable
	varNames <- names(xDataset)									#Get a list of the variable names
	nVar <- length(varNames)									#Get the number of variable names in the list
	lvi.lda = lda(xDataset,CLASSIFICATION,prior = priorDistribution, CV=FALSE)	#Run discriminant analysis
	class.pred = predict(lvi.lda)									#Get class predictions for each observation	
	class.table = table(CLASSIFICATION,class.pred$class)					#Develop contingency table (rows = Actual; columns = predicted classes)
	nDiscFunctions = length(lvi.lda$scaling[1,])						#Get the number of discriminant functions
	for (m in 1:nClasses) {										#Compile actual veruss predicted cross tabulation tables
		for (n in 1: nClasses) {
			VARSET <- c(VARSET,i)
			REFCLASS <- c(REFCLASS, classNumberList[m])
			PREDCLASS <- c(PREDCLASS, classNumberList[n])
			CTAB <- c(CTAB,class.table[m,n]) 
			}
		}
	for (n in 1:nVar) {										#Compile mean variable values by class
		for (m in 1: nClasses) {
			VARSET2 <- c(VARSET2,i)
			CLASS2 <- c(CLASS2, classNumberList[m])
			VARNAMES2 <- c(VARNAMES2, varNames[n])
			MEANS2 <- c(MEANS2,lvi.lda$means[m,n])
			}
		}
	for (n in 1: nDiscFunctions){									#Compiule Discriminant Function Coefficients
		for (m in 1:nVar)	{
			VARSET3 <- c(VARSET3, i)
			VARNAMES3 <- c(VARNAMES3, varNames[m])
			FUNCLABEL3 <- c(FUNCLABEL3,gsub(" ","",paste("LN",toString(n))))
			DFCOEF3 <- c(DFCOEF3,lvi.lda$scaling[m,n])
			}
		}
	for (n in 1: nDiscFunctions){									#Get Discriminant Function B/W Variance Ratios 
		VARSET4 <- c(VARSET4, i)
		FUNCLABEL4 <- c(FUNCLABEL4,gsub(" ","",paste("LN",toString(n))))
		BTWTWCR4 <- c(BTWTWCR4,lvi.lda$svd[n])
		}
	#print (class.table)										#Print predicted (columns) vs. actual (rows) results														
	}
#
CTABALL <- cbind(VARSET,REFCLASS,PREDCLASS,CTAB)						#Cross tabulation data frame
VARMEANS <- cbind.data.frame(VARSET2, CLASS2, VARNAMES2,MEANS2)				#Mean variable values by class
DFUNCT <- cbind.data.frame(VARSET3, VARNAMES3,FUNCLABEL3,DFCOEF3)				#Discriminant Function Coefficients by Variable Name
BWRATIO <- cbind.data.frame(VARSET4,FUNCLABEL4,BTWTWCR4)					#Between to Within Variance ratio for each Discriminant Function
#
