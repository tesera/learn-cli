import os

import rpy2.robjects as robjects
from rpy2.robjects.packages import STAP
from rpy2.robjects.packages import importr

from pylearn.ldanalysis.CohensKhat import CohensKhat
from pylearn.ldanalysis.CombineEvaluationDatasets import CombineEvaluationDatasets
from pylearn.ldanalysis.ldarank import rank_file

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
        rank_file(os.path.join(args['<outputdir>'], 'ASSESS.csv'), rank_coefficient=200)
