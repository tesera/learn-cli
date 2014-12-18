#Running Section 8 of the LVI manual - Yvariable vs Classification Box Plots
#
#Set Working Directorty for each session
setwd("F:\\Rwd")
getwd()
save.image(file="OpenSession.RData")

source('F:\\Rwd\\RScript\\LoadDatasetAndAttachVariableNames.r')
source('F:\\Rwd\\RScript\\DeclareClassificationVariableAsFactor.r')
source('F:\\Rwd\\RScript\\SelectYVariableSubset_v1.r')  #DATA in XVARSELV1.csv
source('F:\\Rwd\\RScript\\CreateYVariableClassificationBoxPlots.r')	
