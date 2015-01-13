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
# from errorlogger import errorLogger
# from inspect import getmembers, stack
# from loghandler import set_full_logpath
from loghandler import SetLogger
from confighandler import ConfigHandler 
from errorhandler   import handlertry
from errorhandler   import raisetry

import abc
import os
import re
import sys


class RHandlerAbstract(object): # ABSTRACT CLASS ------------------------------
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
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def close(self):
        """
        :NAME:
        :DESCRIPTION:
            Closes the [R] environment
        :ARGUMENTS:
        :VARIABLES:
        :METHODS:
        :RETURNS:
        :USAGE:
        """
        pass
    
    @abc.abstractmethod
    def code(self, _code):
        """
        :NAME:
        :DESCRIPTION:
            Passes command line code to the [R] environment
        :ARGUMENTS:
            _code = String or list where each item is a command lines
        :VARIABLES:
        :METHODS:
        :RETURNS:
        :USAGE:
        """
        pass
    
    @abc.abstractmethod
    def connect(self):
        """
        :NAME:
        :DESCRIPTION:
            Establishes and connects to an [R] environment. 
            
        :ARGUMENTS:
        :VARIABLES:
        :METHODS:
        :RETURNS:
        :USAGE:
        """
        pass
    
    @abc.abstractmethod
    def delenv(self, _env):
        """
        :NAME:
        :DESCRIPTION:
            Deletes variables within the [R] environment
        :ARGUMENTS:
            _env = a string containing a single R-variable to delete
                   Or a list of R-variables to delete
    
        :VARIABLES:
        :METHODS:
        :RETURNS:
        :USAGE:
        """
        pass
    
    @abc.abstractmethod
    def env(self):
        """
        :NAME:
        :DESCRIPTION:
            User interface for managing the [R] environment.
        :ARGUMENTS:
        :VARIABLES:
        :METHODS:
        :RETURNS:
        :USAGE:
        """
        pass
    
    @abc.abstractmethod
    def getenv(self, _env):
        """
        :NAME:
        :DESCRIPTION:
            _env = a string containing a single R-variable to retrieve 
                   Or a list of R-variables to retrieve 
        :ARGUMENTS:
        :VARIABLES:
        :METHODS:
        :RETURNS:
        :USAGE:
        """
        pass

    @abc.abstractmethod
    def script(self, _script):
        """
        :NAME:
        :DESCRIPTION:
            Calls an [R] script within the the [R] environment
        :ARGUMENTS:
            _script = String
        :VARIABLES:
        :METHODS:
        :RETURNS:
        :USAGE:
        """
        pass
    
    @abc.abstractmethod
    def setenv(self, _env):
        """
        :NAME:
        :DESCRIPTION:
            Sets variables within the [R] environment
        :ARGUMENTS:
            _env = a string containing a single R-variable to set 
                   Or a list of R-variables to set 
        :VARIABLES:
        :METHODS:
        :RETURNS:
        :USAGE:
        """
        pass
    
    @abc.abstractmethod
    def _cleanup(self):
        """
        :NAME:
        :DESCRIPTION:
            Cleans up the [R] environment
            Intended to be called by close()
        :ARGUMENTS:
        :VARIABLES:
        :METHODS:
        :RETURNS:
        :USAGE:
        """
        pass

    @abc.abstractmethod
    def prep_command(self, _data):
        """"""
        """
        :NAME:
        :DESCRIPTION:
        :ARGUMENTS:
        :VARIABLES:
        :METHODS:
        :RETURNS:
        :USAGE:
        """
        pass


