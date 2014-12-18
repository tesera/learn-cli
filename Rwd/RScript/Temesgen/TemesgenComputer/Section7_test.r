#Running Section 7 of the LVI manual
#Set Working Directorty for each session
setwd("F:\\Rwd")
getwd()
save.image(file="OpenSession.RData")

source('F:\\Rwd\\RScript\\LoadDatasetAndAttachVariableNames.r')
#source('F:\\Rwd\\RScript\\SelectObservationSubset.r')

#UNIQUEVAR = read.csv('F:\\Rwd\\Rdata\\Archived\\LVI\\Demo\\OutputFiles\\UNIQUEVAR.csv')

source('F:\\Rwd\\RScript\\SelectUniqueXVariableSubset.r')  #modified to load data

source('F:\\Rwd\\RScript\\CompileUniqueXVariableCorrelationMatrixSubset.r')
source('F:\\Rwd\\RScript\\CreateUniqueVarCorrelationMatrixFileForPrinting.r')
source('F:\\Rwd\\RScript\\SelectXVariableSubset_v2.1.r')	#modified to load data
source('F:\\Rwd\\RScript\\AddVariableSubsetIndicatorsToCorrelationMatrix.r')
source('F:\\Rwd\\RScript\\WriteUniqueVarCorrelationMatrix.r')
 