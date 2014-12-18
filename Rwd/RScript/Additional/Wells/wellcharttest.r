# This is a test file -- Needs Comments
library(ggplot2)
charttest <- read.csv("/Users/Maxine/Documents/welldetailtest2.txt", header=T)
attach(charttest)
summary(charttest)
charttest$Date <- as.Date(charttest$Date, format="%m/%d/%Y")
str(charttest)
ggplot(charttest, aes(x=Date, y=WT_Elev, colour=Serial_Number, group=Serial_Number)) + geom_line() + ylim(min(WT_Elev), max(WT_Elev))
