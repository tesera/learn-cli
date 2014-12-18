#Running Section 8 of the LVI manual - Test Y versus Unique X Variable Scatter Plots

setwd("F:\\Rwd")
getwd()
save.image(file="OpenSession.RData")

source('F:\\Rwd\\RScript\\LoadDatasetAndAttachVariableNames.r')
source('F:\\Rwd\\RScript\\SelectUniqueXVariableSubset.r')  #modified to load data
source('F:\\Rwd\\RScript\\SelectYVariableSubset_v1.r')  #DATA in XVARSELV1.csv
source('F:\\Rwd\\RScript\\CreateYvXVariableScatterPlots.r')   