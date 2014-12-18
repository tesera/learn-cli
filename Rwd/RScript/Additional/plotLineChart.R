# This is a template for plotting data as a line where the X axis is date
# and the Y axis is some other variable we want to trend by date

# Graphics are handled using the graphics package: ggplot2

# If you have not installed ggplot2 -- run the script installPackages.R. 
# You will only need to do this once.

#Installed packages have to be loaded for a session. Either use the command: 
# library(ggplot2) or run the script loadPackages.R

#If data is in a csv file use the line below to read the data into a data frame. Modify to match file path to yur data
#mydata <- read.csv("/Users/Maxine/Documents/welldetailtest3.txt", header=T)
# Note -- relative paths use forward slashes; 
# absolute paths use back slashes and must be escaped by a double slash

#We will use a dataset that comes with ggplot2 on economics.
data(economics)
mydata <- economics

#Attach the data frame
attach(mydata)

#Summarize the Data
summary(mydata)

#Check the structure of the data
str(mydata)

#Convert Date field to Date class so it is properly plotted. Not required for the economics data set.
#mydata$date <- as.date(mydata$Date, format="%m/%d/%Y")

#Convert a GroupingVariable to factor, so it is used to group data
#mydata$GroupingVariable <- factor(mydata$GroupingVariable)

# STEP1: Plot a basic line chart
myplot <- ggplot (mydata, aes(x=date, y=uempmed)) + geom_line()

#We will now built up our basic line chart one element at a time. 
# You can comment out any elements you do not want. 

# STEP 2: add in a title
myplot <- myplot + opts(title="My DATA EXAMPLE") 

# STEP 3: add in max and min bounds on the Y axis
myplot <- myplot  +  ylim(min(uempmed), max(uempmed))

#STEP 4: Plot the data with a white background
myplot <- myplot  + opts(panel.background=theme_rect(colour=NA)) 

# As a single line the elements above would look like this
#myplot <- ggplot (mydata, aes(x=date, y=uempmed)) + geom_line() + ylim(min(uempmed), max(uempmed)) + opts(title="My DATA EXAMPLE", panel.background=theme_rect(colour=NA)) 
# This is a nice basic plot we can tweak with additional elements below


#STEP5: If we had a GroupingVariable the code would look like this
#myplot <- ggplot (mydata, aes(x=date, y=uempmed, colour=GroupingVariable, group=GroupingVariable)) + geom_line() + ylim(min(uempmed), max(uempmed)) + opts(title="My DATA EXAMPLE", panel.background=theme_rect(colour=NA)) 




# We will continue to add elements to this plot

# STEP 6: add x and y axes back in to create a frame for the data 
myplot <- myplot  + opts(axis.line=theme_segment(colour="grey80"))

# STEP 7: Make the title stand out
myplot <- myplot  + opts(plot.title=theme_text(size=10, colour="#4A5E5C"))

# STEP 8: have Axes labels match title
myplot <- myplot  + opts(axis.title.x=theme_text(size=10, colour="#4A5E5C"), axis.title.y=theme_text(size=10, colour="#4A5E5C", angle=90))

# STEP 9: have the line be a custom colour
myplot <- myplot  + geom_line(colour="#E1E1E1") #mishnote -- I find this colour a bit too light; almost like the black line better. Up to Lori. 

#STEP 10: Display points in addition to the lines
myplot <- myplot  + geom_point(size=2, colour="#6D817F", alpha=1/20) 



# size will depend on the data density of the dataset -- for a line chart points should not dominate the trend. If points are very dense -- line is often best
# alpha=1 all points are opaque; alpha = 0 all points are visible -- set alpha so all points are visible, but able to distinguish areas of greater and lesser point density

#STEP 11: Add a smoother
myplot <- myplot  + stat_smooth(method="loess", span=0.3, se=TRUE, level=0.95, size=0.1, colour="#6D817F",fill="#F4F5EB")

# Smoother Statistical Issues
# the default smoother is loess; other methods available are lm, glm -- in which case you can add a formula: formula = y ~ x, y ~ poly(x, 2), y ~ log(x), etc.
# se =TRUE provides a standard error ; level=0.95 provides confidence limits; 
#span (for loess) controls the wiggliness of the line -- near 0, follows the points at 1 smooth line.

#Smoother Aesthetic issues: Let data dominate; use colour(of line), size(of line), fill(of confidence limits) to accentuate the data BUT NOT INTERFERE

# We could further customize the colours of the group via the following code: 
# STEP 12 -- customise the group colours via RColourBrewer
myplot <- myplot + scale_color_brewer(pal = "Accent")
#RColourBrewer commands that can help in picking colours for graphics: 
# display.brewer.all() -- displays the base palletes
# brewer.pal(9,"BrBG") -- lists 9 colours from the BrBG pallete
# display.brewer.pal(9,"BrBG") -- displays the 9 colours generated above
# colorRampPalette(brewer.pal(9,"BrBG"))(100) -- interpolates 100 colours from the pallete above
# a nice web intro to RColourBrewer is: http://simplystatistics.org/2011/10/17/colors-in-r/


myplot 

#HELP
# ggplot2 - http://docs.ggplot2.org/current/index.html
# geom_line -- http://docs.ggplot2.org/current/geom_line.html
# geom_point - http://docs.ggplot2.org/current/geom_point.html
# smoothing -- http://docs.ggplot2.org/current/stat_smooth.html and http://docs.ggplot2.org/current/geom_smooth.html



