import logging

import rpy2.robjects as robjects
from rpy2.robjects.packages import STAP
from rpy2.robjects.packages import importr

from pylearn.varselect.count_xvar_in_xvarsel import CountXVarInXvarSel
from pylearn.varselect.test_extract_rvariable_combos import ExtractRVariableCombos
from pylearn.varselect.rank_var import RankVar
from pylearn.varselect.remove_highcorvar_from_xvarsel import RemoveHighCorVarFromXVarSel

logger = logging.getLogger('pylearn')

class VarSelect(object):
    importr('subselect')

    def __init__(self):
        self.flog = importr('futile.logger')
        self.r = robjects.r

    def initR(self, args):

        self.r('classVariableName <- "%s"' % args['--yvar'])
        self.r('excludeRowValue <- "%s"' % -1)
        self.r('excludeRowVarName <- "SORTGRP"')
        self.r('xVarSelectCriteria <- "X"')
        self.r('minNvar <- %d' % int(args['--minNvar']))
        self.r('maxNvar <- %d' % int(args['--maxNvar']))
        self.r('nSolutions <- %d' % int(args['--nSolutions']))
        self.r('criteria <- "%s"' % args['--criteria'])

        self.r('lviFileName <- "%s"' % args['--xy-data'])
        self.r('outDir <- "%s"' % args['--output'])
        self.r('xVarSelectFileName <- "%s"' % args['--config'])
        self.r('uniqueVarPath <- "%s/UNIQUEVAR.csv"' % args['--output'])
        self.r('printFileName <- "%s/UCORCOEF.csv"' % args['--output'])
        self.r('xVarCountFileName <- "%s/XVARSELV1_XCOUNT.csv"' % args['--output'])
        self.r('varSelect <- "%s/VARSELECT.csv"' % args['--output'])

    def run(self, args):
        logger.info("Starting variable_selection")

        args['--nSolutions'], args['--minNvar'], args['--maxNvar'] = args['--iteration'].split(':')

        self.initR(args)

        count_xvar_in_xvarsel = CountXVarInXvarSel(args['--output'])
        rank_var = RankVar(args['--output'])
        extract_rvariable_combos = ExtractRVariableCombos(args['--output'])
        remove_highcorvar = RemoveHighCorVarFromXVarSel(args['--output'])
        rvarselect = importr('rlearn')

        currentCount = count_xvar_in_xvarsel.count()
        self.r('initialCount <- scan(xVarCountFileName)')
        logger.info("Initial variable count: %s", self.r['initialCount'])
        rvarselect.vs_IdentifyAndOrganizeUniqueVariableSets(self.r['lviFileName'], self.r['xVarSelectFileName'], self.r['varSelect'])

        # test_EXTRACT_RVARIABLE_COMBOS_v2.Extract_RVariable_Combos_v2() identifies the unique variable sets and organizes them into a new file VARSELV.csv;
        uniqueVarSets = extract_rvariable_combos.extract_rvariable_combos()

        # Rank the variables in terms of their contribution to a model
        ranksVariables = rank_var.rank()

        # test2_XIterativeVarSelCorVarElimination.R runs steps 13 -18 ZCompleteVariableSelectionPlusRemoveCorrelationVariables.R
        rvarselect.vs_CompleteVariableSelectionPlusRemoveCorrelationVariables(self.r['lviFileName'], self.r['uniqueVarPath'], self.r['printFileName'])

        removeCorXVars = remove_highcorvar.remove_high_cor_vars()
        nextCount = count_xvar_in_xvarsel.count()
        logger.info("CurrentCount = %s, nextCount %s", currentCount, nextCount)

        # "Kluge" is: Helps get around an unknown crash when calling test3_XiterativeVarSelCorVarElimination.R
        self.r('xVarCount <- scan(xVarCountFileName)')

        # LOOP THROUGH THE AUTOMATED VARIABLE SELECTION PROCESS TO ELIMINATE VARIABLES THAT DO NOT CONTRIBUTE TO THE MODEL
        counter = 0
        while currentCount != nextCount:
            currentCount = nextCount
            #config part of test_XItertative plus test_ZCompleteVariableSelectionPlusRemoveCorrelationVariables.R
            #r.source("/opt/xvarselect/bin/XIterativeConfFile.R")
            rvarselect.vs_IdentifyAndOrganizeUniqueVariableSets(self.r['lviFileName'], self.r['xVarSelectFileName'], self.r['varSelect'])

            extract_rvariable_combos.extract_rvariable_combos()
            rank_var.rank()

            rvarselect.vs_CompleteVariableSelectionPlusRemoveCorrelationVariables(self.r['lviFileName'], self.r['uniqueVarPath'], self.r['printFileName'])

            remove_highcorvar.remove_high_cor_vars()
            count_xvar_in_xvarsel.count()
            counter = counter +1

        logger.info("Number of Iterations: %s", counter)
