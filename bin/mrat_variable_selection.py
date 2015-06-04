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

from confighandler import ConfigHandler
from loghandler import log
from rhandler import RHandler
from signal         import *

import atexit
import os

class mrat_variable_selection(object):
    def __init__(self, 
                 config_file, # MANDATORY 
                 app_name    = None, 
                 logfile     = None,
                 log_level   = None,
                 screendump  = None,
                 *args, 
                 **kwargs # Must come last
                 ):

        # Set exit and cleanup        
        for sig in (SIGABRT,SIGINT,SIGTERM,SIGQUIT):
            signal(sig, self._cleanup)
        atexit.register(self._cleanup)        

        # NOTE: ConfigHandler will override some of the self.variables 
        # kwargs passed to the __init__ will override the config file. 
        # Configuration loading goes in the following order:
        # 1. Config file parameters
        # 2. keyword args passed into this __init__
        # 3. Mandatory defaults on a package by package basis if they ere not
        #    included in the config file or the kwargs
        self.config = ConfigHandler(
                        self, 
                        app_name    = app_name, # Shown for reference only 
                        logfile     = logfile, # Shown for reference only
                        log_level   = log_level, # Shown for reference only
                        screendump  = screendump, # Shown for reference only
                        config_file = config_file, # Shown for reference only
                        *args,  
                        **kwargs # Must come last
                                    )
        
        # The first call to log will create a log instance if it does not exist. 
        # The "kwargs.pop('app_name'      , None)," lines will override the 
        #  logger parameters obtained from the config file, if any have been 
        #  passed to __init__
        self.local_filename = str(os.path.basename(__file__))
        log.info(   
                 "Starting '__main__' in " + self.local_filename, 
                 app_name     = kwargs.pop('app_name'      , None), 
                 logfile      = kwargs.pop('logfile'       , None),
                 screendump   = kwargs.pop('screendump'    , None),
                 formatter    = kwargs.pop('formatter'     , None),
                 create_paths = kwargs.pop('create_paths'  , None),
                 )

#         self.R = RHandler.rHandler(service = "rserve")
                 
    def _cleanup(self):
        """"""
        log.info("Completing '__main__' in " + self.local_filename)
        
                 
if __name__ == "__main__":
    o = mrat_variable_selection(
         config_file = '../etc/MRAT.conf',
         app_name   = "MRAT", 
         logfile    = "/Users/mikes/GitHub/Tesera/MRAT_Refactor/log/MRAT.log",
         log_level  = 10,
         screendump = True
         )
