#Author: Ian Moss
# Modified by: Ian Moss, Sam Kaharabata & Mishtu Banerjee
#Updated 20150918 MB, SK
#Maintainers: Sam Kaharabata, Mishtu Banerjee, Ian Moss

# Copyright: The Author(s)
#License: Distributed under MIT License
#    [http://opensource.org/licenses/mit-license.html]

#####################################################################
# This is the final step in X Iterative Variable Selection
#setwd("/opt/MRAT_Refactor/Rwd")
#source(paste("/opt/MRAT_Refactor/etc/", "XIterativeVarSel.R.conf", sep = ""))
source("/opt/MRAT_Refactor/Rwd/RScript/test_ZReadXvarselvCount.R")
#xVarCount <- scan("/opt/MRAT_Refactor/Rwd/XVARSELV1_XCOUNT.csv")
step222 <- xVarCount
write.csv(step222, file ="/opt/MRAT_Refactor/Rwd/step222.csv")
