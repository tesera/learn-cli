#Do a one way Anova one variable at a time
yVarNames = names(yDataset)
lapply(names(yDataset[ , 1:2]), function(y) {
  	MV = lm(formula = yDataset[,y] ~ CLASSIFICATION,)
	summary(MV)
})
yVarNames
