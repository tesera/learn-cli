if (excludeRowVarName %in% names(lvinew)) {
	if (excludeRowValue %in% lvinew[,excludeRowVarName]) {
		cat(" Deleting selected rows from variable. \n RemainingNumber of rows in dataframe: ")
		sel <- lvinew[excludeRowVarName]== excludeRowValue
		lvinew <- lvinew[!sel,]
		nLviRows <- length(lvinew[,1])
		cat(nLviRows)
		}
	}
