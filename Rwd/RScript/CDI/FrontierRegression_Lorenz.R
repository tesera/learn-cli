a <- sfa(LNN ~ LNDG + LNLOR, data = cdiData, ineffDecrease = TRUE, truncNorm = FALSE, timeEffect = FALSE, startVal = NULL)
b <- sfa(LNN ~ LNDG, data = cdiData, ineffDecrease = TRUE, truncNorm = FALSE, timeEffect = FALSE, startVal = NULL)
c <- sfa(LNN ~ LNDG + LNLOR + LNDGCDI, data = cdiData, ineffDecrease = TRUE, truncNorm = FALSE, timeEffect = FALSE, startVal = NULL)
#d is eliminated
#d = sfa(LNN ~ LNLOR + LNDGLOR, data = cdiData, ineffDecrease = TRUE, truncNorm = FALSE, timeEffect = FALSE, startVal = NULL)
e <- sfa(LNN ~ LNDG + LNDGLOR, data = cdiData, ineffDecrease = TRUE, truncNorm = FALSE, timeEffect = FALSE, startVal = NULL)


f = sfa(LNG ~ LNDGLOR, data = cdiData, ineffDecrease = TRUE, truncNorm = FALSE, timeEffect = FALSE, startVal = NULL)
g = sfa(LNG ~ LNLOR + LNDGLOR, data = cdiData, ineffDecrease = TRUE, truncNorm = FALSE, timeEffect = FALSE, startVal = NULL)
h = sfa(LNG ~ LNLOR + LNDGLOR + LNDG, data = cdiData, ineffDecrease = TRUE, truncNorm = FALSE, timeEffect = FALSE, startVal = NULL)
i = sfa(LNG ~ LNLOR + LNDG, data = cdiData, ineffDecrease = TRUE, truncNorm = FALSE, timeEffect = FALSE, startVal = NULL)
j = sfa(LNG ~ LNDGLOR + LNDG, data = cdiData, ineffDecrease = TRUE, truncNorm = FALSE, timeEffect = FALSE, startVal = NULL)
#k = sfa(LNG ~ LNDG, data = cdiData, ineffDecrease = TRUE, truncNorm = FALSE, timeEffect = FALSE, startVal = NULL)

l = sfa(LNN ~ LNDG2LOR, data = cdiData, ineffDecrease = TRUE, truncNorm = FALSE, timeEffect = FALSE, startVal = NULL)
m = sfa(LNN ~ LNLOR + LNDG2, data = cdiData, ineffDecrease = TRUE, truncNorm = FALSE, timeEffect = FALSE, startVal = NULL)
n = sfa(LNN ~ LNDG2 + LNDG2LOR, data = cdiData, ineffDecrease = TRUE, truncNorm = FALSE, timeEffect = FALSE, startVal = NULL)
o = sfa(LNN ~ LNDG2, data = cdiData, ineffDecrease = TRUE, truncNorm = FALSE, timeEffect = FALSE, startVal = NULL)

p = sfa(LNLOR ~ LNDG2 + LNNDG2, data = cdiData, ineffDecrease = TRUE, truncNorm = FALSE, timeEffect = FALSE, startVal = NULL)
q = sfa(LNLOR ~ LNDG2, data = cdiData, ineffDecrease = TRUE, truncNorm = FALSE, timeEffect = FALSE, startVal = NULL)
r = sfa(LNLOR ~ LNDG + LNN, data = cdiData, ineffDecrease = TRUE, truncNorm = FALSE, timeEffect = FALSE, startVal = NULL)
s = sfa(LNLOR ~ LNDG2 + LNN + LNNDG2, data = cdiData, ineffDecrease = TRUE, truncNorm = FALSE, timeEffect = FALSE, startVal = NULL)



aTest <- lrtest(a)
bTest <- lrtest(b)
cTest <- lrtest(c)
eTest <- lrtest(e)
fTest <- lrtest(f)
gTest <- lrtest(g)
hTest <- lrtest(h)
iTest <- lrtest(i)
jTest <- lrtest(j)
#kTest <- lrtest(k)
lTest <- lrtest(l)
mTest <- lrtest(m)
nTest <- lrtest(n)
oTest <- lrtest(o)
pTest <- lrtest(p)
qTest <- lrtest(q)
rTest <- lrtest(r)
sTest <- lrtest(s)

# i is the best choice for maximum basal area
# a is the best choice for maximum number of stems per hectare
# optimization problem is to find for a give cdi, a dg that minimizes the error of estimation in dg given maximum G and maximum N