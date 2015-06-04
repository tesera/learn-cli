#!/usr/bin/python

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


from loghandler import SetLogger

import inspect
import functools
import sys


class CustomError(Exception):
    """
    Base user extensible exception class
    Baseclass for dealing with unhandled errors
    Extends class Exception
    """
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)

### Specific classes for dealing with unhandled exceptions
#   Extends class CustomError    


class FatalException(CustomError):
    """
    raise FatalSocketError
    Returns default error + the attached string message
    "Socket encountered a fatal condition. "
    """
    def __init__(self, message = None):
        self.message = ("")
        CustomError.__init__(self, self.message)
        
######
# MAIN

# # The error handler MUST have a log file. 
# # If 'None' is passed, a logger to /dev/null equivalent is created.
# #If anything else is passed, log to a local file "error.log"

# --- HOW TO INSTANTIATE IN SCRIPT ---
# import errorhandler
# from inspect import getmembers, stack
# self.CustomErrorHandler = errorhandler.ErrorHandler(self.log)
# self.err = self.CustomErrorHandler.err()

# --- HOW TO USE THE ERROR HANDLER ---
# try:
#     i = int("notnum") # this will error
# except Exception, e:
#     e = ''.join(["NameOfCatchMethod:", str(e)])
#     self.err(e, getmembers(self), stack())

# IMPORTABLE FUNCTIONS --------------------------------------------------------


class ErrorHandler(object):
    """
    class_obj = ErrorHandler()
    
    DESCRIPTION:
        errorhandler is a class to control exceptions generated in scripts. 
    
        When called within a try:except idiom, the error can be passed here 
        where information can be passed to the logger, custom code can be 
        entered to handle the error, and/or it can be raised as a fatal 
        exception. 
    
    USAGE:
        --- HOW TO INSTANTIATE THE ERROR HANDLER IN AN EXTERNAL SCRIPT ---
        import errorhandler
        from inspect import getmembers, stack
        self.CustomErrorHandler = errorhandler.ErrorHandler(self.log)
        self.err = self.CustomErrorHandler.err()

        --- HOW TO USE THE ERROR HANDLER IN AN EXTERNAL SCRIPT---
        try:
            i = int("notnum") # this will error
        except Exception, e:
            e = ''.join(["MyErrorHandlingMethod:", str(e)])
            self.err(e, getmembers(self), stack())
    
        --- EDITING THE SCRIPT TO ADD ERROR HANDLING METHODS ---
            if   'fatal'                in str(e).lower(): self.FatalError(e)
            elif 'PassThroughException' in str(e): self.PassThroughException(e)
            elif 'MyErrorHandlingMethod' in str(e): self.MyErrorHandlingMethod(e)
            
            After adding the elif statement, use the TEMPLATE method to create
            a matching handling method. 

    METHODS:
        customErr(e, source, frame)
            e = The MODIFIED string passed out from the exception. Normal usage
                dictates the string be pre-pended with the name of the error
                handling method (see above). 
            
            source = The 'getmembers(self)' call found in the self.err call above
            
            frame = The 'stack()' call found in the self.err call above
            
        err(e, source, frame)
            Simply a smaller pointer to customErr()
            
        No other methods are intended or recommended to be user callable.  
    """

    def __init__(self): #, log):
        self.log = SetLogger()
            
    def _format_original_error(self, e):
        return "".join([str(e), ". "])
#         return "".join(["[Original error: ", str(e), "]"])
    
    def _custom_error(self, message, e):
        # Format message
        e = "".join([str(self._format_original_error(e)), message])
        # Send to log
        self.log.error(e)
        return

    def err(self):
        def _err(sourceobj, args, kwargs, e, source, frame):
            return self.customErr(sourceobj, args, kwargs, e, source, frame)
        return _err
            
    def customErr(self, sourceobj, args, kwargs, e, source, frame):
        """
        NAME
            errorhandler
         
        FILE
            errorhandler.py
         
        DESCRIPTION
            Used for generating both custom unhandled exceptions, and 
            for handling exceptions with specific actions. Creates the opportunity 
            for cutom code to be attached to errors and resolve them in a clean 
            format
             
            An existing 'self' object must be passed in with an existing self.log 
            object associated with it!!
                Uses the self.log() parameter of an EXISTING instantiated log object
                to generate output. A logger has to be instantiated in the calling 
                class for this method to be used.
     
        EXAMPLE (USAGE)
            from inspect import getmembers
            from inspect import stack
            import errorhandler
            
            customerr = errorhandler.ErrorHandler(self.log)
            self.err  = customerr.err()           
 
            try:
                print this wont work
            except:
            e = "".join(["ErrorIdentifier: ", "Additional information."])
            self.lasterr = self.err(e, getmembers(self), stack())
                 
        METHODS
            ErrorHandler(self, e, source, frame)
                Error message handler. Generates logfile output
                    self   = The class object using the error handler. Must contain 
                             a self.log object.
    
                    e      = The error message passed from the calling object. I.e.
                             except Exception, e:
    
                    source = The inspect.getmembers(self) passed in from the error 
                             call. 
                    
                    frame  = The inspect.stack() passed in from the error call.
             
            TEMPLATE(self, e)
                Create custom error message and handling code
    
        HIDDEN METHODS
            _format_original_error(e)
            _custom_error(self, message, e)
                     
        """        
