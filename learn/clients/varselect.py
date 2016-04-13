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

    def init(self, args):
        self.count_xvars = CountXVarInXvarSel(args['--output']).count
        self.rank_xvars = RankVar(args['--output']).rank
        self.extract_rvariable_combos = ExtractRVariableCombos(args['--output']).extract_rvariable_combos
        self.remove_highcorvar = RemoveHighCorVarFromXVarSel(args['--output']).remove_high_cor_vars

        self.rlearn = importr('rlearn')

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


    def varselect(self):

        # Input: data_xy.csv, vsel_xy_config.csv
        # Output: VARSELECT.csv
        self.rlearn.vs_IdentifyAndOrganizeUniqueVariableSets(self.r['lviFileName'], self.r['xVarSelectFileName'], self.r['varSelect'])

        # Identifies the unique variable sets
        # Input: VARSELECT.csv
        # Output: vsel_x.csv, vsel_uniquevar.csv
        self.extract_rvariable_combos()

        # Rank the variables in terms of their contribution to a model
        # Input: VARSELECT.csv
        # Output: vsel_varrank.csv (VARRANK.csv)
        self.rank_xvars()

        # Input: data_xy.csv, vsel_uniquevar
        # Output: UCORCOEF.csv
        self.rlearn.vs_CompleteVariableSelectionPlusRemoveCorrelationVariables(self.r['lviFileName'], self.r['uniqueVarPath'], self.r['printFileName'])

        # Removes variables which have a high correlation
        # Input: UCORCOEF.csv, VARRANK.csv
        # Output: vsel_xy_config.csv
        self.remove_highcorvar()


    def run(self, args):
        logger.info("Starting variable_selection")
        args['--nSolutions'], args['--minNvar'], args['--maxNvar'] = args['--iteration'].split(':')
        self.init(args)

        current_nxvar = self.count_xvars()
        self.r('current_nxvar <- %d' % current_nxvar)
        logger.info("Initial variable count: %s", current_nxvar)

        self.varselect()

        next_nxvar = self.count_xvars()
        self.r('xVarCount <- %d' % next_nxvar)
        logger.info("CurrentCount = %s, nxvar %s", current_nxvar, next_nxvar)

        iteration = 0
        while current_nxvar != next_nxvar:
            current_nxvar = next_nxvar

            self.varselect()

            next_nxvar = self.count_xvars()
            iteration = iteration + 1

        logger.info("Number of Iterations: %s", iteration)
