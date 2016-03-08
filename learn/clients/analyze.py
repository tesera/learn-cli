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
        print('running analyze...')
        self.analyze(args['<datafile>'],
                    args['<variablesfile>'],
                    args['--excludeRowVarName'],
                    args['--excludeRowValue'],
                    args['--classVariableName'],
                    args['--priorDistribution'],
                    args['--classNames'],
                    args['<outputdir>'])

        cohens_khat = CohensKhat(args['<outputdir>'])
        cohens_khat.run()

        combine_evaluation = CombineEvaluationDatasets(args['<outputdir>'])
        combine_evaluation.run()

        # todo: yr, rank_coefficient as cli arg?
        rank_varsets(os.path.join(args['<outputdir>'], 'ASSESS.csv'), rank_coefficient=200)

        # summarize all x-vars in varset via dfunct by ?claims pivot
        xy_reference_path = os.path.join(args['<outputdir>'], 'ANALYSIS.csv')
        x_var_dfunct_path = os.path.join(args['<outputdir>'], 'DFUNCT.csv')
        x_vary_summary_path = os.path.join(args['<outputdir>'], 'SUMMARY.csv')

        summarize_xy(xy_reference_path, x_var_dfunct_path, x_vary_summary_path)

        # adjust dfunct coef sign based on summary result value
        adjust_dfunct_coef(x_var_dfunct_path, x_vary_summary_path)
