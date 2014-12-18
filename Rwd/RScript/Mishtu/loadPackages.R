# These are packages that need to be loaded on starting R
# Enter the package name you wish to load in the quotation marks
# Note there are several other graphics packages beyond what we have loaded. See R documentation

# MASS: Functions and datasets to support Venables and Ripley, 'Modern Applied Statistics with S' (4th edition, 2002).
# Includes a number of advanced stats including Multivariate Analysis
# mvaPackageName1 = MASS
library(MASS)

# Subselect package uses data mining techniques to select variable subsets for analysis
library(subselect)

# classificationPackageName = klaR
library (klaR)

# combinatoricsPackageName =combinat
library(combinat)

# Fuzzy C means package
 library(e1071)

# graphicsPackageName1 = ggplot2: Implements Wilkinson's Grammar of Graphics as  interpreted by Wickham
library(ggplot2)

# graphicsPackageName3 = GGally: Helper to ggplot2 -- implements ggpairs
library(GGally)

# graphicsPackageName2 = graphics: Base R Graphics
library(graphics)

# graphicsPackageName4 = RColorBrewer: Helps select good colours for charting and cartography
library(RColorBrewer)

#Mapping packages that add basic maps and ability to read shapefiles to R
library(maps) # basic mapping
library(mapdata) # mapping data sets
library(maptools) # allows for shapefile use
library(scales) # allows for transparencies

# Unit Tests
library(RUnit)

#Other things Ian wants loaded
# ade4 , ade4TkGUI
# ggobi, rgobi