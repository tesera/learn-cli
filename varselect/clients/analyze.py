import rpy2.robjects as robjects
from rpy2.robjects.packages import STAP
from rpy2.robjects.packages import importr

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
