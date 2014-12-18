#Get a subset of observations
lvinew <- subset(lvinew, LVI_BECZ == 'SBPS')
attach(lvinew)
nLviRows <- length(lvinew[,1])