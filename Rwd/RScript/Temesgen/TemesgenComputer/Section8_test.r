#Running Section 8 of the LVI manual
#Set Working Directorty for each session
setwd("F:\\Rwd")
getwd()
save.image(file="OpenSession.RData")

source('F:\\Rwd\\RScript\\LoadDatasetAndAttachVariableNames.r')
source('F:\\Rwd\\RScript\\SelectObservationSubset.r')
source('F:\\Rwd\\RScript\\DeclareClassificationVariableAsFactor.r')

source('F:\\Rwd\\RScript\\SelectUniqueXVariableSubet.r')  #modified to load data
source('F:\\Rwd\\RScript\\SelectXVariableSubset_v1.r')  #modified to load data
source('F:\\Rwd\\RScript\\SelectYVariableSubset_v1.r')  #DATA in XVARSELV1.csv
source('F:\\Rwd\\RScript\\LoadGraphics-R-Package.r')  #DATA in XVARSELV1.csv
source('F:\\Rwd\\RScript\\CreateUniqueVariableClassificationBoxPlots.r')
source('F:\\Rwd\\RScript\\CreateYVariableClassificationBoxPlots.r')	

source('F:\\Rwd\\RScript\\CreateUniqueVariableScatterPlots.r')

source('F:\\Rwd\\RScript\\SelectYVariableSubset_v1.r')
source('F:\\Rwd\\RScript\\SelectUniqueXVariableSubset.r')     #DATA in XVARSELV1

source('F:\\Rwd\\RScript\\SelectXVariableSubset_v1.r')
source('F:\\Rwd\\RScript\\CreateYvXVariableScatterPlots.r')      
 