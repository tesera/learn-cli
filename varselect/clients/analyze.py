import rpy2.robjects as robjects
from rpy2.robjects.packages import STAP
from rpy2.robjects.packages import importr

from pyvarselect.ldanalysis.CohensKhat import CohensKhat
from pyvarselect.ldanalysis.CombineEvaluationDatasets import CombineEvaluationDatasets

class Analyze(object):
    importr('MASS')

    def __init__(self):
        self.analyze = importr('rvarselect').lda_RunLinearDiscriminantVariableAnalysis

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
