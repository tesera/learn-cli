uniqueVector = unique(CLASSIFICATION)
nClasses = length(uniqueVector)
priorDistribution = rep(1/nClasses,nClasses)
