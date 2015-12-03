#!/usr/bin/env python
"""MRAT

Usage:
  mrat.py LVIFILENAME XVARSELECTFILENAME OUTDIR
  mrat.py LVIFILENAME XVARSELECTFILENAME OUTDIR \
 [--classVariableName=<string>] \
 [--excludeRowValue=<int>] \
 [--excludeRowVarName=<string>] \
 [--xVarSelectCriteria=<string>] \
 [--minNvar=<int>] \
 [--maxNvar=<int>] \
 [--nSolutions=<int>] \
 [--criteria=<int>]

Arguments:
  LVIFILENAME  Input file.
  XVARSELECTFILENAME  File containing variable selections.
  OUTDIR  Directory to write results out too.

Options:
  -h --Help  Show this screen.
  --classVariableName=<string>  Class variable name: CLASS5, CLPRDP [default: CLASS5].
  --excludeRowValue=<int>  Variable value to exclude rows from a dataset [default: -1].  
  --excludeRowVarName=<string>  Variable name to exclude rows from a dataset [default: SORTGRP].
  --xVarSelectCriteria=<string>  Variable indicator value [default: X].
  --minNvar=<int>  Minimum number of variables to select [default: 1]
  --maxNvar=<int>  Maximum number of variables to select [default: 20]
  --nSolutions=<int>  Number of iterations to be applied [default: 20]
  --criteria=<string>  Set the criteria to be applied for variables selection: ccr12, Wilkes xi2 zeta2 [default: xi2]

"""
from signal import *
import atexit
import os
import sys
import pdb
from docopt import docopt
from schema import Schema, And, Or, Use, SchemaError, Optional

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
        
        for key, value in config.args.iteritems():
            if('--' in key):
                key = key.strip('-')
                if(value.isdigit()):
                    self.r('%s <- %s' % (key, value))
                else:
                    self.r('%s <- "%s"' % (key, value))
            
        self.r('lviFileName <- "%s"' % config.args['LVIFILENAME'])
        self.r('xVarSelectFileName <- "%s"' % config.args['XVARSELECTFILENAME'])
        self.r('uniqueVarPath <- "%s/UNIQUEVAR.csv"' % config.args['OUTDIR'])
        self.r('printFileName <- "%s/UCORCOEF.csv"' % config.args['OUTDIR'])
        self.r('xVarCountFileName <- "%s/XVARSELV1_XCOUNT.csv"' % config.args['OUTDIR'])
        self.r('varSelect <- "%s/VARSELECT.csv"' % config.args['OUTDIR'])
        self.r.setwd(config.args['WORKINGDIR'] + 'Rwd')

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
        'LVIFILENAME': And(os.path.isfile, error='LVIFILENAME should exist and be readable.'),
        'XVARSELECTFILENAME': And(os.path.isfile, error='XVARSELECTFILENAME should exist and be readable.'),
        'OUTDIR': And(os.path.exists, error='OUTDIR should exist and be writable.'),
        Optional('--classVariableName'): And(str, len),
        Optional('--excludeRowValue'): And(str, len),
        Optional('--excludeRowVarName'): And(str, len),
        Optional('--xVarSelectCriteria'): And(str, len),
        Optional('--minNvar'): And(str, len),
        Optional('--maxNvar'): And(str, len),
        Optional('--nSolutions'): And(str, len),
        Optional('--criteria'): And(str, len)  
    })

    try:
        config.args = schema.validate(args)
        config.args['OUTDIR'] = config.args['OUTDIR'].rstrip('/') + '/';
        config.args['WORKINGDIR'] = os.getcwd().rstrip('/').replace('/bin', '') + '/'

        mrat = MRAT()
        mrat.variable_selection()

    except SchemaError as e:
        exit(e)


        
    