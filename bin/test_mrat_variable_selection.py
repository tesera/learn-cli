##############################################################################
# Removal of the "__license__" line or content from  "__license__", or removal 
# of "__author__" in this or any constituent # component or file constitutes a 
# violation of the licensing and copyright agreement. 
__author__      = "Mike Rightmire"
__copyright__   = "BioCom Software"
__license__     = "Tesera"
__license_file__= "Clause1.PERPETUAL_AND_UNLIMITED_LICENSING_TO_THE_CLIENT.py"
__version__     = "0.9.0.0"
__maintainer__  = "Mike Rightmire"
__email__       = "Mike.Rightmire@BiocomSoftware.com"
__status__      = "Development"
##############################################################################

from confighandler import ConfigHandler
from loghandler     import log
from rhandler       import RHandler
from signal         import *

import atexit
import os
import sys
#Add imports for Python Capabilities moved from R to Python Side 20150903 MB, SK
import test_EXTRACT_RVARIABLE_COMBOS_v2
import RANKVAR
import REMOVE_HIGHCORVAR_FROM_XVARSELV
import COUNT_XVAR_IN_XVARSELV1

class mrat_variable_selection(object):
    """"""
    def __init__(self,*args, **kwargs):
        
        # Set exit and cleanup        
        for sig in (SIGABRT,SIGINT,SIGTERM,SIGQUIT):
            signal(sig, self._cleanup)
        atexit.register(self._cleanup)        

        # NOTE: ConfigHandler will override some of the self.variables 
        # kwargs passed to the __init__ will override the config file. 
        # Configuration loading goes in the following order:
        # 1. Config file parameters
        # 2. keyword args passed into this __init__
        # 3. Mandatory defaults on a package by package basis if they ere not
        #    included in the config file or the kwargs
        # ConfigHandler sets the log file parameters: so app_name, logfile, 
        # screendump, formatter, create_paths arguments should be included.
        # If included here, they will override whats in the config file. If 
        # they a None, the config file will be used. If they are None here, and 
        # not set in the config file...the default loghandler settings will be 
        # used
        self.config = ConfigHandler(
                        config_file = kwargs.pop('config_file', None),
                        *args,  
                        **kwargs 
                        )
        
        # The first call to log will create a log instance if it does not exist. 
        # The "kwargs.pop('app_name'      , None)," lines will override the 
        #  logger parameters obtained from the config file, if any have been 
        #  passed to __init__
        self.local_filename = str(os.path.basename(__file__))
        log.info("Starting '__main__' in " + self.local_filename)
        
        self.R = RHandler.rHandler(
                    service     = self.rhandler_service, 
                    rhandler_host        = self.rhandler_host,  
                    rhandler_port        = self.rhandler_port,
                    rhandler_atomicArray = self.rhandler_atomicArray,  
                    rhandler_arrayOrder  = self.rhandler_arrayOrder,  
                    rhandler_defaultVoid = self.rhandler_defaultVoid,  
                    rhandler_oobCallback = self.rhandler_oobCallback,
                                   )
        
        print 'self.R.code test: "3 + 3"'#333 TESTING ONLY
        print self.R.code('3 + 3') #333 TESTING ONLY
        print 
        
#        print 'self.R.script local test: "/Users/mikes/git/Tesera/MRAT_Refactor/bin/test.R"' #333 TESTING ONLY
#        print self.R.script("/Users/mikes/git/Tesera/MRAT_Refactor/bin/test.R") #333 TESTING ONLY
#        print 
        print 'self.R.script local test: "/opt/MRAT_Refactor/bin/test.R"' #333 TESTING ONLY
        print self.R.script("/opt/MRAT_Refactor/bin/test.R") #333 TESTING ONLY
        print

#        print 'self.R.script remote test: "/home/ec2-user/test.R"' #333 TESTING ONLY
#        print self.R.script("/home/ec2-user/test.R", host='54.164.196.82') #333 TESTING ONLY
#        print

#        print 'self.R.script test: "/Users/mikes/git/Tesera/MRAT_Refactor/bin/XIterativeVarSelCorVarElimination.R"' #333 TESTING ONLY
#        self.R.script("/Users/mikes/git/Tesera/MRAT_Refactor/bin/XIterativeVarSelCorVarElimination.R") #333 TESTING ONLY
#        print
#        print 'self.R.script test: "/opt/MRAT_Refactor/bin/XIterativeVarSelCorVarElimination.R"' #333 TESTING ONLY
#        self.R.script("/opt/MRAT_Refactor/bin/XIterativeVarSelCorVarElimination.R") #333 TESTING ONLY
        print

