CLASSIFICATION = factor(CLASS5)
uniqueVector = unique(CLASSIFICATION)
nClasses = length(uniqueVector)
priorStat = rep(1/nClasses,nClasses)
#Scatter plot matrix
require(lattice)
newData <- subset( as.data.frame(lvinew, select = c(B1_MEAN,B2_MEAN,B3_MEAN,B4_MEAN,B4_STDEV,B5_MEAN,
			B5_STDEV,LVI_LAISRS,LVI_PCA1S,LVI_PCA2S,LVI_NDVI43M,
			LVI_NDVI45S,LVI_NDVI73M,
			LVI_NDVI73S)))

#splom (newData, groups = CLASSIFICATION)
library(MASS)
#lvi.lda = lda(CLASSIFICATION~B1_MEAN+B2_MEAN+B3_MEAN+B4_MEAN+B4_STDEV+B5_MEAN+
#			B5_STDEV+LVI_LAISRS+LVI_PCA1S+LVI_PCA2S+LVI_NDVI43M+
#			LVI_NDVI45S+LVI_NDVI73M+LVI_NDVI73S, data = lvinew, prior = priorStat)
#Manual derivation (7 variables)
#lvi.lda = lda(CLASSIFICATION~B5_MEAN+B7_MEAN+LVI_LAISRM+LVI_NDVI35M+LVI_NDVI43M+
#			LVI_NDVI45M+LVI_WETM, data = lvinew, prior = priorStat)
#Using subselect - 7 variables
#lvi.lda = lda(CLASSIFICATION~B1_MEAN+B3_MEAN+B4_STDEV+B5_MEAN+
#			LVI_NDVI35M+LVI_NDVI45M+
#			LVI_NDVI73M, data = lvinew, prior = priorStat)
#lvi.lda = lda(CLASSIFICATION~B1_MEAN+B3_MEAN+B5_MEAN+
#			LVI_GREENS+LVI_NDVI35M+LVI_NDVI45M+
#			LVI_WETM, data = lvinew, prior = priorStat)
#lvi.lda = lda(CLASSIFICATION~B1_MEAN+B3_MEAN+B5_MEAN+
#			LVI_GREENS+LVI_NDVI35M+LVI_NDVI45M+
#			LVI_NDVI73M, data = lvinew, prior = priorStat)
lvi.lda = lda(CLASSIFICATION~B1_MEAN+B3_MEAN+B5_MEAN+
			LVI_GREENS+LVI_NDVI35M+LVI_NDVI43M+
			LVI_NDVI73M, data = lvinew, prior = priorStat)


#Using subselect - 5 variables
#lvi.lda = lda(CLASSIFICATION~B1_MEAN+B2_MEAN+LVI_GREENS+LVI_NDVI45M+
#			LVI_NDVI73M, data = lvinew, prior = priorStat)
#lvi.lda = lda(CLASSIFICATION~B1_MEAN+B2_MEAN+B5_STDEV+LVI_NDVI45M+
#			LVI_NDVI73M, data = lvinew, prior = priorStat)
#lvi.lda = lda(CLASSIFICATION~B1_MEAN+B3_MEAN+LVI_GREENS+LVI_NDVI45M+
#			LVI_NDVI73M, data = lvinew, prior = priorStat)

class.pred = predict(lvi.lda)
class.table = table(CLASSIFICATION, class.pred$class)
lda.temp = data.frame(class.pred$x, class = class.pred$class)
xyplot(LD1~LD2, data=lda.temp, groups = class, auto.key=list(title="CLASS"))
lvi.lda
