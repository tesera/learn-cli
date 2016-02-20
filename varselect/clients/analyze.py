import rpy2.robjects as robjects
from rpy2.robjects.packages import STAP
from rpy2.robjects.packages import importr

class Analyze(object):

    def __init__(self):
        print('init analyze')
        # self.rpredict = importr('rpredict')

    def run(self, args):
        print('running analyze')
        # self.rpredict.RunLinearDiscriminantVariableAnalysis(args['LVIFILENAME'],
        #                         args['XVARSELECTFILENAME']
        #                         args['--excludeRowVarName']
        #                         args['--excludeRowValue']
        #                         args['--excludeRowValue']
        #                         args['--classVariableName']
        #                         args['--classNames']
        #                         args['--priorDistribution']
        #                         args['OUTDIR'])
