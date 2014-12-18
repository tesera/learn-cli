####################################################
#User Inputs
lviFileName <- "D:\\Rwd\\4_ANALYSIS_MUNICIPAL.txt"


# Enter a variable name and variable value to exclude rows from a dataset
# If the variable name is not in the dataset then no rows will be excluded
# If the excludeRowValue is not listed under the variable name then no rows 
# will be excluded.
excludeRowValue = -1
excludeRowVarName <- 'SORTGRP'

# Enter classification variable name to be used as Y-Variable in Discriminant Analysis 
classVariableName <- 'CLPRDP'

# Enter XVARSELV1
xVarSelectFileName <- "D:\\Rwd\\4_box_plot.csv"

# Enter variable selection criteria ("X" or "Y")
xVarSelectCriteria <- "X"

# End of User Inputs
#########################################################
# Run routines

# Step 1
# Load dataset called lvinew
source("D:\\Rwd\\RScript\\ZLoadDatasetAndAttachVariableNames.r")

# Step 2
# Exclude rows with excludeRowValue associated with excludeRowVarName
source("D:\\Rwd\\RScript\\ZExcludeRowsWithCertainVariableValues.r")

# Step 3
# Declare classification variable as Factor (i.e. identify variable as classification variable)
source("D:\\Rwd\\RScript\\ZDeclareClassificationVariableAsFactor.r")

# Step 4
# Compile a new data subset called xDataset
source("D:\\Rwd\\RScript\\ZSelectXVariableSubset_v1.r")


# Step 5
# Produce Box Plots
source("D:\\Rwd\\RScript\\ZCreateXorYVariableClassificationBoxPlots.r")


