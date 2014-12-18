#Running Section 5 of the LVI manual
#Set Working Directorty for each session
#setwd("F:\\Rwd")
#getwd()
#save.image(file="OpenSession.RData")

source('D:\\Rwd\\RScript\\LoadDatasetAndAttachVariableNames.r')
source('D:\\Rwd\\RScript\\SelectObservationSubset.r')
source('D:\\Rwd\\RScript\\DeclareClassificationVariableAsFactor.r')
#source('D:\\Rwd\\RScript\\ComputeUniformPriorClassProbilityDistribution.r')
source('D:\\Rwd\\RScript\\ComputeSamplePriorClassProbabilityDistribution.r')

#source('D:\\Rwd\\RScript\\SelectXVariableSubset_v1.r')
source('D:\\Rwd\\RScript\\SelectXVariableSubset_v2.r')

source('D:\\Rwd\\RScript\\LoadMASS-R-Package.r')
source('D:\\Rwd\\RScript\\RunLinearDiscriminantAnalysis_MASS_lda.r')
source('D:\\Rwd\\RScript\\RunLinearDiscriminantAnalysis_MASS_lda_TakeOneLeaveOne.r')

