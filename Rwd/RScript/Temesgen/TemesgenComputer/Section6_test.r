#Running Section 6 of the LVI manual

#Set Working Directorty for each session
setwd("F:\\Rwd")
getwd()
save.image(file="OpenSession.RData")

source('F:\\Rwd\\RScript\\LoadDatasetAndAttachVariableNames.r')
#source('F:\\Rwd\\RScript\\SelectObservationSubset.r')
source('F:\\Rwd\\RScript\\DeclareClassificationVariableAsFactor.r')

#source('F:\\Rwd\\RScript\\ComputeUniformPriorClassProbilityDistribution.r')
source('F:\\Rwd\\RScript\\ComputeSamplePriorClassProbabilityDistribution.r')

source('F:\\Rwd\\RScript\\WritePriorDistributionToFile.r')
source('F:\\Rwd\\RScript\\LoadMASS-R-Package.r')

source('F:\\Rwd\\RScript\\SelectXVariableSubset_v2.1.r')
source('F:\\Rwd\\RScript\\RunMultipleLinearDiscriminantAnalysis_MASS_lda_TakeOneLeaveOne.r')
source('F:\\Rwd\\RScript\\WriteMultipleLinearDiscriminantAnalysis_MASS_lda_TOLO_to_File.r')

source('F:\\Rwd\\RScript\\RunMultipleLinearDiscriminantAnalysis_MASS_lda.r')
source('F:\\Rwd\\RScript\\WriteMultipleLinearDiscriminantAnalysis_MASS_lda.r')

system('python F:\\Rwd\\Python\\COHENS_KHAT.py')