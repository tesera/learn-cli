 #Running Section 5 of the LVI manual
#Set Working Directorty for each session
setwd("F:\\Rwd")
getwd()
save.image(file="OpenSession.RData")

source('F:\\Rwd\\RScript\\LoadDatasetAndAttachVariableNames.r')
source('F:\\Rwd\\RScript\\SelectObservationSubset.r')
source('F:\\Rwd\\RScript\\DeclareClassificationVariableAsFactor.r')
source('F:\\Rwd\\RScript\\ComputeUniformPriorClassProbilityDistribution.r')
source('F:\\Rwd\\RScript\\ComputeSamplePriorClassProbabilityDistribution.r')

source('F:\\Rwd\\RScript\\SelectXVariableSubset_v1.r')
source('F:\\Rwd\\RScript\\SelectXVariableSubet_v2.r')

source('F:\\Rwd\\RScript\\LoadMASS-R-Package.r')
source('F:\\Rwd\\RScript\\RunLinearDiscriminantAnalysis_MASS_lda.r')
source('F:\\Rwd\\RScript\\RunLinearDiscriminantAnalysis_MASS_lda_TakeOneLeaveOne.r')

