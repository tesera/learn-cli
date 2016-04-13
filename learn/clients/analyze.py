import logging

import pandas as pd
import pandas.rpy.common as com
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr

from pylearn.lda import cohens_khat, combine_evaluation_datasets

logger = logging.getLogger('pylearn')
importr('MASS')
r = robjects.r
rlearn = importr('rlearn')

def analyze(xy, config, yvar):
    r_xy = com.convert_to_r_dataframe(xy)
    r_config = com.convert_to_r_dataframe(vsel_xy_config)

    args = [
        r_xy,
        r_config,
        'SORTGRP',
        -1,
        yvar,
        'SAMPLE'
    ]

    rlearn.lda(**args)


class Analyze(object):

    def run(self, args):
        outdir = args['--output']
        yvar = args['--yvar']

        xy = pd.read_csv(args['--xy-data'])
        config = pd.read_csv(args['--config'])

        logger.info(':lda: running lda analyze...')
        analyze(xy, config, yvar)

        prior = com.load_data('lda.prior')
        ctabulation = com.load_data('lda.ctabulation')
        posterior = com.load_data('lda.posterior')
        ctball = com.load_data('lda.ctball')
        varmeans = com.load_data('lda.varmeans')
        dfunct = com.load_data('lda.dfunct')
        bwratio = com.load_data('lda.bwratio')

        logger.info(':lda: applying Cohens Khat and writing to ctabsum')
        ctabsum = cohens_khat(ctabulation)

        logger.info(':lda: combininig evaluation datasets into assess')
        assess = combine_evaluation_datasets(ctabsum, posterior, config)

        assess.to_csv(os.path(outdir, 'lda_x_assess.csv'))

        #TODO: eval if we really need to serialize avgp and rloadrank
