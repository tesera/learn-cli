##############################################################################
# Removal of the "__license__" line or content from  "__license__", or removal 
# of "__author__" in this or any constituent # component or file constitutes a 
# violation of the licensing and copyright agreement. 
from distutils.cmd import Command
__author__      = "Mike Rightmire"
__copyright__   = "BioCom Software"
__license__     = "Tesera"
__license_file__= "Clause1.PERPETUAL_AND_UNLIMITED_LICENSING_TO_THE_CLIENT.py"
__version__     = "0.9.3.0"
__maintainer__  = "Mike Rightmire"
__email__       = "Mike.Rightmire@BiocomSoftware.com"
__status__      = "Development"
##############################################################################

from formatters import _format_original_error,_log_error
from customexceptions import CustomError,FatalException
from loghandler import log
import re
import subprocess
import sys
import os

### SPECIFIC ERROR HANDLERS 
# These functions perform specific actions on the 'self' object These are used 
# to handle errors and return to the lone below the error call, UNLESS the 
# a new fatal exception is raised, which will halt all scripts. 
# The keyword 'fatal' in the error message passed to errorhandler will raise a 
# fatal exception and halt the scripts. 

# ErrorHandler calls the proper handler method from here based on the error 
# keyword matched in the error string passed to the ErrorHandler. 
#
# The search is done as...
#  if str(MethodName).lower() in str(error_string).lower():
#
# The error keyword MUST MATCH THE METHOD NAME
#
# NOTE: 
#       THIS MEANS if you have two methods, 'ERR1' AND 'ERR10',
#       'ERR1' will always be the one found...SO IT IS RECOMMENDED YOU NAME
#       THE METHODS VERY UNIQUELY AND CAREFULLY.
#       I.e. 'StringNotFoundInLogError' 
class Handlers(object):

    def TEMPLATE(callobj, args, kwargs, e):
        """
        :NAME:
            template(callobj, args, kwargs, e)
            
        :DESCRIPTION:
        ===========================================================================
        A HANDLER METHOD MUST RETURN: 
            args, kwargs, <Some result, be it True/False/str/whatever>
        ===========================================================================
        
            This is a template for special error handlers to be used by 
            ErrorHandler when called by the handlertry decorator. It both parses 
            the information to be passed to the callobj log, as well as controls 
            attempts to fix the problem.
            
            The method name "TEMPLATE" should be replaced with a human-readable
            name WHICH MATCHES the trigger phrase used in handlertry AND 
            matches the search line in the custom Error string (see usage).  
            
            =================================================================
            'ErrorHandler' calls the proper handler method based on the error 
            keyword matched in the error string passed to the ErrorHandler. 
            =================================================================
            
            The search is done as...
             if str(MethodName).lower() in str(error_string).lower():
            
            The error keyword MUST MATCH THE METHOD NAME. I.e. To match 'TEMPLATE'
            the error string would have to be something like ...
            'Error: TEMPLATE Your thing in line 222 didn't work'
            
            THIS MEANS if you have two methods, 'ERR1' AND 'ERR10', the following...
            'Error: ERR1 Your thing in line 222 didn't work'
            'Error: ERR10 Your thing in line 222 didn't work'
            
            ... will always match method ERR1 ...SO IT IS RECOMMENDED YOU NAME
            THE METHODS VERY UNIQUELY AND CAREFULLY.
            
            I.e. 'StringNotFoundInLogError' 
            
        ===========================================================================
        A HANDLER METHOD MUST RETURN: 
            args, kwargs, <Some result, be it True/False/str/whatever>
        
        The following error is often indicative of the return being incorrect...
        
        Traceback (most recent call last):
             File "test.py", line xx, in <module>
             object.method('arg1', 'arg2', kwarg1=1, kwarg2=2)
             File "/opt/qrnote/lib/errorhandler/trywrappers.py",line 218,in wrapped
             stack()
             TypeError: 'NoneType' object is not iterable
        ===========================================================================
            
               
        :ARGUMENTS:
            self:    The ErrorHandler class object (standard use of self).  
    
            callobj: The "self" class object that used the handlertry decorator
                     which, in turn, resulted in the call of this method. The 
                     handler method can then act directly on this object during it's 
                     attempts to correct the problem.  
                     
            args:    The "args" of the method decorated by handlertry. These
                     can be modified and passed back to the decorated method
                     for its attempts to re-run the method.
                     
            kwargs:  The "kwargs" of the method decorated by handlertry. These
                     can be modified and passed back to the decorated method
                     for its attempts to re-run the method.
                     
            e:       The original error raised by the method decorated by 
                     handlertry. I.e. when the decorator trywrappers.handlertry
                     run the function, it grabs excetions as follows:
                     
                     try:
                         <code>
                     except Exception as e:
                         <e passed here>>
        
        :VARIABLES:
            No userland variables. 
            
        :RETURNS:
            args:    The original passed in parameter 'args', AFTER any 
                     modifications performed by this method.  
            
            kwargs:  The original passed in parameter 'kwargs', AFTER any 
                     modifications performed by this method.  
            
            result:  Any result to be passed back to the original decorated 
                     object method which raised the original error as 'e'.
        
        ===========================================================================
        A HANDLER METHOD MUST RETURN: 
            args, kwargs, <Some result, be it True/False/str/whatever>
        
        The following error is often indicative of the return being incorrect...
        
        Traceback (most recent call last):
             File "test.py", line xx, in <module>
             object.method('arg1', 'arg2', kwarg1=1, kwarg2=2)
             File "/opt/qrnote/lib/errorhandler/trywrappers.py",line 218,in wrapped
             stack()
             TypeError: 'NoneType' object is not iterable
        ===========================================================================
                     
    
        :USAGE:
            <the following lines added to customErr above>
            elif 'TriggerPhrase' in str(e): 
                return self.TriggerPhrase(callobj, args, kwargs, e)
            
            def TriggerPhrase(callobj, args, kwargs, e):
                # Messages and corrective code placed in appropriate places here
                return args, kwargs, result
        """
        # Create custom message to BE SENT TO THE LOGGER
        message = ("".join(["Template message part 1 is a list item. ", 
                            "Template message part 2 is a list item."]))    

        # Sends the message and original error to the LOGGER
        # Remove this line if you don't want an error displayed
        _log_error(message, e)
        ### METHOD ACTIONS
        # CODE BELOW TO CORRECT ISSUE
        # All code should act on the 'callobj' object
        
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # MUST RETURN: args, kwargs, <Some result, be it True/False/str/whatever>
        #
        #The following error is often indicative of the return being incorrect
        #
        # Traceback (most recent call last):
        #     File "test.py", line xx, in <module>
        #     object.method('arg1', 'arg2', kwarg1=1, kwarg2=2)
        #     File "/opt/qrnote/lib/errorhandler/trywrappers.py", line 218, in wrapped
        #     stack()
        #     TypeError: 'NoneType' object is not iterable
    
