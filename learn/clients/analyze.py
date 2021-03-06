import os
import logging
import pandas as pd
from rpy2.robjects import pandas2ri
pandas2ri.activate()
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
from schema import Schema, And, Or
from pylearn.lda import cohens_khat, combine_evaluation_datasets

from learn.utils import is_s3_url

logger = logging.getLogger('pylearn')
importr('MASS')
importr('logging')
importr('jsonlite')
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

    rlearn.lda(*args, modelsFirstVarColumnIndex=5)


class Analyze(object):

    @staticmethod
    def _validate(args):
        schema = Schema({
            '--xy-data': Or(
                os.path.isfile, is_s3_url,
                error='<xy_reference_csv> should exist and be readable.'),
            '--config': Or(
                os.path.isfile, is_s3_url,
                error='--config should exist and be readable.'),
            '--output': Or(
                os.path.exists, is_s3_url,
                error='--output should exist and be writable.'),
            '--yvar': And(str, len),
        }, ignore_extra_keys=True)
        args = schema.validate(args)
        return args

    def run(self, args):
        # disable cloudwatch rlearn logging until it is prod ready
        rlearn.logger_init(log_toAwslogs=False)

        logger.info('Validating args')
        args = self._validate(args)
        outdir = args['--output']
        yvar = args['--yvar']

        xy = pd.read_csv(args['--xy-data'], index_col=0, header=0)
        config = pd.read_csv(args['--config'], header=0)

        logger.info(':lda: running lda analyze...')
        analyze(xy, config, yvar, outdir)

        ctabulation = pd.read_csv(os.path.join(outdir, 'CTABULATION.csv'))
        posterior = pd.read_csv(os.path.join(outdir, 'POSTERIOR.csv'), index_col=['VARSET'])
        # hack; combine_evaluation_datasets is only smart enough to merge on VARSET
        # config has the proper NVAR value
        posterior.drop('NVAR', axis=1, inplace=True)
        dfunct = pd.read_csv(os.path.join(outdir, 'DFUNCT.csv'))

        logger.info(':lda: applying Cohens Khat and writing to ctabsum')
        ctabsum = cohens_khat(ctabulation)

        logger.info(':lda: combininig evaluation datasets into assess')
        assess = combine_evaluation_datasets(ctabsum, posterior, config)

        # remove when rlearn passes data frames back from lda/analyze
        import glob
        files = glob.glob(os.path.join(outdir, '*.csv'))
        for filename in files:
            os.unlink(filename)

        dfunct.to_csv(os.path.join(outdir, 'lda_x_dfunct.csv'), index=False)
        assess.to_csv(os.path.join(outdir, 'lda_x_assess.csv'), index=False)
