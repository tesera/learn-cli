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

# Step 1: a basic scatterplot
myplot <- ggplot (mydata, aes(x=Sepal.Width, y=Sepal.Length)) + geom_point() 

# STEP 2: add in a title
myplot <- myplot + opts(title="My DATA EXAMPLE") 

# STEP 3: add in max and min bounds on the Y and X axis
myplot <- myplot  +  ylim(min(Sepal.Length), max(Sepal.Length)) + xlim(min(Sepal.Width), max(Sepal.Width))



#STEP 4: Plot the data with a white background
myplot <- myplot  + opts(panel.background=theme_rect(colour=NA)) 

# STEP 5: add a grouping variable
myplot <- myplot + aes(x=Sepal.Width, y=Sepal.Length, colour=Species, group=Species)

#The graphical elements added so far as a one liner would look like this
#myplot <- ggplot (mydata, aes(x=Sepal.Width, y=Sepal.Length, colour=Species, group=Species)) + geom_point() + ylim(min(Sepal.Length), max(Sepal.Length)) + opts(title="My DATA EXAMPLE", panel.background=theme_rect(colour=NA)) 

# STEP 6 -- customise the group colours via RColourBrewer
myplot <- myplot + scale_color_brewer(pal = "Accent")
#RColourBrewer commands that can help in picking colours for graphics: 
# display.brewer.all() -- displays the base palletes
# brewer.pal(9,"BrBG") -- lists 9 colours from the BrBG pallete
# display.brewer.pal(9,"BrBG") -- displays the 9 colours generated above
# colorRampPalette(brewer.pal(9,"BrBG"))(100) -- interpolates 100 colours from the pallete above
# a nice web intro to RColourBrewer is: http://simplystatistics.org/2011/10/17/colors-in-r/

# STEP 7: add x and y axes back in to create a frame for the data 
myplot <- myplot  + opts(axis.line=theme_segment(colour="grey80"))

# STEP 8: Make the title stand out
myplot <- myplot  + opts(plot.title=theme_text(size=10, colour="#4A5E5C"))

# STEP 9: have Axes labels match title
myplot <- myplot  + opts(axis.title.x=theme_text(size=10, colour="#4A5E5C"), axis.title.y=theme_text(size=10, colour="#4A5E5C", angle=90))

#STEP 10: Set point size;  set opacity of points via alpha
myplot <- myplot  + geom_point(size=2,  alpha=1/20)
# size will depend on the data density of the dataset -- for a line chart points should not dominate the trend. If points are very dense -- line is often best
# alpha=1 all points are opaque; alpha = 0 all points are visible -- set alpha so all points are visible, but able to distinguish areas of greater and lesser point density

# STEP 11: add a smoother
myplot <- myplot  + stat_smooth(method=lm, se=FALSE, size=0.1, aes(fill=Species))
#myplot <- myplot  + stat_smooth(method=lm,aes(fill=factor(Species)))

myplot 

#HELP
# ggplot2 - http://docs.ggplot2.org/current/index.html
# geom_point - http://docs.ggplot2.org/current/geom_point.html
# smoothing -- http://docs.ggplot2.org/current/stat_smooth.html and http://docs.ggplot2.org/current/geom_smooth.html


