#setwd("/opt/MRAT_Refactor/Rwd")
#source(paste("/opt/MRAT_Refactor/etc/", "XIterativeVarSel.R.conf", sep = ""))
newtestVar <- 7 + 7
#source(paste("/opt/MRAT_Refactor/bin/test_XIterativeVarSelCorVarElimination.R"))
#source("/opt/MRAT_Refactor/Rwd/RScript/ZLoadDatasetAndAttachVariableNames.R")
step211 <- newtestVar
write.csv(step211, file = "step211.csv")
source("/opt/MRAT_Refactor/Rwd/RScript/test_ZReadXvarselvCount.R")
#xVarCount <- scan("/opt/MRAT_Refactor/Rwd/XVARSELV1_XCOUNT.csv")
step222 <- xVarCount
write.csv(step222, file ="/opt/MRAT_Refactor/Rwd/step222.csv")
