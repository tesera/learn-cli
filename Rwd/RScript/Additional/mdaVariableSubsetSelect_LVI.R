CLASSIFICATION = factor(CLASS5)
uniqueVector = unique(CLASSIFICATION)
library(subselect)
lviHmat <- ldaHmat(cbind(B1_MEAN,B1_STDEV,B2_MEAN,B2_STDEV, 
		B3_MEAN,B3_STDEV,B4_MEAN,B4_STDEV,B5_MEAN,B5_STDEV,
		B7_MEAN,B7_STDEV,LVI_LAIIRM,LVI_LAIIRS,LVI_LAISRM,LVI_LAISRS, 
		LVI_PCA1M,LVI_PCA1S,LVI_PCA2M,LVI_PCA2S,LVI_NDVI35M,LVI_NDVI35S,
		LVI_NDVI43M,LVI_NDVI43S,LVI_NDVI45M,LVI_NDVI45S,LVI_NDVI73M, 
		LVI_NDVI73S,LVI_BRIGHTM,LVI_BRIGHTS,LVI_GREENM,LVI_GREENS,
		LVI_WETM,LVI_WETS),CLASSIFICATION)
#Maximize Roy's first root statistic (i.e. largest eigenvalue of HE^(-1) where His the effects matrix and E the error residual
#improve(lviHmat$mat, kmin = 5, kmax = 5, nsol=5, H=lviHmat$H, r=lviHmat$r, crit="ccr12")
#
#Minimize Wilks Lamda where lamda = det(E)/det(T) where E is the error matrix and T is the total variance  
#improve(lviHmat$mat, kmin = 5, kmax = 5, nsol=5, H=lviHmat$H, r=lviHmat$r, crit="Wilks")
#
#Maximize the Chi squared (xi2) index based on the Bartle-Pillai trace test statistic, P
#P = trace(HT^(-1)) where H is effects suns iof squares cross products and T is total sums of squares cross products
#xi2 = P/r where r is the matrix rank
improve(lviHmat$mat, kmin = 5, kmax = 10, nsol=5, H=lviHmat$H, r=lviHmat$r, crit="xi2")

#Maximize Zeta2 (zeta2) coefficient where V = trace(HE^(-1)) and zeta2 = V/(V+r) where r is rank
#improve(lviHmat$mat, kmin = 5, kmax = 5, nsol=5, H=lviHmat$H, r=lviHmat$r, crit="zeta2")

