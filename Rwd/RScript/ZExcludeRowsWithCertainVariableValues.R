if (excludeRowVarName %in% names(lvinew)) {
	if (excludeRowValue %in% lvinew[,excludeRowVarName]) {
		flog.info("Deleting selected rows from variable.")
		sel <- lvinew[excludeRowVarName]== excludeRowValue
		lvinew <- lvinew[!sel,]
		nLviRows <- length(lvinew[,1])
		flog.info("Remaining number of rows in dataframe: %s", nLviRows)
	}
}
