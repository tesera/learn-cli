#This script produces a barchart of the frequency distribution of classes
#Classes are identified as factors()
#load  a csv text file, named lvinorm
lvinew <- read.csv("D:\\Rdata\\LVINEW.txt",header=T,row.names=1)
#Make variable names accessible during session
attach(lvinew)
CLASSIFICATION = factor(CLASS10)
classificationLength = length(CLASSIFICATION)
columnNames = names(lvinew)
nColumns = length(columnNames)
colNames <- NULL
colLengths <- NULL
for (i in 1:nColumns)
{if (length(lvinew[,i])!=classificationLength)
	colNames <- c(colNames,columnNames[i])
{if (length(lvinew[,i])!=classificationLength)
	colLengths <- c(colLengths,length(lvinew[,i]))}}