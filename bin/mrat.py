#!/usr/bin/env python
"""MRAT

Usage:
  mrat.py DATA-FILE VARIABLE-SELECTION-FILE OUTPUT-DIR
  mrat.py DATA-FILE VARIABLE-SELECTION-FILE OUTPUT-DIR [--class=<class>]

Arguments:
    DATA-FILE  Input file.
    VARIABLE-SELECTION-FILE  File containing variable selections.
    OUTPUT-DIR  Directory to write results out too.

Options:
    -h --Help  Show this screen.
    --class=<class>  Class variable name, CLASS5 or CLPRDP [default: CLASS5].

"""
from signal import *
import atexit
import os
import sys
import pdb
from docopt import docopt
from schema import Schema, And, Or, Use, SchemaError

import rpy2.robjects as robjects
from rpy2.robjects.packages import STAP
from rpy2.robjects.packages import importr

import config
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
        
        self.r('lviFileName <- "%s"' % config.args['DATA-FILE'])
        self.r('xVarSelectFileName <- "%s"' % config.args['VARIABLE-SELECTION-FILE'])
        self.r('classVariableName <- "%s"' % config.args['--class'])
        self.r('excludeRowValue = -1')
        self.r('excludeRowVarName <- "SORTGRP"')
        self.r('xVarSelectCriteria <- "X"')
        self.r('minNvar <- 1')
        self.r('maxNvar <- 20')
        self.r('nSolutions <- 10')
        self.r('criteria <- "xi2"')
        self.r('uniqueVarPath <- "%s/UNIQUEVAR.csv"' % config.args['OUTPUT-DIR'])
        self.r('printFileName <- "%s/UCORCOEF.csv"' % config.args['OUTPUT-DIR'])
        self.r('xVarCountFileName <- "%s/XVARSELV1_XCOUNT.csv"' % config.args['OUTPUT-DIR'])
        self.r('varSelect <- "%s/VARSELECT.csv"' % config.args['OUTPUT-DIR'])
        self.r.setwd('/opt/MRAT_Refactor/Rwd')

    def variable_selection(self):
        flog.flog_info("Starting variable_selection")
        currentCount = COUNT_XVAR_IN_XVARSELV1.Count_XVar_in_XVarSelv1()

        # test_XIterativeVarSelCorVarElimination.R
        self.devtools.install('DiscriminantAnalysisVariableSelection')
        davs = importr('DiscriminantAnalysisVariableSelection')
        self.r('initialCount <- scan(xVarCountFileName)')
        flog.flog_info("Initial variable count: %s", self.r['initialCount'])
        davs.vs_IdentifyAndOrganizeUniqueVariableSets(self.r['lviFileName'], self.r['xVarSelectFileName'], self.r['varSelect'])        
        
        # test_EXTRACT_RVARIABLE_COMBOS_v2.Extract_RVariable_Combos_v2() identifies the unique variable sets and organizes them into a new file VARSELV.csv;
        uniqueVarSets = test_EXTRACT_RVARIABLE_COMBOS_v2.Extract_RVariable_Combos_v2()  
        # Rank the variables in terms of their contribution to a model
        ranksVariables = RANKVAR.RankVar()
        
        # test2_XIterativeVarSelCorVarElimination.R runs steps 13 -18 ZCompleteVariableSelectionPlusRemoveCorrelationVariables.R
        davs.vs_CompleteVariableSelectionPlusRemoveCorrelationVariables(self.r['lviFileName'], self.r['uniqueVarPath'], self.r['printFileName'])        
        
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
            davs.vs_IdentifyAndOrganizeUniqueVariableSets(self.r['lviFileName'], self.r['xVarSelectFileName'], self.r['varSelect'])

            test_EXTRACT_RVARIABLE_COMBOS_v2.Extract_RVariable_Combos_v2()
            RANKVAR.RankVar()
            
            #r.source("/opt/MRAT_Refactor/bin/test2_XIterativeVarSelCorVarElimination.R")
            davs.vs_CompleteVariableSelectionPlusRemoveCorrelationVariables(self.r['lviFileName'], self.r['uniqueVarPath'], self.r['printFileName'])        
        
            REMOVE_HIGHCORVAR_FROM_XVARSELV.Remove_HighCorVar_from_XVarSelv()
            nextCount = COUNT_XVAR_IN_XVARSELV1.Count_XVar_in_XVarSelv1()
            counter = counter +1

        flog.flog_info("Number of Iterations: %s", counter)
                 
if __name__ == "__main__":
    args = docopt(__doc__)
    
    schema = Schema({
        'DATA-FILE': And(os.path.isfile, error='VARIABLE-SELECTION-FILE should exist and be readable.'),
        'VARIABLE-SELECTION-FILE': And(os.path.isfile, error='VARIABLE-SELECTION-FILE should exist and be readable.'),
        'OUTPUT-DIR': And(os.path.exists, error='OUTPUT-DIR should exist and be writable.'),
        '--class': And(str, len)
    })

    try:
        config.args = schema.validate(args)
        config.args['OUTPUT-DIR'] = config.args['OUTPUT-DIR'].rstrip('/') + '/';
        mrat = MRAT()
        mrat.variable_selection()

    except SchemaError as e:
        exit(e)


        
    