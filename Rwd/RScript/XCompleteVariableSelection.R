# Run Discriminant Analysis Variable Selection Procedure

#####################################################################
# User Inputs
#
# Enter the path and name of file (with file extension) to be processed
lviFileName <- "D:\\Rwd\\WLREFFIN.csv"						

# Enter a variable name and variable value to exclude rows from a dataset
# If the variable name is not in the dataset then no rows will be excluded
excludeRowValue = 1
excludeRowVarName <- 'SORTGRP'

# Enter classification variable name to be used as Y-Variable in Discriminant Analysis 
classVariableName <- 'CLASS5'

# Set Variable Selection File Name
xVarSelectFileName <- "D:\\Rwd\\XVARSELV1.csv"

# Select Variable Indicator Value
xVarSelectCriteria <- "X" 

# Set minimum and maximum number of variables to select
minNvar <- 1
maxNvar <- 20

# For each number of variables selected between the minimum
# and maximum values set the number of iterations to be applied
nSolutions <- 10

# Set the criteria to be applied for variables selection 
# (one of 4 options as described below)
# criteria <- "ccr12"	#Maximize Roy's first root statistic (i.e. largest eigenvalue of HE^(-1) where His the effects matrix and E the error residual
# criteria <- "Wilkes"	#Minimize Wilks Lamda where lamda = det(E)/det(T) where E is the error matrix and T is the total variance 
# criteria <- "xi2"	#Maximize the Chi squared (xi2) index based on the Bartle-Pillai trace test statistic, P
# criteria <- "zeta2"	#Maximize Zeta2 (zeta2) coefficient where V = trace(HE^(-1)) and zeta2 = V/(V+r) where r is rank
criteria <- "xi2"



# End of User Input
#####################################################################
# Run routines
#
# Step 1
# Load dataset called lvinew
source("D:\\Rwd\\RScript\\ZLoadDatasetAndAttachVariableNames.r")
#
# Step 2
# Exclude rows with excludeRowValue associated with excludeRowVarName
source("D:\\Rwd\\RScript\\ZExcludeRowsWithCertainVariableValues.r")
#
# Step 3
# Declare classification variable as Factor (i.e. identify variable as classification variable)
source("D:\\Rwd\\RScript\\ZDeclareClassificationVariableAsFactor.r")
#
# Step 4
# Variable Selection using xVarSelectFileName (XVARSELV1.csv)
# according to criteria xVarSelectCriteria ("X")
source("D:\\Rwd\\RScript\\ZSelectXVariableSubset_v1.r")
#
# Step 5
# Remove variables with 0 standard deviation
source("D:\\Rwd\\RScript\\ZRemoveVariablesWithZeroStandardDeviation.r")
#
# Step 6
# Load the subselect R package
source("D:\\Rwd\\RScript\\Loadsubselect-R-Package.r")
#
# Step 7
# Run the subselect linear discriminant analysis
source("D:\\Rwd\\RScript\\RunLinearDiscriminantAnalysis_subselect_ldaHmat.r")
#
# Step 8
# Run the subselect variable improvement routine
source("D:\\Rwd\\RScript\\ZRun-ldaHmat-VariableSelection-Improve.r")
#
# Step 9
# Extract variable name subsets from variable selection process 	  
source("D:\\Rwd\\RScript\\ExtractVariableNameSubsets.r")
#
# Step 10
# Overwrite VARSELECT.csv
source("D:\\Rwd\\RScript\\ZWriteVariableSelectFileToCsvFile.r")
#
# Step 11
# Run python code EXTRACT_RVARIABLE_COMBOS_v2.py
system("C:\\Anaconda\\python.exe D:\\Rwd\\Python\\EXTRACT_RVARIABLE_COMBOS_v2.py")             #To import a Phyton executable
#
# Step 12
# Run python code RANKVAR.py
system("C:\\Anaconda\\python.exe D:\\Rwd\\Python\\RANKVAR.py")             #To import a Phyton executable
#	 
#system('python -c "import sys; sys.stdout.write(file('D:\\Rwd\\Python\\EXTRACT_RVARIABLE_COMBOS_v2.py\\', \'r\')  #To write out the phyton codes
