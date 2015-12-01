#Author: Ian Moss
# Modified by: Ian Moss, Sam Kaharabata & Mishtu Banerjee
#Updated 20150918 MB, SK
#Maintainers: Sam Kaharabata, Mishtu Banerjee, Ian Moss

# Copyright: The Author(s)
#License: Distributed under MIT License
#    [http://opensource.org/licenses/mit-license.html]

#####################################################################
#Set Default Working Directory where R places outputs 20150831 MB, IM, SK
#setwd("/opt/MRAT_Refactor/Rwd")
# Iteratively Run Discriminant Analysis Variable Selection
# and XVariable Reduction To Eliminate Correlations >= 0.8
# or Correlations <= -0.8.

################################################################################
# Source environment
#source(paste("/opt/MRAT_Refactor/etc/", "XIterativeVarSel.R.conf", sep = ""))
#source(paste(HOME_CONF,"XIterativeVarSel.R.conf", sep = ""))
#source(paste("/shared/GitHub/Tesera/MRAT_Refactor/etc/","XIterativeVarSel.conf", sep = ""))

#####################################################################
# Step 3
# Initialize Variable selection process
#20150831 Add test_ to ZCompleteVariableSelectionPlusRemoveCorrelationVariables.R MB, IM, SK
source(paste(HOME_RWD,"RScript/test2_ZCompleteVariableSelectionPlusRemoveCorrelationVariables.R", sep = ""))
#source(paste(HOME_RWD,"RScript/ZReadXvarselvCount.R", sep = ""))

