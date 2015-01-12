##############################################################################
# Removal of the "__license__" line or content from  "__license__", or removal 
# of "__author__" in this or any constituent # component or file constitutes a 
# violation of the licensing and copyright agreement. 
__author__      = "Mike Rightmire"
__copyright__   = "BioCom Software"
__license__     = "Tesera"
__license_file__= "Clause1.PERPETUAL_AND_UNLIMITED_LICENSING_TO_THE_CLIENT.py"
__version__     = "0.9.3.0"
__maintainer__  = "Mike Rightmire"
__email__       = "Mike.Rightmire@BiocomSoftware.com"
__status__      = "Development"
##############################################################################

from checks         import checkPathFormat
from checks         import directoryExists
from checks         import fileExists
from errorhandler   import handlertry
from errorhandler   import raisetry
from inspect        import stack 

import datetime
import logging
import os
import re
import sys

class SetLogger(object):
    """
    :NAME:
    SetLogger( app_name, 
               [logfile, 
                log_path, 
                log_level, 
                screendump, 
                create_paths]) 

    :DESCRIPTION:
    setLogger is a log object manager intended to handle the details of 
    creating and altering a logger. 
    
    The setLogger class is a singleton, meaning
    once an object is created by a calling script, all CHILD SCRIPTS attempting  
    to instantiate a setLogger object will - in actuality - recieve the existing
    setLogger object. The advantage of this is that each object, function or 
    child process of the original script can simply call setLogger once and 
    in-the-blind to continue logging appropriately.   
     
    :ARGUMENTS:
    app_name:  The friendly name of the application actually instantiating a log 
               object. This is the name used to create a python "logging.logger"
               instance, and the name that will appear next to the data in 
               the log file to identify what application generated the log 
               information.
               
               MANDATORY: No default at this time, however does not need to 
                          be set if the setLogger object exists and is called by 
                          a child script or process. 
               
               
                
    logfile:   The filename (only) of the logfile to which log data will be 
               written. 
               
               DEFAULTS TO: "" which causes setLogger to use <app_name>.log as
               the filename.
               
               Passing "None" as logfile tells set logger not to log to a file.
                  
    log_path:  The full DIRECTORY (ONLY) path to the logfile.

               I.e. "/var/log/dir1/dir2/"

               DEFAULTS TO: "./"
               
    log_level: The logging object's "log level" as defined by the Python 
               "logging" module. This sets the level of message that is actually 
               passed to the logger to be included in the logfile.
               
               Can be passed as a number between 0 and 50.
               
               Can be passed as one of the following strings:
                 critical
                 error
                 warning
                 info
                 debug
                 
               DEFAULTS TO: 40 (ERROR) 
                   
    screendump (True/False): 
               If screendump is set to True, all log info that passes the log
               level and filters (is to be written to the log file) will also 
               be written to STD_OUT.
               
    create_paths (True/False):
               If True, in the event the log_path does not exist, it will be 
               created. If False, an exception si raised. 
               
               DEFAULTS TO: False 

    :METHODS:
    screendump()
        :Description: 
            Will dump the contents of the current logfile to STD_OUT.

        :Parameters:
            None
    
        
    purge()
        :Description: 
            Will erase the contents of the existing logfile, with a post-erase 
            marker to identify that an erase has been performed. 

        :Parameters:
            None

        
    logfile(name = <str>, [migrate = <True/False>])
        NOT YET IMPLEMENTED.

        :Description: 
            Changes the file name of the current log.
        
        :Parameters:
            name: Changes the name of the current logfile to "name".

            migrate: If True, the contents of the existing log are moved to the 
            new log. DEFAULTS TO: True.

            NO DEFAULT.
         
    level(level = <int>)
        NOT YET IMPLEMENTED.

        :Description: 
            Changes the logger default level to "new_level".
        
        :Parameters:
            level:
               Can be passed as a number between 0 and 50.
               
               Can be passed as one of the following strings:
                 critical
                 error
                 warning
                 info
                 debug
                 
               DEFAULTS TO: 40 (ERROR) 

    name(name = <str>)
        NOT YET IMPLEMENTED.

        :Description: 
            Changes app_name.
        
        :Parameters:
            name:
               The friendly name of the application actually instantiating a log 
               object. This is the name used to create a python "logging.logger"
               instance, and the name that will appear next to the data in 
               the log file to identify what application generated the log 
               information.               
               Can be passed as one of the following strings:
                 critical
                 error
                 warning
                 info
                 debug
                 
               NO DEFAULT 

    formatter(format = <str>)
        NOT YET IMPLEMENTED.

        :Description: 
            Changes the format of the data written to the logfile.
        
        :Parameters:
            format:
               A Python 2.x printf style formatting string accepted by the 
               Python standard "logging" module.  

               NO DEFAULT     

    dump(dumping = <True/False>)
        NOT YET IMPLEMENTED.

        :Description: 
            Changes whether the data written to the log file are also dumped 
            to STD_OUT. 
        
        :Parameters:
            dumping: 
            <True/False>

               DEFAULTS TO: False     
    
    :RETURNS:
        A standard Python "logging" module logger object. 
    
    :USAGE:
    (ParentClass.py)
    class ParentClass(object):
        def __init__(self):
            self.log = SetLogger(app_name = "MyApp", 
                                 logfile = "MyApp.log",
                                 log_path = "/var/log/MyDir/", 
                                 log_level = "INFO", 
                                 screendump = True,
                                 create_paths = False)

        def parentMethod(self, var = None)
            self.log.info("I will log to "MyApp.log"")
            self.log.info("var was set to " + str(var))
            
    
    (ChildClass.py)
    class ChildClass(ParentClass):
        def __init__(self):
            self.log = SetLogger()
        
        def childMethod(self, var = None):
            self.log.info("I will log to the same file as ParentClass objects.")
            self.log.info("var was set to " + str(var))
            self.log.debug("I will only log if PARAM "log_level" was "DEBUG")

    (script.py)
    obj1 = ParentClass()
    obj2 = ChildClass()
    
    obj1.parentMethod(1)
    obj2.childMethod(2)
    
    (MyApp.log)
    2014-12-23 15:35:42,510 - MyApp - INFO - I will log to "MyApp.log"")
    2014-12-23 15:35:42,511 - MyApp - INFO - var was set to 1
    2014-12-23 15:35:42,512 - MyApp - INFO - I will log to the same file 
                                             as ParentClass objects.
    2014-12-23 15:35:42,513 - MyApp - INFO - var was set to 2
    """    
    __exists = False
    
    def __new__(cls, 
                app_name     = None, 
                logfile      = None,
                log_path     = None, 
                log_level    = None, 
                screendump   = None, 
                formatter    = None,
                create_paths = None 
                ):
        """
        This is a singleton class. 
        
        The __new__ method is called prior to instantiation with __init__. 
        If there's already an instance of the class, the existing object is 
        returned. If it doesn't exist, a new object is instantiated with 
        the __init__.
        """
        # __init__ is called no matter what, so...
        # If there is NOT an instance, just create an instance 
        # This WILL run __init__
        if not hasattr(cls, 'instance'):
            cls.instance = super(SetLogger, cls).__new__(cls)
            return cls.instance

        # Else if an instance does exist, set a flag since
        # __init__is called, but flag halts completion (just returns)           
        else:
            cls.instance.__exists = True
            return cls.instance
        
    def __init__(self, 
                app_name     = None, 
                logfile      = None,
                log_path     = None, 
                log_level    = None, 
                screendump   = None, 
                formatter    = None,
                create_paths = None 
                ):

        # If here is an existing setlogger object, return without running the 
        # __init__. The __new__ will send the existing object as the retrun
        if self.__exists:
            #The following checks to see if the passed in parameters of 
            # SetLogger are different than what is current. 
            # If yes, delete and recreate current log 
            # if (({self.var:True, None:True}.get(var)): do something
            # Means if 'var' == self.var OR None, then do something
            if ( 
                ({self.app_name:True,   None:True}.get(app_name))   and 
                ({self.logfile:True,    None:True}.get(logfile))    and
                ({self.log_path:True,   None:True}.get(log_path))   and
                ({self.log_level:True,  None:True}.get(log_level))  and
                ({self.formatter:True,  None:True}.get(format))  and
                ({self.screendump:True, None:True}.get(screendump))
               ):
                #########################################
                # log object exists and Nothing has changed
                # Just return object                        
                return # From __init__                                  
                #########################################

            else:
                if (
                    ((logfile != self.logfile) and (logfile is not None)) or 
                    ((log_path != self.log_path) and (log_path is not None))
                    ):
                        if logfile  is None: logfile = self.logfile 
                        if log_path is None: log_path = self.log_path 
                        self.change_logfile(logfile, log_path, migrate = True)

        self.app_name  = self._check_app_name(app_name)
        self.logfile   = self._check_logfile(logfile)
        self.log_path  = self._check_log_path(log_path)
        self.log_level = self._check_log_level(log_level)
        self.formatter = self._set_formatter(formatter)
        self.screendump = self._check_boolean(screendump)
        self.create_paths = self._check_boolean(create_paths)
        # Do the work to create the logger object
        self.full_log_path = self._set_full_log_path(self.log_path, self.logfile)
        self.formatter = self._set_formatter()
        # Start the perm log
        self._set_logger()


    # ________________________________________________________________________
    # LOGGING OVERRIDES
    # Using ONLY the standard logging levels as recommended by the 
    # logging documentation

    def critical(self, *args, **kwargs): # LOGGING OVERRIDES__________________
        return self.logger.critical(*args, **kwargs)
 
    def error(self, *args, **kwargs):
        return self.logger.error(*args, **kwargs)
     
    def warning(self, *args, **kwargs):
        return self.logger.warning(*args, **kwargs)
     
    def info(self, *args, **kwargs):
        return self.logger.info(*args, **kwargs)
     
    def debug(self, *args, **kwargs):
        return self.logger.debug(*args, **kwargs)                

    #__________________________________________________________________________
    # PUBLIC METHODS            

    def del_log(self, app_name):# PUBLIC METHODS_______________________________
        """"""
        self._remove_logger(app_name)
        