###############################################################################
# FOR NOW, LEAVE 'e' ALONE        
#         # Source is inspect.getmembers(self)
#         # EXAMPLE SOURCE (a list of tuples):
#         #[('MAX_LENGTH', 16384), 
#         # ('TSTART', 'TWILIOSOCK'), 
#         # ('__doc__', None), 
#         # ('__implemented__', <implementedBy twisted.internet.protocol.Protocol>), 
#         # ('__init__', <bound method Handler.__init__ of <twistedlisten.Handler instance at 0x02E05EB8>>), 
#         # ('__module__', 'twistedlisten'), 
#         # ('__providedBy__', <implementedBy twistedlisten.Handler>), 
#         # ('__provides__', <implementedBy twistedlisten.Handler>), 
#         # ('_buffer', ''), 
#         # ('_busyReceiving', False), 
#         # ('_checkdata', <bound method Handler._checkdata of <twistedlisten.Handler instance at 0x02E05EB8>>), 
#         # ('_parsedata', <bound method Handler._parsedata of <twistedlisten.Handler instance at 0x02E05EB8>>), 
#         # ('<some_method>', <bound method <class>.<method> of <someinstance instance at 0x02E05EB8>>), 
#         #]
#         errorin = str(source[6][1])
#         errorin = errorin.replace("implementedBy", "")
#         errorin = "".join(c for c in errorin if c not in "<>")
#         errorin = errorin + "." + str(frame[0][3])
#         errorin = errorin + "(line:" + str(frame[0][2]) + "): "
#         e = errorin + str(e)

                        
        #EXTERNAL ERRORS
        if   'fatal'                in str(e).lower(): self.FatalError(sourceobj, args, kwargs, e)
        elif 'PassThroughException' in str(e): self.PassThroughException(sourceobj, args, kwargs, e)
        elif 'InvalidPath'          in str(e): self.InvalidPath(sourceobj, args, kwargs, e)
        elif 'ConfigFileNotFound'   in str(e): self.ConfigFileNotFound(sourceobj, args, kwargs, e)
        elif 'ConfigFileParseError' in str(e): self.ConfigFileParseError(sourceobj, args, kwargs, e)
        elif 'ConfigFileNoOption'   in str(e): self.ConfigFileNoOption(sourceobj, args, kwargs, e)
        elif 'ParameterNotSet'      in str(e): self.ParameterNotSet(sourceobj, args, kwargs, e)
        elif 'FullPathDoesNotExist'      in str(e): self.FullPathDoesNotExist(sourceobj, args, kwargs, e)

        elif 'PathDoesNotExist'     in str(e): 
            return self.PathDoesNotExist(sourceobj, args, kwargs, e)
        
        # elif: # More error checks here
    
