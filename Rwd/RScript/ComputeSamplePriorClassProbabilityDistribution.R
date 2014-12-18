uniqueVector = unique(CLASSIFICATION)
nClasses = length(uniqueVector)
classNames <- sort(uniqueVector)	#sort the class names or numbers and assign them to class names
nClasses = length(classNames)		#Compute total number of classes
nObs = length(CLASSIFICATION)		#Compute total number of observations
classCount = 0				#Initialize class count value
classP <- 0					#Initialize class proportion value
#
#Initialize classCount and classP vector
for (i in 1:(nClasses-1)) {
	classCount <- c(classCount,0)
	classP <- c(classP,0)
	}
#
#Calculate number of observations in each class
for (i in 1:nObs)
	for (j in 1:nClasses) {
		if (classNames[j] == CLASSIFICATION[i]) 
			classCount[j]<-classCount[j]+1
		}
#
#Calculate classP proportions for each class
for (i in 1:nClasses) {
	classP[i] = classCount[i]/nObs
	}
#
priorDistribution <- classP		#Initialize prior distribution