#     def formatter(self, format):
#         """
#         NOT YET IMPLEMENTED
#         Intended to change the log formatting of the existing handlers
#         """
#         raise NotImplementedError

#     def level(self, level = 40):
#         """
#         NOT YET IMPLEMENTED
#         Intended to change the logging level of the existing handlers
#         """
#         raise NotImplementedError

    def change_logfile(self, 
                       logfile, 
                       log_path, 
                       migrate = True):
        """
        NOT YET IMPLEMENTED
        Intended to change the current logfile of the existing handler
        """
        try:
            self.logger.debug(''.join(["Attempting to change logfile from '", 
                                      self.full_log_path, 
                                      "' to '", 
                                      str(log_path), "/",
                                      str (logfile),
                                      "'. "
                                      ])) 
        except NameError, e:
            pass

        source          = self.full_log_path
        self.logfile    = self._check_logfile(logfile)
        self.log_path   = self._check_log_path(log_path)
        self.full_log_path = self._set_full_log_path(self.log_path, self.logfile)

        try:
            create_paths = self.create_paths
        except NameError, e:
            create_paths = False

        
        self._migrate_log_data(self.full_log_path, source, create_paths)

        self.logger = self._set_logger()
        
        self.logger.info(''.join(["Logfile migrated to '", 
                                  self.full_log_path, 
                                  "'. "
                                  ]))         

    def purge(self):
        """
        Deletes the current contents of the logfile on disk. 
        WARNING: Security risk. 
                 Ensure the purge process if verified as authorized and 
                 that successful purges are written to the start of the new log. 
        """
        @raisetry(''.join(["Failed to purge '", 
                           str(self.full_log_path), 
                           "'. "]))

        def _purge(self):
            if fileExists(self.full_log_path): 
                os.remove(self.full_log_path)
                with open(self.full_log_path, 'w', 0):
                    os.utime(self.full_log_path, datetime.datetime.now())


        self.logger.critical(''.join(["Attempting to purge '", 
                                      str(self.full_log_path), "'. "]))
        _purge(self)

        self.logger.critical(''.join(["Successfully purged '", 
                                      str(self.full_log_path), "'. "]))

