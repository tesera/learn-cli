#Review correlations amongst variables
#Running Section 7 of the LVI manual

#####################################################################
#User Inputs
#
#Enter the path and name of file (with file extension) to be processed
lviFileName <- "D:\\Rwd\\WLREFFIN.csv"		
#
#Set Variable Selection File Name
xVarSelectFileName <- "D:\\Rwd\\XVARSELV1.csv"

#Select Variable Indicator Value
xVarSelectCriteria <- "X" 
#
#Enter the name of the correlation matrix print file (e.g.CORCOEF.csv)
printFileName<-"CORCOEF_VRI.csv"
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
source("D:\\Rwd\\RScript\\ZSelectXVariableSubset_v1.r")
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
source("D:\\Rwd\\RScript\\ZWriteUniqueVarCorrelationMatrix.r")
 