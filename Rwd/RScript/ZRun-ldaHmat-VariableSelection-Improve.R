#Analyze the xDataset to determine best variable subsets using leaps and bounds (improve) algorithm
#
lviHmat <- ldaHmat(xDataset,CLASSIFICATION)	#Set X and Y variables, where Y variables are classification sets
lviVariableSets <- improve(lviHmat$mat, kmin = minNvar, kmax = maxNvar, nsol=nSolutions, H=lviHmat$H, r=lviHmat$r, crit=criteria, force=TRUE, setseed = true)
#
cat(" Results from subselect improve variable selection process.")
lviVariableSets						#Print results
