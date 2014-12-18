# Running Section 6 of the LVI manual
# Linear Discriminant Analysis for MUltiple X-Variable Sets

####################################################
#User Inputs
#lviFileName <- "/shared/GitHub/Tesera/Rwd/ANALYSIS_CENSUS.csv"
#lviFileName <- "/shared/GitHub/Tesera/Rwd/ANALYSIS_MUNICIPAL.csv"
#lviFileName <- "/shared/GitHub/Tesera/Rwd/ANALYSIS_MUNICIPAL_LRESIDENT.csv"
#lviFileName <- "/shared/GitHub/Tesera/Rwd/ANALYSIS_MUNICIPAL_LRESIDENT_LBASEMENT_NO-LMULTIFAM.csv"
lviFileName <- "/shared/GitHub/Tesera/Rwd/ANALYSIS_MUNICIPAL_SSH7_25_SPDIASTR1_4_LRESIDENT_LBASEMENT_NO-LMULTIFAM.csv"
#lviFileName <- "/shared/GitHub/Tesera/Rwd/ANALYSIS_MUNICIPAL_SSH9plus28plus143_LRESIDENT_LBASEMENT_NO-LMULTIFAM.csv"
#lviFileName <- "/shared/GitHub/Tesera/Rwd/ANALYSIS_MUNICIPAL_SAGESAN3plus4_LRESIDENT_LBASEMENT_NO-LMULTIFAM.csv"
#lviFileName <- "/shared/GitHub/Tesera/Rwd/ANALYSIS_MUNICIPAL_SAGESANplus12_SDIASTRDplus23679_LRESIDENT_LBASEMENT_NO-LMULTIFAM.csv"

# Enter a variable name and variable value to exclude rows from a dataset
# If the variable name is not in the dataset then no rows will be excluded
# If the excludeRowValue is not listed under the variable name then no rows 
# will be excluded.
excludeRowValue = -1
excludeRowVarName <- 'SORTGRP'

# Enter classification variable name to be used as Y-Variable in Discriminant Analysis 
classVariableName <- 'CLPRDP'

# Enter 'UNIFORM' or 'SAMPLE' to indicate type of prior distribution 
priorDistribution <- 'SAMPLE' 
# Note prior distribution will be written to a file called PRIOR.csv

# The XVARSELV.csv file to do the Variable Selection
# This file was produced in the course of completing the variable 
# selection procedures
xVarSelectFileName <- "/shared/GitHub/Tesera/Rwd/XVARSELV.csv"

#Identify working directory - for now this should not be changed
wd <- '/shared/GitHub/Tesera/Rwd'

####################################################################
# Run routines

# Step 0 Set Working Directory
setwd(wd)

# Step 1
# Load dataset called lvinew
source("/shared/GitHub/Tesera/Rwd/RScript/ZLoadDatasetAndAttachVariableNames.r")

# Step 2
# Exclude rows with excludeRowValue associated with excludeRowVarName
source("/shared/GitHub/Tesera/Rwd/RScript/ZExcludeRowsWithCertainVariableValues.r")

# Step 3
# Declare classification variable as Factor (i.e. identify variable as classification variable)
source("/shared/GitHub/Tesera/Rwd/RScript/ZDeclareClassificationVariableAsFactor.r")

# Step 4
# Get prior distribution to be used in Discriminant Analysis
source("/shared/GitHub/Tesera/Rwd/RScript/ZComputePriorClassProbabilityDistribution.r")

# Step 5
# Write prior distribution to file
source("/shared/GitHub/Tesera/Rwd/RScript/WritePriorDistributionToFile.r")

# Step 6
# Load MASS package
source("/shared/GitHub/Tesera/Rwd/RScript/LoadMASS-R-Package.r")

# Step 7
# Get the multiple variable subsets XVARSELV.csv
source("/shared/GitHub/Tesera/Rwd/RScript/ZSelectXVariableSubset_v2.1.r")

# Step 8
# Run Multiple Discriminant Analysis - Take One - Leave One
source("/shared/GitHub/Tesera/Rwd/RScript/RunMultipleLinearDiscriminantAnalysis_MASS_lda_TakeOneLeaveOne.r")

# Step 9
# Write two new files to the working directory - CTABULATION.csv - POSTERIOR.csv
source("/shared/GitHub/Tesera/Rwd/RScript/WriteMultipleLinearDiscriminantAnalysis_MASS_lda_TOLO_to_File.r")

# Step 10
# Run  Multiple Discriminant Analysis - All Data
source("/shared/GitHub/Tesera/Rwd/RScript/RunMultipleLinearDiscriminantAnalysis_MASS_lda.r")

# Step 11
# Write files - CTABALL.csv VARMEANS.csv DFUNCT.csv BWRATIO.csv
source("/shared/GitHub/Tesera/Rwd/RScript/WriteMultipleLinearDiscriminantAnalysis_MASS_lda.r")

# Step 12
# Generate COHENS_KHAT statistics
system("/usr/bin/python2 /shared/GitHub/Tesera/Rwd/Python/COHENS_KHAT_R.py")

# Step 13
# Combine evaluation datasets into one file: ASSESS.csv
system("/usr/bin/python2 /shared/GitHub/Tesera/Rwd/Python/COMBINE_EVALUATION_DATASETS_R.py")

