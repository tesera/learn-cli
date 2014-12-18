# Author: Ian Moss
# Modified by: Mishtu Banerjee
# Updated 20130512

# Copyright: The Author(s)
#License: Distributed under MIT License
#    [http://opensource.org/licenses/mit-license.html]


# This file re-applies parts of the LVI Process to the MRAT data.
# Corresponding LVI scripts are noted. 



# STEP 0 -- GET THE WORKING DIRECTORY AND SET IT TO THE DATA PATH FOR THE SELECTED CITY
#  Modified from LVI script SetRwd.R

# Windows Example: 
setwd("E:/Apps/TSIAnalytics/Data/Moncton/")

# Mac Example
#setwd("/Users/Maxine/Documents/TSIAnalytics/Data/Moncton")
getwd()



# STEP 1 -- LOAD THE ANALYSIS.TXT FILE FORTHE SELECTED CITY
# Based on the LVI Script LoadDatasetAndAttachVariableNames.R
# Load  a csv text file &
# Make variable names accessible during session
# Paths can be relative and will look like this: myfile <- read.csv("/Users/Maxine/Documents/welldetailtest3.txt", header=T)
# Paths can be absolute and look like this(note escape backslasshes): myfile <- "D:\\Rwd\\LVINEW.csv"
# Paths need not be in TSIAnalytics mydata <- read.csv("/Users/Maxine/Documents/welldetailtest3.txt", header=T)

# Windows Path: 
myfile <- "E:/Apps/TSIAnalytics/Data/Moncton/ANALYSIS.txt"

# MAC Path
# myfile <- "/Users/Maxine/Documents/TSIAnalytics/Data/Moncton/SUMZ.txt"	#Enter file name and address for lvi -- dataset
#myfile <- "/Users/Maxine/Documents/TSIAnalytics/Data/Moncton/ANALYSIS.txt"	#Enter file name and address for lvi -- dataset 

mydata <- read.csv(myfile,header=T,row.names=1)	#Read file and put in R dataframe lvinew

attach(mydata)							#Attach variable names to each of the columns

VarNames <- names(mydata)				#Print variable names in interpreter

CaseRows <- length(mydata[,1])			#Count the number of rows or observations (for use in extracting variable subsets)

# List Variable Names, Case Rows, and Structure of the data
VarNames
CaseRows
str(mydata) 							#Prints the structure of the dataframe
head(mydata) 							#Shows a few lines of data 



#STEP 2 -- SET THE CLASSIFICATION FACTOR
#Modified from LVI script DeclareClassificationVariableAsFactor

#Declare the variable indicating the classes associated with each observation as a factor
#This is used as the Y-variable in discriminant analysis
CLASSIFICATION = factor(EL5Y)							#CLASS5 is a variable name in lvinew with numeric class labels; this may be changed
uniqueClasses = sort(unique(CLASSIFICATION))					#Get unique list of class names and sort them in order
classNumberList <- as.numeric(levels(uniqueClasses)[uniqueClasses])	#Convert factors back into a list of numbers
nClasses = length(uniqueClasses)	

#Some summary info on the classification variable: CLASSIFICATION
str(CLASSIFICATION)
summary(CLASSIFICATION)
length(CLASSIFICATION)




#STep 3 -- CALCULATE PRIOR PROBABILITIS FROM SAMPLE DATA
#Modified from LVI script ComputeSamplePriorClassProbabilityDistribution.R

uniqueVector = unique(CLASSIFICATION)
nClasses = length(uniqueVector)
classNames <- sort(uniqueVector)	#sort the class names or numbers and assign them to class names
nClasses = length(classNames)		#Compute total number of classes
nObs = length(CLASSIFICATION)		#Compute total number of observations
classCount = 0				#Initialize class count value
classP <- 0					#Initialize class proportion value
#
#Initialize classCount and classP vector
for (i in 1:(nClasses-1)) {
	classCount <- c(classCount,0)
	classP <- c(classP,0)
	}
