import logging

import pandas as pd
import pandas.rpy.common as com
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr

from pylearn.varselect import count_xvars, rank_xvars, extract_xvar_combos, remove_high_corvar

logger = logging.getLogger('pylearn')
importr('subselect')
r = robjects.r
rlearn = importr('rlearn')

def organize(xy, config):
    r_xy = com.convert_to_r_dataframe(xy)
    r_config = com.convert_to_r_dataframe(vsel_xy_config)

    rlearn.organize(r_xy, r_config)

    return com.load_data('vs.varselect')

def complete(xy, uniquevar):
    r_xy = com.convert_to_r_dataframe(xy)
    r_uniquevar = com.convert_to_r_dataframe(uniquevar)

    rlearn.complete(r_xy, r_uniquevar)

    varselect = com.load_data('vs.varselect')
    return com.load_data('vs.ucorcoef')

def varselect(self, xy, config):

    # Identify and organize variable sets (varsets)
    varselect = organize(xy, config)

    # Identifies the unique variable sets
    vsel_x, vsel_uniquevar = extract_xvar_combos(varselect)

    # Rank the variables in terms of their contribution to a model
    varrank = rank_xvars(varselect)

    # Complete var select and remove correlation variables
    ucorcoef = complete(xy, uniquevar)

    # Removes variables which have a high correlation
    config = remove_high_corvar(ucorcoef, vsel_varrank)

    return config


class VarSelect(object):

    def run(self, args):
        logger.info("Starting variable_selection")

        args['--nSolutions'], args['--minNvar'], args['--maxNvar'] = args['--iteration'].split(':')

        # TODO: work in these args into the mix
        # r('classVariableName <- "%s"' % args['--yvar'])
        # r('excludeRowValue <- "%s"' % -1)
        # r('excludeRowVarName <- "SORTGRP"')
        # r('xVarSelectCriteria <- "X"')
        # r('minNvar <- %d' % int(args['--minNvar']))
        # r('maxNvar <- %d' % int(args['--maxNvar']))
        # r('nSolutions <- %d' % int(args['--nSolutions']))
        # r('criteria <- "%s"' % args['--criteria'])

        xy = pd.read_csv(args['--xy-data'])
        config = pd.read_csv(args['--config'])

        current_nxvar = self.count_xvars(config)
        r('current_nxvar <- %d' % current_nxvar)
        logger.info("Initial variable count: %s", current_nxvar)

        config = varselect(xy, config)

        next_nxvar = self.count_xvars(config)
        r('xVarCount <- %d' % next_nxvar)
        logger.info("CurrentCount = %s, nxvar %s", current_nxvar, next_nxvar)

        # Run variable selection while model improves
        iteration = 0
        while current_nxvar != next_nxvar:
            current_nxvar = next_nxvar

            config = varselect(xy, config)

            next_nxvar = self.count_xvars(config)
            iteration = iteration + 1

        logger.info("Number of Iterations: %s", iteration)
