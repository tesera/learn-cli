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

import functools
# from errorhandler import ErrorHandler

def raisetry(msg):
    """
    :NAME:
        raisetry(msg)
        
    :DESCRIPTION:
        raisetry is a decorator which functions to customize the try/except
        paradigm in Python by attaching the parameter "msg" to the raised 
        exception.
        
    :ARGUMENTS:
        msg:    A string which is added to the raised error message.
        
    :RETURNS:
        Raises an exception
        
    :USAGE:
        @raisetry("Class.method: Attempting to open " + str(invalidfilename))
        FH = open("invalidfilename, "r+", 0)

        ---------------------
        The above replaces...
        ---------------------
        
        msg = "Class.method: Attempting to open " + str(invalidfilename)
        try:
            FH = open("invalidfilename, "r+", 0)

        except Exception as err:
            if not err.args: 
                err.args=('',)
            
            err.args = (
                (cls + "." + module + ": " + msg + ". " + err.args[0],) + 
                        err.args[1:]
                        )
            raise
    """    
    def concrete_decorator(func):

        @functools.wraps(func)
        def wrapped(self, *args, **kwargs):

            cls = str(self.__class__.__name__)
            module = func.__name__

            try:
                result = func(self, *args, **kwargs)
                return result
                            
            except Exception as err:
                err = _dress_msg(cls, module, msg, err, args, kwargs)
                raise
        
        return wrapped

    return concrete_decorator      

def handlertry(msg = "", tries = 1):
    """
    :NAME:
        handlertry([msg, tries = n])
        
    :DESCRIPTION:
        handlertry is a decorator which customizes the try/except
        paradigm in Python. The "msg" parameter is optional and contains a 
        "human readable signal phrase" which is passed to the 
        ErrorHandler.customErr method. 'msg' can also be omitted and the "signal
        phrase" can be included in the error message itself. 
         
        The customErr method in turn uses the phrase to send control to the 
        appropriate ErrorHandler.<handler_method>.  
        
        The ErrorHandler.<handler_method> determines the additional (if any) 
        processing to be used in an attempt to correct the problem that raised 
        the error. 
        
        The "tries" parameter determine how many time the original function 
        (that generated the error) will be retried in the attempt to resolve the
        original error. 
        
        I.e.
        
        1. originalclass.originalmethod is passed to handlertry with "tries = 3"
        
        2. originalmethod is tried, but raises an error (this is try one)
        
        3. Error passed to ErrorHandler.customErr
        
        4. ErrorHandler.customErr tries to fix the problem, and passes control 
           back to handlertry.
        
        5. Handlertry tries to run originalmethod again, errors again (I.e. fix 
           did not work)
        
        6. ErrorHandler.customErr tries to fix the problem again (try 2). Got to 
           step 5 again. If the method works this time, control is returned back 
           to originalclass.originalmethod AT THE LINE FOLLOWING THE END OF 
           originalmethod. 
        
        7. If it fails, Repeat 5 & 6 (try 3)
        
        8. Regardless of whether the issue was fixed or not, since try 3 was 
           the last try control is returned back to originalclass.originalmethod 
           AT THE LINE FOLLOWING THE END OF originalmethod.    
        
    :ARGUMENTS:
        msg:    A string which is added to the raised error message.
                This string should contain a "trigger message" to allow  
                handlertry to drop control to a pre-defined routine to either 
                correct the error or prep the package for controlled shutdown.
                
                If the msg is "", ErrorHandler.UnknownException is used. 
                
        tries:  The number of times to attempt to run the decorated function. 
                
                If the decorated function SUCCEEDS, tries stop and control is 
                returned to the original calling script. 
                
                If the decorated  method FAILS, control is passed to the 
                ErrorHandler class which attempts to fix the problem, and 
                re-runs the decorated function.    
                
                When the number of "tries" is exhausted, control is returned to 
                the original calling script, REGARDLESS of whether the issue was 
                fixed or not.  
                
                Control is always returned to THE LINE FOLLOWING THE NORMAL 
                RETURN OF THE DECORATED METHOD.
                
                DEFAULTS TO: 1
        
    :RETURNS:
        handlertry returns three arguments: the original args passed to 
        handlertry, including any modifications made by ErrorHandler; the 
        original kwargs passed to handlertry, including any modifications made 
        by ErrorHandler; and a "result" which can be anything. The 'result'
        return is simply passed back from handlertry to the decorated function.   
        
    :USAGE:
        @handlertry(''.join(["InvalidFileName:", 
                             "Error when attempting to open ", 
                             str(invalidfilename)]), 
                             tries = 2)
        FH = open("invalidfilename, "r+", 0)

        ------------------------
        The above results in ...
        ------------------------

    1. Attempting to run the line of code 'FH = open("invalidfilename, "r+", 0)'

    2. Upon failure, control is passed to ErrorHandler.customErr()

    3. Based on the "InvalidFileName" in the message, control is passed to
       ErrorHandler.InvalidFileName(). 

    4a.If the InvalidFileName handler can correct the issue, control is passed 
       back to the calling script, at the line FOLLOWING the completion of the 
       originally decorated method and code continues to run.
       
    4b.If the InvalidFileName handler CANNOT correct the issue, it can continue 
       to try and fix the issue, and re-run the decorated method, for "tries" 
       number of attempts...until success or control is passed back to the line 
       following the decorated method.  
    """    
    
    def concrete_decorator(func):

        @functools.wraps(func)
        def wrapped(self, *args, **kwargs):

            #----------------------------------------------------------------
            # In this def, 'self' refers to the object that called handlertry
            #----------------------------------------------------------------
            
            import errorhandler
            from inspect import getmembers, stack
            CustomErrorHandler = errorhandler.ErrorHandler()
#             handler = CustomErrorHandler.err()

            cls = str(self.__class__.__name__)
            module = func.__name__

            success = False
            tally = 1
            while ((success is False) and (tally <= tries)):

                try:
                    result = func(self, *args, **kwargs)
                    success = True
    
                except Exception as err:
                    e = _dress_msg(cls, module, msg, err, args, kwargs)
                    args, kwargs, result = CustomErrorHandler.customErr(
                                                self, 
                                                args, 
                                                kwargs, 
                                                e,
                                                getmembers(self), 
                                                stack()
                                                                        )
                    tally += 1
                    
            return result
            
        return wrapped

    return concrete_decorator          

def _dress_msg(cls, module, msg, err, args, kwargs):
    try:
        err = str(err.args[0])
    except Exception, e:
        err = str(err)

# This worked before, but not on the PI        
#     if not err.args: 
#         err.args=('',)
    
    if len(args) == 0:      
        args = None
    
    if len(kwargs) == 0:    
        kw = None
    else:
        kw = ""
        for key in kwargs.keys():
            kw = kw + "'" + str(key) + ":" + str(kwargs[key]) + "', "
        kw = kw[:len(kw) - 2]

# This worked before, but not on the PI        
#     err.args = (
#                 (cls + "." + module + ": " + msg + 
#                  "*args: " + str(args) + 
#                  "; **kwargs: " + str(kw) + "; " + 
#                  err.args[0],
#                  ) + 
#                 err.args[1:]
#                 )
    err = ''.join([cls, ".", module,": ", 
                   msg, 
                   "; *args: ", 
                   str(args) + 
                   "; **kwargs: ", 
                   str(kw), 
                   "; ", 
                   err
                   ]) 

    return err


if __name__ == "__main__":
    print "no test"