#         else: self.UnknownException(sourceobj, args, kwargs, e)
        else: return self.PathDoesNotExist(sourceobj, args, kwargs, e)    
            
    ### SPECIFIC ERROR HANDLERS 
    # These functions perform specific actions on the 'self' object These are used 
    # to handle errors and return to the lone below the error call, UNLESS the 
    # a new fatal exception is raised, which will halt all scripts. 
    # The keyword 'fatal' in the error message passed to errorhandler will raise a 
    # fatal exception and halt the scripts. 
    
    def TEMPLATE(self, sourceobj, args, kwargs, e):
        # Create custom message to BE SENT TO THE LOGGER
        message = ("".join(["Template message part 1 is a list item. ", 
                            "Template message part 2 is a list item."]))    
        # Sends the message and original error to the LOGGER
        # Remove this line if you don't want an error displayed
        self._custom_error(message, e)
        ### METHOD ACTIONS
        # CODE BELOW TO CORRECT ISSUE
        # All code acts on the self object
        return str(sys._getframe().f_code.co_name)

    def ConfigFileNotFound(self, sourceobj, args, kwargs, e):
        # Create custom message to BE SENT TO THE LOGGER
        message = ("".join(["The configuration file was not found. ", 
                            "Please verify the file exists in the ", 
                            "appropriate path and is readable."]))    
        # Sends the message and original error to the LOGGER
        # Remove this line if you don't want an error displayed
        self._custom_error(message, e)
        ### METHOD ACTIONS
        # CODE BELOW TO CORRECT ISSUE
        # All code acts on the self object
        raise FatalException()

    def ConfigFileNoOption(self, sourceobj, args, kwargs, e):
        # Create custom message to BE SENT TO THE LOGGER
        message = ("".join(["Unable to find the specified section or option", 
                            "(variable) in config file. ", 
                            "Please verify the contents of the file. "]))    
        # Sends the message and original error to the LOGGER
        # Remove this line if you don't want an error displayed
        self._custom_error(message, e)
        ### METHOD ACTIONS
        # CODE BELOW TO CORRECT ISSUE
        # All code acts on the self object
        return # To line following calling error
        
    def ConfigFileParseError(self, sourceobj, args, kwargs, e):
        # Create custom message to BE SENT TO THE LOGGER
        message = ("".join(["The configuration file contains errors. ", 
                            "Please verify the contents of the file. "]))    
        # Sends the message and original error to the LOGGER
        # Remove this line if you don't want an error displayed
        self._custom_error(message, e)
        ### METHOD ACTIONS
        # CODE BELOW TO CORRECT ISSUE
        # All code acts on the self object
        raise FatalException()
    
    def FullPathDoesNotExist(self, sourceobj, args, kwargs, e):
        # Custom message to BE SENT TO THE LOGGER
        message = ''.join(["Either the path passed does not exist, ", 
                           "or the end file  does not exist."])

        # Sends the message and original error to the LOGGER
        self._custom_error(message, e)

        ### METHOD ACTIONS
        result = False
        kwargs["path"] = raw_input("enter a correct path...")
    
        return args, kwargs, result

    def InitFailure(self, sourceobj, args, kwargs, e):
        # Create custom message to BE SENT TO THE LOGGER
        message = ("")
        # Sends the message and original error to the LOGGER
        # Remove this line if you don't want an error displayed
        self._custom_error(message, e)
        ### METHOD ACTIONS
        # CODE HERE TO CORRECT ISSUE
        raise FatalException()

    def InvalidPath(self, sourceobj, args, kwargs, e):
        # Create custom message to BE SENT TO THE LOGGER
        message = ''.join([e, 
                           "Path does not appear to be a valid format of ", 
                           "'<drive>:\path\path\\' in Windows or '/path/path/' ", 
                           "for Linux/OSX. ", 
                           "NOTE: There MAY be a required ending slash."
                           ])
        # Sends the message and original error to the LOGGER
        # Remove this line if you don't want an error displayed
        self._custom_error(message, e)
        ### METHOD ACTIONS
        # CODE HERE TO CORRECT ISSUE IF DESIRED
        raise FatalException()
        
    def ParameterNotSet(self, sourceobj, args, kwargs, e):
        # Custom message to BE SENT TO THE LOGGER
        message = ("A script parameter (variable) does not exist " +
                   "or is the wrong type")
        # Sends the message and original error to the LOGGER
        self._custom_error(message, e)
        ### METHOD ACTIONS

    def PassThroughException(self, sourceobj, args, kwargs, e):
        # Custom message to BE SENT TO THE LOGGER
        message = ("")
        # Sends the message and original error to the LOGGER
        self._custom_error(message, e)
        ### METHOD ACTIONS
        
    def PathDoesNotExist(self, sourceobj, args, kwargs, e):
        # Custom message to BE SENT TO THE LOGGER
        message = ''.join(["The path passed does not exist, ", 
                           "or 'path = <value>' was not set ", 
                           "when calling method. "])

        # Sends the message and original error to the LOGGER
        self._custom_error(message, e)

        ### METHOD ACTIONS
        result = False
        kwargs["path"] = raw_input("enter a correct path...")
    
        return args, kwargs, result
        
    def FileDoesNotExist(self, sourceobj, args, kwargs, e):
        # Custom message to BE SENT TO THE LOGGER
        message = ("The file passed does not exist. ")
        # Sends the message and original error to the LOGGER
        self._custom_error(message, e)
        ### METHOD ACTIONS
        
    def FatalError(self, sourceobj, args, kwargs, e):
        # Custom message to BE SENT TO THE LOGGER
        message = ("")
        # Sends the message and original error to the LOGGER
        self._custom_error(message, e)
        ### METHOD ACTIONS
        raise FatalException(e)
    
    def UnknownException(self, sourceobj, args, kwargs, e):
        # Custom message to BE SENT TO THE LOGGER
        message = ("".join(["An unidentified exception was passed. ", 
                            "'errorhandler' does not know what to do. ", 
                            "Calling fatal exception and halting. "]))
        # Sends the message and original error to the LOGGER
        self._custom_error(message, e)
        ### METHOD ACTIONS
        raise FatalException(e)    


if __name__ == "__main__":
    
    pass    
    