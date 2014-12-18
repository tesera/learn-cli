#Running Section 8 of the LVI manual - Yvariable vs Classification Box Plots
#
#Set Working Directorty for each session
#setwd("D:\\Rwd")
#getwd()
#save.image(file="OpenSession.RData")

source('D:\\Rwd\\RScript\\LoadDatasetAndAttachVariableNames.r')
source('D:\\Rwd\\RScript\\DeclareClassificationVariableAsFactor.r')
source('D:\\Rwd\\RScript\\SelectYVariableSubset_v1.r')  #DATA in XVARSELV1.csv
source('D:\\Rwd\\RScript\\CreateYVariableClassificationBoxPlots.r')	
