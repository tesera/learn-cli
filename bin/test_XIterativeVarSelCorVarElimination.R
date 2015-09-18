#Author: Ian Moss
# Modified by: Ian Moss, Sam Kaharabata & Mishtu Banerjee
#Updated 20150918 MB, SK
#Maintainers: Sam Kaharabata, Mishtu Banerjee, Ian Moss

# Copyright: The Author(s)
#License: Distributed under MIT License
#    [http://opensource.org/licenses/mit-license.html]


#This is latest working version 20150914 SK MB
#Set Default Working Directory where R places outputs 20150831 MB, IM, SK
setwd("/opt/MRAT_Refactor/Rwd")
# Iteratively Run Discriminant Analysis Variable Selection
# and XVariable Reduction To Eliminate Correlations >= 0.8
# or Correlations <= -0.8.

################################################################################
# Source environment
source(paste("/opt/MRAT_Refactor/etc/", "XIterativeVarSel.R.conf", sep = ""))
#source(paste(HOME_CONF,"XIterativeVarSel.R.conf", sep = ""))

#####################################################################
# Step 2
# Read XVARSELV1_XCOUNT -- Contains the number of X Variables in the data

source(paste(HOME_RWD,"RScript/test_ZReadXvarselvCount.R", sep = ""))
initialCount <- xVarCount
write.csv(initialCount, file = "zzz.csv") #SK added 20150901 - this works

#####################################################################
# Step 3
# Initialize Variable selection process
source(paste(HOME_RWD,"RScript/test_ZCompleteVariableSelectionPlusRemoveCorrelationVariables.R", sep = ""))
#source(paste(HOME_RWD,"RScript/ZReadXvarselvCount.R", sep = ""))

#Confirming we got to Step 3 (step 10 in underlying file) 20150831 MB
cat(myZCompleteTest)
write.csv(myZCompleteTest, file="zzzStep10.csv")

#####################################################################

