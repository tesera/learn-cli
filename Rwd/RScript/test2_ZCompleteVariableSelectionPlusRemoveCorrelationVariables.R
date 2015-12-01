install('DiscriminantAnalysisVariableSelection')
library('DiscriminantAnalysisVariableSelection')


source("/opt/MRAT_Refactor/Rwd/RScript/ZLoadDatasetAndAttachVariableNames.R")
step13 <- 3.13
write.csv(step13, file = "step13.csv")
#
# Step 14
# Exclude rows with excludeRowValue associated with excludeRowVarName
source("/opt/MRAT_Refactor/Rwd/RScript/ZExcludeRowsWithCertainVariableValues.R")
step14 <- 3.14
write.csv(step14, file = "step14.csv")
#	 
# Step 15
# Variable Selection using xVarSelectFileName (UNIQUEVAR.csv)
# according to criteria xVarSelectCriteria ("X")
source("/opt/MRAT_Refactor/Rwd/RScript/ZSelectUniqueXVariableSubset.R")
step15 <- 3.15
write.csv(step15, file = "step15.csv")
#
# Step 16
# Generate correlations amongst variables
source("/opt/MRAT_Refactor/Rwd/RScript/CompileUniqueXVariableCorrelationMatrixSubset.R")
step16 <- 3.16
write.csv(step16, file = "step16.csv")
#
# Step 17
# Create correlation matrix for printing
source("/opt/MRAT_Refactor/Rwd/RScript/CreateUniqueVarCorrelationMatrixFileForPrinting.R")
step17 <- 3.17
write.csv(step17, file = "step17.csv")
#
# Step 18
# Write correlation matrix R
source("/opt/MRAT_Refactor/Rwd/RScript/ZWriteUniqueVarCorrelationMatrix.R")
step18 <- 3.18
write.csv(step18, file = "step18.csv")
#
# Step 19
# Update XVARSELV1 to remove variable pairs with high correlation coeficients
#system("/usr/bin/python2 /shared/GitHub/Tesera/Rwd/Python/REMOVE_HIGHCORVAR_FROM_XVARSELV.py")
#
# Step 20
# Count number of eligible X-Variables in XVARSELV1.csv
# Write to file XVARSELV1_COUNT
#system("/usr/bin/python2 /shared/GitHub/Tesera/Rwd/Python/COUNT_XVAR_IN_XVARSELV1.py")

