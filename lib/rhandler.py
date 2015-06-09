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
from functions      import checkURL
 
# from loghandler     import SetLogger
from loghandler     import log
from signal         import *
# from pyRserve.rexceptions import RConnectionRefused

import abc
import atexit
import os
import pyRserve as R
import re
import subprocess
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
            RHanlder.close()
            
        :DESCRIPTION:
            Closes the [R] environment connection. 
            
        :ARGUMENTS:
            None

        :RETURNS:
            None
            
        :USAGE:
            RHandlerObject.close()
        """
        pass
    
    @abc.abstractmethod
    def code(self, _code, sanity = False):
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
    
#     @abc.abstractmethod
#     def cmd(self, _data):
#         """"""
#         """
#         :NAME:
#         :DESCRIPTION:
#         :ARGUMENTS:
#         :VARIABLES:
#         :METHODS:
#         :RETURNS:
#         :USAGE:
#         """
#         pass

    @abc.abstractmethod
    def status(self):
        """"""
        """
        :NAME:
            RHandler.status()
            
        :DESCRIPTION:
            Returns an string informational string regarding the [R] 
            environment connection. 
             
        :ARGUMENTS:
            None
            
        :RETURNS:
            String
            
        :USAGE:
        RHandlerObject.status()
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
    def __init__(self, *args, **kwargs):    
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

        self.config = ConfigHandler()

        self._load_vars(dict(kwargs))
        
        self.connect()

# ___________________________________________________________________________
# PRIVATE METHODS 

    """ ===================================================================="""
    """ === PRIVATE METHODS ================================================"""

    """@handlertry()"""
    def _check_oobCallback(self, oobCallback):
        # Acceptable parameters need to be determined
#         log.debug("oobCallback '" + str(oobCallback) + "'...OK")
        return oobCallback
    
    """@handlertry()"""
    def _check_arrayOrder(self, arrayOrder):
        allowable = ["C"] # Add other allowed values here
        for allowed in allowable:
            if str(arrayOrder) == str(allowed): 
#                 log.debug("arrayOrder '" + str(arrayOrder) + "'...OK")
                return arrayOrder 
        
        err = ''.join(["arrayOrder '", str(arrayOrder), 
                       "'. Does not appear to be valid. "])
       
        log.debug(err)
        raise AttributeError('InvalidRservearrayOrder: ' + err)
        
    """@handlertry()"""
    def _check_defaultVoid(self, defaultVoid):
        """"""
        if type(defaultVoid) is bool:
#            log.debug("defaultVoid '" + str(defaultVoid) + "'...OK")
           return defaultVoid

        else:
           err = ''.join(["defaultVoid is '", str(defaultVoid), 
                           "'. Must be boolean (True/False)"])
           log.debug(err)
           raise type(e), type(e)('InvalidRservedefaultVoid: '+err+e.message)

    """@handlertry()"""
    def _check_atomicArray(self, atomicArray):
        """"""
        if type(atomicArray) is bool:
#            log.debug("atomicArray '" + str(atomicArray) + "'...OK")
           return atomicArray

        else:
           err = ''.join(["atomicArray is '", str(atomicArray), 
                           "'. Must be boolean (True/False)"])
           log.debug(err)
           raise type(e), type(e)('InvalidRserveatomicArray: '+err+e.message)
 
    """@handlertry()"""
    def _check_host(self, host):
        if checkURL(host):
#             log.debug("Host '" + str(host) + "'...OK")
            return host 
        else:
            
            err = ''.join(["Server: '", str(host), 
                           "' does not appear to be valid."])
            log.debug(err)
            raise AttributeError('InvalidRserveServer: ' +err)
        
    """@handlertry()"""
    def _check_port(self, port):
        try:
            port = int(port)
#             log.debug("Port '" + str(port) + "'...OK")
            return port

        except (ValueError) as e:
            err = ''.join(["Port '", str(port), 
                           "' does not appear to be valid."])
            log.debug(err)
            raise type(e), type(e)('InvalidRservePort: ' + err + e.message)

    """@handlertry()"""
    def _check_file_path(self, filepath = None, host = 'localhost'):
        """
        This only veifies that the path is in the correct format, 
        not that it exists, is readable, or contains good [R] data
        """
        err = ''.join(["File path '", str(filepath), 
                       "' appears invalid. "])

        if filepath is None: 
            raise ValueError(err + "'filepath' cannot be 'None'.")
        
        # If here, the filepath passed is a path and/or filename
        # Strip illegal characters
        # This automatically converts what was passed into a string
        filepath = (''.join(c for c in str(filepath) if re.match("[a-zA-z0-9 -_./\\ ]", c)))

        # filepath must start with either '/' or './'
        # If it has neither, we assume local directory
        if not re.match('^\s*[./|/].*$', filepath): 
            filepath = './' + filepath
         
        # filepath cannot end with '/'     
        if filepath.endswith('/'):
            err = err + "'filepath' cannot end with a '/'."
            raise ValueError(err)

### Kind of redundant. Better to just catch the failure to open error ========        
#         # Check that directory exists and, if not, create it
#         #THIS ONLY WORKS IF FILE IS ON THE LOCALHOST
#         if 'local' in str(host).lower():
#             if not fileExists(filepath):
#                 err = ''.join([
#                                "'filepath' of '", 
#                                str(filepath), 
#                                "' does not exist."
#                                ])
#                 raise ValueError(err)
# 
#         else:
# #             raise NotImplementedError('havent yet coded getting file from non local machine.')
# =============================================================================
                    
        return os.path.abspath(filepath)
            
    """@handlertry('RhandlerCleanupError')"""
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

    """@handlertry("RCommandSanityFail:")"""
    def _cmd(self, _command):
        """
        =======================================================================
        =======================================================================
        FOR NOW, we're just going to return the command, under the assumption 
        that the coder knows what s/he is doing. Eventually, this should run a 
        series of sanity checks on the command to prevent breakage.
        =======================================================================
        =======================================================================        

        All commands should be checked through here before being passed onto 
        the R environment.
        
        If the command is good, just return the command. 
        
        If the command is bad, throw an error which will send it to the 
        'RCommandSanityFail' which can try to correct (be VEEERY careful with 
        this and use a popup to confirm changes...otherwise an [R] command
        may be corrected improperly and may silently give bad results.)
        
        If the command CAN be corrected by 'RCommandSanityFail', this (_cmd)
        method will be re-run and the corrected command will be returned. 
        
        If the command CAN NOT be corrected by 'RCommandSanityFail', control 
        will return just past the exception block and 'None' an be returned 
        which should be handled by the calling method.   
        
        :NAME: _cmd(_command)
        
        :DESCRIPTION:
            Does a sanity and security check on the command passed to ensure it 
            won't break [R]. 
            
            I.e.
            last_name = "Johnny Walker; drop tables 'students';"
            
        :ARGUMENTS:
            _command:    String. The [R] command to be run.
             
        :RETURNS:
            string: The sanitized or corrected command if good. 
            ...OR...
            'None' if the string cannot be sanitized/corrected. 
        
        :USAGE:
            class RHandler(object):
                def method(_command):
                    command = self._cmd(command)
                    if command is not None: 
                        return self.conn.eval(command)
                    else:
                        # popup message here?
                        return False
        """
        if _command is not None: 
        # ==============================================
        # RUN SANITY CHECKS HERE or additional checks in 
        # errorhandler.handlers.RCommandSanityFail
        # If code is bad/unsafe and cannot be corrected, 
        # set _command = None
        # ==============================================
            return _command

        else:
            err = ''.join(["[R] command '", 
                           str(_command), 
                           "' failed sanity check. ", 
                           "Refusing to send to [R] environment."])
            log.error(err)
            _command = None
            return None # _command = 'None' if here

    """@handlertry()"""
    def _load_vars(self, kwargs):
        rhandler_host             = kwargs.pop("rhandler_host","localhost")
        self.rhandler_host        = self._check_host(rhandler_host)
        
        rhandler_port             = kwargs.pop("port"         ,"6311")
        self.rhandler_port        = self._check_port(rhandler_port)
        
        rhandler_atomicArray      = kwargs.pop("atomicArray"  , True)
        self.rhandler_atomicArray = self._check_atomicArray(rhandler_atomicArray)
        
        rhandler_arrayOrder       = kwargs.pop("arrayOrder"   , "C")
        self.rhandler_arrayOrder  = self._check_arrayOrder(rhandler_arrayOrder)
        
        rhandler_defaultVoid      = kwargs.pop("defaultVoid"  , False)
        self.rhandler_defaultVoid = self._check_defaultVoid(rhandler_defaultVoid)
                
        rhandler_oobCallback      = kwargs.pop("oobCallback"  , None)
        self.rhandler_oobCallback = self._check_oobCallback(rhandler_oobCallback)

    """@handlertry()"""
    def _prep_string_command(self, _data):
        """
        FOR FUTURE
        """
        try:
            _data + "STRINGTEST" # no error = Already a string
            # Can add more checks here
            return _data
        except TypeError, e: # Not a string
            return False
        finally:
            raise

    """@handlertry()"""
    def _prep_list_command(self, _data):
        """
        FOR FUTURE
        """
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

    """ @handlertry('RFileNotFound:')"""
    def _source_local_R_file(self, filename):
            # filename should be the complete path and verified at this point 
            with open (filename, "r", 0) as FH:
                result = FH.read()
            return result

    """@handlertry('RemoteRFileNotFound:')"""
    def _source_remote_R_file(self, 
                              filename, 
                              HOST = None, 
                              USER = None,
                              PORT = None, 
                              PEM = None 
                              ):
        # Change this to get data from config file 
        if PEM is None: PEM = str(self.script_server_pem)
        # "/Users/mikes/Documents/Work/BioComSoftware/Jobs/2014-10-10-Tesera/Tesera.pem"
        if USER is None: USER = str(self.script_server_user)
#         USER = 'ec2-user'
        if PORT is None: PORT = str(self.script_server_port)
#         PORT = '22'
        if HOST is None: HOST = str(self.script_server_host)
#         HOST = '54.164.196.82'

        command = ['cat', filename]
        
        ssh = ['ssh', '-i', PEM, '-p', PORT, USER + '@' + HOST]
        run = ssh + command
        
        proc = subprocess.Popen(run, shell=False, 
                                stdout=subprocess.PIPE) 
        result = proc.communicate()[0]

        return result
    
#______________________________________________________________________________
# PUBLIC METHODS (OVERIDDEN FROM ABSTRACT)

    """ ===================================================================="""
    """ === PUBLIC METHODS ================================================="""
    """@handlertry("PassThroughException:")"""
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
        # Clean close
        try:
            self.conn.close()
            log.info("Connection '" + str(self.conn) + "' closed.")

        except Exception as e:
            err = ''.join([
                           "Unable to close connection '", str(self.conn), 
                           "'. Skipping.",
                           e.message
                           ])
            log.error(err)
            
        # other stuff
        return
    
    """@handlertry("PassThroughException:")"""
    def code(self, command, sanity = False):
        """
        :NAME:
            RHandler.code('3 + 3', [sanity = True/False])
            
        :DESCRIPTION:
            Passes command line code to the [R] environment and returns the 
            result of processed code. 
            
        :ARGUMENTS:
            command = String containing an [R] command
            sanity  = <True/False>. If True, the command is chacked only for 
                      sanity in an [R] environment. Retirns the command if
                      the command is good. Returns False if the command is 
                      invalid or unsafe. 
                      
                      The sanity check will attempt to both strip out dangerous 
                      code, as well correct bad code. So a CHECK OF THE RETURNED 
                      CODE SHOULD ALWAYS BE MADE!
                        
        :RETURNS:
            Good code, sanity=False: The result of the original code 
                                     after being run within the [R] environment. 
                                     
            Good code, sanity=True:  The original code. 
            
            Bad code, sanity=False:  The result of the corrected/cleaned code 
                                     after being run within the [R] environment, 
                                     or 'None' if not correctable.  
 
            Bad code, sanity=True:   The corrected/cleaned code or 'None' if 
                                     not correctable.  
  
                                     
                                      
        :USAGE:
        """
        command = self._cmd(command)
        
        if command is not None:
            if sanity: # Do sanity check only
                return command
            else: 
                return self.conn.eval(command)

        else:
            # popup message here?
            return False
        
    """@handlertry(tries = 2) # One attempt to correct"""
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
        try:
            self.conn = R.connect(
                                  host          = self.rhandler_host, 
                                  port          = self.rhandler_port, 
                                  atomicArray   = self.rhandler_atomicArray, 
                                    #arrayOrder was removed. See __doc__ 
    #                               arrayOrder    = self.arrayOrder, 
                                  defaultVoid   = self.rhandler_defaultVoid, 
                                  oobCallback   = self.rhandler_oobCallback)
            # Cheap check
            if ( int(self.conn.eval("3*3")) == 9):
                log.info(''.join(["Established connection to Rserve with ", 
                                       "host:", 
                                       str(self.rhandler_host), ", ",  
                                       "port:", 
                                       str(self.rhandler_port), ", ", 
                                       "atomicArray: DEPRICATED/UNUSED, ",
                                       "defaultVoid:", 
                                       str(self.rhandler_defaultVoid), ", ", 
                                       "oobCallback:", 
                                       str(self.rhandler_oobCallback), "."
                                       ]))
                log.debug('Testing [R] environment...OK')

            else:
                raise ValueError()

        except ValueError, e:
            err = ''.join(["[R] environment connection returning garbage ", 
                         "to attempted eval of (3*3). Please troubleshoot. ", 
                         str(e)])
