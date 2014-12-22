##############################################################################
# Removal of the "__license__" line or content from  "__license__", or removal 
# of "__author__" in this or any constituent # component or file constitutes a 
# violation of the licensing and copyright agreement. 
__author__      = "Mike Rightmire"
__copyright__   = "BioCom Software"
__license__     = "Tesera"
__license_file__= "Clause1.PERPETUAL_AND_UNLIMITED_LICENSING_TO_THE_CLIENT.py"
__version__     = "0.9.0.3"
__maintainer__  = "Mike Rightmire"
__email__       = "Mike.Rightmire@BiocomSoftware.com"
__status__      = "Development"
##############################################################################

from checks import fileExists
from inspect import getmembers, stack
from loghandler import setLogger
from confighandler import configHandler 

import errorhandler
import sys
 
class rserveHandler:
    """
    Creates an rserve handler for managing the [R] environment
    as well as passing objects back and forth and running the environment
    
    The intent is for this handler to blind whether a local install of rserve
    is used, or whether a commercial package such as "Domino labs", "Alteryx"
    or something else
    """
    def __init__(self, 
                 provider       = None, 
                 config_file    = "../etc/XIterativeVarSel.py.conf", 
                 logfile        = "../log/XIterativeVarSel.log",
                 screendump     = False, 
                 debug          = False,
                 **kw): # **kw MUST COME LAST WITHOUT COMMA    
        # For now, no parameters passed. This may change to accommodate the 
        # needs of the many different potential environments. 
        # IT'S CRITICAL that the parameters passed wont change regardless of 
        # what end rserve environment we.
        """
        """
        self.provider       = provider
        self.config_file    = config_file
        self.logfile        = logfile
        self.screendump     = screendump
        self.debug          = debug

        self._load_config_file()        

        sys.exit() #333

        self._start_logging()

        for i in self.__dict__.keys(): #333
            print i, self.__dict__[i] #3333
        
        
        # Override any self.vars passed into class
        print "loading keyword overrides..." #333
        self._override_with_kw_vars(kw)
        print "Done."

        # Errorhandler
        print "Setting error handler..." #333
        self._set_errorhandler()
        print "Done."





        # Errorhandler
        print "Setting errorhandler..." #333
        self._set_errorhandler()
        print "Done." #333

        
#         # Set errorhandler ----------------------------------------------------
#         self.CustomErrorHandler = errorhandler.errorhandler(self.log)
#         self.err = self.CustomErrorHandler.err()
                        

### PRIVATE METHODS ===========================================================
    def _load_config_file(self):
        """
        """
        if ((self.config_file is None) or
            (self.config_file == "")
            ): return

        self.config = configHandler(config_file = self.config_file,
                                    screendump = True, 
                                    debug = True 
                                    )
        self.config.load_vars(self)

        return

    def _set_errorhandler(self):
        customErrorHandler = errorhandler.errorhandler(self.log)
        self.err = customErrorHandler.err()
        
    def _start_logging(self):
        try:
            # Test for a string
            self.logfile + "string"
 
        except NameError, e:
            e = ''.join(["ParameterNotSet: ", 
                         "Variable 'self.logfile' does not appear to exist. ", 
                         "Please confirm there is an entry in the ", 
                         "configuration file or the config_file parameter ",
                         "has been properly passed into the class. ", 
                         "A default logfile will be created in this directory."
                         ])
#             print e
            self.logfile = ''.join(["./",self.__class__.__name__,".log"])
         
        except (TypeError, AttributeError), e:
            e = ''.join(["ParameterNotSet: ", 
                         "Variable 'self.logfile' does not appear to ", 
                         "be a string. Please confirm the entry in the ", 
                         "configuration file or the config_file parameter ",
                         "has been properly passed into the class. ", 
                         "A default logfile will be created in this directory."
                         ])
#             print e
            self.logfile = ''.join(["./",self.__class__.__name__,".log"])
 
        # epicarlo is the main callable, so use createLogger and not checkLogger
        self.log = createLogger(app_name = self.__class__.__name__, 
                                logfile = self.logfile, 
                                log_level = self.log_level, 
                                screen = self.log_to_screen)
 
        self.log.info(''.join([str(self.__class__.__name__), 
                               " logger started."
                               ]))
                
    def open(self):
        """
        NAME:
            rserveHandler.open()
            
        DESCRIPTION:
            Creates the [R] namespace within the rserve environment.
            
        ARGS:
            None
            
        RETURNS:
            None
            
        RAISES:
            None
        """
        pass
    
if __name__ == "__main__":
    o = rserveHandler()
    print "object = ", o
    