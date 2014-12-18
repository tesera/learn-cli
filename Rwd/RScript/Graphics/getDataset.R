#Make variable names accessible during session

#load  a csv text file

# Paths on a Mac will look like this: myfile <- read.csv("/Users/Maxine/Documents/welldetailtest3.txt", header=T)
#Paths on a PC will look like this(note escape backslasshes): myfile <- "D:\\Rwd\\LVINEW.csv" 
myfile <- "D:\\Rwd\\LVINEW.csv"			#Enter file name and address for lvi -- dataset 

mydata <- read.csv(myfile,header=T,row.names=1)	#Read file and put in R dataframe lvinew

attach(mydata)							#Attach variable names to each of the columns

VarNames <- names(mydata)					#Print variable names in interpreter

CaseRows <- length(mydata[,1])				#Count the number of rows or observations (for use in extracting variable subsets)

#List Variable Names, Case Rows, and Structure of the data
VarNames
CaseRows
str(mydata) # Prints the structure of the dataframe