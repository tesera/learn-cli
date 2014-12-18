# This is a template for plotting histograms. 
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

# STEP1: Plot a basic histogram
myplot <- ggplot (mydata, aes(Sepal.Width)) + geom_histogram(aes(y=..count..), binwidth=0.1)
# Choose a binwidth that matches the precision of the data; not just the one that makes the prettiest looking histogram
# alternative to y=..count.. i y=..desnisty

# STEP 2: add in a title
myplot <- myplot + opts(title="My DATA EXAMPLE") 


#STEP 4: Plot the data with a white background
myplot <- myplot  + opts(panel.background=theme_rect(colour=NA)) 

#Step 5: Add in a smoothed density estimate
myplot <- myplot + geom_density()

#Conventional Histogram -- as a one liner
#myplot <- ggplot (mydata, aes(Sepal.Width)) + geom_histogram(aes(y=..density..), binwidth=0.1) + opts(title="My DATA EXAMPLE", panel.background=theme_rect(colour=NA))

#Histogram as frquency polygon by species group
#myplot <- ggplot (mydata, aes(Sepal.Width)) + geom_freqpoly(aes(y=..density.., colour=Species), binwidth=0.1) + opts(title="My DATA EXAMPLE", panel.background=theme_rect(colour=NA))

# STEP 6: add x and y axes back in to create a frame for the data 
myplot <- myplot  + opts(axis.line=theme_segment(colour="grey80"))

# STEP 7: make the histogram and smoothed density a background on which to stage density polygons
myplot <- myplot + geom_histogram(aes(y=..count..), binwidth=0.1, colour="grey50", fill="grey95") + geom_density(colour="grey")

# Step 8: add in frequency polygons for each group
myplot <- myplot + geom_freqpoly(aes(y=..count.., colour=Species), binwidth=0.1)
#Note -- something funky happening with freqpoly -- density should be below histogram

# STEP 9 -- customise the group colours via RColourBrewer
myplot <- myplot + scale_color_brewer(pal = "Accent")
#RColourBrewer commands that can help in picking colours for graphics: 
# display.brewer.all() -- displays the base palletes
# brewer.pal(9,"BrBG") -- lists 9 colours from the BrBG pallete
# display.brewer.pal(9,"BrBG") -- displays the 9 colours generated above
# colorRampPalette(brewer.pal(9,"BrBG"))(100) -- interpolates 100 colours from the pallete above
# a nice web intro to RColourBrewer is: http://simplystatistics.org/2011/10/17/colors-in-r/


# STEP 10: Make the title stand out
myplot <- myplot  + opts(plot.title=theme_text(size=10, colour="#4A5E5C"))

# STEP 11: have Axes labels match title
myplot <- myplot  + opts(axis.title.x=theme_text(size=10, colour="#4A5E5C"), axis.title.y=theme_text(size=10, colour="#4A5E5C", angle=90))

 
myplot 

#HELP
# ggplot2 - http://docs.ggplot2.org/current/index.html
# geom_histogram - http://docs.ggplot2.org/current/geom_histogram.html
# geom_density - http://docs.ggplot2.org/current/geom_density.html and http://docs.ggplot2.org/current/stat_density.html
# geom_freqpoly - http://docs.ggplot2.org/current/geom_freqpoly.html



