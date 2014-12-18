#Make variable names accessible during session
#load  a csv text file, named lvinew
ibcFileName <- "MONCTON_ANALYSIS.csv"			#Enter file name and address for lvi dataset 
ibcnew <- read.csv(ibcFileName,header=T,row.names=1)	#Read file and put in R dataframe lvinew
attach(ibcnew)							#Attach variable names to each of the columns
ibcVarNames <- names(ibcnew)					#Print variable names in interpreter
nIbcRows <- length(ibcnew[,1])				#Count the number of rows or observations (for use in extracting variable subsets)
#lvinew.subset <- lvinew