class RHandler(object): # FACTORY ---------------------------------------------
    """
    This is a factory class that will call and return a subclass.

    It is NOT an abstract class.

    The objects classes that are instantiated by this factory will be 
    subclasses of RHandler  
    """
    @staticmethod
    def rHandler(service, *args, **kwargs):
        # Raw rserve implementation
        if      re.match("^rs.*$", str(service.lower())):
                    return rserveHandler(*args, **kwargs)
        
        # Domino labs server
        elif    re.match("^dom.*$", str(service.lower())):
                    raise NotImplementedError

        # Revolution analytics RWS server
        elif    re.match("^rev.*$", str(service.lower())):
                    raise NotImplementedError
                
        # Alteryx services
        elif    re.match("^alter.*$", str(service.lower())):
                    raise NotImplementedError

        else:
            e = ''.join(["RserveHandler.rserveHandler: ", 
                         "'service' parameter does not resolve to ", 
                         "any provided rserve service. Options include: ", 
                         "\n 'rserve' for a raw rserve environment. ", 
                         "\n 'rev' for a Revolution Analytics environment. ", 
                         "\n 'domino' for a Domino Labs environment. ", 
                         "\n 'alteryx' for an Alteryx environment. ", 
                         ])
            raise TypeError(e)
        
    
# class rserveHandler(RHandlerAbstract): # Handler object for a raw Rserve env    
class rserveHandler(object): # Handler object for a raw Rserve env    
    def __init__(self, *args, **kwargs): # **kw MUST COME LAST WITHOUT COMMA    
        """
        Optional params:
        host        = None, 
        port        = None, 
        atomicArray = None, 
        arrayOrder  = None, 
        defaultVoid = None, 
        oobCallback = None,
        
        """        
        self.log = SetLogger() # this should have been set by calling script        
        
        # ConfigHandler is a singleton. This should return an existing obj
        self.config = ConfigHandler()

        # These MUST come after parsing the config , to allow for overrides
        # but BEFORE the final SetLogger. 
        self._override_with_kw_vars(kwargs)

        self._set_mandatory_defaults({"port":6311,
                                      "atomicArray":True, 
                                      "arrayOrder":"C", 
                                      "defaultVoid":False, 
                                      "oobCallback":None,
#                                       "boogerhead":1
                                      })

        self.log.debug("rserveHandler object instantiated.")

        sys.exit() #333

# ___________________________________________________________________________
# PRIVATE METHODS 

    @handlertry("FATAL: rhandler._override_with_kw_vars")
    def _override_with_kw_vars(self, kwargs):
        for key in kwargs.keys():
            self.config.__dict__[key] =  kwargs[key]
        return True
        
#     @handlertry("PassThroughException: rhandler._set_mandatory_defaults")

    @handlertry("PassThroughException: rhandler._set_mandatory_defaults")
    def _set_mandatory_defaults(self, _dict):
        """
        In the event the config file does not have the mandatory variables, 
        and they are not passed in as __init__ variables, they can be set here.
        These defaults can be modified. The order of setting defaults should be:
        1. config file
        2. __init__ parameters
        3. Here (_set_mandatory_defaults) 
        """
        for key in _dict.keys():
            if key not in self.config.__dict__.keys():
                self.config.__dict__[key] = _dict[key]
        return

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
              

    def _prep_string_command(self, _data):
        try:
            _data + "STRINGTEST" # no error = Already a string
            # Can add more checks here
            return _data
        except TypeError, e: # Not a string
            return False
        finally:
            raise

    def _prep_list_command(self, _data):
        try:
            # Check for list    
            _data.append("DELETEME")
            _data.pop() # Remove the test DELETEME
            _data = "\n".join(_data) # Now a string
            # Can add more checks here
            return _data
        except TypeError, e: # Not a list
            return False
        finally:
             raise
         
    def connect(self,        # Override abstract connect  
                host        = 'localhost', 
                port        = 6311, # Rserve default
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
                     
        
  
# ____________________________________________________________________________
# Public methods                

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
#     from RserveHandler import rserveHandler
    o = RHandler()    
    o = Test.test(4)
    
    o = RserveHandler.rserveHandler(service = "rserve",
#                                     screendump = True, 
#                                     debug = True, 
#                                     log_level = 40
                                    )
    print "object = ", o

    