#             log.error(err)
            raise ValueError('RserveReturningGarbage: ' + err)

        except (R.rexceptions.RConnectionRefused) as e:
            err = ''.join([
                           "[R] environment does not appear to be running ", 
                           "on server '",
                           str(self.rhandler_host),  
                           "'. ", 
                           str(e)
                         ])
#             log.error(err)
            raise ValueError('RserveNotRunning: ' + err)

        return self.conn

    @handlertry("PassThroughException:")
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
    
    @handlertry("PassThroughException:")
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
    
    @handlertry("PassThroughException:")
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

    """@handlertry()"""
    def script(self, filename, host = 'localhost'):
        """
        :NAME:
            RHandler.script(filename, [host = localhost])
            
        :DESCRIPTION:
            Calls an [R] script within the the [R] environment.

        :ARGUMENTS:
            filename = (String) FULLPATH to the file. Acceptable values are:
                       - /dir/dir/script.R

                       - ./script.R (same directory in which RHandler exists)

                       - script.R (same directory in which RHandler exists)
                       
            host    = (String) Whether the script lives on the localhost (where
                      RHandler is running), on the Rserve host, or an another
                      machine. Acceptable values are:  
                      - localhost(where RHandler is running)

                      - local(where RHandler is running)

                      - remote (where Rserve is running)

                      - rserve (where Rserve is running)

                      - <hostname> a FQDN of a server upon which the script 
                                   lives. ssh will be used to connect to the 
                                   server and obtain the script. 

                      - xx.xx.xx.xx The IP address of a server upon which the 
                                    script lives. ssh will be used to connect 
                                    to the server and obtain the script.
                    
                      DEFAULTS TO 'localhost'

        :RETURNS:
            The normally output results of the script. 
            
        :USAGE:
            RHandler.script('/dir/dir/script.R', host = localhost)
        
        """
        #===========================
        # FUTURE
        # FOR self._source_remote_R_file()
        # Differentiate between a remote host that is and is not the same as the 
        # rserve host. If it IS the same host as the reserve host, have rserve
        # run the scirpt and return the results...if it is NOT the same host, 
        # use the current method of reading the file nd passing it to the rserve
        # host. Might be best to have two separate calls for this, as currently
        # self._source_local_R_file() and self._source_remote_R_file() both
        # return a command and not a result.
        # 
        # self._source_remote_R_file() is pretty slow right now. Needs to be 
        # addressed. 
        
        # This confirms the file...don't repeat
        filename = self._check_file_path(filepath = filename, host = host)

        if 'local' in str(host).lower():        
            try:#____________________________________________________
                command = self._source_local_R_file(filename)
            
            except (NameError, AttributeError, ValueError) as e:
                e.message = ('RScriptFileDoesNotExist: ' + e.message)
                raise type(e)(e.message)

        elif 'remot' in str(host).lower():
            command = self._source_remote_R_file(filename, host)
            
        elif 'rser' in str(host).lower():
            command = self._source_remote_R_file(filename, host)
        
        elif checkURL(host):
            command = self._source_remote_R_file(filename, host)
        
        else:
            err = ''.join([
                           "RScriptFileDoesNotExist: ",
                           "Unable to determine file location from 'host'='",
                           str(host), "'. Aborting." 
                           ])

            raise ValueError(err)                          
                            
#         _cmd =  ''.join(["source(paste(", 
#                          str(kwargs["fullpath"]), 
#                          ', sep = ""'])

        command = self._cmd(command)
            
        return self.conn.eval(command)
         
    #@handlertry("PassThroughException:")

    """@handlertry()"""
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

    """@handlertry("PassThroughException:")"""
    def status(self):
        """"""
        return str(self.conn)
        