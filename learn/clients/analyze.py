import os
import logging

import rpy2.robjects as robjects
from rpy2.robjects.packages import STAP
from rpy2.robjects.packages import importr

from pylearn.ldanalysis.CohensKhat import CohensKhat
from pylearn.ldanalysis.CombineEvaluationDatasets import CombineEvaluationDatasets
from pylearn.ldanalysis.varset import export_rloadrank, export_avgp

logger = logging.getLogger('pylearn')

class Analyze(object):
    importr('MASS')

    def __init__(self):
        self.analyze = importr('rlearn').lda_RunLinearDiscriminantVariableAnalysis

    def run(self, args):
        logger.info(':lda: running lda analyze...')
        aargs = [
            args['--xy-data'],
            args['--config'],
            'SORTGRP',
            -1,
            args['--yvar'],
            'SAMPLE',
            args['--output']
        ]

        self.analyze(*aargs)

        logger.info(':lda: running CohensKhat...')
        cohens_khat = CohensKhat(args['--output'])
        cohens_khat.run()

        logger.info(':lda: running CombineEvaluationDatasets...')
        combine_evaluation = CombineEvaluationDatasets(args['--output'])
        combine_evaluation.run()

        xy_reference_path = os.path.join(args['--output'], 'ANALYSIS.csv')
        x_var_dfunct_path = os.path.join(args['--output'], 'DFUNCT.csv')
        x_vary_summary_path = os.path.join(args['--output'], 'SUMMARY.csv')

        logger.info(':lda: exporting relative loading ranks for all unique xvars in varsets (rloadrank)')
        export_rloadrank(dfunct_path=x_var_dfunct_path, xy_path=xy_reference_path, outfile=x_vary_summary_path)

        logger.info(':lda: exporting an average p file per unique xvar in varsets')
        export_avgp(dfunct_path=x_var_dfunct_path, xy_path=xy_reference_path, outdir=args['--output'])
