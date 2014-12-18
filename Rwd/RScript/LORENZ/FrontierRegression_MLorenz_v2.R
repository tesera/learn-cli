a <- sfa(LNN ~ LNDG, data = cdiData, ineffDecrease = FALSE, truncNorm = FALSE, timeEffect = FALSE, startVal = NULL)
b <- sfa(LNN ~ LNDG + LNLMAX, data = cdiData, ineffDecrease = FALSE, truncNorm = FALSE, timeEffect = FALSE, startVal = NULL)
c <- sfa(LNN ~ LNDG + LNLMAX + LNDGLM, data = cdiData, ineffDecrease = FALSE, truncNorm = FALSE, timeEffect = FALSE, startVal = NULL)
d <- sfa(LNN ~ LNDG + LNLAREA, data = cdiData, ineffDecrease = FALSE, truncNorm = FALSE, timeEffect = FALSE, startVal = NULL)
e <- sfa(LNN ~ LNDG + LNLAREA + LNDGLA, data = cdiData, ineffDecrease = FALSE, truncNorm = FALSE, timeEffect = FALSE, startVal = NULL)
f <- sfa(LNN ~ LNDG + LNGINI, data = cdiData, ineffDecrease = FALSE, truncNorm = FALSE, timeEffect = FALSE, startVal = NULL)
g <- sfa(LNN ~ LNDG + LNGINI + LNDGGI, data = cdiData, ineffDecrease = FALSE, truncNorm = FALSE, timeEffect = FALSE, startVal = NULL)


aTest <- lrtest(a)
bTest <- lrtest(b)
cTest <- lrtest(c)
dTest <- lrtest(d)
eTest <- lrtest(e)
fTest <- lrtest(f)
gTest <- lrtest(g)