#         print self.R.code(None) #333 TESTING ONLY


        #import routineLviApplications
        #print '\n Reading VARRANK.csv'
        #tableName = 'XVARSELV1'
        #printTypes = 'YES'
        #nLines = 10000
        #oldDict, newDict = routineLviApplications.createNewDataDictionaryFromFile(tableName, printTypes, nLines)
        #varSelKeyVarNameList = ['VARNAME']
        #readErrorFileName = 'ERROR_'+ tableName
        #varSelHeader, varSelDict = routineLviApplications.ReadCsvDataFileAndTransformIntoDictionaryFormat_v2(oldDict, newDict, tableName, \
        #                                                                                                 readErrorFileName, varSelKeyVarNameList)
        ## Count remaining X-Variables
        #xVarCount = 0
        #for varName in varSelDict:
        #    if varSelDict[varName]['XVARSEL']=='X':
        #        xVarCount = xVarCount + 1

        #print '\n There are',xVarCount,'eligible X-Variables remaining in XVARSELV1.'
        #fileName = 'XVARSELV1_XCOUNT'
        #floatFormat = '%0.6f'
        #varCountList = [[xVarCount]]
        #routineLviApplications.writeListArrayToCsvFile(varCountList, fileName, floatFormat)
        currentCount = COUNT_XVAR_IN_XVARSELV1.Count_XVar_in_XVarSelv1()  #20150914 SK MB

        # self.R.script("/opt/MRAT_Refactor/Rwd/RScript/test_ZReadXvarselvCount.R")
        # print self.R.script("/opt/MRAT_Refactor/Rwd/RScript/test_ZReadXvarselvCount.R")

        # print 'self.R.scripttest :"/opt/MRAT_Refactor/bin/test_XIterativeVarSelCorVarElimination.R"'
        #self.R.script("/opt/MRAT_Refactor/bin/SixplusSix.R")
        #
        self.R.script("/opt/MRAT_Refactor/bin/test_XIterativeVarSelCorVarElimination.R") #333 TESTING ONLY
        #print self.R.script("/opt/MRAT_Refactor/bin/test_XIterativeVarSelCorVarElimination.R")
        # best to break apart test_XIterativeVarSelCorVarElimination.R
        # so that we call the Rs then the Pythons
        #
        #
        #print 'EXTRACT_RVARIABLE_COMBOS_v2.py'
        test_EXTRACT_RVARIABLE_COMBOS_v2.Extract_RVariable_Combos_v2() #20150904 MB IM SK  
        RANKVAR.RankVar() #20150908 SK
        
        self.R.script("/opt/MRAT_Refactor/bin/test2_XIterativeVarSelCorVarElimination.R") #20150911 SK
        REMOVE_HIGHCORVAR_FROM_XVARSELV.Remove_HighCorVar_from_XVarSelv()  #20150908 SK to be added later
        nextCount = COUNT_XVAR_IN_XVARSELV1.Count_XVar_in_XVarSelv1()  #20150908 SK and 20150914 SK MB
        print "currentCount = ", currentCount, "  nextCount = ", nextCount
        print "\n"
        #self.R.script("/opt/MRAT_Refactor/bin/test3_XIterativeVarSelCorVarElimination.R") #20150912 SK
        self.R.script("/opt/MRAT_Refactor/bin/kluge.R") #20150915 a cobbledTogetherInelegantSolution SK MB
        #counter = 0
        while currentCount != nextCount:
            
            #config part of test_XItertative plus test_ZCompleteVariableSelectionPlusRemoveCorrelationVariables.R
            self.R.script("/opt/MRAT_Refactor/bin/XIterativeConfFile.R")
            #self.R.script("/opt/MRAT_Refactor/Rwd/RScript/test_ZCompleteVariableSelectionPlusRemoveCorrelationVariables.R)
            test_EXTRACT_RVARIABLE_COMBOS_v2.Extract_RVariable_Combos_v2()
            RANKVAR.RankVar()
            self.R.script("/opt/MRAT_Refactor/bin/test2_XIterativeVarSelCorVarElimination.R")
            REMOVE_HIGHCORVAR_FROM_XVARSELV.Remove_HighCorVar_from_XVarSelv()
            nextCount = COUNT_XVAR_IN_XVARSELV1.Count_XVar_in_XVarSelv1()
            #counter = counter +1
            #if counter > 100: break
                 
    def _cleanup(self):
        """"""
        log.info("Completing '__main__' in " + self.local_filename)
        log.info('Clean exit.')
        sys.exit(0)
        
                 
if __name__ == "__main__":
    o = mrat_variable_selection(
        config_file = "../etc/MRAT.conf",
#         app_name   = "MRAT", 
#         logfile    = "/Users/mikes/GitHub/Tesera/MRAT_Refactor/log/MRAT.log",
         log_level  = 10,
         screendump = True
         )
