#Produce boxplots
#This function creates 1 graph at a time with the y variables
#
yDataLength <- length(yDataset[1,])
lapply(names(yDataset[ , 1:yDataLength]), function(y) {
  	old.par <- par(no.readonly = TRUE)
	on.exit(par(old.par))
	par("ask"=TRUE)
   	boxplot(yDataset[, y] ~ CLASSIFICATION,
           main = y)})