#
#Calculate number of observations in each class
for (i in 1:nObs)
	for (j in 1:nClasses) {
		if (classNames[j] == CLASSIFICATION[i]) 
			classCount[j]<-classCount[j]+1
		}
#
#Calculate classP proportions for each class
for (i in 1:nClasses) {
	classP[i] = classCount[i]/nObs
	}
#
priorDistribution <- classP		#Initialize prior distribution
priorDistribution



# STEP 4 -- GET THE XVARIABLE SET FOR DISCRIMINANT ANALYSIS
# Modified from LVI script SelectXVariableSubet_v2.R

# Select X-variable data subset from original file
# load  a csv text file, named VARSELXNEW.csv to select X-variables
fileName <- "XVARSELV2.csv"	#Set file name for variable selection input
xVarSel <- read.csv(fileName,header=T,row.names=1,stringsAsFactors=FALSE, 
	strip.white=TRUE, na.strings = c("NA",""))
#
attach(xVarSel)				#Make variable names accessible during session by attaching the variable names
nRows <- length(xVarSel[,1])		#Get the number of rows or X-variables in xVarSel
varNameList <- names(xVarSel)		#Get potential list of xVariables
nCols <- length(varNameList)		#Get number of columns in data frame
DUMMY <- rep(0,CaseRows)		#Create a DUMMY vector of zeros of length 1 (initial) dataset dataset

# Get the list of elgible x variables and select the variables from the datafile 
# and put them in a vector, each vector to be analyzed in turn
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

xVarSel
str(xDataset)
summary(xDataset)



# STEP 5 RUN DISCRIMINANT ANALYSIS
# Moified from LVI script RunLinearDiscriminantAnalysis_MASS_lda.R

#Run discriminant analysis.
#CLASSIFICATION previously entered and defined as Factor
#XDataset previously extracted 
#priorDistribution defined using previous previous script.
#CV=TRUE produces results using leave-one-out-cross-validation.
#Paackage MASS has already been loaded prior to running this script.
#
#lda output statistics for CV = FALSE:
#lvi.lda$prior containins Prior probailities of groupsdeimen
#lvi.lda$counts contains the number of obesvations by class
#lvi.lda$means contains the means of the xVariables by class
#lvi.lda$scaling contains the discriminant function coefficients rescaled 
	#by the square root of the diagonal elements in the covariance matrix
#lvi.lda$svd are the ratios of between to within-group standard deviations in the linear discriminant variables
	#The squares of these figures are the canoxSelectnical F-statistics
#lvi.lda$N is the number of observations
library(MASS) #Just in case you forgot to load it earlier

mrat.lda = lda(xDataset,CLASSIFICATION,prior = priorDistribution, CV=FALSE)
mratclass.pred = predict(mrat.lda)
mratclass.table = table(CLASSIFICATION, mratclass.pred$class)

mrat.lda
mratclass.table



#STEP 6 -- GET COEFFICIENTS FROM DISCRIMINANT ANALYSIS REQUIRED FOR PARAM.TXT

mratDiscrim1 <- mratclass.pred$x[,1]
head(mratDiscrim1)
summary(mratDiscrim1)

#DiscrimModel <- lm(mratDiscrim1 ~ xDataset)
#Gets error message
#Error in model.frame.default(formula = mratDiscrim1 ~ xDataset, drop.unused.levels = TRUE) : 
#  invalid type (list) for variable 'xDataset'

# However -- this works: amodel <- lm(mratDiscrim1 ~ AGE_SAN2)
# This works: rawvar <- cbind(AGE_SAN2,DEN_BLDA,DEN_ROAD,PCNT_R2,PDITC_500)
# Then the lm function works: mymodel <- lm(mratDiscrim1 ~ rawvar)
# For now -- will do manually
#Note -- can get coefficients via: mymodel$coefficients
#Note -- Can print out to file via: write.csv(mymodel$coefficients,file="mytestcoeff2.csv", row.names=TRUE,na="")