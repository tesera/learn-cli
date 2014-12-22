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
from errorlogger import errorLogger
from inspect import stack 

import logging
import os
import re
    
def _check_app_name(app_name):
    errorlog.write(("Checking app_name of '" + str(app_name) + "'..."))

    if ((app_name is None) or (app_name == "")):
        errorlog.write(("app_name is Null. Setting to calling script name"))
        caller_frame = stack()[1]
        app_name = caller_frame[1]
        app_name = os.path.basename(app_name)
        app_name = ''.join(c for c in app_name if re.match("[a-zA-z0-9]", c))

    try:
        app_name + "string"
        return app_name
    
    except TypeError, e:
        msg = ("Parameter 'app_name' not a valid string. " + 
               str(e))
        errorlog.write(msg)
        raise Exception(str(e))
        
def _check_logfile(log_path, logfile, app_name):
    if  (logfile is ""): 
        return ''.join([log_path, str(app_name), ".log"])
    
    elif (logfile is None):
        # No log file will be written 
        return None
    else:
        try:
            logfile + "string"
            return logfile
        
        except TypeError, e:
            msg = ("Parameter 'logfile' not a valid string. " + 
                   str(e) + 
                   "\n" + 
                   "Continuing with default logfile name..."
                   )
            errorlog.write(msg)
            return ''.join([log_path, str(app_name), ".log"])
        
def _check_log_level(log_level):
    if "CRITICAL"   in str(log_level).upper(): return "CRITICAL" 
    if "ERROR"      in str(log_level).upper(): return "ERROR"
    if "WARNING"    in str(log_level).upper(): return "WARNING"
    if "INFO"       in str(log_level).upper(): return "INFO"
    if "DEBUG"      in str(log_level).upper(): return "DEBUG"
    if "NOTSET"     in str(log_level).upper(): return "NOTSET" 

    try: 
        log_level = int(log_level)
        if ((log_level >= 0) and (log_level <= 50)): 
            return log_level
        else:
            raise Exception("")

    except Exception, e:
        msg = ("Parameter 'log_level' (" + 
               str(log_level) + ") " +
               "does not appear to meet criteria of an integre between " + 
               "0 and 50, or one of the following keywords..."  + "\n" + 
               "CRITICAL" + "\n" 
               "ERROR" + "\n"
               "WARNING" + "\n"
               "INFO" + "\n"
               "DEBUG" + "\n"
               "NOTSET"  + "\n"
               "Setting to a default of 'DEBUG'"
               )
        errorlog.write(msg)
    
    return 10
    
def _check_log_path(log_path):
    # Check log_path first, to get it out of the way :-)
    errorlog.write(("Checking log path of '" + str(log_path) + "'..."))

    if   ((log_path is None) or 
          (log_path == "")
          ): 
            # Set to the local directory
            log_path = "./"
#                 if not directoryExists(log_path):
#                     os.mkdir("./log")

    else:
        # If directory HAS been passed...
        # Verify its (at least) an actual windows or linux path format
        # Does NOT check if it exists
        if not checkPathFormat(log_path):
            errorlog.write("File path is not in a usable format.")
#                 errorlogger.cleanup(False) # Override setting due to error
            raise Exception(log_path_err)
        
    errorlog.write(("log_path set to : '" + str(log_path) + "'"))
    return log_path
    
def _generate_logger(app_name, log_level):
        # create logger
        errorlog.write("Instantiating persistent logger...")
        logger = logging.getLogger(app_name)

        errorlog.write(("Setting log level of " + str(log_level)))
        logger.setLevel(level=log_level)

        return logger

