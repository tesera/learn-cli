# R Shiny app that produces a heatmap of selectable variables on a GIS based map
# outputted to a web browser
# V1.1 Fri 1 Nov 2013 S.Kaharabata, M.Banerjee TSI
# modified to include a histogram Thru 31 Oct 2013 M.Banerjee and S.Kaharabata TSI
# modified to include sizing of panels and colouring of histogram 1 Nov 2013
# Server code
#
#
#


library(shiny)
library(maps)
library(mapdata)
library(sp) # required by maptools
library(maptools)
library(scales)
library(RColorBrewer)
library(ggplot2)
library(rgeos) # to replace gpclib
library(plyr) # best to load before reshape
library(reshape)
library(mapproj)
library(rgdal)
library(grid) #required by gridExtra
library(gridExtra)
library(shapefiles)

setwd("E:/Rwd/Rscript/Shiny/SiteIndex")

# Step 1 Read/loading the target shapefile
#readOGR(dsn="directoryWhereShapefilesAreLocated",layer="NameOfShapefileWithoutFileExtension") 
shapeData = readOGR(dsn="E:/Rwd/Rdata/Archived/SLS/SiteIndex", layer="SLS_Demo_Subset")

# Step 2 Get row numbers from .dbf / explicitly identifies attribute rows by the .dbf offset.
shapeData@data$id = rownames(shapeData@data)
#shapeData@data$id = shapeData@data[,"OBJECTID_1"]

# Step 3 Makes centroid (point layer) from polygon "FORTIFY"
# Creating centroids so that ggplot can use it - melting polygons into points
shapeData.points = fortify(shapeData, region="id") # takes a while to process on an Intel i3

# Step 4 Reading in .csv which will be joined to .dbf using "MERGE"
# this is the path to the dataset please change accordingly to yours
mydata <- read.csv("E:/Rwd/Rdata/Archived/SLS/SiteIndex/Final_SI_Comparison_subset.csv")

# Step 5 Joins the points to their corresponding attributes and finalizes the data preparation 
shapeData.df = join(shapeData.points, shapeData@data, by="id")

# Step 6 Merge makes an inner join of the shapefile's data frame and the .csv on a common item (usually the spatial key)
mygeomdata <- merge(shapeData.df, mydata, by.x="OBJECTID_1", by.y="OBJECTID_1")
#mygeomdata <- shapeData.df

# Define server logic required to plot various variables as heatmap
# Step 7 Create map
shinyServer(function(input, output) {

  # Compute the forumla text in a reactive expression since it is 
  # shared by the output$caption and output$cropPlot expressions

  formulaText <- reactive({
    paste("Variable:", input$var)
  })

  # Return the formula text for printing as a caption
  output$caption <- renderText({
    formulaText()
  })

# "environment <-environment()" and "environment = environment" in ggplot captures the local environment
# so that local and external variables can be passed across functions. There is a way to declare global variables
# but this has not been explored for this app. See the following for more info:
# http://stackoverflow.com/questions/10659133/local-variables-within-aes?rq=1
  
# ggplot has some hard rules about passing variables and functions so we need to
# be aware of this. Refer to the above link on StackOverflow.
  
# get(input$var)  converts the string input$var into a variable (http://cran.r-project.org/doc/FAQ/R-FAQ.html#How-can-I-turn-a-string-into-a-variable_003f)
# without this and in combination of "environment", aes() does not see the variable being passed
# and instead sees it as a pure character ie string.
  
  environment<-environment() 
  myplot <- ggplot(mygeomdata, aes(long, lat, group = group, fill = get(input$var)), environment = environment)
# myplot <- myplot + labs(x = "Easting", y = "Northing") + scale_fill_gradient(low = "ghostwhite", high = "steelblue")
  myplot <- myplot + labs(x = "Easting", y = "Northing") + scale_fill_gradientn(colours=c( "#8C510A","#D8B365","#F6E8C3","#C7EAE5","#5AB4AC","#01665E"))
  myplot <- myplot + geom_polygon()
  myplot <- myplot + coord_equal()
  myhist <- ggplot (mygeomdata, aes(get(input$var)), environment=environment) + geom_histogram(aes(y=..count..), fill = "#5AB4AC")
  
# Generate a plot of the requested variable against map 

   output$mapPlot <- renderPlot({
   
#    this prints the two graphs into a column but it can be easily modified for 2 cols
#    it also adjust the size of the myplot to be 2x that of myhist; grid,arrange and arrangeGrob need gridExtra
     print(grid.arrange(arrangeGrob(myplot, myhist, ncol = 2, widths=c(2,1))))
   
   })

})