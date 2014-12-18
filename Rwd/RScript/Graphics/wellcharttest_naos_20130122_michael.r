# This is a pattern file for plotting a dataset where the X axis is date and the Y axis is some other variable we want to trend by date
#Load ggplot2 Note: only needs to be loaded once 
#library(ggplot2) 

#Read the data into a data frame
charttest <- read.csv("/apps/TSIAnalytics/Data/6-21_2.txt", header=T)

#Attach the data frame
attach(charttest)

#Summarize the Data
summary(charttest)

#Convert Date field to Date class so it is properly plotted
charttest$Date <- as.Date(charttest$Date, format="%m/%d/%Y")

#Convert Serial_Number to factor, so it is used to group data
charttest$Serial_Number <- factor(charttest$Serial_Number)

#Check structure of the data
str(charttest)

#Plot the data with a white background
#naosplot <- ggplot (charttest, aes(x=Date, y=WT_Elev)) + geom_point(alpha=1/20) + stat_smooth(se=FALSE, colour="#6D817F", size=0) + ylim(min(WT_Elev), max(WT_Elev)) + opts(title="NAOS DATA EXAMPLE", panel.background=theme_rect(colour=NA))
#naosplot <- ggplot (charttest, aes(x=Date, y=WT_Elev)) + geom_point(alpha=1/20) + stat_smooth(level = 0.99, colour="#6D817F", size=0) + ylim(min(WT_Elev), max(WT_Elev)) + opts(title="NAOS DATA EXAMPLE", panel.background=theme_rect(colour=NA))
#naosplot <- ggplot (charttest, aes(x=Date, y=WT_Elev)) + geom_line(colour="#E1E1E1") + geom_point(alpha=1/20) + stat_smooth(level = 0.99, colour="#6D817F", size=0) + ylim(min(WT_Elev), max(WT_Elev)) + opts(title="NAOS DATA EXAMPLE", panel.background=theme_rect(colour=NA))
#naosplot <- ggplot (charttest, aes(x=Date, y=WT_Elev)) + geom_line(colour="#E1E1E1") + geom_point(colour="#6D817F", alpha=1/20) + stat_smooth(level = 0.99, colour="#6D817F", size=0.5, fill="red") + ylim(min(WT_Elev), max(WT_Elev)) + opts(title="NAOS DATA EXAMPLE", plot.title=theme_text(size=20, colour="red"), panel.background=theme_rect(colour=NA))
naosplot <- ggplot (charttest, aes(x=Date, y=WT_Elev)) + geom_line(colour="#E1E1E1") + geom_point(colour="#6D817F", alpha=1/20) + stat_smooth(level = 0.99, colour="#6D817F", size=0.5, fill="#F4F5EB") + ylim(min(WT_Elev), max(WT_Elev)) + opts(title="NAOS DATA EXAMPLE", plot.title=theme_text(size=20, colour="red"), panel.background=theme_rect(colour=NA))
naosplot
