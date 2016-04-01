import os
import logging

import pandas as pd

import rpy2.robjects as robjects
from rpy2.robjects.packages import STAP
from rpy2.robjects.packages import importr

from pylearn.ldanalysis.CohensKhat import CohensKhat
from pylearn.ldanalysis.CombineEvaluationDatasets import CombineEvaluationDatasets
from pylearn.ldanalysis.varset import get_xvars, get_rloadrank, get_avgp

logger = logging.getLogger('pylearn')

class Analyze(object):
    importr('MASS')

    def __init__(self):
        self.analyze = importr('rlearn').lda_RunLinearDiscriminantVariableAnalysis

    def run(self, args):
        outdir = args['--output']
        yvar = args['--yvar']

        logger.info(':lda: running lda analyze...')
        aargs = [
            args['--xy-data'],
            args['--config'],
            'SORTGRP',
            -1,
            yvar,
            'SAMPLE',
            outdir
        ]

        self.analyze(*aargs)

        logger.info(':lda: running CohensKhat...')
        cohens_khat = CohensKhat(outdir)
        cohens_khat.run()

        logger.info(':lda: running CombineEvaluationDatasets...')
        combine_evaluation = CombineEvaluationDatasets(outdir)
        combine_evaluation.run()

        xy_reference_path = os.path.join(outdir, 'ANALYSIS.csv')
        x_var_dfunct_path = os.path.join(outdir, 'DFUNCT.csv')

        xy = pd.read_csv(xy_reference_path)
        dfunct = pd.read_csv(x_var_dfunct_path)

        logger.info(':lda: exporting relative loading ranks for all unique xvars in varsets (rloadrank)')
        rloadrank = get_rloadrank(xy=xy, dfunct=dfunct, yvar=yvar)
        rloadrank.to_csv(os.path.join(outdir, 'RLOADRANK.csv'))

        logger.info(':lda: exporting an average p file per unique xvar in varsets')
        all_xvars = get_xvars(dfunct)
        avgp = get_avgp(xy, all_xvars)
        avgp.to_csv(os.path.join(outdir, 'AVGP.csv'))
