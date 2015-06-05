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

from confighandler  import ConfigHandler 
from errorhandler   import handlertry
from errorhandler   import raisetry
from functions      import override_kw_vars
from functions      import set_mandatory_defaults
from functions      import fileExists
from functions      import pathExists
# from loghandler     import SetLogger
from loghandler     import log
from signal         import *

import abc
import atexit
import os
import pyRserve as R
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
    def cmd(self, _data):
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
        
    
class rserveHandler(RHandlerAbstract): # Handler object for a raw Rserve env    
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
        # Set exit and cleanup        
        for sig in (SIGABRT,SIGINT,SIGTERM,SIGQUIT):
            signal(sig, self._cleanup)
        atexit.register(self._cleanup)  

        log.debug("Instantiating rserveHandler object.")
        
#         self.log = SetLogger() # this should have been set by calling script        
        
#         # ConfigHandler is a singleton. This should return an existing obj
#         self.config = ConfigHandler()

#         # These MUST come after parsing the config , to allow for overrides
#         # but BEFORE the final SetLogger. 
#         override_kw_vars(self, kwargs) # set in both self and self.config objs
#         override_kw_vars(self.config, kwargs) # set in both self and self.config
        
#         set_mandatory_defaults(self.config, 
#                                {"port"        :6311,
#                                 "atomicArray" :True, 
#                                 "arrayOrder"  :"C", 
#                                 "defaultVoid" :False, 
#                                 "oobCallback" :None,
# #                               "boogerhead":1
#                                 })

        self.rhandler_host  = kwargs.pop("rhandler_host"       ,"localhost")
        self.rhandler_port           = kwargs.pop("port"         ,"6311")
        self.rhandler_atomicArray    = kwargs.pop("atomicArray"  , True)
        self.rhandler_arrayOrder     = kwargs.pop("arrayOrder"   , "C")
        self.rhandler_defaultVoid    = kwargs.pop("defaultVoid"  , False)
        self.rhandler_oobCallback    = kwargs.pop("oobCallback"  , None)

        print 'self.rhandler_host  =', self.rhandler_host # kwargs.pop("rhandler_host"       ,"localhost")
        print 'self.rhandler_port           =', self.rhandler_port # kwargs.pop("port"         ,"6311")
        print 'self.rhandler_atomicArray    =', self.rhandler_atomicArray # kwargs.pop("atomicArray"  , True)
        print 'self.rhandler_arrayOrder     =', self.rhandler_arrayOrder# kwargs.pop("arrayOrder"   , "C")
        print 'self.rhandler_defaultVoid    =', self.rhandler_defaultVoid# kwargs.pop("defaultVoid"  , False)
        print 'self.rhandler_oobCallback    =', self.rhandler_oobCallback # kwargs.pop("oobCallback"  , None)

        self.connect()
        

# ___________________________________________________________________________
# PRIVATE METHODS 

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
        log.debug("Cleaning up Rhandler...")
        # do stuff
        self.close()
        # other stuff
        return

#     def _load_config_file(self):
#         """
#         """
#         log.debug(("Loading config file" + str(self.config_file)))
#         
#         if ((self.config_file is None) or
#             (self.config_file == "")
#             ): return
# 
#         self.config = configHandler(config_file = self.config_file,
#                                     screendump = True, 
#                                     debug = True 
#                                     )
#         self.config.load_vars(self)
#         
#         return

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
#         log.info(''.join([str(self.__class__.__name__), 
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
         


