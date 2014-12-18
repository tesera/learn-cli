# These are packages that do not come with base R that we need to install for mrat.
# They only need to be installed once. Subsequently they need to be loaded on starting R
# Enter the package name you wish to install in the quotation marks

#MASS package from Modern Applied Statistics with S by W.N. Venables and B.D. Ripley
 mvaPackageName = "MASS"
 install.packages(mvaPackageName)

 # subselect package provides methods for automated variable selection from large data sets where variable relationships are not obvious
 subselectPackageName = "subselect"
 install.packages(subselectPackageName)

 # klaR provides tools to help in the classification and visualization of multivariate data
 mvaHelper = "klaR"
 install.packages(mvaHelper)

 # combinat for calculating combinations and permutations
 combinatHelper = "combinat"
 install.packages(combinatHelper)

 # Fuzzy c means package is  - e1071
 fuzzyCPackage = "e1071"
  install.packages(fuzzyCPackage)

# ggplot2 implements Wilkinson's Grammar of Graphics as interpreted by Wickham. 
graphicsPackageName = "ggplot2"
install.packages(graphicsPackageName)

graphicsHelperName = "GGally"
install.packages(graphicsHelperName)

colourHelperName = "RColorBrewer"
install.packages(colourHelperName)

mapPackageName = "maps"
install.packages(mapPackageName)

mapdataPackageName = "mapdata"
install.packages(mapdataPackageName)

# maptools allows you to use shapefiles in R
maptoolsPackageName = "maptools"
install.packages(maptoolsPackageName)

# scales provides for transparency in maps and graphics
scalesPackageName = "scales"
install.packages(scalesPackageName)

unittestPackageName = "RUnit"
install.packages(unittestPackageName)

#Other installs from Ian
# Add all the other packages Ian is useing