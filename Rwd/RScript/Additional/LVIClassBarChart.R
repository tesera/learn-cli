classNames = unique(CLASSIFICATION)		#Get uniqe list of class names
classNames <- sort(classNames)		#Sort class names
nClasses <- length(classNames)		#Calculate number of classes
nObs = length(CLASSIFICATION)			#Calculate number of observations
classCount = 0					#Initialize class count vector
#
#Initialize nClasses vector with 0 for each class
for (i in 1:(nClasses-1)) {	
	classCount <- c(classCount,0)
	}
#
#Calculate number of observations in each class
for (i in 1:nObs)
	for (j in 1:nClasses) {
		if (classNames[j] == CLASSIFICATION[i]) 
			classCount[j]<-classCount[j]+1
		}
#
#Make bar chart
barplot(classCount, main = "Histogram", xlab = "Classes", ylab = "Nobs",
names.arg = classNames, col = rainbow(length(classCount)))
