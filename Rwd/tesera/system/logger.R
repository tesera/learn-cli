library("logging")
basicConfig()

Log <- function(var, file) {
	write.csv(var, file)
	loginfo(var)
}

LogInfo <- function(val) {
	loginfo(val)
}