#Running Section 10 of the LVI manual
#Set Working Directorty for each session
#setwd("F:\\Rwd")
#getwd()
#save.image(file="OpenSession.RData")

source('D:\\Rwd\\RScript\\LoadDatasetAndAttachVariableNames.r')
#source('D:\\Rwd\\RScript\\SelectObservationSubset.r')
source('D:\\Rwd\\RScript\\DeclareClassificationVariableAsFactor.r')

#source('D:\\Rwd\\RScript\\ComputeUniformPriorClassProbilityDistribution.r')
source('D:\\Rwd\\RScript\\ComputeSamplePriorClassProbabilityDistribution.r')

source('D:\\Rwd\\RScript\\SelectXVariableSubset_v1.r')

source('D:\\Rwd\\RScript\\LoadklaR-R-Package.r')
source('D:\\Rwd\\RScript\\LoadCombinat-R-Package.r')
source('D:\\Rwd\\RScript\\RunLinearDiscriminantAnalysis_klaR_pvs.r')
