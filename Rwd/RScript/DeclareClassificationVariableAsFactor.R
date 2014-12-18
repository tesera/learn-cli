#Declare the variable indicating the classes associated with each observation as a factor
#This is used as the Y-variable in discriminant analysis
#
CLASSIFICATION = factor(CLASS5)							#CLASS5 is a variable name in lvinew with numeric class labels; this may be changed
uniqueClasses = sort(unique(CLASSIFICATION))					#Get unique list of class names and sort them in order
classNumberList <- as.numeric(levels(uniqueClasses)[uniqueClasses])	#Convert factors back into a list of numbers
nClasses = length(uniqueClasses)							#Count the number of classes