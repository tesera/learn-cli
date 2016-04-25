import os
import logging

import pandas as pd
from rpy2.robjects import pandas2ri
pandas2ri.activate()

import rpy2.robjects as robjects
from rpy2.robjects.packages import importr

from pylearn.lda import cohens_khat, combine_evaluation_datasets

logger = logging.getLogger('pylearn')
importr('MASS')
importr('logging')
r = robjects.r
rlearn = importr('rlearn')

def analyze(xy, config, yvar, output):

    args = [
        xy,
        config,
        'SORTGRP',
        -1,
        yvar,
        False,
        output,
        True
    ]

    rlearn.lda(*args)


class Analyze(object):

    def run(self, args):
        rlearn.logger_init()
        outdir = args['--output']
        yvar = args['--yvar']

        xy = pd.read_csv(args['--xy-data'])
        config = pd.read_csv(args['--config'])

        logger.info(':lda: running lda analyze...')
        analyze(xy, config, yvar, outdir)

        ctabulation = pd.read_csv(os.path.join(outdir, 'CTABULATION.csv'))
        posterior = pd.read_csv(os.path.join(outdir, 'POSTERIOR.csv'), index_col=['VARSET'])
        dfunct = pd.read_csv(os.path.join(outdir, 'DFUNCT.csv'))

        logger.info(':lda: applying Cohens Khat and writing to ctabsum')
        ctabsum = cohens_khat(ctabulation)

        logger.info(':lda: combininig evaluation datasets into assess')
        assess = combine_evaluation_datasets(ctabsum, posterior, config)

        # todo: hack; remove once rlearn fixed
        import glob
        files = glob.glob(os.path.join(outdir, '*.csv'))
        for filename in files:
            os.unlink(filename)

        dfunct.to_csv(os.path.join(outdir, 'lda_x_dfunct.csv'), index=False)
        assess.to_csv(os.path.join(outdir, 'lda_x_assess.csv'), index=False)
