# This is a template for a scatter matrix where the X and Y axes 
# are assumed to be quantitative variables.
# If they are groups -- you should set them as the 'colour' variable.

# You will need to have both ggplot2 and GGally installed via install.packages 
# and loaded via library()
# If you have not installed ggplot2 and GGally -- run the scripts
# installPackages.R. You will only need to do this once.

# Installed pacakages have to be loaded for a session. 
# Either use the commnands: library(ggplot2)  and libarary(GGally) 
# or run the script loadPackages.R

# If data is in a csv file use the line below to read into a data frame. 
 #Modify to match file path to yur data
# mydata <- read.csv("/Users/Maxine/Documents/welldetailtest3.txt", header=T)

# We will use a dataset that comes with R -- the famous iris dataset.
# It was used by Edgar Anderson to demonstrate introgressive hybridization.
#  Anderson provided the data to Ronald Fisher who used it to create 
# discriminant analysis to classify individuals into their correct species. 
data(iris)
mydata <- iris

#Attach the data frame
attach(mydata)

#Summarize the Data
summary(mydata)



#Check structure of the data
str(mydata)

# You might have to convert some variables to dates or factors depending 
# on the structure of your data. 

# Convert Date field to Date class so it is properly plotted. 
# Not required for the iris and economics data sets.
#mydata$date <- as.date(mydata$Date, format="%m/%d/%Y")

# Convert a GroupingVariable to factor, so it is used to group data
# Not required for the iris and economics data sets. 
#mydata$GroupingVariable <- factor(mydata$GroupingVariable)


# Uncomment the version of the scatterplot matrix you want

# A basic black and white scatterplot matrix
#myplot <- ggpairs(iris)

# Add a title
#myplot <- ggpairs(iris,title="My Scatterplot Matrix")

# Add a groupiing variable
# myplot <- ggpairs(iris, colour='Species', title="My Scatterplot Matrix")

# Add a trtansparency factor: alpha. 
# alpha=1 means all points are opaque. alpha=0 all points are transparent.
# alphas can be in ratio or decimal form 1/2.5=0.4
myplot <- ggpairs(iris, colour='Species', alpha=1/2.5, title="My Scatterplot Matrix")

# Can also remove elements. For example blanking out the diagonal of the scatterplot matrix
# myplot <- ggpairs(iris, colour='Species', alpha=0.4, title="My Scatterplot Matrix", diag="blank")
# other options: upper="blank", lower="blank"




#View the finished plot
myplot 


#-------------------- Compare to Options for a regular scatterplot in ggplot2
#Plot the data with a white background
#myplot <- ggplot (mydata, aes(x=Sepal.Width, y=Sepal.Length, colour=Species, group=Species)) + geom_point() + ylim(min(Sepal.Length), max(Sepal.Length)) + opts(title="My DATA EXAMPLE", panel.background=theme_rect(colour=NA)) 

#If we had a GroupingVariable the code would look like this
#myplot <- ggplot (mydata, aes(x=date, y=uempmed, colour=GroupingVariable, group=GroupingVariable)) + geom_line() + ylim(min(uempmed), max(uempmed)) + opts(title="My DATA EXAMPLE", panel.background=theme_rect(colour=NA)) 

#HELP
# http://cran.r-project.org/web/packages/GGally/GGally.pdf


