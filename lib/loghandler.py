##############################################################################
# Removal of the "__license__" line or content from  "__license__", or removal 
# of "__author__" in this or any constituent # component or file constitutes a 
# violation of the licensing and copyright agreement. 
__author__      = "Mike Rightmire"
__copyright__   = "BioCom Software"
__license__     = "Tesera"
__license_file__= "Clause1.PERPETUAL_AND_UNLIMITED_LICENSING_TO_THE_CLIENT.py"
__version__     = "0.9.2.0"
__maintainer__  = "Mike Rightmire"
__email__       = "Mike.Rightmire@BiocomSoftware.com"
__status__      = "Development"
##############################################################################

from checks import checkPathFormat
from checks import directoryExists
from checks import fileExists
from errorhandler import handlertry
from errorhandler import raisetry
from inspect import stack 

import datetime
import logging
import os
import re

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

    dump_to_screen(dumping = <True/False>)
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
                app_name = None, 
                logfile = "",
                log_path = None, 
                log_level = 40, 
                screendump = False, 
                create_paths = False 
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
                 app_name = None, 
                 logfile = "",
                 log_path = None, 
                 log_level = 40, 
                 screendump = False,
                 create_paths = False 
                ):

        if self.__exists: return
        
        # Start the temp logger "loghanderStartup"
        # This logger and logfile are removed when permanent logger is set 
        self._start_templog(app_name     = "loghanderStartup", 
                            logfile      = "./loghandlertmp.log", 
                            log_level    = log_level, 
                            formatter    = None,
                            screendump   = screendump
                            )

        # Set and check params        
        self.app_name  = app_name   ; self._check_app_name()
        self.logfile   = logfile    ; self._check_logfile()
        self.log_path  = log_path   ; self._check_log_path()
        self.log_level = log_level  ; self._check_log_level()
        self.screendump = screendump
        self.create_paths = create_paths

        # Do the work to create the logger object
        self._set_full_logpath()
        self._set_formatter() 

        self._start_log(app_name     = self.app_name, 
                            logfile      = self.full_log_path, 
                            log_level    = self.log_level, 
                            formatter    = self.formatter,
                            screendump   = self.screendump
                            )
        
        self._migrate_templog()
        self._remove_handler("loghanderStartup")


    # ________________________________________________________________________
    # LOGGING OVERRIDES
    # Using ONLY the standard logging levels as recommended by the 
    # logging documentation

    def critical(self, *args, **kwargs):
        return self.logger.critical(*args, **kwargs)
 
    def error(self, *args, **kwargs):
        return self.logger.error(*args, **kwargs)
     
    def warning(self, *args, **kwargs):
        return self.logger.warning(*args, **kwargs)
     
    def info(self, *args, **kwargs):
        return self.logger.info(*args, **kwargs)
     
    def debug(self, *args, **kwargs):
        return self.logger.debug(*args, **kwargs)                

    # ________________________________________________________________________
    # USER METHODS

    def level(self, level = 40):
        """
        NOT YET IMPLEMENTED
        Intended to change the logging level of the existing handlers
        """
        raise NotImplementedError

    def name(self, name):
        """
        NOT YET IMPLEMENTED
        Intended to change the logger name of the existing handlers
        """
        raise NotImplementedError

    def formatter(self, format):
        """
        NOT YET IMPLEMENTED
        Intended to change the log formatting of the existing handlers
        """
        raise NotImplementedError

    def dump_to_screen(self, dumping = False):
        """
        NOT YET IMPLEMENTED
        Intended to change the current setting for 'screendump' of the existing
        handlers (which determines if items written to the log are also 
        printed to the screen.
        """
        raise NotImplementedError

    def screendump(self):
        """
        Dumps the current logfile contents to std out.
        """
        _list = self._read()
        for line in _list:
            print line

    def logfile(self, name = None, migrate = True):
        """
        NOT YET IMPLEMENTED
        Intended to change the current logfile of the existing handler
        """
        raise NotImplementedError
    
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

    def _check_app_name(self):
        @raisetry(''.join(["Failure setting 'self.app_name'. ",  
                                   "Parameter passed: '",
                                   str(self.app_name), 
                                   "'. "]))
        def _checkit(self):

            self.templog.debug(''.join(["Checking parameter 'app_name'."]))

            # Verify string and clean
            # This can deliver nonsense if a nonsense object is passed in as 
            # app_name, but it will be functional nonsense
            self.app_name = (''.join(c for c in str(self.app_name) 
                                     if re.match("[a-zA-z0-9]", c)))

            if ((self.app_name is None) or (self.app_name == "")):
                err = ''.join(["Paraneter 'app_name' must be a valid, ", 
                                          "non-zero-length string. "])
                self.templog.debug(err)
                raise ValueError(err)                                                          

            return True

        _checkit(self)
        self.templog.debug(''.join(["'app_name': ", str(self.app_name)]))
        return True 

    def _check_logfile(self):
        self.templog.debug(''.join(["Checking parameter 'logfile'."]))

        @raisetry(''.join(["Failure setting 'self.logfile'. ",  
                           "Parameter passed: '",str(self.logfile), "'. "]))        
        def _checkit(self):
            if  (self.logfile is ""):
                self.logfile = self.app_name
                return True
    
            elif self.logfile is None:
                return False
             
            else:
                    # String and clean
                    logfile = (''.join(c for c in str(self.logfile) 
                                                if re.match("[a-zA-z0-9]", c)))
                    if ".log" not in (logfile[-4:]).lower():
                        self.logfile = logfile + ".log" 
                    return True

        self.templog.debug(''.join(["'logfile': " + str(self.logfile)]))
        return True

    def _check_log_level(self):

        self.templog.debug(''.join(["Checking parameter 'log_level'."]))

        @raisetry(''.join(["Failure setting 'self.log_level'. ",  
                           "Parameter passed: '",str(self.log_level), "'. "]))
        def _checkit(self):        
        
            # Check for text settings
            # No need for elif since each if returns
            if "CR" in str(self.log_level).upper(): 
                self.log_level = "CRITICAL"
                return True
                 
            if "ER" in str(self.log_level).upper(): 
                self.log_level = "ERROR"
                return True
                
            if "WA" in str(self.log_level).upper(): 
                self.log_level = "WARNING"
                return True

            if "IN" in str(self.log_level).upper(): 
                self.log_level = "INFO"
                return True

            if "DE" in str(self.log_level).upper(): 
                self.log_level = "DEBUG"
                return True
            
            if "NO" in str(self.log_level).upper(): 
                self.log_level = "NOTSET"
                return True 

            # If here, log_level is either numerical or invalid        
            self.log_level = (''.join(c for c in str(self.log_level) 
                                     if re.match("[0-9]", c)))
            self.log_level = int(self.log_level)
            
            if ((self.log_level >= 0) and (self.log_level <= 50)): 
                return True

            else:
                msg = (''.join(["'log_level': '", str(self.log_level),
                                "' is not a correct indicator"]))
                self.templog.debug(msg)
                raise Exception(msg)

        _checkit(self)            
        self.templog.debug("'log_level': " + str(self.log_level))
        return True

    def _check_log_path(self):

        self.templog.debug(''.join(["Checking parameter 'log_path'."]))

        @raisetry(''.join(["Failure setting 'self.log_path'. ",  
                           "Parameter passed: '",str(self.log_path), "'. "]))
        def _checkit(self):        
            if   ((self.log_path is None) or 
                  (self.log_path == "")
                  ): 
                    # Set to the local directory
                    self.log_path = "./"
                    self.templog.debug(''.join(["'log_path' was None. ", 
                                                "Setting to './'"]))
                    return True

            # String and clean
            self.log_path = (''.join(c for c in str(self.log_path) 
                                        if re.match("[a-zA-z0-9/.\\:]", c)))
            #####################################################################
            # REPLACE THE FOLLOWING WITH THE PATHING CONVERSION MODULE
            # Which will modify the path to the current OS standards based on 
            # the directories passed in any format
            if self.log_path[-1:] != "/": self.log_path = self.log_path + "/"
            #####################################################################

            if not checkPathFormat(self.log_path, endslash = True):
                 msg = ("File path is not in a usable format.")
                 self.templog.debug(msg)
                 raise Exception(msg)
                
            if not directoryExists(self.log_path):
                if self.create_paths:
                    self.templog.debug("File path does not exist. Creating.")
                    os.mkdir(self.log_path)
                else:
                    self.templog.debug("File path does not exist.")
                    raise Exception("File path does not exist.")                    
            
            # If here, path seems OK, exists and has been set in self.log_path
            # so just return 
            self.templog.debug("'log_path': " + str(self.log_path))
            return True
        
        _checkit(self)    

    def _isExistingLogger(self, app_name):
        """
        """
        if app_name in str(logging.Logger.manager.loggerDict.keys()):
            return True
        else:
            return False
    
    def _migrate_templog(self):
        @raisetry(''.join(["Failure migrating templog './loghandlertmp.log' ", 
                           "to permanent log path '", 
                           str(self.full_log_path), 
                           "'. "]))
        def _setit(self):
            with open("./loghandlertmp.log", "r", 0) as IN:
                with open(self.full_log_path, "w", 0) as OUT:
                    for line in IN: OUT.write(line)
            # Use perm logger not templog         
            self.logger.debug(''.join(["templog migrated to .", 
                                       self.full_log_path]))

        @raisetry(''.join(["Failure removing templog './loghandlertmp.log'. "]))
        def _remove_tempfile(self):
            os.remove("./loghandlertmp.log")
            
        _setit(self)
        _remove_tempfile(self)
        # Use perm logger not templog         
        self.logger.debug(''.join(["templog './loghandlertmp.log' purged."]))
        return True
        
    def _read(self):
        """"""
        _list = open(self.full_log_path, "r", 0).read().splitlines()
        return _list
 
    def _remove_handler(self, app_name):

        @handlertry(''.join(["PassThroughException: ", 
                            "Failure removing logging handler '",
                           str(app_name), "'. " 
                           ]))
        def _setit(self, app_name):
            self.logger.debug(''.join(["Attempting to remove handler '", 
                                   str(app_name), "'..." 
                                   ]))

            if self._isExistingLogger(app_name):
                del logging.Logger.manager.loggerDict[app_name]

            self.logger.debug(''.join(["handler '", 
                                       str(app_name), 
                                       "' removed. " 
                                       ]))

        _setit(self, app_name)

    def _set_fileHandler(self, 
                         logfile, 
                         log_level,
                         formatter 
                         ):
        self.templog.debug("Setting filehandler to " + logfile + ".")

        @raisetry(''.join(["Failure setting filehandler '", 
                           str(logfile), 
                           "'. "]))
        def _setit(self,                          
                   logfile, 
                   log_level,
                   formatter 
                   ):
            
            fh = logging.FileHandler(self.full_log_path)
            fh.setLevel(level=log_level)
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)
            return True
        
        _setit(self, logfile, log_level, formatter)
        return True

    def _set_formatter(self):
        self.templog.debug("Setting formatter.")

        @raisetry(''.join(["Failure setting formatter."]))
        def _setit(self):
            self.formatter = logging.Formatter(
                        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                        )
            return True
        
        _setit(self)
        return True

    def _set_full_logpath(self):

        @raisetry(''.join(["Failure setting full log path. "]))
        def _setit(self):
            self.full_log_path = self.log_path + self.logfile
            return True
        
        _setit(self)
        self.templog.debug(''.join(["'full_log_path': ", 
                                    self.full_log_path]))
        return True

    def _set_screendump(self, 
                        screendump, 
                        log_level,
                        formatter 
                        ):
        self.templog.debug("Setting screendump.")

        @raisetry(''.join(["Failure setting screendump." ]))
        def _setit(self, 
                   screendump, 
                   log_level,
                   formatter 
                   ):
            if screendump:
                ch = logging.StreamHandler()
                ch.setLevel(level=log_level)
                ch.setFormatter(formatter)
                self.logger.addHandler(ch)
                self.templog.debug("Screendump ON.")
                return True

            else:
                self.templog.debug("Screendump OFF.")
                return True

        _setit(self, screendump, log_level, formatter)
        return True

    # For now, only the standard logging levels are supported as recommended
    # by the logging documentation

    def _start_log(self, 
                   app_name     = "loghanderStartup", 
                   logfile      = "./loghandlertmp.log", 
                   log_level    = 10, 
                   formatter    = None,
                   screendump   = False
                   ): 
        
        @raisetry(''.join(["Unable to open the log. "]))
        def _log(self, 
                 app_name, 
                 logfile, 
                 log_level,
                 formatter, 
                 screendump
                 ):
            
            # Remove the existing logger
            if self._isExistingLogger(app_name):
                self._remove_handler(app_name)
            
            logger = logging.getLogger(app_name)
            logger.setLevel(level=log_level)
            if ((formatter is "") or (formatter is None)): 
                formatter = logging.Formatter(
                        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
            # create file handler which logs even debug messages
            fh = logging.FileHandler("./loghandlertmp.log")
            fh.setLevel(level=log_level)
            fh.setFormatter(formatter)
    
            # create console handler with a higher log level
            if screendump:
                ch = logging.StreamHandler()
                ch.setLevel(level=log_level)
                ch.setFormatter(formatter)
            else:
                ch = False
                    
            # add the handlers to the logger
            if fh: logger.addHandler(fh)
            if ch: logger.addHandler(ch)
            return logger
        
        logger = _log(self,                  
                      app_name, 
                      logfile, 
                      log_level,
                      formatter, 
                      screendump
                      )
        
        logger.info(''.join(["logger started as '", 
                             str(app_name), 
                             "' at '",
                             str(logfile),
                             "'. " 
                             ]))
        self.logger = logger
        
        return logger
    
    @raisetry(''.join(["Unable to open the startup log. "]))
    def _start_templog(self, 
                       app_name     = "loghanderStartup", 
                       logfile      = "./loghandlertmp.log", 
                       log_level    = 10, 
                       formatter    = None,
                       screendump   = False
                       ):
        
                self.templog = self._start_log(app_name, 
                                               logfile, 
                                               log_level, 
                                               formatter,
                                               screendump
                                               )
         
                self.templog.info("Temp startup log created.")    

                      
if __name__ == "__main__":
    
    log = SetLogger(app_name = "realAppName", 
                    logfile = "test.log",
                    log_path = "/shared/GitHub/Tesera/MRAT_Refactor/log", 
                    log_level = 10, 
                    screendump = True, 
                    )
    
    
    log.logger.debug("This is a log test of log.logger.debug")

    log.debug("This is a log test of log.debug")
    log.info("This is a log test of log.info")
    log.warning("This is a log test of log.warning")
    log.error("This is a log test of log.error")
    log.critical("This is a log test of log.critical")

    #-----------------------
    
#     log = SetLogger(app_name = "realAppName", 
#                     logfile = "test.log",
#                     log_path = "/shared/GitHub/Tesera/MRAT_Refactor/log", 
#                     log_level = 10, 
#                     screendump = True, 
#                     )
#     
#     
#     log.logger.debug("This is a log test of log.logger.debug")
# 
#     log.debug("This is a log test of log.debug")
#     log.info("This is a log test of log.info")
#     log.warning("This is a log test of log.warning")
#     log.error("This is a log test of log.error")
#     log.critical("This is a log test of log.critical")
