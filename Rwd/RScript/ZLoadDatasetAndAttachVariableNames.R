#Make variable names accessible during session
#load  a csv text file, named lvinew
lvinew <- read.csv(lviFileName,header=T,row.names=1)	#Read file and put in R dataframe lvinew
attach(lvinew)							#Attach variable names to each of the columns
lviVarNames <- names(lvinew)					#Print variable names in interpreter
nLviRows <- length(lvinew[,1])				#Count the number of rows or observations (for use in extracting variable subsets)
#lvinew.subset <- lvinew
cat(" lvinew has the following number of rows: ")
cat(nLviRows)
