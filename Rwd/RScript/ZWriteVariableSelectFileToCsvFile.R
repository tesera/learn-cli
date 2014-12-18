cat(" Writing list of variable selections to VARSELECT.csv.") 
write.csv(SOLSUM,file="VARSELECT.csv", row.names=FALSE,na="")

