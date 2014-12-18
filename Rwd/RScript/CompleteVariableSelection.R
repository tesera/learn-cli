#Run Discriminant Analysis Variable Selection Procedure

#####################################################################
#User Inputs
#
#Enter the path and name of file (with file extension) to be processed
lviFileName <- "D:\\Rwd\\WLREFFIN.csv"						

#Enter a variable name and variable value to exclude rows from a dataset
#If the variable name is not in the dataset then no rows will be excluded
excludeRowValue = 1
excludeRowVarName = 'SORTGRP'

#Enter classification variable name to be used as Y-Variable in Discriminant Analysis 
CLASSIFICATION = factor(CLASS5)

#Set Variable Selection File Name
xVarSelectFileName <- "D:\\Rwd\\XVARSELV1.csv"

#Select Variable Indicator Value
xVarSelectCriteria <- "X" 

End of User Input
#####################################################################
#Run routines
#
#Step 1
#Load dataset called lvinew
source('D:\\Rwd\\RScript\\ZLoadDatasetAndAttachVariableNames.r')
#
#Step 2
#Exclude rows with excludeRowValue associated with excludeRowVarName
source('D:\\Rwd\\RScript\\ZExcludeRowsWithCertainVariableValues.r')
#
#Step 3
#Declare classification variable as Factor (i.e. identify variable as classification variable)
source('D:\\Rwd\\RScript\\ZDeclareClassificationVariableAsFactor.r')
#
#Step 4
#Variable Selection using xVarSelectFileName (XVARSELV1.csv)
#according to criteria xVarSelectCriteria ("X")
source('D:\\Rwd\\RScript\\ZSelectXVariableSubset_v1.r')
#
#Step 5
#Remove variables with 0 standard deviation
source('D:\\Rwd\\RScript\\ZRemoveVariablesWithZeroStandardDeviation.r')


#source('D:\\Rwd\\RScript\\Loadsubselect-R-Package.r')

#source('D:\\Rwd\\RScript\\RunLinearDiscriminantAnalysis_subselect_ldaHmat.r')

#source('D:\\Rwd\\RScript\\Run-ldaHmat-VariableSelection-Improve.r')
	  
#source('D:\\Rwd\\RScript\\ExtractVariableNameSubsets.r')

#source('D:\\Rwd\\RScript\\WriteDataframeToCsvFile.r')

#system('python D:\\Rwd\\Python\\EXTRACT_RVARIABLE_COMBOS.py')             #To import a Phyton executable
	  
#system('python -c "import sys; sys.stdout.write(file('D:\\Rwd\\Python\\EXTRACT_RVARIABLE_COMBOS_v2.py\\', \'r\')  #To write out the phyton codes
