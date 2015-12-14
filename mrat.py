#!/usr/bin/env python
"""MRAT

Usage:
  mrat LVIFILENAME XVARSELECTFILENAME OUTDIR
  mrat LVIFILENAME XVARSELECTFILENAME OUTDIR \
 [--classVariableName=<string>] \
 [--excludeRowValue=<int>] \
 [--excludeRowVarName=<string>] \
 [--xVarSelectCriteria=<string>] \
 [--minNvar=<int>] \
 [--maxNvar=<int>] \
 [--nSolutions=<int>] \
 [--criteria=<int>] \
 [--s3Bucket=<string>]

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
  --minNvar=<int>  Minimum number of variables to select [default: 1].
  --maxNvar=<int>  Maximum number of variables to select [default: 20].
  --nSolutions=<int>  Number of iterations to be applied [default: 20].
  --criteria=<string>  Set the criteria to be applied for variables selection: ccr12, Wilkes xi2 zeta2 [default: xi2].
  --s3Bucket=<string>  If paths reside on an S3 bucket.

"""
from signal import *
import atexit
import os
import sys
import pdb
import boto3
import tempfile
from urlparse import urlparse
from docopt import docopt
from schema import Schema, And, Or, Use, SchemaError, Optional

import rpy2.robjects as robjects
from rpy2.robjects.packages import STAP
from rpy2.robjects.packages import importr

from libvariableselection.count_xvar_in_xvarsel import CountXVarInXvarSel
from libvariableselection.test_extract_rvariable_combos import ExtractRVariableCombos
from libvariableselection.rank_var import RankVar
from libvariableselection.remove_highcorvar_from_xvarsel import RemoveHighCorVarFromXVarSel

#, RANKVAR, REMOVE_HIGHCORVAR_FROM_XVARSELV, COUNT_XVAR_IN_XVARSELV1

#flog.flog_appender(flog.appender_file('mrat.log'))

class MRAT(object):
    r = None
    
    def __init__(self):
        global flog
        self.r = robjects.r
        flog = importr('futile.logger')

        for key, value in args.iteritems():
            if('--' in key):
                key = key.strip('-')
                if(value is not None and value.isdigit()):
                    self.r('%s <- %s' % (key, value))
                else:
                    self.r('%s <- "%s"' % (key, value))
            
        self.r('lviFileName <- "%s"' % args['LVIFILENAME'])
        self.r('outDir <- "%s"' % args['OUTDIR'])
        self.r('xVarSelectFileName <- "%s"' % args['XVARSELECTFILENAME'])
        self.r('uniqueVarPath <- "%s/UNIQUEVAR.csv"' % args['OUTDIR'])
        self.r('printFileName <- "%s/UCORCOEF.csv"' % args['OUTDIR'])
        self.r('xVarCountFileName <- "%s/XVARSELV1_XCOUNT.csv"' % args['OUTDIR'])
        self.r('varSelect <- "%s/VARSELECT.csv"' % args['OUTDIR'])

    def variable_selection(self, args):
        flog.flog_info("Starting variable_selection")
        count_xvar_in_xvarsel = CountXVarInXvarSel(args['OUTDIR'])
        rank_var = RankVar(args['OUTDIR'])
        extract_rvariable_combos = ExtractRVariableCombos(args['OUTDIR'])
        remove_highcorvar = RemoveHighCorVarFromXVarSel(args['OUTDIR'])
        davs = importr('DiscriminantAnalysisVariableSelection')
        
        currentCount = count_xvar_in_xvarsel.count()
        self.r('initialCount <- scan(xVarCountFileName)')
        flog.flog_info("Initial variable count: %s", self.r['initialCount'])
        davs.vs_IdentifyAndOrganizeUniqueVariableSets(self.r['lviFileName'], self.r['xVarSelectFileName'], self.r['varSelect'])        
        
        # test_EXTRACT_RVARIABLE_COMBOS_v2.Extract_RVariable_Combos_v2() identifies the unique variable sets and organizes them into a new file VARSELV.csv;
        uniqueVarSets = extract_rvariable_combos.extract_rvariable_combos()  
        
        # Rank the variables in terms of their contribution to a model
        ranksVariables = rank_var.rank()
        
        # test2_XIterativeVarSelCorVarElimination.R runs steps 13 -18 ZCompleteVariableSelectionPlusRemoveCorrelationVariables.R
        davs.vs_CompleteVariableSelectionPlusRemoveCorrelationVariables(self.r['lviFileName'], self.r['uniqueVarPath'], self.r['printFileName'])        
        
        

        removeCorXVars = remove_highcorvar.remove_high_cor_vars()
        nextCount = count_xvar_in_xvarsel.count()
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

            extract_rvariable_combos.extract_rvariable_combos()
            rank_var.rank()

            davs.vs_CompleteVariableSelectionPlusRemoveCorrelationVariables(self.r['lviFileName'], self.r['uniqueVarPath'], self.r['printFileName'])        
        
            remove_highcorvar.remove_high_cor_vars()
            count_xvar_in_xvarsel.count()
            counter = counter +1

        flog.flog_info("Number of Iterations: %s", counter)
        exit(0)
                 
if __name__ == "__main__":
    args = docopt(__doc__)
    outdir = args['OUTDIR']

    if(args['--s3Bucket'] == None):
        args['LVIFILENAME'] = os.path.abspath(args['LVIFILENAME'])
        args['XVARSELECTFILENAME'] = os.path.abspath(args['XVARSELECTFILENAME'])
        args['OUTDIR'] = os.path.abspath(args['OUTDIR'])
    else:
        s3_client = boto3.client('s3')
        args['OUTDIR'] = tempdir = tempfile.mkdtemp('mrat')
        try:
            for key in ['LVIFILENAME', 'XVARSELECTFILENAME']:
                dl = tempdir + '/' + args[key].split('/')[-1]
                s3_client.download_file(args['--s3Bucket'], args[key].strip('/'), dl)
                args[key] = dl
        except Exception as e:
            exit(e)

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
        Optional('--criteria'): And(str, len),  
        Optional('--s3Bucket'): Or(None, And(str, len))
    })

    try:
        args = schema.validate(args)
        args['OUTDIR'] = args['OUTDIR'].rstrip('/') + '/';
        args['WORKINGDIR'] = os.getcwd().rstrip('/').replace('/bin', '') + '/'

        mrat = MRAT()
        mrat.variable_selection(args)

        if(args['--s3Bucket'] is not None):
            for outfile in os.listdir(tempdir):
                up = ("%s/%s" % (outdir, outfile)).strip('/')
                outfile = ("%s/%s" % (tempdir, outfile))
                s3_client.upload_file(outfile, args['--s3Bucket'], up.strip('/'))

    except SchemaError as e:
        exit(e)


        
    