#         return args, kwargs, True
        return args, kwargs, str(sys._getframe().f_code.co_name)

    def ConfigFileNotFound(callobj, args, kwargs, e):
        # Create custom message to BE SENT TO THE LOGGER
        message = ("".join(["The configuration file was not found. ", 
                            "Please verify the file exists in the ", 
                            "appropriate path and is readable."]))    
        # Sends the message and original error to the LOGGER
        # Remove this line if you don't want an error displayed
        _log_error(message, e)
        ### METHOD ACTIONS
        # CODE BELOW TO CORRECT ISSUE
        # All code acts on the self object
        raise FatalException()

    def ConfigFileNoOption(callobj, args, kwargs, e):
        # Create custom message to BE SENT TO THE LOGGER
        message = ("".join(["Unable to find the specified section or option", 
                            "(variable) in config file. ", 
                            "Please verify the contents of the file. "]))    
        # Sends the message and original error to the LOGGER
        # Remove this line if you don't want an error displayed
        _log_error(message, e)
        ### METHOD ACTIONS
        # CODE BELOW TO CORRECT ISSUE
        # All code acts on the self object
        return args, kwargs, None
        
    def ConfigFileParseError(callobj, args, kwargs, e):
        # Create custom message to BE SENT TO THE LOGGER
        message = ("".join(["The configuration file contains errors. ", 
                            "Please verify the contents of the file. "]))    
        # Sends the message and original error to the LOGGER
        # Remove this line if you don't want an error displayed
        _log_error(message, e)
        ### METHOD ACTIONS
        # CODE BELOW TO CORRECT ISSUE
        # All code acts on the self object
        raise FatalException()
    
    def PassThroughException(callobj, args, kwargs, e):
        # Custom message to BE SENT TO THE LOGGER
        message = ("")
        # Sends the message and original error to the LOGGER
        _log_error(message, e)
        ### METHOD ACTIONS
        return args, kwargs, None
        
    def PathDoesNotExist(callobj, args, kwargs, e):
        # Custom message to BE SENT TO THE LOGGER
        message = ''.join(["The path passed does not exist, ", 
                           "or 'path = <value>' was not set ", 
                           "when calling method. "])

        # Sends the message and original error to the LOGGER
        _log_error(message, e)

        ### METHOD ACTIONS
        result = False
        
        # Here a dialogue box could be raised to get the corrected path
        # The return gor to the tryhandler, which will try and run the original
        # calling method again with the original variable names...so it's 
        # important the callobj.variable is changed before returning.The 
        # callobj does not have to be returned. It is modified in place. 
        # Just the modified kwargs needs to be changed. 
