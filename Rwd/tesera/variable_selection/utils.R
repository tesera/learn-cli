SetInitialCount <- function() {
	assign("initialCount", scan(xVarCountFileName), envir = .GlobalEnv)
}
