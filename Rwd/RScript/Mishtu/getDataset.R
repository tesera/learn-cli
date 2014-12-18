# Load  a csv text file &
# Make variable names accessible during session
#Author: Ian Moss
#Modified by: Miahtu Banerjee
# Updated 20130414



# Paths can be relative and will look like this: myfile <- read.csv("/Users/Maxine/Documents/welldetailtest3.txt", header=T)
# Paths can be absolute and look like this(note escape backslasshes): myfile <- "D:\\Rwd\\LVINEW.csv"
#Paths need not be in TSIAnalytics mydata <- read.csv("/Users/Maxine/Documents/welldetailtest3.txt", header=T)

#Windows Path: myfile <- "/apps/TSIAnalytics/Data/Moncton/ANALYSIS.txt"

#MAC Path
myfile <- "/Users/Maxine/Documents/TSIAnalytics/Data/Moncton/ANALYSIS.txt"	#Enter file name and address for lvi -- dataset 

mydata <- read.csv(myfile,header=T,row.names=1)	#Read file and put in R dataframe lvinew

attach(mydata)							#Attach variable names to each of the columns

VarNames <- names(mydata)				#Print variable names in interpreter

CaseRows <- length(mydata[,1])			#Count the number of rows or observations (for use in extracting variable subsets)

# List Variable Names, Case Rows, and Structure of the data
VarNames
CaseRows
str(mydata) 							#Prints the structure of the dataframe
head(mydata) 							#Shows a few lines of data 