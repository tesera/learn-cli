b <- sfa(LNN ~ LNDG, data = cdiData, ineffDecrease = TRUE, truncNorm = FALSE, timeEffect = FALSE, startVal = NULL)
bTest <- lrtest(b)
