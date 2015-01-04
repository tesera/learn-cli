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

from checks import fileExists
from errorlogger import errorLogger
from inspect import getmembers, stack
from loghandler import set_full_logpath
from loghandler import setLogger
from confighandler import configHandler 

import errorhandler
import os
import sys
 
class rserveHandler:
    """
    Creates an rserve handler for managing the [R] environment
    as well as passing objects back and forth and running the environment
    
    The intent is for this handler to blind whether a local install of rserve
    is used, or whether a commercial package such as "Domino labs", "Alteryx"
    or something else
    
    WHAT DOES THIS NEED TO PROVIDE?
    - Create a a connection to an [R] runtime environment
    - Isolate [R] runtime environments
    - Call and return values from [R] scripts
    - Allow the submission of [R[ code    
    - Manage an [R] environment
    - Close (and clean) an [R] environment
    - (possibly) manage the memory of [R] environment
    - Pass data objects to [R[ environment
    - Convert data objects to and from forms suitable for the selected [R] environment
    
    """
    def __init__(self, 
                 service        = None, 
                 config_file    = "../etc/XIterativeVarSel.py.conf", 
                 logfile        = "XIterativeVarSel.log",
                 log_path       = None,
                 log_level      = 40,
                 screendump     = False, 
                 debug          = False,
                 **kw): # **kw MUST COME LAST WITHOUT COMMA    

        """
        """        

        # Create temporary startup log. 
        # This allows for logging to be set by the config file
        # But still track what's happening
        self.app_name = self._get_app_name()
        self.log = setLogger(app_name = self.app_name, 
                             logfile = "startup.log",
                             log_path = "./", #Always local for startup
                             log_level = log_level,
                             screendump = screendump, 
                             debug = debug
                             )
        
        self.log.debug("Temp logger started.")
        
        # These MUST come after parsing the logfile, to allow for overrides. 
        self.app_name       = self._set_app_name()
        self.service        = self._set_service_flag(service)
        self.config_file    = config_file
        self.logfile        = logfile
        self.screendump     = screendump
        self.debug          = debug
    
    #         self.errorlog = errorLogger("rservehandler", 
#                                     screendump = screendump, 
#                                     debug = debug)

        self._load_config_file()        

        # This is a local function to do pre and post calling the 
        # loghandler.setLoggger method
        self.log = self._setLogger(
#                              app_name = self.app_name, 
#                              logfile = self.logfile,
#                              log_path = self.log_path, 
#                              log_level = self.log_level, 
#                              screendump = self.screendump, 
#                              debug = self.debug
                             )
        self.log.debug("Permanent Log file started.")

        # Override any self.vars passed into class
        print "loading keyword overrides..." #333
        self._override_with_kw_vars(kw)
        print "Done."

        for i in self.__dict__.keys(): #333
            print i, self.__dict__[i] #3333

        sys.exit() #333

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
                        

# ___________________________________________________________________________
# PRIVATE METHODS 
    def _connect_raw_rserve(self, 
                host        = 'localhost', 
                port        = 6311, 
                atomicArray = True, 
                arrayOrder  = 'C', 
                defaultVoid = False, 
                oobCallback = None
                ):
        """
        :NAME:
            _connect_raw_rserve
        
        :DESCRIPTION:
            Crates the rserve service connection as a raw connection to an 
            Rserve instance.
        
        :ARGS:
            host: provide hostname where Rserve runs, or leave as empty string 
                  to connect to localhost.
                  Default localhost
            
            port: Rserve port number. 
                  Default: 6311
            
            atomicArray:
                    If True: when a result from an Rserve call is an array with 
                    a single element that single element is returned. Otherwise 
                    the array is returned unmodified.
                    Default: True
            
            arrayOrder:
                    The order in which data in multi-dimensional arrays is 
                    returned. Provide 'C' for c-order, F for fortran. 
                    Default: 'C'
            
            defaultVoid:
                    If True then calls to conn.r('..') don't return a result by 
                    default.
                    Default: False
            
            oobCallback:
                    Callback to be executed when self.oobSend/oobMessage is 
                    called from R. The callback receives the submitted data and 
                    a user code as parameters. If self.oobMessage was used, 
                    the result value of the callback is sent back to R.
                    Default: lambda data, code=0: 
                             None (oobMessage will return NULL)

        :RETURNS:
        :METHODS:
        
        """

    def _get_app_name(self):
        app_name = os.path.basename(__file__)
        app_name = app_name.rsplit(".", 1)
        return app_name[0]

    def _load_config_file(self):
        """
        """
        self.log.debug(("Loading config file" + str(self.config_file)))
        
        if ((self.config_file is None) or
            (self.config_file == "")
            ): return

        self.config = configHandler(config_file = self.config_file,
                                    screendump = True, 
                                    debug = True 
                                    )
        self.config.load_vars(self)
        
        return

    def _set_app_name(self):
        return self._get_app_name()
    
    def _set_errorhandler(self):
        customErrorHandler = errorhandler.errorhandler(self.log)
        self.err = customErrorHandler.err()
        
