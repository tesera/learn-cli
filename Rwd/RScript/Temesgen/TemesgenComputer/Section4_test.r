#Running Section 4 of the LVI manual

#Set Working Directorty for each session
setwd("F:\\Rwd")
getwd()
save.image(file="OpenSession.RData")

#source('F:\\Rwd\\RScript\\installPackages.r')
source('F:\\Rwd\\RScript\\LoadDatasetAndAttachVariableNames.r')
nLviRows

#Optional
#source('F:\\Rwd\\RScript\\SelectObservationSubset.r')  
#nLviRows

source('F:\\Rwd\\RScript\\DeclareClassificationVariableAsFactor.r')
nClasses

source('F:\\Rwd\\RScript\\SelectXVariableSubset_v1.r')
XVARSEL

source('F:\\Rwd\\RScript\\Loadsubselect-R-Package.r')

source('F:\\Rwd\\RScript\\RunLinearDiscriminantAnalysis_subselect_ldaHmat.r')

source('F:\\Rwd\\RScript\\Run-ldaHmat-VariableSelection-Improve.r')
	  
source('F:\\Rwd\\RScript\\ExtractVariableNameSubsets.r')

source('F:\\Rwd\\RScript\\WriteDataframeToCsvFile.r')

system('python F:\\Rwd\\Python\\EXTRACT_RVARIABLE_COMBOS.py')             #To import a Phyton executable
	  
#system('python -c "import sys; sys.stdout.write(file('D:\\Rwd\\Python\\EXTRACT_RVARIABLE_COMBOS_v2.py\\', \'r\')  #To write out the phyton codes
