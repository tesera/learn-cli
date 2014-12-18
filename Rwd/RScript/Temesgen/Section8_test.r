#Running Section 8 of the LVI manual
#Set Working Directorty for each session
#setwd("D:\\Rwd")
#getwd()
#save.image(file="OpenSession.RData")

source('D:\\Rwd\\RScript\\LoadDatasetAndAttachVariableNames.r')
source('D:\\Rwd\\RScript\\SelectObservationSubset.r')
source('D:\\Rwd\\RScript\\DeclareClassificationVariableAsFactor.r')

source('D:\\Rwd\\RScript\\SelectUniqueXVariableSubset.r')  #modified to load data
source('D:\\Rwd\\RScript\\CreateUniqueVariableClassificationBoxPlots.r')
source('D:\\Rwd\\RScript\\CreateUniqueVariableScatterPlots.r')

#source('D:\\Rwd\\RScript\\SelectXVariableSubset_v1.r')  #modified to load data
source('D:\\Rwd\\RScript\\SelectYVariableSubset_v1.r')  #DATA in XVARSELV1.csv
source('D:\\Rwd\\RScript\\LoadGraphics-R-Package.r')  #DATA in XVARSELV1.csv
source('D:\\Rwd\\RScript\\CreateYVariableClassificationBoxPlots.r')	


#source('D:\\Rwd\\RScript\\SelectYVariableSubset_v1.r')
#source('D:\\Rwd\\RScript\\SelectUniqueXVariableSubset.r')     #DATA in XVARSELV1

#source('D:\\Rwd\\RScript\\SelectXVariableSubset_v1.r')
source('D:\\Rwd\\RScript\\CreateYvXVariableScatterPlots.r')      
 