#     def set_full_log_path(self, log_path, logfile):
#         """"""
#         return self._set_full_log_path(log_path, logfile)

    def dump(self):
        """
        Dumps the current logfile contents to std out.
        """
        _list = self._read()
        for line in _list:
            print line

    #__________________________________________________________________________
    # PRIVATE METHODS            

    @raisetry("Failure changing app_name.")
    def _change_logfile(self, full_log_path): # PRIVATE METHODS________________
        """"""
        raise NotImplementedError()
    
# #         if self._isExistingLogger(app_name):
# #             self._remove_logger(app_name)
# #                     
# #             logger = logging.getLogger(app_name)
# #             logger.setLevel(level=log_level)
# #             if ((formatter is "") or (formatter is None)): 
# #                 formatter = logging.Formatter(
# #                         '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# 
#         # create file handler which logs even debug messages
# 
#                                      
#         fh = logging.FileHandler(self.full_log_path)
#         fh.setLevel(level=self.log_level)
#         fh.setFormatter(self.formatter)
# 
#         # create console handler with a higher log level
# #         if self.screendump:
# #             ch = logging.StreamHandler()
# #             ch.setLevel(level=self.log_level)
# #             ch.setFormatter(self.formatter)
# #         else:
# #             ch = False
#                 
#         # add the handlers to the logger
#         if fh: self.logger.addHandler(fh)
# #         if ch: logger.addHandler(ch)
# 
#         self.full_log_path = full_log_path
#         
#         return self.logger
            
    def _check_app_name(self, app_name):
        @raisetry(''.join(["Failure setting 'self.app_name'. ",  
                                   "Parameter passed: '",
                                   str(app_name), 
                                   "'. "]))
        def _checkit(self, app_name):
            if app_name is None:
                try:
                    app_name = self.app_name
                except NameError, e:
                    e = "app_name cannot be Null"
                    raise TypeError(e)
                    
