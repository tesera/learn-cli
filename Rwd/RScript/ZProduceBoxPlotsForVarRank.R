#Make variable names accessible during session
#load  a csv text file, named lvinew
varRank <- read.csv(varRankFileName,header=T,row.names=1)	#Read file and put in R dataframe lvinew
attach(varRank)							#Attach variable names to each of the columns
varRankNames <- names(varRank)				#Print variable names in interpreter
nVarRankRows <- length(varRank[,1])				#Count the number of rows or observations (for use in extracting variable subsets)

order.varRank <- order(varRank$IMPORTANCE, decreasing=TRUE)

cat("\n There are the following numbr of variables in varRank: ", nVarRankRows)

print (varRankNames)
print (varRank[order.varRank,])

lapply (rownames(varRank[order.varRank[1:nVarRankRows],]), function (y){
  	old.par <- par(no.readonly = TRUE)
	on.exit(par(old.par))
	par("ask"=TRUE)
   	boxplot(lvinew[,y] ~ CLASSIFICATION,
           main = y)})

