#Make variable names accessible during session
#load  a csv text file, named cdi
cdiFileName <- "D:\\Rwd\\TOLKOPLOTCDI_v2.csv"			#Enter file name and address for lvi dataset 
cdiData <- read.csv(cdiFileName,header=T,row.names=1)	#Read file and put in R dataframe lvinew
attach(cdiData)							#Attach variable names to each of the columns
cdiVarNames <- names(cdiData)					#Print variable names in interpreter
nCdiRows <- length(cdiData[,1])				#Count the number of rows or observations (for use in extracting variable subsets)

