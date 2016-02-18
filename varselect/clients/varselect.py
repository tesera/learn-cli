import rpy2.robjects as robjects
from rpy2.robjects.packages import STAP
from rpy2.robjects.packages import importr

from pyvarselect.count_xvar_in_xvarsel import CountXVarInXvarSel
from pyvarselect.test_extract_rvariable_combos import ExtractRVariableCombos
from pyvarselect.rank_var import RankVar
from pyvarselect.remove_highcorvar_from_xvarsel import RemoveHighCorVarFromXVarSel

class VarSelect(object):
    importr('subselect')

    def __init__(self):
        self.flog = importr('futile.logger')
        self.r = robjects.r

    def initR(self, args):

        for key, value in args.iteritems():
            if('--' in key):
                key = key.strip('-')
                if(value is not None and value.isdigit()):
                    self.r('%s <- %s' % (key, value))
                else:
                    self.r('%s <- "%s"' % (key, value))

        self.r('lviFileName <- "%s"' % args['LVIFILENAME'])
        self.r('outDir <- "%s"' % args['OUTDIR'])
        self.r('xVarSelectFileName <- "%s"' % args['XVARSELECTFILENAME'])
        self.r('uniqueVarPath <- "%s/UNIQUEVAR.csv"' % args['OUTDIR'])
        self.r('printFileName <- "%s/UCORCOEF.csv"' % args['OUTDIR'])
        self.r('xVarCountFileName <- "%s/XVARSELV1_XCOUNT.csv"' % args['OUTDIR'])
        self.r('varSelect <- "%s/VARSELECT.csv"' % args['OUTDIR'])

    def run(self, args):
        self.initR(args)

        self.flog.flog_info("Starting variable_selection")
        count_xvar_in_xvarsel = CountXVarInXvarSel(args['OUTDIR'])
        rank_var = RankVar(args['OUTDIR'])
        extract_rvariable_combos = ExtractRVariableCombos(args['OUTDIR'])
        remove_highcorvar = RemoveHighCorVarFromXVarSel(args['OUTDIR'])
        rvarselect = importr('rvarselect')

        currentCount = count_xvar_in_xvarsel.count()
        self.r('initialCount <- scan(xVarCountFileName)')
        self.flog.flog_info("Initial variable count: %s", self.r['initialCount'])
        rvarselect.vs_IdentifyAndOrganizeUniqueVariableSets(self.r['lviFileName'], self.r['xVarSelectFileName'], self.r['varSelect'])

        # test_EXTRACT_RVARIABLE_COMBOS_v2.Extract_RVariable_Combos_v2() identifies the unique variable sets and organizes them into a new file VARSELV.csv;
        uniqueVarSets = extract_rvariable_combos.extract_rvariable_combos()

        # Rank the variables in terms of their contribution to a model
        ranksVariables = rank_var.rank()

        # test2_XIterativeVarSelCorVarElimination.R runs steps 13 -18 ZCompleteVariableSelectionPlusRemoveCorrelationVariables.R
        rvarselect.vs_CompleteVariableSelectionPlusRemoveCorrelationVariables(self.r['lviFileName'], self.r['uniqueVarPath'], self.r['printFileName'])

        removeCorXVars = remove_highcorvar.remove_high_cor_vars()
        nextCount = count_xvar_in_xvarsel.count()
        self.flog.flog_info("CurrentCount = %s, nextCount %s", currentCount, nextCount)

        # "Kluge" is: Helps get around an unknown crash when calling test3_XiterativeVarSelCorVarElimination.R
        self.r('xVarCount <- scan(xVarCountFileName)')

        # LOOP THROUGH THE AUTOMATED VARIABLE SELECTION PROCESS TO ELIMINATE VARIABLES THAT DO NOT CONTRIBUTE TO THE MODEL
        counter = 0
        while currentCount != nextCount:
            currentCount = nextCount
            #config part of test_XItertative plus test_ZCompleteVariableSelectionPlusRemoveCorrelationVariables.R
            #r.source("/opt/xvarselect/bin/XIterativeConfFile.R")
            rvarselect.vs_IdentifyAndOrganizeUniqueVariableSets(self.r['lviFileName'], self.r['xVarSelectFileName'], self.r['varSelect'])

            extract_rvariable_combos.extract_rvariable_combos()
            rank_var.rank()

            rvarselect.vs_CompleteVariableSelectionPlusRemoveCorrelationVariables(self.r['lviFileName'], self.r['uniqueVarPath'], self.r['printFileName'])

            remove_highcorvar.remove_high_cor_vars()
            count_xvar_in_xvarsel.count()
            counter = counter +1

        self.flog.flog_info("Number of Iterations: %s", counter)
