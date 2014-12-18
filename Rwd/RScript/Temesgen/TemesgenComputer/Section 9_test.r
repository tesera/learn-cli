#Running Section 10 of the LVI manual
#Set Working Directorty for each session
setwd("F:\\Rwd")
getwd()
save.image(file="OpenSession.RData")

system('python F:\\Rwd\\Python\\COMBINE_EVALUATION_DATASETS.py')

data <- read.csv('F:\\Rwd\\ASSESS.csv')

dim(data)
names(data)
data$KHAT