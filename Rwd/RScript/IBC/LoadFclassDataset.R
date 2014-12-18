#Make variable names accessible during session
#load  a csv text file, named lvinew
fclassFileName <- "FCLASS.csv"			#Enter file name and address for lvi dataset 
fclass <- read.csv(fclassFileName,header=T,row.names=1)	#Read file and put in R dataframe lvinew
attach(fclass)							#Attach variable names to each of the columns
fclassVarNames <- names(fclass)					#Print variable names in interpreter
nFclassRows <- length(fclass[,1])				#Count the number of rows or observations (for use in extracting variable subsets)

