#Produce boxplots
#This function creates 1 graph at a time with the y variables
#
xDataLength <- length(xDataset[1,])
lapply(names(xDataset[ , 1:xDataLength]), function(y) {
  	old.par <- par(no.readonly = TRUE)
	on.exit(par(old.par))
	par("ask"=TRUE)
   	boxplot(xDataset[, y] ~ CLASSIFICATION,
           main = y)})
