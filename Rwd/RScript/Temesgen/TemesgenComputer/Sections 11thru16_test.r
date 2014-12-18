#Running Section 10 of the LVI manual
#Set Working Directorty for each session
setwd("F:\\Rwd")
getwd()
save.image(file="OpenSession.RData")

#Section 11
system('F:\\Rwd\\Phyton\\NN_ZSCORE.py')


#Section 12
system('F:\\Rwd\\Phyton\\NN_XDIST.py')

#Section 13
system('F:\\Rwd\\Phyton\\NN_YDIST.py')

data13 <- read.csv('F:\\Rwd\\Rdata\\Archived\\LVI\\Demo\\OutputFiles\\ASSESS.csv')


#Section 14
system('F:\\Rwd\\Phyton\\NN_TARG_REF.py')

data14 <- read.csv('F:\\Rwd\\Rdata\\Archived\\LVI\\Demo\\OutputFiles\\NNTARGET64.csv')
dim(data14)

#Section 15
system('F:\\Rwd\\Phyton\\COMPILE_NN_TARGET_YSTATS.py')


#Section 16
system('F:\\Rwd\\Phyton\\PIVOT_TABLE.py')
 