setwd("/opt/MRAT_Refactor/Rwd")
source(paste("/opt/MRAT_Refactor/etc/", "XIterativeVarSel.R.conf", sep = ""))
#testVar <- 6 + 6
#source(paste("/opt/MRAT_Refactor/bin/test_XIterativeVarSelCorVarElimination.R"))
source("/opt/MRAT_Refactor/Rwd/RScript/ZLoadDatasetAndAttachVariableNames.R")
step1 <- 3.1
write.csv(step1, file = "step1.csv")
testVar <- 6 + 6

