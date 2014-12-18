#Running Section 8 of the LVI manual - Xvariable vs Classification Box Plots & X Variable Scatter Plots
#
#Set Working Directorty for each session
#setwd("D:\\Rwd")
#getwd()
#save.image(file="OpenSession.RData")

source('D:\\Rwd\\RScript\\LoadDatasetAndAttachVariableNames.r')
#source('D:\\Rwd\\RScript\\SelectObservationSubset.r')
source('D:\\Rwd\\RScript\\DeclareClassificationVariableAsFactor.r')


source('D:\\Rwd\\RScript\\SelectUniqueXVariableSubset.r')  #modified to load data
source('D:\\Rwd\\RScript\\CreateUniqueVariableClassificationBoxPlots.r')
source('D:\\Rwd\\RScript\\CreateUniqueVariableScatterPlots.r')

 