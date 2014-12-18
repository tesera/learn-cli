#Declare the variable indicating the classes associated with each observation as a factor
#This is used as the Y-variable in discriminant analysis
#
newClass <- unlist(lvinew[classVariableName])
CLASSIFICATION <- factor(newClass)
nclassObs <- length(CLASSIFICATION)
uniqueClasses = sort(unique(CLASSIFICATION))					#Get unique list of class names and sort them in order
classNumberList <- as.numeric(levels(uniqueClasses)[uniqueClasses])	#Convert factors back into a list of numbers
nClasses = length(uniqueClasses)							#Count the number of classes
cat(" There are the following number of classes in the classification: ", nClasses)
cat("\n There are the following number of factor observations: ", nclassObs)