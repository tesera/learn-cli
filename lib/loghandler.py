##############################################################################
# Removal of the "__license__" line or content from  "__license__", or removal 
# of "__author__" in this or any constituent # component or file constitutes a 
# violation of the licensing and copyright agreement. 
__author__      = "Mike Rightmire"
__copyright__   = "BioCom Software"
__license__     = "Jeff Wright"
__license_file__= "Clause1.PERPETUAL_AND_UNLIMITED_LICENSING_TO_THE_CLIENT.py"
__version__     = "0.9.0.3"
__maintainer__  = "Mike Rightmire"
__email__       = "Mike.Rightmire@BiocomSoftware.com"
__status__      = "Development"
##############################################################################

from checks import directoryExists
from checks import checkPathFormat
import logging
import os
import re

### Depricated methods, for compatibility
def check_logger(log, callingobj, log_path = "" ):
    return checkLogger(log, callingobj, log_path = "" )


def create_logger(app_name, logfile = "", log_level = 40, screen = True):
    return createLogger(app_name,logfile = "", log_level = 40, screen = True)


log_path_err = ''.join(["The parameter 'log_path' passed to loghandler ", 
                       "does not appear to meet the required format of either:", 
                       " '<letter>:\path\path\' or '/path/path/'."])

    
def createLogger(app_name, 
                 logfile = "",
                 log_path = None, 
                 log_level = 40, 
                 screen = True):
    """
    self.logger = createLogger(app_name, 
                               logfile = "", 
                               log_level = 40, 
                               screen = True)
    
    DESCRIPTION

        Create logged is intended to create log objects for use within other 
        classes.

        app_name  = Name of the class or application

        logfile   = The file to write error messages to. The default value is 
                    sys.stderr (the stderr as defined by the Python 'sys' 
                    module.) If logfile = None no log file will be used and 
                    logging will be only to the screen.    

        log_level = The log level to be output. Must be an integer (int).
            CRITICAL 50
            ERROR    40
            WARNING  30
            INFO     20
            DEBUG    10
            NOTSET   0

    METHODS
        create_logger(app_name, logfile, log_level)
    
    EXAMPLE
        from logger import create_logger
        self.log = create_logger(self.__class__.__name__, 
                                 logfile, 
                                 log_level)  

    """
    # Checks for logfile. If none, set a default logfile in local directory
    # If nothing is passed, set to default logfile path and name
    if log_path is None:
        log_path = './log/'
        if not directoryExists(log_path):
            os.mkdir("./log")

    if  logfile is "": 
        logfile = ''.join([log_path, str(app_name), ".log"])
        
    elif logfile is None:
        # No log file will be written 
        logfile = None

    else: 
        # Blindly accept whatever was passed in 
        # Put checks in here eventually
        logfile = str(logfile)

    # Checks that log level is an integer. 
    # If it fails, sets to default level of 40 (error)
    try: 
        log_level = int(log_level)
    except: 
        log_level = 40
    
    # create self.logger with 'spam_application'
    logger = logging.getLogger(app_name)
    logger.setLevel(level=log_level)
    formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                                 )

    # Create dev/null for defaults
    nh = logging.FileHandler(os.devnull)
    nh.setLevel(level=log_level)
    
    # create file handler which logs even debug messages
    if logfile is not None:
        fh = logging.FileHandler(logfile)
        fh.setLevel(level=log_level)
        fh.setFormatter(formatter)
    else:
        fh = False

    # create console handler with a higher log level
    if screen:
        ch = logging.StreamHandler()
        ch.setLevel(level=log_level)
        ch.setFormatter(formatter)
    else:
        ch = False

    # add the handlers to the logger
    if fh: logger.addHandler(fh)
    if ch: logger.addHandler(ch)
    # ALWAYS ADD THE NULL HANDLER
    logger.addHandler(nh)

    return logger

def checkLogger(log, # Do not set a default. SOMETHING must be passed 
                callingobj, # The calling object or None 
                log_path = "" # Path to the logfile (NOT including filename)
                ):
    
    # Check log_path first, to get it out of the way :-)
    if   (log_path is None): 
        log_path = "" 
    elif (log_path == ""): # default
        log_path = "./log"
    else:
        # Verify its (at least) an actual windows or linux path format
        # Does NOT check if it exists
        if not checkPathFormat:
            raise Exception(log_path_err)
    
    ### Start checking what the passed log is
    # If 'log' is an existing loghandler object, just return it back
    if   ('log' and 'class') in str(type(log)).lower():
        return log

    # log = None means specifically no logging desired 
    elif log is None:
        return createLogger(
                app_name = None, 
                logfile = None, 
                log_level = 10, 
                screen = False
                )
        
    # Blank string passed. (Should never do this)
    # A default screen log and logfile are created
    elif log == "":
        app_name = "loghandler" 
        log_file = ""        # Will use createLogger default
        log_path = log_path  # Will use what is set here in checkLogger
        screen = True        # Same as createLogger default
        
    # Otherwise, if no log object but callingobj is actually a class object 
    # - get its name
    elif "class" in str(type(callingobj)).lower():
        app_name = callingobj.__class__.__name__
        log_file = "" # Will use createLogger default
        log_path = log_path  # Will use what is set here in checkLogger
        screen = True # Same as createLogger default

    # If log is just a string, use the string
    else:
        # 'log' had to be passed something or an error raised. Just use it as is 
        app_name = str(log)
        log_file = "" # Will use createLogger default
        log_path = log_path  # Will use what is set here in checkLogger
        screen = True # Same as createLogger default
                
    # Return a new log object
    if "\\" in log_path: 
        logfile = ''.join([log_path, "\\", app_name, ".log"])
    elif "/" in log_path:
        logfile = ''.join([log_path, "/", app_name, ".log"])
    else:
        logfile = ''.join([log_path, "", app_name, ".log"])

    return createLogger(
            app_name = app_name, 
            logfile = logfile, 
            log_level = 10, # log_level = 40, screen = False,
            )        

if __name__ == "__main__":
    log = createLogger(
                       app_name = 'loghandlerAppName', 
                       logfile = "", 
                       log_level = 10, 
                       screen = True
                       )
    log.debug("This is a log test")

    newlog = checkLogger("checkLoggerAppName", None)
    newlog.debug("Test of checkLogger run with active log")    
        
    newlog = checkLogger(None, None)
    newlog.debug("Test of newlog created with None as log")