#     def _start_logging(self):
#         try:
#             # Test for a string
#             self.logfile + "string"
#  
#         except NameError, e:
#             e = ''.join(["ParameterNotSet: ", 
#                          "Variable 'self.logfile' does not appear to exist. ", 
#                          "Please confirm there is an entry in the ", 
#                          "configuration file or the config_file parameter ",
#                          "has been properly passed into the class. ", 
#                          "A default logfile will be created in this directory."
#                          ])
# #             print e
#             self.logfile = ''.join(["./",self.__class__.__name__,".log"])
#          
#         except (TypeError, AttributeError), e:
#             e = ''.join(["ParameterNotSet: ", 
#                          "Variable 'self.logfile' does not appear to ", 
#                          "be a string. Please confirm the entry in the ", 
#                          "configuration file or the config_file parameter ",
#                          "has been properly passed into the class. ", 
#                          "A default logfile will be created in this directory."
#                          ])
# #             print e
#             self.logfile = ''.join(["./",self.__class__.__name__,".log"])
#  
#         # epicarlo is the main callable, so use createLogger and not checkLogger
#         self.log = createLogger(app_name = self.__class__.__name__, 
#                                 logfile = self.logfile, 
#                                 log_level = self.log_level, 
#                                 screen = self.log_to_screen)
#  
#         self.log.info(''.join([str(self.__class__.__name__), 
#                                " logger started."
#                                ]))

    def _set_service_flag(self, service):
        """"""
        if   (("rserve" in str(service).lower()) or
              ("raw"    in str(service).lower())):
              return "RAW"
        
        elif (("domin" in str(service).lower())):
              return "DOMINO"

        elif (("alteryx" in str(service).lower())):
              return "ALTERYX"          

        elif (("revo" in str(service).lower())):
              return "REVOLUTION"
          
        elif (("dataiku" in str(service).lower())):
              return "DATAIKU"
          
        elif (("alpine" in str(service).lower())):
              return "ALPINE"

        # A raw connection to an Rserve installation is the current default          
        else:
              return "RAW"
              

    def _setLogger(self):
        self.log.debug(("Starting permanent log..."))

        self.full_log_path = set_full_logpath(
                                              self.log_path, 
                                              self.logfile, 
                                              self.app_name)        

        self.log = setLogger(app_name = self.app_name, 
                             logfile = self.logfile,
                             log_path = self.log_path, 
                             log_level = self.log_level, 
                             screendump = self.screendump, 
                             debug = self.debug
                             )
        
        self.log.info("Permanent logger started.")

        self.log.debug(''.join(["rservehandler: Transferring startup log ", 
                                      "to permanent log file '", 
                                      str(self.full_log_path),
                                      "'."]))
        
        result = self.errorlog.transfer(self.full_log_path)
        if not result:
            e = ''.join(["rservehandler._transfer_initial_error_log:", 
                         "Unknown failure attempting to transfer the existing ",
                         "temporary errorlog log file to the permanent one.\n",
                         "ORIGINAL ERROR:", 
                         str(result), 
                         "Continuing."])
            self.log.debug(e) 
        
  
# ____________________________________________________________________________
# Public methods                

    def connect(self, *args, **kwargs):
        """"""
        pass 
            
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
    o = rserveHandler(screendump = True, debug = True, log_level = 40)
    print "object = ", o
    