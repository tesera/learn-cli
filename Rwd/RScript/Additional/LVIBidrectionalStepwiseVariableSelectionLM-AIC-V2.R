#load  a csv text file, named lvinorm
lvinew <- read.csv("D:\\Rdata\\LVINEW.txt",header=T,row.names=1)
#Make variable names accessible during session
attach(lvinew)
#Print variable names
names(lvinew)
#Select the Landsat variables as the x variables
varSubset <- lvinew[, 16:27]
#Select the 5 class classification as the Y-variables
yVar <- lvinew[,102]
library(MASS)
CLASSIFICATION = factor(CLASS5)
fit <- lm(cbind(B1_MEAN,B1_STDEV,B2_MEAN,B2_STDEV, 
		B3_MEAN,B3_STDEV,B4_MEAN,B4_STDEV,B5_MEAN,B5_STDEV,
		B7_MEAN,B7_STDEV,LVI_LAIIRM,LVI_LAIIRS,LVI_LAISRM,LVI_LAISRS, 
		LVI_PCA1M,LVI_PCA1S,LVI_PCA2M,LVI_PCA2S,LVI_NDVI35M,LVI_NDVI35S,
		LVI_NDVI43M,LVI_NDVI43S,LVI_NDVI45M,LVI_NDVI45S,LVI_NDVI73M, 
		LVI_NDVI73S,LVI_BRIGHTM,LVI_BRIGHTS,LVI_GREENM,LVI_GREENS,
		LVI_WETM,LVI_WETS)~CLASSIFICATION, data = lvinew)
		
step <- stepAIC(fit, direction=c("both"))
#The following command shows the final model plus the variables that were
#added (+) or removed at each step(-)
step$anova # display results
summary(step)

