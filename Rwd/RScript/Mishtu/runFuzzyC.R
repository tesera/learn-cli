# Load  a csv text file &
# Make variable names accessible during session
#Author: Ian Moss
#Modified by: Miahtu Banerjee
# Updated 20130414

library("e1071")
setwd("E:/Apps/TSIAnalytics/Data/Moncton")

# Paths can be relative and will look like this: myfile <- read.csv("/Users/Maxine/Documents/welldetailtest3.txt", header=T)
# Paths can be absolute and look like this(note escape backslasshes): myfile <- "D:\\Rwd\\LVINEW.csv"
#Paths need not be in TSIAnalytics mydata <- read.csv("/Users/Maxine/Documents/welldetailtest3.txt", header=T)

#Windows Path: myfile <- "/apps/TSIAnalytics/Data/Moncton/ANALYSIS.txt"

#MAC Path
#myfile <- "/Users/Maxine/Documents/TSIAnalytics/Data/Moncton/SUMZ.txt"	#Enter file name and address for lvi -- dataset
myfile <- "E:/Apps/TSIAnalytics/Data/Moncton/ANALYSIS.txt"	#Enter file name and address for lvi -- dataset 

mydata <- read.csv(myfile,header=T,row.names=1)	#Read file and put in R dataframe lvinew

attach(mydata)							#Attach variable names to each of the columns

VarNames <- names(mydata)				#Print variable names in interpreter

CaseRows <- length(mydata[,1])			#Count the number of rows or observations (for use in extracting variable subsets)

# List Variable Names, Case Rows, and Structure of the data
VarNames
CaseRows
str(mydata) 							#Prints the structure of the dataframe
head(mydata) 							#Shows a few lines of data 



#Select X-variable data subset from original file
#load  a csv text file, named VARSELXNEW.csv to select X-variables
fileName <- "XVARSELV2.csv"	#Set file name for variable selection input
xVarSel <- read.csv(fileName,header=T,row.names=1,stringsAsFactors=FALSE, 
	strip.white=TRUE, na.strings = c("NA",""))
#
attach(xVarSel)				#Make variable names accessible during session by attaching the variable names
nRows <- length(xVarSel[,1])		#Get the number of rows or X-variables in xVarSel
varNameList <- names(xVarSel)		#Get potential list of xVariables
nCols <- length(varNameList)		#Get number of columns in data frame
DUMMY <- rep(0,CaseRows)		#Create a DUMMY vector of zeros of length 1 (initial) dataset dataset

#Get the list of elgible x variables and select the variables from the datafile 
#and put them in a vector, each vector to be analyzed in turn
for (i in 1:nRows) {
	xDataset <- data.frame(DUMMY)						#Start a new xDataset
	for (j in 4:nCols) {
		#print (xVarSel[i,j])
		if (!(xVarSel[i,j] == "N"))	{				#If not xVarSel[i,j] == "N"
			xDataset[,xVarSel[i,j]] <- get(xVarSel[i,j])	#Add the variable of name xVarSel[i,j] to the xDataset
			}
		}
	xDataset$DUMMY <- NULL							#Remove the DUMMY variable
	#print(i)									#Use this to check that the right number of varibale sets are being produced	
	#print(names(xDataset))							#Use this to check that each set of variables is being correctly compiled into xDataset 
	}	

# NOW WE DO THE FUZZY C MEANS PART
normxDataset <- scale(xDataset,center=TRUE, scale=TRUE)
myfuzzyresults <- cmeans(xDataset, centers=9, iter.max = 1000, verbose = FALSE, dist = "euclidean", method = "cmeans", m = 2, rate.par = NULL, weights = 1, control = list())
myfuzzyresults

# We Need to write to files: 
mycenters <- myfuzzyresults$centers
myclusters <- myfuzzyresults$cluster
mymemberships <- myfuzzyresults$membership

# Write these 2 files
write.csv(myclusters,file="FCLASS.csv", row.names=TRUE,na="")
write.csv(mycenters,file="FCENTROID.csv", row.names=TRUE,na="")
write.csv(mymemberships,file="FMEMBERS.csv", row.names=TRUE,na="")

#Declare the variable indicating the classes associated with each observation as a factor
#This is used as the Y-variable in discriminant analysis
#
CLASSIFICATION = factor(myclusters)							#CLASS5 is a variable name in lvinew with numeric class labels; this may be changed
uniqueClasses = sort(unique(CLASSIFICATION))					#Get unique list of class names and sort them in order
classNumberList <- as.numeric(levels(uniqueClasses)[uniqueClasses])	#Convert factors back into a list of numbers
nClasses = length(uniqueClasses)	

yDataset <- data.frame(EL5Y, NEL5Y)
attach(yDataset)

#Do a one way Anova one variable at a time
yVarNames = names(yDataset)
lapply(names(yDataset[ , 1:2]), function(y) {
  	MV = lm(formula = yDataset[,y] ~ CLASSIFICATION,)
	summary(MV)
})
yVarNames
