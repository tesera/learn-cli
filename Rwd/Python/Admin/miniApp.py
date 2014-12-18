#!/usr/bin/env python
"""
miniApp: Tools to create simple apps within the XAYA framework (used in TSIAnalytics). 
Based on the Stand Structure Compiler developed by Mishtu Banerjee and Ian Moss (2005-2006),
and further enhanced by Ian Moss (2006- present).

CurrentRevisionDate:20130709


Author(s): Mishtu Banerjee, Ian Moss
Contact: mishtu.banerjee@tesera.com, ian.moss@tesera.com

Copyright: The Author(s)
License: Distributed under MIT License
    [http://opensource.org/licenses/mit-license.html]



Dependencies:
    Python interpreter and base libraries
    miniGraph
    
"""

import sys
import miniGraph

def getConfig(filename='', defpath='', altpath='', pathkeyslist=[]):
    '''
    This function gets the data from a config file in XAYA format.
    filename -- the name of the config file. 
    defpath -- the default path in which to look for the config file.
    altpath -- an alternate path path that can be tried if the config file is not found in defpath.
    pathkeyslist -- a list of filepath keywords in the config file, example: ['edaDataInPath', 'edaDataOutPath']
    '''
    #Try the default path, e.g in TSIAnalytics,  '/apps/TSIAnalytics/Config.txt'
    #If it does not work, try configFilePath
    myConfig = miniGraph.readGraph(filepath = defpath+filename)
    if myConfig ==  'File not opened, could not find'+defpath + filename:
        myConfig = miniGraph.readGraph(filepath = altpath+filename)
    # Account for paths that do not start from defualt C drive in Windows systems
    #The drive has to be added explicitly via a keyword 'drive'. 
    if myConfig.has_key('drive'):
        myDrive = myConfig['drive'][0] + ':'
        for configAddress in pathkeyslist: #myConfig:
            if not configAddress == 'drive': #Not really necessary any more mb 20130709
                myConfig[configAddress] = [myDrive + myConfig[configAddress][0]]
                #print mratConfig[configAddress]
            
    return myConfig

    
def createConfig(configGraph={}, filename='', configpath=''):
    '''
    This function creates a config file from parameter inputs
    configGraph -- a xaya format graph
    filename -- the name of the config file, e.g myConfig.txt
    confgpath -- the location config files are to be placed in, eg /apps/TSIAnalytics/Config/
    '''
    

def saveConfig():
    '''
    saves a config file (w+) mode, or entry to existi configfile (a+) mode. 
    see saveDataset in miniStats and writeGraph in miniGraph
    '''
def elicitConfig():
    '''
    This function uses raw_input to allow a user to interactively update a config file or create
    a new config file. 
    Wraps createConfig and saveConfig in a simple interactive command line interface
    '''
 
def executeWorkflow():
    '''
    Python
    http://stackoverflow.com/questions/1186789/what-is-the-best-way-to-call-a-python-script-from-another-python-script
    http://docs.python.org/2/library/subprocess.html
    http://sharats.me/the-ever-useful-and-neat-subprocess-module.html
    http://stackoverflow.com/questions/7152340/using-python-subprocess-call-to-invoke-python-script
    
    R
    http://stackoverflow.com/questions/6688177/executing-an-r-script-from-python
    http://stackoverflow.com/questions/6434569/executing-an-r-script-in-python-via-subprocess-popen
    http://stat.ethz.ch/R-manual/R-patched/library/utils/html/Rscript.html
    http://thirteen-01.stat.iastate.edu/snoweye/hpsc/?item=rscript
    
    General approach:(can be seq. from route; can be recursive)
        Identify root data sets
        Execute 1 arc from root
        Identify next arc
        Repeat until tail data sets are reached
        Have to bring in Config info at somepoint, at least to id config giles to use with Workflow scripts.
    
    BASIC Inputs:
        A list of Workflow Scripts.
        A list of CSV Files (if path is a squence, might not need this)
        A Network of input-output relationships from root data to tail data
            The network could be simplified if the same data set is not run on > 1 script
    
    Functions that executeWorkflow will need to call:
        executeScript -- runs a workflow script; distinguishes between .py and .R; optin for other programs
        findWorkflowPaths. Identifies the order of paths through an analysis network
        modifyConfig -- allows for mis-stream modification to config files, where further user input needed
        somekindoferrorhandling -- to be determined
        somekindofsecturity -- to be determined; e.g check against a master list of scripts; confirm script contents so no trojan horses
        
    What I need to Practice: Recursion; Subprocess module
        
        

    '''
    
def assembleApp(workflowGraph={}, configList=[], appName='', appPath='', compiled="N"):
    '''
    Creates a customized version of the TSIAnalytics folder, with just the code required. 
    and any initial data sets (based on root nodes in workflowGraph)
    workflowGraph -- input graph; if it is the whole of TSIAnalytics, re-creates TSIAnalytics.
    configList -- config file(s) needed to supportthe workflow
    appName -- name of application. Workflow scripts will be placed in the App directory 
    under that name, and have the app anme appended to the front of theirworkflow name
    appPath -- A custom version of TSIAnalytics will be placed in this path, with the App name.
    compiled -- whether inported code is as .pyc, .pyo (object files) or .py (human readable)
    
    
    App specific scripts are placed as a subdirectory within Apps; which itself is a 
    subdirectory within TSIAnalytics. 
    Essentially, function reads the workflow scripts, finds all the import statement;
    identifies which are either in TSIAnalytics base directory, or in Workflows, and 
    therby graps all the dependencies needed for an applicationto run. 
    
    Future: Consider expanding, to create a python egg automatically
    '''

def selectAnalysisVariables(varSelCriteria = 'Y', varSelTypedList = [[]]):
    ''' 
    Inputs
        varSelCriteria      Select variables that has a value that meets the varSelCriteria, e.g.
        varSelTypedList    This is a table that has the following column names in the first row:
                            TVID:       A unique id identifying each of the variables in dataDict (integer)
                            VARNAME:    Variable name that can be found in the dataDict (string)
                            XVARSELV:   An indicator whether the variable has been identified as an
                                        an X-variable (i.e. X), or Y-variable (i.e. Y), or unselected variable,
                                        (i.e. N; all strings). The indicator must correspond with the varSelCriteria.

                            e.g. TVID	VARNAME	XVARSEL
                                    1	LVI_ELEV	X
                                    2	LVI_SLOPE	X
                                    3	LVI_ASPECT	N
                                    4	LVI_DSPH	N
                                    5	LVI_DVPH	Y
    Outputs
        varSelList          A list of X or Y variable names to be selected from a dataset for further analysis
               
        
    Original file from: routineLviApplications.ReadXVarSelv1XorYVariableList
    July 31 2013
    '''
    
    end_i = len(varSelTypedList)
    varSelList = []
    for i in range(0,end_i,1):
         if varSelTypedList[i][2] == varSelCriteria:
            newVar = varSelTypedList[i][1]
            varSelList.append(newVar)   
    return varSelList
