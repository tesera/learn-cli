#Running Section 4 of the LVI manual

Set Working Directorty for each session
setwd("D:\\Rwd")
getwd()
save.image(file="OpenSession.RData")

#source('D:\\Rwd\\RScript\\installPackages.r')
source('D:\\Rwd\\RScript\\LoadDatasetAndAttachVariableNames.r')
nLviRows

#Optional
#source('D:\\Rwd\\RScript\\SelectObservationSubset.r')  
#nLviRows

source('D:\\Rwd\\RScript\\DeclareClassificationVariableAsFactor.r')
nClasses

source('D:\\Rwd\\RScript\\SelectXVariableSubset_v1.r')
XVARSEL

source('D:\\Rwd\\RScript\\Loadsubselect-R-Package.r')

source('D:\\Rwd\\RScript\\RunLinearDiscriminantAnalysis_subselect_ldaHmat.r')

source('D:\\Rwd\\RScript\\Run-ldaHmat-VariableSelection-Improve.r')
	  
source('D:\\Rwd\\RScript\\ExtractVariableNameSubsets.r')

source('D:\\Rwd\\RScript\\WriteDataframeToCsvFile.r')

system('python D:\\Rwd\\Python\\EXTRACT_RVARIABLE_COMBOS.py')             #To import a Phyton executable
	  
#system('python -c "import sys; sys.stdout.write(file('D:\\Rwd\\Python\\EXTRACT_RVARIABLE_COMBOS_v2.py\\', \'r\')  #To write out the phyton codes
