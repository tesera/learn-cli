##############################################################################
# Removal of the "__license__" line or content from  "__license__", or removal 
# of "__author__" in this or any constituent # component or file constitutes a 
# violation of the licensing and copyright agreement. 
__author__      = "Mike Rightmire"
__copyright__   = "BioCom Software"
__license__     = "Tesera"
__license_file__= "Clause1.PERPETUAL_AND_UNLIMITED_LICENSING_TO_THE_CLIENT.py"
__version__     = "0.9.1.0"
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

class setLogger(object):
    """
    """    

    def __new__(cls, 
                app_name = None, 
                logfile = "",
                log_path = None, 
                log_level = 40, 
                screendump = False, 
                create_paths = False 
                ):
        """
        This is a singletone class. The __new__ method is called prior to 
        instantiation with __init__. If there's already an instance of the
        class, the existing object is returned. If it doesn't exist, a new 
        object is instantiated with the __init__.
        """
        if not hasattr(cls, 'instance'):
            cls.instance = super(setLogger, cls).__new__(cls)
        return cls.instance
        
    def __init__(self, 
                 app_name = None, 
                 logfile = "",
                 log_path = None, 
                 log_level = 40, 
                 screendump = False,
                 create_paths = False 
                ):

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
#         self._set_logger()

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
    #  logging documentation

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

    def level(self):
        """
        Intended to change the logging level of the existing handlers
        """
        raise NotImplementedError

    def name(self):
        """
        Intended to change the logger name of the existing handlers
        """
        raise NotImplementedError

    def formatter(self):
        """
        Intended to change the log formatting of the existing handlers
        """
        raise NotImplementedError

    def dump_to_screen(self, dumping = False):
        """
        Intended to change the current setting for 'screendump' of the existing
        handlers (which determines if items written to the log are also 
        printed to the screen.
        """
        raise NotImplementedError

    def screendump(self):
        """
        Dumps the current logfile conents to std out.
        """
        _list = self_read()
        for line in _list:
            print line

    def logfile(self, newfile = None):
        """
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
                    os.utime(self.full_log_path, times)


        self.logger.critical(''.join(["Attempting to purge '", 
                                      str(self.full_log_path), "'. "]))
        _purge(self)

        self.logger.critical(''.join(["Successfully purged '", 
                                      str(self.full_log_path), "'. "]))
                
            
    def _read(self):
        """"""
        _list = open(self.full_log_path, "r", 0).read().splitlines()
        return _list
 
    def _isExistingLogger(self, app_name):
        """
        """
        if app_name in str(logging.Logger.manager.loggerDict.keys()):
            return True
        else:
            return False
    
#     def _set_logger(self):
# 
#         @raisetry(''.join(["Failure calling 'logging.getLogger'. "]))
#         def _setit(self):
#             self.logger = logging.getLogger(self.app_name)
#             return True
#         
#         _setit(self)
#         self.templog.debug("getLogger called with '" + self.app_name + "'.")
#         return True
    
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
    
    def _set_full_logpath(self):

        @raisetry(''.join(["Failure setting full log path. "]))
        def _setit(self):
            self.full_log_path = self.log_path + self.logfile
            return True
        
        _setit(self)
        self.templog.debug(''.join(["'full_log_path': ", 
                                    self.full_log_path]))
        return True

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
            if "CR" in str(self.log_level).upper(): 
                self.log_level = "CRITICAL"
                return True
                 
            if "ER" in str(self.log_level).upper(): 
                self.log_level = "ERROR"; return True
                
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

                      
if __name__ == "__main__":
    
    log = setLogger(app_name = "realAppName", 
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
    
#     log = setLogger(app_name = "realAppName", 
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
