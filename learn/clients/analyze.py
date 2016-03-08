import os

import rpy2.robjects as robjects
from rpy2.robjects.packages import STAP
from rpy2.robjects.packages import importr

from pylearn.ldanalysis.CohensKhat import CohensKhat
from pylearn.ldanalysis.CombineEvaluationDatasets import CombineEvaluationDatasets
from pylearn.ldanalysis.varset import rank_varsets, summarize_xy, adjust_dfunct_coef

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

        # todo: yr, rank_coefficient as cli arg?
        rank_varsets(os.path.join(args['--output'], 'ASSESS.csv'), rank_coefficient=200)

        # summarize all x-vars in varset via dfunct by ?claims pivot
        xy_reference_path = os.path.join(args['--output'], 'ANALYSIS.csv')
        x_var_dfunct_path = os.path.join(args['--output'], 'DFUNCT.csv')
        x_vary_summary_path = os.path.join(args['--output'], 'SUMMARY.csv')

        summarize_xy(xy_reference_path, x_var_dfunct_path, x_vary_summary_path)

        # adjust dfunct coef sign based on summary result value
        adjust_dfunct_coef(x_var_dfunct_path, x_vary_summary_path)
