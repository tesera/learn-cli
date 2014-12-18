# This is a pattern file for plotting a scatter chart where the X and Y axes are assumed to be quantitative variables
#If you have not installed ggplot2 -- run the script installPackages.R. You will only need to do this once.

#Installed pacakages have to be loaded for a session. Either use the commnand: library(ggplot2) or run the script loadPackages.R

#If data is in a csv file use the line below to read the data into a data frame. Modify to match file path to yur data
#mydata <- read.csv("/Users/Maxine/Documents/welldetailtest3.txt", header=T)

#We will use a dataset that comes with R -- the famour iris dataset of Edgar Anderson used by Fisher to create discriminant analysis
data(iris)
mydata <- iris

#Attach the data frame
attach(mydata)

#Summarize the Data
summary(mydata)

#Convert Date field to Date class so it is properly plotted. Not required for the economics data set.
#mydata$date <- as.date(mydata$Date, format="%m/%d/%Y")

#Convert a GroupingVariable to factor, so it is used to group data
#mydata$GroupingVariable <- factor(mydata$GroupingVariable)

#Check structure of the data
str(mydata)

#Plot the data with a white background
#myplot <- ggplot (mydata, aes(x=Sepal.Width, y=Sepal.Length, colour=Species, group=Species)) + geom_point() + ylim(min(Sepal.Length), max(Sepal.Length)) + opts(title="My DATA EXAMPLE", panel.background=theme_rect(colour=NA)) 

#If we had a GroupingVariable the code would look like this
#myplot <- ggplot (mydata, aes(x=date, y=uempmed, colour=GroupingVariable, group=GroupingVariable)) + geom_line() + ylim(min(uempmed), max(uempmed)) + opts(title="My DATA EXAMPLE", panel.background=theme_rect(colour=NA)) 
myplot <- ggplot (mydata, aes(x=Sepal.Width, y=Sepal.Length, colour=Species, group=Species)) + geom_point() + stat_smooth(method=lm,aes(fill=factor(Species))) + ylim(min(Sepal.Length), max(Sepal.Length)) + opts(title="My DATA EXAMPLE", panel.background=theme_rect(colour=NA))
myplot 

