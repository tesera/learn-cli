dbh2 <- LNDG - log(450)
cxd <- dbh2 * LNMLOR
n = sfa(LNN ~ dbh2 + LNMLOR + cxd, data = cdiData, ineffDecrease = TRUE, truncNorm = FALSE, timeEffect = FALSE, startVal = NULL)
o = sfa(LNN ~ dbh2 + LNMLOR, data = cdiData, ineffDecrease = TRUE, truncNorm = FALSE, timeEffect = FALSE, startVal = NULL)

nTest <- lrtest(n)
