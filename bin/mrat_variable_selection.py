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

        self.config = ConfigHandler(self, "../etc/MRAT.conf")
        self.config.load_vars(self.__class__.__name__)

        self.log = SetLogger()
#         self.log = SetLogger(app_name   = self.app_name, 
#                              logfile    = self.logfile,
#                              log_path   = self.log_path, 
#                              log_level  = self.log_level, 
#                              screendump = self.screendump, 
#                              )
        
        self.log.debug("End of MRATmain run.")


if __name__ == "__main__":
    # It is assumed that the log and 
    class main_program(object):
        def __init__(self):
            self.config = ConfigHandler(self, "../etc/MRAT.conf")
            self.section = "mrat_variable_selection"
            self.config.load_vars(self.section)
        
            self.app_name  = self.config.getattr(self.section, "app_name")
            self.logfile   = self.config.getattr(self.section, "logfile")
            self.log_path  = self.config.getattr(self.section, "log_path")
            self.log_level = self.config.getattr(self.section, "log_level")
        
            self.log = SetLogger(app_name       = self.app_name, 
                                 logfile        = self.logfile,
                                 log_path       = self.log_path, 
                                 log_level      = self.log_level, 
                                 screendump     = True, 
                                 )


    obj = main_program()

#     obj = mrat_variable_selection(
#                    log_level = 10, 
#                    screendump = True, 
#                     )

#     obj = mrat_variable_selection({'log_level':10,'screendump':True}) 
