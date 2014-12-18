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
#
# Enter the name of the correlation matrix print file 
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
#Variable Selection using xVarSelectFileName (UNIQUEVAR.csv)
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
source("D:\\Rwd\\RScript\\ZWriteCorrelationMatrix.r")
#
#Step 6
#Update XVARSELV1 to remove variable pairs with high correlation coeficients
system("C:\\Anaconda\\python.exe D:\\Rwd\\Python\\REMOVE_HIGHCORVAR_FROM_XVARSELV.py")
#
#Step 7 
# Count number of eligible X-Variables in XVARSELV1.csv
# Write to file XVARSELV1_COUNT
system("C:\\Anaconda\\python.exe D:\\Rwd\\Python\\COUNT_XVAR_IN_XVARSELV1.py")


 