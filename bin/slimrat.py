from confighandler  import ConfigHandler
from loghandler     import log
from rhandler       import RHandler
from signal         import *

import atexit
import os
import sys

import test_EXTRACT_RVARIABLE_COMBOS_v2
import RANKVAR
import REMOVE_HIGHCORVAR_FROM_XVARSELV
import COUNT_XVAR_IN_XVARSELV1

class mrat_variable_selection(object):
    """"""
    def __init__(self, *args, **kwargs):

        for sig in (SIGABRT, SIGINT, SIGTERM, SIGQUIT):
            signal(sig, self._cleanup)
        atexit.register(self._cleanup)

        # Bridge specific setup
        self.config = ConfigHandler(
            config_file = kwargs.pop('config_file', None),
            *args,
            **kwargs
        )

        self.local_filename = str(os.path.basename(__file__))
        log.info("Starting '__main__' in " + self.local_filename)

        self.R = RHandler.rHandler(
            service                 = self.rhandler_service,
            rhandler_host           = self.rhandler_host,
            rhandler_port           = self.rhandler_port,
            rhandler_atomicArray    = self.rhandler_atomicArray,
            rhandler_arrayOrder     = self.rhandler_arrayOrder,
            rhandler_defaultVoid    = self.rhandler_defaultVoid,
            rhandler_oobCallback    = self.rhandler_oobCallback,
        )
        # Bridge specific setup


        # RUN AUTO VARIABLE SELECTION AND ASSOCIATED SUB SCRIPTS IN R & PYTHON
        currentCount = COUNT_XVAR_IN_XVARSELV1.Count_XVar_in_XVarSelv1()
        # run the Discriminant Analysis and Variable selection procedures.
        # todo:ian what does that "#333 TESTING ONLY" mean?
        self.R.script("/opt/MRAT_Refactor/bin/test_XIterativeVarSelCorVarElimination.R") #333 TESTING ONLY
        # identify the unique variable sets and organizes them into a new file VARSELV.csv
        uniqueVarSets = test_EXTRACT_RVARIABLE_COMBOS_v2.Extract_RVariable_Combos_v2()
        # rank the variables in terms of their contribution to a model
        ranksVariables = RANKVAR.RankVar()
        self.R.script("/opt/MRAT_Refactor/bin/test2_XIterativeVarSelCorVarElimination.R")
        removeCorXVars = REMOVE_HIGHCORVAR_FROM_XVARSELV.Remove_HighCorVar_from_XVarSelv()

        nextCount = COUNT_XVAR_IN_XVARSELV1.Count_XVar_in_XVarSelv1()

        print "currentCount = ", currentCount, "  nextCount = ", nextCount, "\n"


        # "Kluge" is: Helps get around an unknown crash when calling test3_XiterativeVarSelCorVarElimination.R
        self.R.script("/opt/MRAT_Refactor/bin/kluge.R")

        # LOOP THROUGH THE AUTOMATED VARIABLE SELECTION PROCESS TO ELIMINATE VARIABLES THAT DO NOT CONTRIBUTE TO THE MODEL
        counter = 0
        while currentCount != nextCount:
            currentCount = nextCount

            self.R.script("/opt/MRAT_Refactor/bin/XIterativeConfFile.R")

            test_EXTRACT_RVARIABLE_COMBOS_v2.Extract_RVariable_Combos_v2()
            RANKVAR.RankVar()
            self.R.script("/opt/MRAT_Refactor/bin/test2_XIterativeVarSelCorVarElimination.R")
            REMOVE_HIGHCORVAR_FROM_XVARSELV.Remove_HighCorVar_from_XVarSelv()

            nextCount = COUNT_XVAR_IN_XVARSELV1.Count_XVar_in_XVarSelv1()
            counter = counter + 1

        print "Number of Iterations: ", counter, "\n"

    def _cleanup(self):
        """"""
        log.info("Completing '__main__' in " + self.local_filename)
        log.info('Clean exit.')
        sys.exit(0)

if __name__ == "__main__":
    o = mrat_variable_selection(
        config_file = "../etc/MRAT.conf",
#         app_name   = "MRAT",
#         logfile    = "/Users/mikes/GitHub/Tesera/MRAT_Refactor/log/MRAT.log",
         log_level  = 10,
         screendump = True
    )