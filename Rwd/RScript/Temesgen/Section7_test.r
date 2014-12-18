#Running Section 7 of the LVI manual
#Set Working Directorty for each session
#setwd("D:\\Rwd")
#getwd()
#save.image(file="OpenSession.RData")

source('D:\\Rwd\\RScript\\LoadDatasetAndAttachVariableNames.r')
#source('D:\\Rwd\\RScript\\SelectObservationSubset.r')

#UNIQUEVAR = read.csv('D:\\Rwd\\Rdata\\Archived\\LVI\\Demo\\OutputFiles\\UNIQUEVAR.csv')

source('D:\\Rwd\\RScript\\SelectUniqueXVariableSubset.r')  #modified to load data

source('D:\\Rwd\\RScript\\CompileUniqueXVariableCorrelationMatrixSubset.r')
source('D:\\Rwd\\RScript\\CreateUniqueVarCorrelationMatrixFileForPrinting.r')
source('D:\\Rwd\\RScript\\SelectXVariableSubset_v2.1.r')	#modified to load data
source('D:\\Rwd\\RScript\\AddVariableSubsetIndicatorsToCorrelationMatrix.r')
source('D:\\Rwd\\RScript\\WriteUniqueVarCorrelationMatrix.r')
 