def _createLogger(app_name, 
              logfile = "",
              log_path = None, 
              log_level = 40, 
              screendump = False, 
              debug = False, 
             ):
    """
    self.logger = createLogger(app_name, 
                               logfile = "", 
                               log_level = 40, 
                               screendump = True)
    
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
    logger = _generate_logger(app_name, log_level)
    nh = _set_devnull(log_level)        
    formatter = _set_formatter()
    
    # create file handler which logs even debug messages
    if logfile is not None:
        errorlog.write(("Creating logfile handler: " + str(logfile)))
        fh = _set_fileHandler(logfile, log_level, formatter)

    else:
        errorlog.write("Logger will not write to a file.")
        fh = False

    # create console handler with a higher log level
    if screendump:
        errorlog.write(("Creating STDOUT handler: "))
        ch = _set_streamHandler(log_level, formatter)
    else:
        errorlog.write("Logger will not write screen.")
        ch = False

    errorlog.write("Adding handlers to logger...")
    # add the handlers to the logger
    if fh: logger.addHandler(fh)
    if ch: logger.addHandler(ch)
    # ALWAYS ADD THE NULL HANDLER
    logger.addHandler(nh)

    return logger

def _isExistingLogger(app_name):
    """
    """
    if app_name in str(logging.Logger.manager.loggerDict.keys()):
        return True
    else:
        return False
    
def _set_devnull(log_level):
        errorlog.write("Creating mandatory null handler...")
        # Create dev/null for defaults
        nh = logging.FileHandler(os.devnull)
        nh.setLevel(level=log_level)
        return nh

def _set_fileHandler(logfile, log_level, formatter):
    fh = logging.FileHandler(logfile)
    fh.setLevel(level=log_level)
    fh.setFormatter(formatter)
    return fh

def _set_formatter():
        errorlog.write("Setting log formatter...")
        return logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                    )

def _setLogger(app_name):    
    if _check_app_name(app_name):
        logger = logging.getLogger(app_name)
        return logger
    else:
        msg = "Unable to set variable 'logger'."
        errorlog.write(msg)

def _set_streamHandler(log_level, formatter):
    ch = logging.StreamHandler()
    ch.setLevel(level=log_level)
    ch.setFormatter(formatter)
    return ch
        
def checkLogger(
                app_name, # Do not set a default. SOMETHING must be passed
#                 log, # Do not set a default. SOMETHING must be passed 
#                 callingobj, # The calling object or None 
                log_path = "", # Path to the logfile (NOT including filename)
                debug = False, #Always default checkLogger to true
                screendump = False
                ):
    """"""
    raise NotImplementedError()

    

def setLogger(app_name = None, 
              logfile = "",
              log_path = None, 
              log_level = 40, 
              screendump = False, 
              debug = False
              ):
    """"""
    global errorlog
    errorlog = errorLogger('loghandler', screendump = screendump, debug = debug)

    original_app_name = app_name
    app_name = _check_app_name(app_name)

    errorlog.write("----- Starting loghandler.setLogger ----- ")
    errorlog.write(("app_name    = " + str(app_name)))
    errorlog.write(("logfile     = " + str(logfile)))
    errorlog.write(("log_path    = " + str(log_path)))
    errorlog.write(("log_level   = " + str(log_level)))
    errorlog.write(("screendump  = " + str(screendump)))
    errorlog.write(("debug       = " + str(debug)))
    
    if _isExistingLogger(app_name):
        # logger already exists
        # FOR NOW, if it exists, AND all the params passed were the defaul
        # (implying the call was 'setLogger()', then just return existing 
        # In a future version that parameters can be checked against what was
        # passed into setLogger and the logger can be modified. 
        if ((original_app_name == None) and  
            (logfile == "")             and 
            (log_path == None)          and  
            (log_level == 40)           and  
            (screendump == False)       and 
            (debug == False)
            ):
            return logging.Logger.manager.loggerDict[app_name]

    #If a existing logger exists, and no parameters were sent to the 
    # setLogger()...then a return will have already happened. 
    # If not create logger
    
    # Checks for logfile. If none, set a default logfile in local directory
    # If nothing is passed, set to default logfile path and name
    log_path = _check_log_path(log_path)
    logfile = _check_logfile(log_path, logfile, app_name)
    log_level = _check_log_level(log_level)
        
    return _createLogger(app_name, 
                         logfile,
                         log_path, 
                         log_level, 
                         screendump, 
                         debug, 
                         )
                      
if __name__ == "__main__":
    
    log = setLogger(
                       app_name = None, 
                       logfile = "", 
                       log_level = 10, 
                       screendump = True, 
                       debug = True
                       )
    log.debug("This is a log test")
    
    log = setLogger()
    log.debug("This is a log test after second setLogger")
    