#             self.templog.debug(''.join(["Checking parameter 'app_name' (", 
#                                         str(app_name), 
#                                         "). "]))

            # Verify string and clean
            # This can deliver nonsense if a nonsense object is passed in as 
            # app_name, but it will be functional nonsense
            app_name = (''.join(c for c in str(app_name) 
                                if re.match("[a-zA-z0-9]", c)))

            if ((app_name is None) or (app_name == "")):
                err = ''.join(["Paraneter 'app_name' must be a valid, ", 
                                          "non-zero-length string. "])
                self.templog.debug(err)
                raise ValueError(err)                                                          

            return app_name

        app_name = _checkit(self, app_name)
#         self.templog.debug(''.join(["'app_name': ", str(app_name)]))
        return app_name 

    def _check_boolean(self, screendump):
        if screendump is None:
            try:
                return self.screendump
            except AttributeError, e:
                return False

        # Check for strings instead of proper bool            
        if (("t" in str(screendump).lower())): 
            return True

        if (("f" in str(screendump).lower())): 
            return False

        # Check for numbers instead of proper bool                        
        try:
            if int(screendump) == 1: return True
            if int(screendump) == 0: return False
        except ValueError, e:
            return False

        # Check for proper bool
        if isinstance(screendump, bool):
            return screendump
        else:
            e = "Parameter 'screendump' must be boolean (True/False)"
            raise TypeError(e)
            
    def _check_logfile(self, logfile):
#         self.templog.debug(''.join(["Checking parameter 'logfile' (", 
#                                     str(logfile), 
#                                     "). "]))

        @raisetry(''.join(["Failure setting 'self.logfile'. ",  
                           "Parameter passed: '",str(logfile), "'. "]))        
        def _checkit(self, logfile):
            if (logfile is None):
                try:
                    logfile = self.logfile
                except NameError, e:
                    logfile = self.app_name
                    return logfile

            if  (logfile is ""):
                logfile = self.app_name
                return logfile
    
            elif logfile is False:
                return False
             
            else:
                    # String and clean
                    logfile = (''.join(c for c in str(logfile) 
                                                if re.match("[a-zA-z0-9.]", c)))
                    if ".log" not in (logfile[-4:]).lower():
                        logfile = logfile + ".log" 
                    return logfile

        result = _checkit(self, logfile)
#         self.templog.debug(''.join(["'logfile': " + str(result)]))
        return result

    def _check_log_level(self, log_level):
