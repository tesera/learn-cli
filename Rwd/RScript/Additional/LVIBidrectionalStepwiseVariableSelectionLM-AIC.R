#Select the Landsat variables as the x variables
varSubset <- lvinew[, 16:27]
#Select the 5 class classification as the Y-variables
yVar <- lvinew[,102]
library(MASS)
CLASSIFICATION = factor(CLASS5)
fit <- lm(CLASSIFICATION ~ B1_MEAN + B1_STDEV + B2_MEAN + B2_STDEV + 
		B3_MEAN + B3_STDEV + B4_MEAN + B4_STDEV +
		B5_MEAN + B5_STDEV + B7_MEAN + B7_STDEV + LVI_LAIIRM +
		LVI_LAIIRS + LVI_LAISRM + LVI_LAISRS + LVI_PCA1M + LVI_PCA1S +
		LVI_PCA2M + LVI_PCA2S + LVI_NDVI35M + LVI_NDVI35S + LVI_NDVI43M + 
		LVI_NDVI43S + LVI_NDVI45M + LVI_NDVI45S + LVI_NDVI73M + 
		LVI_NDVI73S + LVI_BRIGHTM + LVI_BRIGHTS + LVI_GREENM + LVI_GREENS +
		LVI_WETM + LVI_WETS, data=lvinew)
		
step <- stepAIC(fit, direction="backward")
step$anova # display results
summary(step)

