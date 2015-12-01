from signal import *
import atexit
import os
import sys
import pdb
import docopt

import rpy2.robjects as robjects
from rpy2.robjects.packages import STAP
from rpy2.robjects.packages import importr

import test_EXTRACT_RVARIABLE_COMBOS_v2
import RANKVAR
import REMOVE_HIGHCORVAR_FROM_XVARSELV
import COUNT_XVAR_IN_XVARSELV1

#flog.flog_appender(flog.appender_file('mrat.log'))

class MRAT(object):
    r = None
    devtools = None
    
    def __init__(self):
        global flog
        self.r = robjects.r
        self.devtools = importr('devtools')
        flog = importr('futile.logger')

    def variable_selection(self):
        flog.flog_info("Starting variable_selection")
        # setup
        self.r.source(os.environ['MRATPATH'] + '/etc/XIterativeVarSel.R.conf')
        currentCount = COUNT_XVAR_IN_XVARSELV1.Count_XVar_in_XVarSelv1()

        # test_XIterativeVarSelCorVarElimination.R
        # use logging library
        self.devtools.install('DiscriminantAnalysisVariableSelection')
        davs = importr('DiscriminantAnalysisVariableSelection')
        self.r('initialCount <- scan(xVarCountFileName)')
        flog.flog_info("Initial variable count: %s", self.r['initialCount'])
        davs.vs_IdentifyAndOrganizeUniqueVariableSets(self.r['lviFileName'], self.r['xVarSelectFileName'], 'VARSELECT.csv')        
        
        # test_EXTRACT_RVARIABLE_COMBOS_v2.Extract_RVariable_Combos_v2() identifies the unique variable sets and organizes them into a new file VARSELV.csv;
        uniqueVarSets = test_EXTRACT_RVARIABLE_COMBOS_v2.Extract_RVariable_Combos_v2()  
        # Rank the variables in terms of their contribution to a model
        ranksVariables = RANKVAR.RankVar()
        
        # test2_XIterativeVarSelCorVarElimination.R runs steps 13 -18 ZCompleteVariableSelectionPlusRemoveCorrelationVariables.R
        davs.vs_CompleteVariableSelectionPlusRemoveCorrelationVariables(self.r['lviFileName'], self.r['uniqueVarPath'], 'UCORCOEF.csv')        
        
        removeCorXVars = REMOVE_HIGHCORVAR_FROM_XVARSELV.Remove_HighCorVar_from_XVarSelv()
        nextCount = COUNT_XVAR_IN_XVARSELV1.Count_XVar_in_XVarSelv1()
        flog.flog_info("CurrentCount = %s, nextCount %s", currentCount, nextCount)
        
        # "Kluge" is: Helps get around an unknown crash when calling test3_XiterativeVarSelCorVarElimination.R
        self.r('xVarCount <- scan(xVarCountFileName)')
        
        # LOOP THROUGH THE AUTOMATED VARIABLE SELECTION PROCESS TO ELIMINATE VARIABLES THAT DO NOT CONTRIBUTE TO THE MODEL
        counter = 0
        while currentCount != nextCount:
            currentCount = nextCount
            #config part of test_XItertative plus test_ZCompleteVariableSelectionPlusRemoveCorrelationVariables.R
            #r.source("/opt/MRAT_Refactor/bin/XIterativeConfFile.R")
            davs.vs_IdentifyAndOrganizeUniqueVariableSets(self.r['lviFileName'], self.r['xVarSelectFileName'], 'VARSELECT.csv')

            test_EXTRACT_RVARIABLE_COMBOS_v2.Extract_RVariable_Combos_v2()
            RANKVAR.RankVar()
            
            #r.source("/opt/MRAT_Refactor/bin/test2_XIterativeVarSelCorVarElimination.R")
            davs.vs_CompleteVariableSelectionPlusRemoveCorrelationVariables(self.r['lviFileName'], self.r['uniqueVarPath'], 'UCORCOEF.csv')        
        
            REMOVE_HIGHCORVAR_FROM_XVARSELV.Remove_HighCorVar_from_XVarSelv()
            nextCount = COUNT_XVAR_IN_XVARSELV1.Count_XVar_in_XVarSelv1()
            counter = counter +1

        flog.flog_info("Number of Iterations: %s", counter)
                 
if __name__ == "__main__":
    mrat = MRAT()
    mrat.variable_selection()
