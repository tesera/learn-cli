import os

import rpy2.robjects as robjects
from rpy2.robjects.packages import STAP
from rpy2.robjects.packages import importr

from pylearn.ldanalysis.CohensKhat import CohensKhat
from pylearn.ldanalysis.CombineEvaluationDatasets import CombineEvaluationDatasets
from pylearn.ldanalysis.varset import export_rloadrank, export_avgp

class Analyze(object):
    importr('MASS')

    def __init__(self):
        self.analyze = importr('rlearn').lda_RunLinearDiscriminantVariableAnalysis

    def run(self, args):
        print 'running analyze...'
        self.analyze(args['<xy_reference_csv>'],
                    args['--config'],
                    'SORTGRP',
                    -1,
                    args['--yvar'],
                    'SAMPLE',
                    args['--output'])

        cohens_khat = CohensKhat(args['--output'])
        cohens_khat.run()

        combine_evaluation = CombineEvaluationDatasets(args['--output'])
        combine_evaluation.run()

        xy_reference_path = os.path.join(args['--output'], 'ANALYSIS.csv')
        x_var_dfunct_path = os.path.join(args['--output'], 'DFUNCT.csv')
        x_vary_summary_path = os.path.join(args['--output'], 'SUMMARY.csv')

        # export relative loading ranks for all unique xvars in varsets
        export_rloadrank(dfunct_path=x_var_dfunct_path, xy_path=xy_reference_path, outfile=x_vary_summary_path)

        # export an average p file per unique xvar in varsets
        export_avgp(dfunct_path=x_var_dfunct_path, xy_path=xy_reference_path, outdir=args['--output'])
