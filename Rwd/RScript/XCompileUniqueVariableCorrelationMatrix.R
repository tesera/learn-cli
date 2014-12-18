#Review correlations amongst variables
#Running Section 7 of the LVI manual

#####################################################################
# User Inputs
#
# Enter the path and name of file (with file extension) to be processed
lviFileName <- "D:\\Rwd\\WLREFFIN.csv"		
#
# Enter the name of the unique variable selection file name and path
uniqueVarPath <- "D:\\Rwd\\UNIQUEVAR.csv"

#Enter the name of the correlation matrix print file 
# (this is to be defined as UCORCOEF.csv in this case without the file path)
# Results will be written to currently active R directory
printFileName<-"UCORCOEF.csv"
#
#End of user inputs
########################################################################
#Run routines
#
#Step 1
#Load dataset called lvinew
source("D:\\Rwd\\RScript\\ZLoadDatasetAndAttachVariableNames.r")
#
#Step 2
#Variable Selection using xVarSelectFileName (XVARSELV1.csv)
#according to criteria xVarSelectCriteria ("X")
source("D:\\Rwd\\RScript\\ZSelectUniqueXVariableSubset.r")
#
#Step 3
#Generate correlations amongst variables
source("D:\\Rwd\\RScript\\CompileUniqueXVariableCorrelationMatrixSubset.r")
#
#Step 4
#Create correlation matrix for printing
source("D:\\Rwd\\RScript\\CreateUniqueVarCorrelationMatrixFileForPrinting.r")
#
#Step 5
#Write correlation matrix R
source("D:\\Rwd\\RScript\\ZWriteUniqueCorrelationMatrix.r")
#


