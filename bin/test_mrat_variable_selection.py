# TSIBRIDGE SPECIFIC IMPORTS
from confighandler import ConfigHandler
from loghandler import log
from signal import *
from loader import AutoLoadRLibs

import atexit
import os
import sys
import pdb
import rpy2.robjects as robjects
from rpy2.robjects.packages import STAP
from rpy2.robjects.packages import importr

# AUTOMATED VARIABLE SELECTION SPECIFIC IMPORTS
import test_EXTRACT_RVARIABLE_COMBOS_v2
import RANKVAR
import REMOVE_HIGHCORVAR_FROM_XVARSELV
import COUNT_XVAR_IN_XVARSELV1

# STEP 0 -- ABSTRACT ANALYTICS PROCESS TO A CLASS (EXAMPLE: AUTOMATED VARIABLE SELECTION)
class mrat_variable_selection(object):
    def __init__(self, *args, **kwargs):
        r = robjects.r
        tesera = AutoLoadRLibs('../Rwd/tesera/')
        loginfo = tesera.system.LogInfo

        # Set exit and cleanup        
        for sig in (SIGABRT,SIGINT,SIGTERM,SIGQUIT):
            signal(sig, self._cleanup)
        atexit.register(self._cleanup)        

        self.local_filename = str(os.path.basename(__file__))
        self.config = ConfigHandler(config_file = kwargs.pop('config_file', None), *args, **kwargs)
        
        loginfo("Starting '__main__' in " + self.local_filename)
        loginfo("rpy2 invole sample: ' + str(tesera.test.SquareIt(4))")

        # setup
        r.source(os.environ['MRATPATH'] + '/etc/XIterativeVarSel.R.conf')
        currentCount = COUNT_XVAR_IN_XVARSELV1.Count_XVar_in_XVarSelv1()

        # test_XIterativeVarSelCorVarElimination.R
        # use logging library
        tesera.variable_selection.SetInitialCount()
        tesera.system.Log(r['initialCount'], "zzz.csv")
        r.source('./RScript/test_ZCompleteVariableSelectionPlusRemoveCorrelationVariables.R')
        tesera.system.Log(r['myZCompleteTest'], "zzzStep10.csv")

        # test_EXTRACT_RVARIABLE_COMBOS_v2.Extract_RVariable_Combos_v2() identifies the unique variable sets and organizes 
        #them into a new file VARSELV.csv;
        uniqueVarSets = test_EXTRACT_RVARIABLE_COMBOS_v2.Extract_RVariable_Combos_v2() #20150904 MB IM SK  
        # RANKVAR.RankVar() ranks the variables in terms of their contribution to a model
        ranksVariables = RANKVAR.RankVar() #20150908 SK
        
        # test2_XIterativeVarSelCorVarElimination.R runs steps 13 -18 ZCompleteVariableSelectionPlusRemoveCorrelationVariables.R
        r.source("/opt/MRAT_Refactor/bin/test2_XIterativeVarSelCorVarElimination.R") #20150911 SK
        
        removeCorXVars = REMOVE_HIGHCORVAR_FROM_XVARSELV.Remove_HighCorVar_from_XVarSelv()  #20150908 SK to be added later
        nextCount = COUNT_XVAR_IN_XVARSELV1.Count_XVar_in_XVarSelv1()  #20150908 SK and 20150914 SK MB
        print "currentCount = ", currentCount, "  nextCount = ", nextCount
        print "\n"
        
        # "Kluge" is: Helps get around an unknown crash when calling test3_XiterativeVarSelCorVarElimination.R
        r.source("/opt/MRAT_Refactor/bin/kluge.R") #20150915 a cobbledTogetherInelegantSolution SK MB

        
        # STEP 3 -- LOOP THROUGH THE AUTOMATED VARIABLE SELECTION PROCESS TO ELIMINATE VARIABLES THAT DO NOT CONTRIBUTE TO THE MODEL
        #ORIGINALLY THIS WAS 'STEP 4' IN XIterativeVarSelCorVarElimination.R
        counter = 0
        while currentCount != nextCount:
            
            currentCount = nextCount
            #config part of test_XItertative plus test_ZCompleteVariableSelectionPlusRemoveCorrelationVariables.R
            r.source("/opt/MRAT_Refactor/bin/XIterativeConfFile.R")
            #self.R.script("/opt/MRAT_Refactor/Rwd/RScript/test_ZCompleteVariableSelectionPlusRemoveCorrelationVariables.R)
            test_EXTRACT_RVARIABLE_COMBOS_v2.Extract_RVariable_Combos_v2()
            RANKVAR.RankVar()
            r.source("/opt/MRAT_Refactor/bin/test2_XIterativeVarSelCorVarElimination.R")
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
    o = mrat_variable_selection(config_file = "../etc/MRAT.conf", log_level  = 10, screendump = True)