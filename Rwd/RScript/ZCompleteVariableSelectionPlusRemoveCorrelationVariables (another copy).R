# Run Discriminant Analysis Variable Selection Procedure

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
source("D:\\Rwd\\RScript\\Loadsubselect-R-Package.R")
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
# Step 13
# Reload LVI dataset
source("D:\\Rwd\\RScript\\ZLoadDatasetAndAttachVariableNames.r")
#
# Step 14
# Exclude rows with excludeRowValue associated with excludeRowVarName
source("D:\\Rwd\\RScript\\ZExcludeRowsWithCertainVariableValues.r")
#	 
# Step 15
# Variable Selection using xVarSelectFileName (UNIQUEVAR.csv)
# according to criteria xVarSelectCriteria ("X")
source("D:\\Rwd\\RScript\\ZSelectUniqueXVariableSubset.r")
#
# Step 16
# Generate correlations amongst variables
source("D:\\Rwd\\RScript\\CompileUniqueXVariableCorrelationMatrixSubset.r")
#
# Step 17
# Create correlation matrix for printing
source("D:\\Rwd\\RScript\\CreateUniqueVarCorrelationMatrixFileForPrinting.r")
#
# Step 18
# Write correlation matrix R
source("D:\\Rwd\\RScript\\ZWriteUniqueVarCorrelationMatrix.r")
#
# Step 19
# Update XVARSELV1 to remove variable pairs with high correlation coeficients
system("C:\\Anaconda\\python.exe D:\\Rwd\\Python\\REMOVE_HIGHCORVAR_FROM_XVARSELV.py")
#
# Step 20
# Count number of eligible X-Variables in XVARSELV1.csv
# Write to file XVARSELV1_COUNT
system("C:\\Anaconda\\python.exe D:\\Rwd\\Python\\COUNT_XVAR_IN_XVARSELV1.py")

