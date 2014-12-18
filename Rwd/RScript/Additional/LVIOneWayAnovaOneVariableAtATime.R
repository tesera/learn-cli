#load  a csv text file, named lvinorm
lvinew <- read.csv("D:\\Rdata\\LVINEW.txt",header=T,row.names=1)
#Make variable names accessible during session
attach(lvinew)
#Print variable names
names(lvinew)
#Assign CLASS5 as a classification variable using the factor() function
CLASSIFICATION = factor(CLASS5)
#Get library MASS
library(MASS)
#Do a one way Anova one variable at a time
lapply(names(lvinew[ , 1:85]), function(y) {
  	MV = lm(formula = lvinew[,y] ~ CLASSIFICATION,)
	summary(MV)
})