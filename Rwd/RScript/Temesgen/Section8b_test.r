#Running Section 8 of the LVI manual - Test Y versus Unique X Variable Scatter Plots

#setwd("D:\\Rwd")
#getwd()
#save.image(file="OpenSession.RData")

source('D:\\Rwd\\RScript\\LoadDatasetAndAttachVariableNames.r')
source('D:\\Rwd\\RScript\\SelectUniqueXVariableSubset.r')  #modified to load data
source('D:\\Rwd\\RScript\\SelectYVariableSubset_v1.r')  #DATA in XVARSELV1.csv
source('D:\\Rwd\\RScript\\CreateYvXVariableScatterPlots.r')   