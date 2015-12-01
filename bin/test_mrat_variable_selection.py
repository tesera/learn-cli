# TSIBRIDGE SPECIFIC IMPORTS
#from confighandler import ConfigHandler
#from loghandler import log
from signal import *

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

flog = importr('futile.logger')
devtools = importr('devtools')
#flog.flog_appender(flog.appender_file('mrat.log'))

# STEP 0 -- ABSTRACT ANALYTICS PROCESS TO A CLASS (EXAMPLE: AUTOMATED VARIABLE SELECTION)
class mrat_variable_selection(object):
    def __init__(self, *args, **kwargs):
        r = robjects.r
        flog.flog_info("Starting '__main__'")
        
        # setup
        r.source(os.environ['MRATPATH'] + '/etc/XIterativeVarSel.R.conf')
        currentCount = COUNT_XVAR_IN_XVARSELV1.Count_XVar_in_XVarSelv1()

        # test_XIterativeVarSelCorVarElimination.R
        # use logging library
        devtools.install('DiscriminantAnalysisVariableSelection')
        davs = importr('DiscriminantAnalysisVariableSelection')
        r('initialCount <<- scan(xVarCountFileName)')
        flog.flog_info("Initial variable count: %s", r['initialCount'])
        davs.vs_IdentifyAndOrganizeUniqueVariableSets(r['lviFileName'], r['xVarSelectFileName'], 'VARSELECT.csv')        
        
        # test_EXTRACT_RVARIABLE_COMBOS_v2.Extract_RVariable_Combos_v2() identifies the unique variable sets and organizes them into a new file VARSELV.csv;
        uniqueVarSets = test_EXTRACT_RVARIABLE_COMBOS_v2.Extract_RVariable_Combos_v2()  
        # Rank the variables in terms of their contribution to a model
        ranksVariables = RANKVAR.RankVar()
        
        # test2_XIterativeVarSelCorVarElimination.R runs steps 13 -18 ZCompleteVariableSelectionPlusRemoveCorrelationVariables.R
        r.source("/opt/MRAT_Refactor/bin/test2_XIterativeVarSelCorVarElimination.R")        
        #davs.vs_CompleteVariableSelectionPlusRemoveCorrelationVariables(r['lviFileName'], r['uniqueVarPath'], 'UCORCOEF.csv')        
        
        removeCorXVars = REMOVE_HIGHCORVAR_FROM_XVARSELV.Remove_HighCorVar_from_XVarSelv()
        nextCount = COUNT_XVAR_IN_XVARSELV1.Count_XVar_in_XVarSelv1()
        print "currentCount = ", currentCount, "  nextCount = ", nextCount
        print "\n"
        
        # "Kluge" is: Helps get around an unknown crash when calling test3_XiterativeVarSelCorVarElimination.R
        r.source("/opt/MRAT_Refactor/bin/kluge.R") 
        
        # LOOP THROUGH THE AUTOMATED VARIABLE SELECTION PROCESS TO ELIMINATE VARIABLES THAT DO NOT CONTRIBUTE TO THE MODEL
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
                 
if __name__ == "__main__":
    o = mrat_variable_selection(log_level  = 10, screendump = True)