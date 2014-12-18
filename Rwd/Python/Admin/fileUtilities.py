import os
from operator import concat

def checkFileIfItExists(filepath):
    fileExists = 1
    if not os.path.exists(filepath):
        fileExists = 0
    return fileExists

def createNewFileIfNotExisting(filepath):
    if not os.path.exists(filepath):
        newFile = open(filepath,'w')
        newFile.close()
    return

def deleteFileIfItExists(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)
    return

def writeToFile(textLine = '', writeFilePath = ''):
    if not os.path.exists(writeFilePath):
        myFile = open(writeFilePath,'w')
    else:
        myFile = open(writeFilePath,'a')
    print >> myFile, textLine
    myFile.close()
    return

def newFilePath(filepath, filename):
    '''
    Author:  Ian Moss
    Last Modified Jan 23, 2006 (source file: READv1)
    Converted to following dictionary format:
    {('VariableName','TableName'):'Type'}
    where type is an integer, string or float
    Updated: August 27, 2012 (Mishtu Banerjee, Ian Moss)
    Copyright Ian Moss
    '''
    FileKind = '.txt'
    newFilename = concat(filename, FileKind)
    newFilePath = concat(filepath, newFilename)
    return newFilePath

def newFilePath_v2(filepath, filename, fileExtension):
    '''
    Author:  Ian Moss
    Last Modified Jan 23, 2006 (source file: READv1)
    Converted to following dictionary format:
    {('VariableName','TableName'):'Type'}
    where type is an integer, string or float
    Updated: August 27, 2012 (Mishtu Banerjee, Ian Moss)
    Copyright Ian Moss
    '''
    newFilename = concat(filename, fileExtension)
    newFilePath = concat(filepath, newFilename)
    return newFilePath