#         try:
#             self.templog.debug(''.join(["Checking parameter 'log_level' (", 
#                                         str(log_level), 
#                                         "). "]))
#         except Exception, e:
#             pass

        @raisetry(''.join(["Failure setting 'log_level'. ",  
                           "Parameter passed: '",str(log_level), "'. "]))
        def _checkit(self, log_level):        
            if log_level is None:
                try:
                    log_level = self.log_level
                except NameError, e:
                    pass
        
            # Check for text settings
            # No need for elif since each if returns
            if "C" in str(log_level).upper()[:1]: 
                log_level = "CRITICAL"
                return log_level
                 
            if "E" in str(log_level).upper()[:1]: 
                log_level = "ERROR"
                return log_level
                
            if "W" in str(log_level).upper()[:1]: 
                log_level = "WARNING"
                return log_level

            if "I" in str(log_level).upper()[:1]: 
                log_level = "INFO"
                return log_level

            if "D" in str(log_level).upper()[:1]: 
                log_level = "DEBUG"
                return log_level
            
            if "NO" in str(log_level).upper()[:1]: 
                log_level = "NOTSET"
                return log_level 

            # If here, log_level is either numerical or invalid        
            log_level = (''.join(c for c in str(log_level) 
                                     if re.match("[0-9]", c)))
            try:
                log_level = int(log_level)
            except ValueError, e:
                log_level = 40
                return log_level
            
            if ((log_level >= 0) and (log_level <= 50)): 
                return log_level
            else:
                msg = (''.join(["'log_level': '", str(log_level),
                                "' is not a correct integer ", 
                                "(0 <= log_level <=50)."]))
                raise Exception(msg)

        result = _checkit(self, log_level)            

#         try:
#             self.templog.debug("'log_level': " + str(result))
#         except Exception, e:
#             pass
            
        return result

    def _check_log_path(self, log_path):

#         self.templog.debug(''.join(["Checking parameter 'log_path' (", 
#                                     str(log_path), 
#                                     "). "]))

        @raisetry(''.join(["Failure setting 'self.log_path'. ",  
                           "Parameter passed: '",
                           str(log_path), 
                           "'. "]))
        def _checkit(self, log_path):
            if log_path is None:
                try:
                    log_path = self.log_path
                except NameError, e:
                    log_path = "./"
                    return log_path
                    
            if   (log_path == ""):
                    # Set to the local directory
                    log_path = "./"
                    return log_path

            # String and clean
            log_path = (''.join(c for c in str(log_path) 
                                        if re.match("[a-zA-z0-9/.\\:]", c)))
            #####################################################################
            # REPLACE THE FOLLOWING WITH THE PATHING CONVERSION MODULE
            # Which will modify the path to the current OS standards based on 
            # the directories passed in any format
            if log_path[-1:] != "/": log_path = log_path + "/"
            #####################################################################

            if not checkPathFormat(log_path, endslash = True):
                 msg = ("File path is not in a usable format.")
                 raise Exception(msg)
                
            if not directoryExists(log_path):
                if self.create_paths:
                    os.mkdir(log_path)
                else:
                    raise Exception("File path does not exist.")                    
            
            # If here, path seems OK, exists and has been set in log_path
            # so just return 
#             self.templog.debug("'log_path': " + str(log_path))
            return log_path
        
        result = _checkit(self, log_path)
        return result    

    def _isExistingLogger(self, app_name):
        """"""
        try:
            if app_name in str(logging.Logger.manager.loggerDict.keys()):
                return True
            else:
                return False
        except Exception, e:
            return False
    
    def _migrate_log_data(self, 
                     dest, 
                     source = None, 
                     create_paths = None):
        """
        Private method.
        
        _migrate_log_data(self, source = None, dest = None) 
        
        "source" and "dest" MUST be the full log file path with file name 
        and extension I.e. "/der12/dr2/filename.log"
        """
#         self.logger.info(''.join(["Migrating log '", 
#                                   str(source), 
#                                   "' to '", str(dest), 
#                                   "'. "]))
        # If source and dest are identical, just return
        if source == dest:
            return True
        
        #______________________________________________________________________
        @raisetry(''.join(["loghandler._migrate_log: ", 
                           "Destination path must exist and cannot be Null. ", 
                           "Param passed: '", 
                           str(dest), 
                           "'. "]))
        def _checkParams(self, source, dest, create_paths):
            # If create_paths is not passed, use the object's current setting 
            if create_paths is None: create_paths = self.create_paths

            #Raises error if None or ""
            len(dest)
            
            # Check the dir is already there
            if not directoryExists(dest): 
                if create_paths:
                    os.mkdir(os.path.dirname(dest))
                else:
                    raise AttributeError()

            # If no source is not passed, set the source to the current
            # logfile. Current logfile is re-set to the new log path AFTER
            # the migration is successful            
            if source is None: source = self.full_log_path
            
            return True
        #______________________________________________________________________