#______________________________________________________________________________
# PUBLIC METHODS (OVERIDDEN FROM ABSTRACT)

    #@handlertry("PassThroughException:")
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
        self.conn.close()
        # other stuff
        return
    
    #@handlertry("PassThroughException:")
    def code(self, _cmd):
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
        _cmd = self.cmd(_cmd)
        return self.conn.eval(_cmd)
        
    #@handlertry("PassThroughException:")
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
        raise NotImplementedError
    
    #@handlertry("PassThroughException:")
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
        raise NotImplementedError
    
    #@handlertry("PassThroughException:")
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
        raise NotImplementedError

    #@handlertry("", tries = 2)
    def script(self, *args, **kwargs):
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
        # Two ways to do this:
        # 1. Call a source command within the R environ
        # 2. Copy the text of the script file into  Python var, and eval that
        # Need to determine which is faster and less troublesome
        # Assuming number 1
        # Format: source(paste(HOME_CONF,"XIterativeVarSel.R.conf", sep = ""))
        try:#____________________________________________________
            # If kwargs["fullpath"] is not set, will trigger the exception
            # which goes on to check for path and filename separately
            if not fileExists(kwargs["fullpath"]):
                # kwargs["fullpath"] set, but invalid
                raise Exception("FullPathDoesNotExist") 
            
        except (NameError, AttributeError), e:
            try:#____________________________________________________
                if not pathExists(kwargs["path"]): 
                    raise Exception("PathDoesNotExist")
    
            except (NameError, AttributeError), e:
                raise Exception("PathDoesNotExist")
            
    
            try:#____________________________________________________
                if not fileExists(kwargs["filename"]): 
                    raise Exception("FileDoesNotExist") 
    
            except (NameError, AttributeError), e:
                    raise Exception("FileDoesNotExist") 

            ##########################################################
            # REPLACE THIS WITH THE PATH HANDLER
            # For now just add a "/"
            kwargs["path"] = kwargs["path"] + "/"
            ##########################################################

            kwargs["fullpath"] = kwargs["path"] + kwargs["filename"]
                
    
        _cmd =  ''.join(["source(paste(", 
                         str(kwargs["fullpath"]), 
                         ', sep = ""'])
            

        _cmd = self.cmd(_cmd)
        
        print "_cmd = ", _cmd #3333
        
        self.conn.eval(_cmd)
         
    #@handlertry("PassThroughException:")
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
        raise NotImplementedError
    
    #@handlertry("PassThroughException:")
    def cmd(self, _cmd):
        """

        FOR NOW, we're just going to return the command, under the assumption 
        that the coder knows what s/he is doing. Eventually, this should run a 
        series of sanity checks on the command to prevent breakage.
        
        Proper procedure will be that all commands be checked through here
        before being passed onto the R environment, so we need something in 
        place...
        
        :NAME:
        :DESCRIPTION:
            Preps a command before being sent to code
        :ARGUMENTS:
        :VARIABLES:
        :METHODS:
        :RETURNS:
        :USAGE:
        """
        return _cmd
        
        # FUTURE
        # if string: return self._prep_string_command(_cmd)
        # elif list: return self._prep_list_command(_cmd)
        # elif something else: return something else
        # else: ups

#     #@handlertry("PassThroughException:")
    def connect(self): # No defaults at this level. Always use config vars
        """
        :NAME:
            connect([host        = 'localhost', 
                    port        = 6311, # Rserve default
                    atomicArray = True, # Sets R to return arrays
                    arrayOrder  = 'C', 
                    defaultVoid = False, 
                    oobCallback = None
                    ])
        
        :DESCRIPTION:
            Creates the rserve service connection as a raw connection to an 
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
                    
                    In other words, if the [R] interpreter environment creates
                    an array, you get a Python array back. 
                     
                    Default: True
 
            arrayOrder: DEPRICATED
                    The order in which data in multi-dimensional arrays is 
                    returned. Provide 'C' for c-order, F for fortran. 

                    Default: 'C'
                    
                    --- DEPRICATED --------------------------------------------
                    arrayOrder HAS BEEN REMOVED FROM pyRserve...ALTHOUGH IT 
                    STILL APPEARS IN A help(pyRserve). Apparently other bugfixes 
                    made it redundant.
                    
                    Attempts to use it will raise an error.  
                    --- DEPRICATED --------------------------------------------
            
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
        print 'self.server=', self.rhandler_host#333
        print 'port          =', self.rhandler_port#333 
        print 'atomicArray   =',  self.rhandler_atomicArray,#333 
        #arrayOrder was removed. See __doc__ 
        #                               arrayOrder    = self.arrayOrder, 
        print 'defaultVoid   = ', self.rhandler_defaultVoid,#333 
        print 'oobCallback   = ', self.rhandler_oobCallback#333
                
        self.conn = R.connect(host          = self.rhandler_host, 
                              port          = self.rhandler_port, 
                              atomicArray   = self.rhandler_atomicArray, 
                                #arrayOrder was removed. See __doc__ 
#                               arrayOrder    = self.arrayOrder, 
                              defaultVoid   = self.rhandler_defaultVoid, 
                              oobCallback   = self.rhandler_oobCallback)
        # Cheap check
        try:
            if ( int(self.conn.eval("3*3")) == 9):
                log.debug(''.join(["Established connection to Rserve with ", 
                                       "host:", 
                                       str(self.server), ", ",  
                                       "port:", 
                                       str(self.port), ", ", 
                                       "atomicArray: DEPRICATED/UNUSED, ",
                                       "defaultVoid:", 
                                       str(self.defaultVoid), ", ", 
                                       "oobCallback:", 
                                       str(self.defaultVoid), "."
                                       ]))
            else:
                raise ValueError()
                print "self.testvar inside _connect", self.testvar #3333

        except ValueError, e:
            e = ''.join(["[R] environment connection returning garbage ", 
                         "to attempted eval of (3*3). Please troubleshoot. ", 
                         str(e)])
            raise ValueError(e)

        return self.conn

        
  
# ____________________________________________________________________________
# Public methods                
        
    
if __name__ == "__main__":
    print "must be called from mrat_variable_selection.py"
    from mrat_variable_selection import mrat_variable_selection
    o = mrat_variable_selection()
    print o.R.script(
                    path = "/bs/path", 
                    filename = "bsfilename", 
#                     fullpath = "/shared/GitHub/Tesera/MRAT_Refactor/bin/XIterativeVarSelCorVarElimination.R"
                     )
    
    
    
    
#     print o.R.script("/bs/path", "bsfilename")