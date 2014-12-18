# R Shiny app that produces a heatmap of selectable variables on a GIS based map
# outputted to a web browser
# V1.1 Fri 1 Nov 2013 S.Kaharabata, M.Banerjee TSI
# User Interface code
# modified to include sizing of panels and colouring of histogram 1 Nov 2013
#
#
#


library(shiny)

# Define UI for mapping of probability enquiry application
#uidata <- read.csv("E:/Rwd/Rdata/Archived/SLS/SiteIndex/Final_SIs.csv", header = T, row.names=1)
uidata <- read.csv("E:/Rwd/Rdata/Archived/SLS/SiteIndex/Final_SI_Comparison_subset.csv", header = T, row.names=1)
#uidata <- read.shapefile("E:/Rwd/Rdata/Archived/SLS/SiteIndex/SLS_Demo_Subset.shp")
#read.dbf(dbf.name, header=FALSE)

attach(uidata)
VarNames <- names(uidata)

shinyUI(pageWithSidebar(

  # Application title
  headerPanel("SLS Forest Site Productivity"),

  # Sidebar with controls to select the variable to plot
  #

  sidebarPanel(
    tags$head(
      tags$style(type="text/css", "select { width: 100px; }"), # defines width of dropdown panel
      tags$style(type='text/css', ".span4 { max-width: 150px; }") # defines width of panel containing dropdown panel
    # the above code then indirectly controls how wide the graphing panel is
      ),
    selectInput("var", "Variable:",
             choices = VarNames)
   ),

  # Show the caption and plot of the requested variable

  mainPanel(
    h3(textOutput("caption")),

    plotOutput("mapPlot")
  )
))