#         @raisetry(''.join(["Failure migrating templog './loghandlertmp.log' ", 
#                            "to permanent log path '", 
#                            str(self.full_log_path), 
#                            "'. "]))

        def _setit(self, source, dest):
            with open(source, "r", 0) as IN:
                with open(dest, "a+", 0) as OUT:
                    for line in IN: OUT.write(line)
            # Use perm logger not templog         
#             self.logger.info(''.join(["'", source, "' log migrated to '", 
#                                        dest, "'. "]))
            self.full_log_path = dest
            self.log_path = os.path.dirname(dest)
            self.logfile  = os.path.basename(dest)
#             self._start_log()
            return True

        #______________________________________________________________________
            
        _checkParams(self, source, dest, create_paths)
        _setit(self, source, dest)
        self._remove_file(source)
        return True
        
    def _read(self):
        """"""
        _list = open(self.full_log_path, "r", 0).read().splitlines()
        return _list

    def _remove_file(self, _file):
        @raisetry(''.join(["Failure removing log '", 
                           str(_file),
                           "'." ]))
        def _removeit(self, _file):
            os.remove(_file)
#             self.logger.debug(''.join(["File '", 
#                                    str(_file), 
#                                    "' removed."]))

            return True

        _removeit(self, _file)
 
    def _remove_handler(self):
        raise NotImplementedError
        # Logger.removeHandler(hdlr)
        
    def _remove_logger(self, app_name):

#         @handlertry(''.join(["PassThroughException: ", 
#                             "Failure removing logging handler '",
#                            str(app_name), "'. " 
#                            ]))
        def _setit(self, app_name):
#             self.logger.debug(''.join(["Attempting to remove handler '", 
#                                    str(app_name), "'..." 
#                                    ]))

            if self._isExistingLogger(app_name):
                del logging.Logger.manager.loggerDict[app_name]

#                 self.logger.debug(''.join(["handler '", 
#                                            str(app_name), 
#                                            "' removed. " 
#                                            ]))
            else:
                pass
#                 self.logger.debug(''.join(["handler '", 
#                                            str(app_name), 
#                                            "' did not exist. Skipping. " 
#                                            ]))                
        _setit(self, app_name)

#     def _set_fileHandler(self, 
#                          logfile, 
#                          log_level,
#                          formatter 
#                          ):
# #         self.templog.debug("Setting filehandler to " + logfile + ".")
# 
#         @raisetry(''.join(["Failure setting filehandler '", 
#                            str(logfile), 
#                            "'. "]))
#         def _setit(self,                          
#                    logfile, 
#                    log_level,
#                    formatter 
#                    ):
#             
#             fh = logging.FileHandler(self.full_log_path)
#             fh.setLevel(level=log_level)
#             fh.setFormatter(formatter)
#             self.logger.addHandler(fh)
#             return True
#         
#         _setit(self, logfile, log_level, formatter)
#         return True

    def _set_formatter(self, format = None):
        # format will be implemented as a string to change the logging format
        @raisetry(''.join(["Failure setting formatter."]))
        def _setit(self):
            
#             self.formatter = logging.Formatter(
            return logging.Formatter(
                        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                        )
        
        result = _setit(self)
        return result

    def _set_full_log_path(self, log_path, logfile):

        @raisetry(''.join(["Failure setting full log path. "]))
        def _setit(self, log_path, logfile):
            logfile = self._check_logfile(logfile)
            log_path = self._check_log_path(log_path)
            result = (log_path + logfile)
            return result
        
        result = _setit(self, log_path, logfile)
#         self.templog.debug(''.join(["'full_log_path': ", 
#                                     str(result)]))
        return result

    def _set_logger(self):
        
        # Remove the existing logger
        if self._isExistingLogger(self.app_name):
            self._remove_logger(self.app_name)

        logger = logging.getLogger(self.app_name)
        logger.setLevel(level=self.log_level)
        if ((self.formatter is "") or (self.formatter is None)): 
            self.formatter = self._set_formatter()

        # create file handler which logs even debug messages
        fh = logging.FileHandler(self.full_log_path)
        fh.setLevel(level=self.log_level)
        fh.setFormatter(self.formatter)

        # create console handler with a higher log level
        if self.screendump:
            ch = logging.StreamHandler()
            ch.setLevel(level=self.log_level)
            ch.setFormatter(self.formatter)
        else:
            ch = False
                
        # add the handlers to the logger
        if fh: logger.addHandler(fh)
        if ch: logger.addHandler(ch)
        
        self.logger = logger

        self.logger.info(''.join(["Logger started at  '", 
                                  self.full_log_path, 
                                  "' with screendump: ", 
                                  str(self.screendump), 
                                  "."
                                  ]))        
        return logger
    
