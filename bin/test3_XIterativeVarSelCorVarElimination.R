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
#333 BETTER TO USE pwd TO SET THIS, BUT RStudio is REPORTING THE ORIGINAL DIR NOT THE CURRENT
#333 FIGURE THAT OUT

#####################################################################
# Step 1
# Initialize count of eligible X-Variables in XVARSELV1.csv
# Write to file XVARSELV1_COUNT
#333 This Python call should be removed from [R] and handled directly by the Python controlling script
# commenting out the following commands in this step 20150828 by MB and SK

#COMMAND <- paste("/usr/bin/python2 ",HOME_BIN,"COUNT_XVAR_IN_XVARSELV1.py", sep="")
#print(paste("COMMAND = ",COMMAND)) #3333
#system(COMMAND)

#####################################################################
# Step 2
# Read XVARSELV1_XCOUNT

#source(paste(HOME_RWD,"RScript/test_ZReadXvarselvCount.R", sep = ""))
#initialCount <- xVarCount
#write.csv(initialCount, file = "zzz.csv") #SK added 20150901 - this works

#####################################################################

#Step 3A TEST 20150831 -- See if Data frame can be passed
#source("/opt/MRAT_Refactor/Rwd/RScript/ZLoadDatasetAndAttachVariableNames.R")



# Step 3
# Initialize Variable selection process
#20150831 Add test_ to ZCompleteVariableSelectionPlusRemoveCorrelationVariables.R MB, IM, SK
#source(paste(HOME_RWD,"RScript/test_ZCompleteVariableSelectionPlusRemoveCorrelationVariables.R", sep = ""))
#source(paste(HOME_RWD,"RScript/test_ZReadXvarselvCount.R", sep = "")) commented out 20150915 SK MB
#xVarCount <- scan("/opt/MRAT_Refactor/Rwd/XVARSELV1_XCOUNT.csv")
#step21 <- xVarCount
#write.csv(step21, file = "myStep21.csv")

#Confirming we got to Step 3 (step 10 in underlying file) 20150831 MB
#cat(myZCompleteTest)
#write.csv(myZCompleteTest, file="zzzStep10.csv")


#####################################################################
# Step 4
#repeat {
#	if (initialCount == xVarCount) {
#		break
#		} else {
#		initialCount <- xVarCount
#		}
#	source(paste(HOME_RWD,"RScript/ZCompleteVariableSelectionPlusRemoveCorrelationVariables.R", sep = ""))
#	source(paste(HOME_RWD,"RScript/ZReadXvarselvCount.R", sep = ""))
#	}
#

#20150831 MB, IM, SK A test to see if script has gotten this far
#print("myZCompleteTest")
