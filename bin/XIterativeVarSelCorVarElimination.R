# Iteratively Run Discriminant Analysis Variable Selection
# and XVariable Reduction To Eliminate Correlations >= 0.8
# or Correlations <= -0.8.

################################################################################
# Source environment
source(paste(HOME_CONF,"XIterativeVarSel.R.conf", sep = ""))
#source(paste("/shared/GitHub/Tesera/MRAT_Refactor/etc/","XIterativeVarSel.conf", sep = ""))
#333 BETTER TO USE pwd TO SET THIS, BUT RStudio is REPORTING THE ORIGINAL DIR NOT THE CURRENT
#333 FIGURE THAT OUT

#####################################################################
# Step 1
# Initialize count of eligible X-Variables in XVARSELV1.csv
# Write to file XVARSELV1_COUNT
#333 This Python call should be removed from [R] and handled directly by the Python controlling script
COMMAND <- paste("/usr/bin/python2 ",HOME_BIN,"COUNT_XVAR_IN_XVARSELV1.py", sep="")
print(paste("COMMAND = ",COMMAND)) #3333
system(COMMAND)

#####################################################################
# Step 2
# Read XVARSELV1_XCOUNT
source(paste(HOME_RWD,"RScript/ZReadXvarselvCount.R", sep = ""))
initialCount <- xVarCount

#####################################################################
# Step 3
# Initialize Variable selection process
source(paste(HOME_RWD,"RScript/ZCompleteVariableSelectionPlusRemoveCorrelationVariables.R", sep = ""))
source(paste(HOME_RWD,"RScript/ZReadXvarselvCount.R", sep = ""))

#####################################################################
# Step 4
repeat {
	if (initialCount == xVarCount) {
		break
		} else {
		initialCount <- xVarCount
		}
	source(paste(HOME_RWD,"RScript/ZCompleteVariableSelectionPlusRemoveCorrelationVariables.R", sep = ""))
	source(paste(HOME_RWD,"RScript/ZReadXvarselvCount.R", sep = ""))
	}
