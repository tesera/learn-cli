#Running Section 8 of the LVI manual - Xvariable vs Classification Box Plots & X Variable Scatter Plots
#
#Set Working Directorty for each session
setwd("F:\\Rwd")
getwd()
save.image(file="OpenSession.RData")

source('F:\\Rwd\\RScript\\LoadDatasetAndAttachVariableNames.r')
#source('F:\\Rwd\\RScript\\SelectObservationSubset.r')
source('F:\\Rwd\\RScript\\DeclareClassificationVariableAsFactor.r')


source('F:\\Rwd\\RScript\\SelectUniqueXVariableSubset.r')  #modified to load data
source('F:\\Rwd\\RScript\\CreateUniqueVariableClassificationBoxPlots.r')
source('F:\\Rwd\\RScript\\CreateUniqueVariableScatterPlots.r')

 