#         logger.info(''.join(["logger started as '", 
#                          str(app_name), 
#                          "' at '",
#                          str(full_log_path),
#                          "'. " 
#                          ]))

#     def check_app_name(self, app_name):
#         """"""
#         return self._check_app_name(app_name)
#         
#     def check_logfile(self, logfile):
#         """"""
#         return self._check_logfile(logfile)
# 
#     def check_log_level(self, log_level):
#         return self._check_log_level(log_level)
#         
#     def check_log_path(self, log_path):
#         """"""
#         return self._check_log_path(log_path)

#     def _set_screendump(self, 
#                         screendump, 
#                         log_level,
#                         formatter 
#                         ):
# #         self.templog.debug("Setting screendump.")
# 
#         @raisetry(''.join(["Failure setting screendump." ]))
#         def _setit(self, 
#                    screendump, 
#                    log_level,
#                    formatter 
#                    ):
#             if screendump:
#                 ch = logging.StreamHandler()
#                 ch.setLevel(level=log_level)
#                 ch.setFormatter(formatter)
#                 self.logger.addHandler(ch)
# #                 self.templog.debug("Screendump ON.")
#                 return True
# 
#             else:
# #                 self.templog.debug("Screendump OFF.")
#                 return True
# 
#         _setit(self, screendump, log_level, formatter)
#         return True

    # For now, only the standard logging levels are supported as recommended
    # by the logging documentation

#     @raisetry(''.join(["Unable to complete '_start_log()'. "]))
#     def _start_log(self): 
# 
#         logger = self._set_logger(
# #                                   self.app_name, 
# #                               self.full_log_path, 
# #                               self.log_level,
# #                               self.formatter, 
# #                               self.screendump
#                       )
#         
# #         logger.info(''.join(["logger started as '", 
# #                              str(self.app_name), 
# #                              "' at '",
# #                              str(self.full_log_path),
# #                              "'. " 
# #                              ]))
#         self.logger = logger
#             
#     @raisetry(''.join(["Unable to open the startup log. "]))
#     def _start_templog( self, 
#                         app_name = "loghandler", 
#                         logfile = "./loghandler.log",
# #                         log_path = "./", 
#                         log_level = 40, 
#                         screendump = False, 
#                         create_paths = False 
#                        ):
        
#                 self.templog = self._set_logger(
#                                             app_name      = app_name, 
#                                             logfile       = logfile,
#                                             log_level     = log_level,
#                                             formatter     = None, 
#                                             screendump    = screendump
#                                             )
         
#                 self.templog.info("Temp startup log created.")

                      
if __name__ == "__main__":
    
    log = SetLogger(app_name = "realAppName", 
                    logfile = "test.log",
                    log_path = "/shared/GitHub/Tesera/MRAT_Refactor/log", 
                    log_level = 10, 
                    screendump = True, 
                    )
    
    log.debug("This is a log test of log.debug")
#     log.info("This is a log test of log.info")
#     log.warning("This is a log test of log.warning")
#     log.error("This is a log test of log.error")
#     log.critical("This is a log test of log.critical")
# 
#     log.migrate(dest = "/shared/GitHub/Tesera/MRAT_Refactor/log/migrated.log", 
#                 source = "/shared/GitHub/Tesera/MRAT_Refactor/log/test.log", 
#                 create_paths = False)

    log.debug("--------------------------------------")
    log.debug("This is line one in migradted")
    log.debug("This is line two in migradted")

    log = SetLogger(app_name = "NEWrealAppName", 
#                     logfile = "NEWtest.log",
#                     log_path = "/shared/GitHub/Tesera/MRAT_Refactor/log", 
                    log_level = 20, 
#                     screendump = True, 
                    )

    log.debug("This is line one in new set")
    log.debug("This is line two in new set")
    
    log = SetLogger(app_name = "NEWrealAppName", 
                    logfile = "NEWtest.log",
                    log_path = "/shared/GitHub/Tesera/MRAT_Refactor/log", 
                    log_level = 10, 
#                     screendump = True, 
                    )
 
    log.debug("This is line one in SECOND new set")
    log.debug("This is line two in SECOND new set")
    