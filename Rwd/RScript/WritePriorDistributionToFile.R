PRIOR <- cbind.data.frame(CLASS = classNames,PRIORD = priorDistribution)
write.csv(PRIOR,file="PRIOR.csv", row.names=FALSE,na="")
