# TSIBRIDGE SPECIFIC IMPORTS
from confighandler import ConfigHandler
from loghandler     import log
from rhandler       import RHandler
from signal         import *

import atexit
import os
import sys
import pdb
import rpy2.robjects as robjects
from rpy2.robjects.packages import STAP

# AUTOMATED VARIABLE SELECTION SPECIFIC IMPORTS
import test_EXTRACT_RVARIABLE_COMBOS_v2
import RANKVAR
import REMOVE_HIGHCORVAR_FROM_XVARSELV
import COUNT_XVAR_IN_XVARSELV1


# STEP 0 -- ABSTRACT ANALYTICS PROCESS TO A CLASS (EXAMPLE: AUTOMATED VARIABLE SELECTION)
class mrat_variable_selection(object):
    """"""
    def __init__(self,*args, **kwargs):
        r = robjects.r
        
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
        # STEP 1 -- DO SIMPLE SANITY TESTS THAT INFORMATION CORRECTLY PASSES FROM R TO PYTHON
        print 'self.R.code test: "3 + 3" -> ' + str(self.R.code('3 + 3'))
        print 'rpy2 test: "3 + 3" -> ' + str(r('3 + 3'))

        print 'self.R.script local test: "/opt/MRAT_Refactor/bin/test.R" -> ' + str(self.R.script("/opt/MRAT_Refactor/bin/test.R"))
        
        # with open('/opt/MRAT_Refactor/bin/test.R', 'r') as f:
        #     string = f.read()
        # func = STAP(string, 'tesera')
        print 'rpy2 local test: "/opt/MRAT_Refactor/bin/test.R" -> '
        str(r.source('/opt/MRAT_Refactor/bin/test.R', True, False, True))
        

        # setup
        r.source(os.environ['MRATPATH'] + '/etc/XIterativeVarSel.R.conf')
        currentCount = COUNT_XVAR_IN_XVARSELV1.Count_XVar_in_XVarSelv1()
        r.source("/opt/MRAT_Refactor/bin/test_XIterativeVarSelCorVarElimination.R")
     
        sys.exit(0);

        # test_EXTRACT_RVARIABLE_COMBOS_v2.Extract_RVariable_Combos_v2() identifies the unique variable sets and organizes 
        #them into a new file VARSELV.csv;
        uniqueVarSets = test_EXTRACT_RVARIABLE_COMBOS_v2.Extract_RVariable_Combos_v2() #20150904 MB IM SK  
        # RANKVAR.RankVar() ranks the variables in terms of their contribution to a model
        ranksVariables = RANKVAR.RankVar() #20150908 SK
        
        # test2_XIterativeVarSelCorVarElimination.R runs steps 13 -18 ZCompleteVariableSelectionPlusRemoveCorrelationVariables.R
        self.R.script("/opt/MRAT_Refactor/bin/test2_XIterativeVarSelCorVarElimination.R") #20150911 SK
        removeCorXVars = REMOVE_HIGHCORVAR_FROM_XVARSELV.Remove_HighCorVar_from_XVarSelv()  #20150908 SK to be added later
        nextCount = COUNT_XVAR_IN_XVARSELV1.Count_XVar_in_XVarSelv1()  #20150908 SK and 20150914 SK MB
        print "currentCount = ", currentCount, "  nextCount = ", nextCount
        print "\n"
        
        # "Kluge" is: Helps get around an unknown crash when calling test3_XiterativeVarSelCorVarElimination.R
        self.R.script("/opt/MRAT_Refactor/bin/kluge.R") #20150915 a cobbledTogetherInelegantSolution SK MB

        
        # STEP 3 -- LOOP THROUGH THE AUTOMATED VARIABLE SELECTION PROCESS TO ELIMINATE VARIABLES THAT DO NOT CONTRIBUTE TO THE MODEL
        #ORIGINALLY THIS WAS 'STEP 4' IN XIterativeVarSelCorVarElimination.R
        counter = 0
        while currentCount != nextCount:
            
            currentCount = nextCount
            #config part of test_XItertative plus test_ZCompleteVariableSelectionPlusRemoveCorrelationVariables.R
            self.R.script("/opt/MRAT_Refactor/bin/XIterativeConfFile.R")
            #self.R.script("/opt/MRAT_Refactor/Rwd/RScript/test_ZCompleteVariableSelectionPlusRemoveCorrelationVariables.R)
            test_EXTRACT_RVARIABLE_COMBOS_v2.Extract_RVariable_Combos_v2()
            RANKVAR.RankVar()
            self.R.script("/opt/MRAT_Refactor/bin/test2_XIterativeVarSelCorVarElimination.R")
            REMOVE_HIGHCORVAR_FROM_XVARSELV.Remove_HighCorVar_from_XVarSelv()
            nextCount = COUNT_XVAR_IN_XVARSELV1.Count_XVar_in_XVarSelv1()
            counter = counter +1

        print "Number of Iterations: ", counter
        print "\n"


    # STEP 4 -- GUARANTEE CLEAN EXIT         
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