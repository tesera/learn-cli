# bc: setwd inside XIterativeVarSel.R.conf http://stackoverflow.com/questions/13770304/risks-of-using-setwd-in-a-script
# setwd("/opt/MRAT_Refactor/Rwd")

# Iteratively Run Discriminant Analysis Variable Selection
# and XVariable Reduction To Eliminate Correlations >= 0.8
# or Correlations <= -0.8.
# source("./etc/XIterativeVarSel.R.conf")

# Read XVARSELV1_XCOUNT -- Contains the number of X Variables in the data
source("RScript/test_ZReadXvarselvCount.R")
initialCount <- xVarCount

write.csv(initialCount, file = "zzz.csv") #SK added 20150901 - this works

# Initialize Variable selection process
source("RScript/test_ZCompleteVariableSelectionPlusRemoveCorrelationVariables.R")

#Confirming we got to Step 3 (step 10 in underlying file) 20150831 MB
cat(myZCompleteTest)
write.csv(myZCompleteTest, file="zzzStep10.csv")
