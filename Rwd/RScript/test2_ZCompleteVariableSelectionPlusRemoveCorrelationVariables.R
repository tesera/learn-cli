# Run Discriminant Analysis Variable Selection Procedure

# Run routines
#
# Step 1
# Load dataset called lvinew
#source("/shared/GitHub/Tesera/Rwd/RScript/ZLoadDatasetAndAttachVariableNames.R")
#source("/opt/MRAT_Refactor/Rwd/RScript/ZLoadDatasetAndAttachVariableNames.R")
#step1 <- 3.1
#write.csv(step1, file = "step1.csv")
#
# Step 2
# Exclude rows with excludeRowValue associated with excludeRowVarName
#source("/shared/GitHub/Tesera/Rwd/RScript/ZExcludeRowsWithCertainVariableValues.R")
#source("/opt/MRAT_Refactor/Rwd/RScript/ZExcludeRowsWithCertainVariableValues.R")
#step2 <- 3.2
#write.csv(step2, file = "step2.csv")
#
#
# Step 3
# Declare classification variable as Factor (i.e. identify variable as classification variable)
#source("/shared/GitHub/Tesera/Rwd/RScript/ZDeclareClassificationVariableAsFactor.R")
#source("/opt/MRAT_Refactor/Rwd/RScript/ZDeclareClassificationVariableAsFactor.R")
#step3 <- 3.3
#write.csv(step3, file = "step3.csv")
#
# Step 4
# Variable Selection using xVarSelectFileName (XVARSELV1.csv)
# according to criteria xVarSelectCriteria ("X")
#source("/shared/GitHub/Tesera/Rwd/RScript/ZSelectXVariableSubset_v1.R")
#source("/opt/MRAT_Refactor/Rwd/RScript/ZSelectXVariableSubset_v1.R")
#step4 <- 3.4
#write.csv(step4, file = "step4.csv")
#
# Step 5
# Remove variables with 0 standard deviation
#source("/shared/GitHub/Tesera/Rwd/RScript/ZRemoveVariablesWithZeroStandardDeviation.R")
#source("/opt/MRAT_Refactor/Rwd/RScript/ZRemoveVariablesWithZeroStandardDeviation.R")
#step5 <- 3.5
#write.csv(step5, file = "step5.csv")
#
# Step 6
# Load the subselect R package
#source("/shared/GitHub/Tesera/Rwd/RScript/Loadsubselect-R-Package.R")
#source("/opt/MRAT_Refactor/Rwd/RScript/Loadsubselect-R-Package.R")
#step6 <- 3.6
#write.csv(step6, file = "step6.csv")
#
# Step 7
# Run the subselect linear discriminant analysis
#source("/shared/GitHub/Tesera/Rwd/RScript/RunLinearDiscriminantAnalysis_subselect_ldaHmat.R")
#source("/opt/MRAT_Refactor/Rwd/RScript/RunLinearDiscriminantAnalysis_subselect_ldaHmat.R")
#step7 <- 3.7
#write.csv(step7, file = "step7.csv")
##
# Step 8
# Run the subselect variable improvement routine
#source("/shared/GitHub/Tesera/Rwd/RScript/ZRun-ldaHmat-VariableSelection-Improve.R")
#source("/opt/MRAT_Refactor/Rwd/RScript/ZRun-ldaHmat-VariableSelection-Improve.R")
#step8 <- 3.8
#write.csv(step8, file = "step8.csv")
#
# Step 9
# Extract variable name subsets from variable selection process 	  
#source("/shared/GitHub/Tesera/Rwd/RScript/ExtractVariableNameSubsets.R")
#source("/opt/MRAT_Refactor/Rwd/RScript/ExtractVariableNameSubsets.R")
#step9 <- 3.9
#write.csv(step9, file = "step9.csv")
#
# Step 10
# Overwrite VARSELECT.csv
#source("/shared/GitHub/Tesera/Rwd/RScript/ZWriteVariableSelectFileToCsvFile.R")
#source("/opt/MRAT_Refactor/Rwd/RScript/ZWriteVariableSelectFileToCsvFile.R")
#step10 <- 3.10
#write.csv(step10, file = "step10.csv")
#

#An arbitrary expression
#myZCompleteTest<- "Did we get to step 10" 


# Step 11
# Run python code EXTRACT_RVARIABLE_COMBOS_v2.py
# 20150831 Commenting out Steps 11 to end MB, IM, SK
#system("/usr/bin/python2 /shared/GitHub/Tesera/Rwd/Python/EXTRACT_RVARIABLE_COMBOS_v2.py")             #To import a Phyton executable
#
# Step 12
# Run python code RANKVAR.py
#system("/usr/bin/python2 /shared/GitHub/Tesera/Rwd/Python/RANKVAR.py")             #To import a Phyton executable
#
# Step 13
# Reload LVI dataset
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

