#Produce boxplots
#This function creates 1 graph at a time with the y variables
#selected starting in columns 1 to 81 
lapply(names(lvinew[ , 1:81]), function(y) {
  	old.par <- par(no.readonly = TRUE)
	on.exit(par(old.par))
	par("ask"=TRUE)
   	boxplot(lvinew[, y] ~ CLASSIFICATION,
           main = y)})