#         kwargs["path"] = raw_input("enter a correct path...")
#         if <successful>: result = True
    
        return args, kwargs, result

    def RserveReturningGarbage(callobj, args, kwargs, e):
        # Custom message to BE SENT TO THE LOGGER
        message = ''.join(["The path passed does not exist, ", 
                           "or 'path = <value>' was not set ", 
                           "when calling method. "])

        # Sends the message and original error to the LOGGER
        _log_error(message, e)

        ### METHOD ACTIONS
        return args, kwargs, None
    
    def RScriptFileDoesNotExist(callobj, args, kwargs, e):
        # Custom message to BE SENT TO THE LOGGER
        message = ''.join([
                           "The file name passed does not exist, ", 
                           "or was otherwise invalid. "
                           ])

        # Sends the message and original error to the LOGGER
        _log_error(message, e)

        ### METHOD ACTIONS
        # Eventually, place a popup here asking to clarify the filepath name
        # and location. However, for now, returning anything else would lead
        # to corrupted mathematical data...so this is a fatal error. 
        raise FatalException(e)
    
    def RserveNotRunning(callobj, args, kwargs, e):
        """"""
        # Custom message to BE SENT TO THE LOGGER
        message = ''.join(["Rserve may not be running."])
        # Sends the message and original error to the LOGGER
        _log_error(message, e)

        ### METHOD ACTIONS
        log.error('Attempting to restart Rserve environment...')
        PEM  = "/Users/mikes/Documents/Work/BioComSoftware/Jobs/2014-10-10-Tesera/Tesera.pem"
        USER = "ec2-user"
        PORT = '22'
        SERVER = str(callobj.rhandler_host)
        command = ['/sbin/service', 'Rserve', 'restart']
#         command = ['R', 'CMD', 'Rserve', '--vanilla']
#         command = ['ls']
        
        ssh = ['ssh', '-i', PEM, '-p', PORT, USER + '@' + SERVER]
        run = ssh + command
        
        proc = subprocess.Popen(run, shell=False, 
#                                 stdout=subprocess.PIPE) 
        stdin=None, stdout=None, stderr=None, close_fds=True)

        result = proc.communicate()[0]
        
        return args, kwargs, None
         
    def FileDoesNotExist(callobj, args, kwargs, e):
        # Custom message to BE SENT TO THE LOGGER
        message = ("The file passed does not exist. ")
        # Sends the message and original error to the LOGGER
        _log_error(message, e)
        ### METHOD ACTIONS
        result = False
        
        # Here a dialogue box could be raised to get the corrected path
        # The return gor to the tryhandler, which will try and run the original
        # calling method again with the original variable names...so it's 
        # important the callobj.variable is changed before returning.The 
        # callobj does not have to be returned. It is modified in place. 
        # Just the modified kwargs needs to be changed. 
#         kwargs["file"] = raw_input("enter a correct path...")
#         if <successful>: result = True
    
        return args, kwargs, result
        
    def FatalError(callobj, args, kwargs, e):
        # Custom message to BE SENT TO THE LOGGER
        message = ("")
        # Sends the message and original error to the LOGGER
        _log_error(message, e)
        ### METHOD ACTIONS
        raise FatalException(e)
    
    @classmethod
    def UnknownException(callobj, args, kwargs, e):
        # Custom message to BE SENT TO THE LOGGER
        message = ("".join(["An unidentified exception was passed. ", 
                            "'errorhandler' does not know what to do. ", 
                            "Calling fatal exception and halting. "]))
        # Sends the message and original error to the LOGGER
    #     _log_error(message, e)
        ### METHOD ACTIONS
        raise FatalException(e) # Does not return    
