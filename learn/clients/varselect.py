import os
import logging
import os
import pandas as pd
from rpy2.robjects import pandas2ri
pandas2ri.activate()

import rpy2.robjects as robjects
from rpy2.robjects.packages import importr

from pylearn.varselect import (count_xvars, rank_xvars, extract_xvar_combos,
                               remove_high_corvar)

logger = logging.getLogger('pylearn')
importr('subselect')
importr('logging')
importr('jsonlite')
r = robjects.r
rlearn = importr('rlearn')

def var_select(xy, config, args):
    args['--nSolutions'], args['--minNvar'], args['--maxNvar'] = args['--iteration'].split(':')

    varselect = rlearn.vs_selectVars(xy=xy, config=config,
        yName=args['--yvar'],
        removeRowValue=-1,
        removeRowColName='SORTGRP',
        improveCriteriaVarName=args['--criteria'],
        minNumVar=int(args['--minNvar']),
        maxNumVar=int(args['--maxNvar']),
        nSolutions=int(args['--nSolutions']))

    return pandas2ri.ri2py(varselect)

def get_var_corr(xy, uniquevar, args):
    ucorcoef = rlearn.vs_getVarCorrelations(xy, uniquevar,
        removeRowValue=-1,
        removeRowColName='SORTGRP')

    return pandas2ri.ri2py(ucorcoef)

def varselect(data_xy, xy_config, args):

    logger.info('Identify and organize variable sets (varsets)')
    varselect = var_select(data_xy, xy_config, args)

    logger.info('Identify the unique variable sets')
    vsel_x, uniquevar = extract_xvar_combos(varselect)

    logger.info('Rank the variables in terms of their contribution to a model')
    varrank = rank_xvars(varselect)

    logger.info('Complete var select and remove correlation variables')
    ucorcoef = get_var_corr(data_xy, uniquevar, args)

    logger.info('Remove variables which have a high correlation')
    config = remove_high_corvar(varrank, xy_config, ucorcoef)

    return (vsel_x, varrank, config)


class VarSelect(object):

    def run(self, args):
        # disable cloudwatch rlearn logging until it is prod ready
        rlearn.logger_init(log_toAwslogs=False)
        logger.info("*** Starting Variable Selection ***")
        outdir = args['--output']

        data_xy = pd.read_csv(args['--xy-data'], index_col=0, header=0)
        xy_config = pd.read_csv(args['--config'], index_col=0, header=0)

        current_nxvar = count_xvars(xy_config)
        r('current_nxvar <- %d' % current_nxvar)
        logger.info("Initial variable count: %s", current_nxvar)

        vsel_x, varrank, xy_config = varselect(data_xy, xy_config, args)

        next_nxvar = count_xvars(xy_config)
        r('xVarCount <- %d' % next_nxvar)
        logger.info("First iteration Complete %s with variables left.", next_nxvar)
        iteration = 1

        logger.info("Run variable selection while model improves")

        while current_nxvar > next_nxvar:
            iteration += 1
            current_nxvar = next_nxvar

            try:
                vsel_x, varrank, xy_config = varselect(data_xy, xy_config, args)
            except Exception as e:
                logger.error(
                    ('Variable selection stopped due to an error'
                     'Results from iteration %d will be used') % (iteration-1))
                logger.error(e)

            next_nxvar = count_xvars(xy_config)

            logger.info("Iteration %s complete with %s variables left.",
                        iteration, next_nxvar)

        logger.info("Number of Iterations: %s", iteration)
        varrank.to_csv(os.path.join(outdir, 'vsel_varrank.csv'))
        vsel_x.to_csv(os.path.join(outdir, 'vsel_x.csv'))
