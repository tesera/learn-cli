#Assign CLASS5 as a classification variable using the factor() function
CLASSIFICATION = factor(CLASS5)
#Get unique class name values
classNames = unique(CLASSIFICATION)
varNames = names(lvinew)
#Do pairwise t-tests one variable at a time
lapply(names(lvinew[ , 1:85]), function(y) 
	{pairwise.t.test(lvinew[,y],CLASSIFICATION)
	})
varNames