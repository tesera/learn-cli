#Run take-one-leave-one discriminant analysis
#CLASSIFICATION previously entered and defined as Factor
#XDataset previously extracted 
#priorDistribution defined using previous previous script.
#CV=TRUE produces results using leave-one-out-cross-validation.
# 
#Paackage MASS has already been loaded prior to running this script.
#
#lda output statistics for CV = TRUE
#lvi.lda$class containins the predicted class
#lvi.lad$posterior contains the posterior probability assigned to each class-observation combination
#
lvi.lda = lda(xDataset,CLASSIFICATION,prior = priorDistribution, CV=TRUE)
#
#
class.pred = lvi.lda$class
class.table = table(CLASSIFICATION,class.pred)

