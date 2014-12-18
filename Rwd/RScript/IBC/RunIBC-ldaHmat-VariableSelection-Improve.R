minNvar <- 5				#Set the minimumn number of variables
maxNvar <- 5				#Set the maximum number of variables
nSolutions <- 5				#Set the number of solutions for each N number of variables
#Set the criteria for selecting variables
#criteria <- "ccr12"			#Maximize Roy's first root statistic (i.e. largest eigenvalue of HE^(-1) where His the effects matrix and E the error residual
#criteria <- "Wilkes"			#Minimize Wilks Lamda where lamda = det(E)/det(T) where E is the error matrix and T is the total variance 
criteria <- "xi2"				#Maximize the Chi squared (xi2) index based on the Bartle-Pillai trace test statistic, P
#criteria <- "zeta2"			#Maximize Zeta2 (zeta2) coefficient where V = trace(HE^(-1)) and zeta2 = V/(V+r) where r is rank
#
#Analyze the xDataset to determine best variable subsets using leaps and bounds (improve) algorithm
#
ibcHmat <- ldaHmat(xDataset,CLASSIFICATION)	#Set X and Y variables, where Y variables are classification sets
ibcVariableSets <- improve(ibcHmat$mat, kmin = minNvar, kmax = maxNvar, nsol=nSolutions, H=ibcHmat$H, r=ibcHmat$r, crit=criteria)
#
ibcVariableSets				#Print results