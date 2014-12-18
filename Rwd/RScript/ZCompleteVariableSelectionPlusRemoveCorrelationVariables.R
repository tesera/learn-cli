# Run Discriminant Analysis Variable Selection Procedure

# Run routines
#
# Step 1
# Load dataset called lvinew
source("/shared/GitHub/Tesera/Rwd/RScript/ZLoadDatasetAndAttachVariableNames.R")
#
# Step 2
# Exclude rows with excludeRowValue associated with excludeRowVarName
source("/shared/GitHub/Tesera/Rwd/RScript/ZExcludeRowsWithCertainVariableValues.R")
#
# Step 3
# Declare classification variable as Factor (i.e. identify variable as classification variable)
source("/shared/GitHub/Tesera/Rwd/RScript/ZDeclareClassificationVariableAsFactor.R")
#
# Step 4
# Variable Selection using xVarSelectFileName (XVARSELV1.csv)
# according to criteria xVarSelectCriteria ("X")
source("/shared/GitHub/Tesera/Rwd/RScript/ZSelectXVariableSubset_v1.R")
#
# Step 5
# Remove variables with 0 standard deviation
source("/shared/GitHub/Tesera/Rwd/RScript/ZRemoveVariablesWithZeroStandardDeviation.R")
#
# Step 6
# Load the subselect R package
source("/shared/GitHub/Tesera/Rwd/RScript/Loadsubselect-R-Package.R")
#
# Step 7
# Run the subselect linear discriminant analysis
source("/shared/GitHub/Tesera/Rwd/RScript/RunLinearDiscriminantAnalysis_subselect_ldaHmat.R")
#
# Step 8
# Run the subselect variable improvement routine
source("/shared/GitHub/Tesera/Rwd/RScript/ZRun-ldaHmat-VariableSelection-Improve.R")
#
# Step 9
# Extract variable name subsets from variable selection process 	  
source("/shared/GitHub/Tesera/Rwd/RScript/ExtractVariableNameSubsets.R")
#
# Step 10
# Overwrite VARSELECT.csv
source("/shared/GitHub/Tesera/Rwd/RScript/ZWriteVariableSelectFileToCsvFile.R")
#
# Step 11
# Run python code EXTRACT_RVARIABLE_COMBOS_v2.py
system("/usr/bin/python2 /shared/GitHub/Tesera/Rwd/Python/EXTRACT_RVARIABLE_COMBOS_v2.py")             #To import a Phyton executable
#
# Step 12
# Run python code RANKVAR.py
system("/usr/bin/python2 /shared/GitHub/Tesera/Rwd/Python/RANKVAR.py")             #To import a Phyton executable
#
# Step 13
# Reload LVI dataset
source("/shared/GitHub/Tesera/Rwd/RScript/ZLoadDatasetAndAttachVariableNames.R")
#
# Step 14
# Exclude rows with excludeRowValue associated with excludeRowVarName
source("/shared/GitHub/Tesera/Rwd/RScript/ZExcludeRowsWithCertainVariableValues.R")
#	 
# Step 15
# Variable Selection using xVarSelectFileName (UNIQUEVAR.csv)
# according to criteria xVarSelectCriteria ("X")
source("/shared/GitHub/Tesera/Rwd/RScript/ZSelectUniqueXVariableSubset.R")
#
# Step 16
# Generate correlations amongst variables
source("/shared/GitHub/Tesera/Rwd/RScript/CompileUniqueXVariableCorrelationMatrixSubset.R")
#
# Step 17
# Create correlation matrix for printing
source("/shared/GitHub/Tesera/Rwd/RScript/CreateUniqueVarCorrelationMatrixFileForPrinting.R")
#
# Step 18
# Write correlation matrix R
source("/shared/GitHub/Tesera/Rwd/RScript/ZWriteUniqueVarCorrelationMatrix.R")
#
# Step 19
# Update XVARSELV1 to remove variable pairs with high correlation coeficients
system("/usr/bin/python2 /shared/GitHub/Tesera/Rwd/Python/REMOVE_HIGHCORVAR_FROM_XVARSELV.py")
#
# Step 20
# Count number of eligible X-Variables in XVARSELV1.csv
# Write to file XVARSELV1_COUNT
system("/usr/bin/python2 /shared/GitHub/Tesera/Rwd/Python/COUNT_XVAR_IN_XVARSELV1.py")

