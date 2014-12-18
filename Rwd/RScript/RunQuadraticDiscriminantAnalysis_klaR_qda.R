#Run discriminant analysis.
#CLASSIFICATION previously entered and defined as Factor
#XDataset previously extracted 
#priorDistribution defined using previous previous script.
#CV=TRUE produces results using leave-one-out-cross-validation.
#Paackage MASS has already been loaded prior to running this script.
#
#lda output statistics for CV = FALSE:
#lvi.lda$prior containins Prior probailities of groupsdeimen
#lvi.lda$counts contains the number of obesvations by class
#lvi.lda$means contains the means of the xVariables by class
#lvi.lda$scaling contains the discriminant function coefficients rescaled 
	#by the square root of the diagonal elements in the covariance matrix
#lvi.lda$svd are the ratios of between to within-group standard deviations in the linear discriminant variables
	#The squares of these figures are the canoxSelectnical F-statistics
#lvi.lda$N is the number of observations

lvi.lda = qda(xDataset,CLASSIFICATION,prior = priorDistribution, CV=FALSE)
class.pred = predict(lvi.lda)
class.table = table(CLASSIFICATION, class.pred$class)
