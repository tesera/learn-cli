##############################################################################
# Removal of the "__license__" line or content from  "__license__", or removal 
# of "__author__" in this or any constituent # component or file constitutes a 
# violation of the licensing and copyright agreement. 
__author__      = "Mike Rightmire"
__copyright__   = "BioCom Software"
__license__     = "Tesera"
__license_file__= "Clause1.PERPETUAL_AND_UNLIMITED_LICENSING_TO_THE_CLIENT.py"
__version__     = "0.9.0.0"
__maintainer__  = "Mike Rightmire"
__email__       = "Mike.Rightmire@BiocomSoftware.com"
__status__      = "Development"
##############################################################################

from loghandler import SetLogger
from confighandler import ConfigHandler

class mrat_variable_selection(object):
    def __init__(self, 
                 app_name   = "MRAT", 
                 logfile    = "MRAT.log",
                 log_path   = "/shared/GitHub/Tesera/MRAT_Refactor/log", 
                 log_level  = 40,
                 screendump = False,
                 ):

        # Explicit is better than implicit, and more tedious
        self.app_name      = app_name 
        self.logfile       = logfile
        self.log_path      = log_path 
        self.log_level     = log_level
        self.screendump    = screendump

        self.config = ConfigHandler(
                                    log_level = 10,
                                    screendump = True,
                                    config_file = "../etc/MRAT.conf"
                                    )
        self.log = SetLogger()
        
        self.log.debug("End of MRATmain run.")
        print "End of MRATmain run."

if __name__ == "__main__":
    # It is assumed that the log and 
    class main_program(object):
        def __init__(self):
            obj = mrat_variable_selection()

    o = main_program()