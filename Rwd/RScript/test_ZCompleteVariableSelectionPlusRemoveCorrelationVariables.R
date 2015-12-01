library('devtools')
install('DiscriminantAnalysisVariableSelection')
library('DiscriminantAnalysisVariableSelection')

# Run Discriminant Analysis Variable Selection Procedure
vs.DiscriminantAnalysisVariableSelection(lviFileName, xVarSelectFileName, "VARSELECT.csv")

#An arbitrary expression
myZCompleteTest<- "Did we get to step 10" 