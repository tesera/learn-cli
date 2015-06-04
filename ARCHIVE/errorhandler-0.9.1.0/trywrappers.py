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


import functools

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

def handlertry(msg, tries = 1):
    """
    :NAME:
        handlertry(msg)
        
    :DESCRIPTION:
        handlertry is a decorator which functions to customize the try/except
        paradigm in Python. The "msg" parameter must contain a "signal phrase" 
        which will be passed to the ErrorHandler class to determine additional 
        processing in an attempt to correct the error. If the error cannot be 
        corrected, the calling sofwtare can be cleanly closed in a controlled 
        manne.
        
    :ARGUMENTS:
        msg:    A string which is added to the raised error message.
                This string shoudl contain a "trigger message" to allow  
                handlertry to drop control to a pre-defined routin to either 
                correct the error or prep the package for controlled shutdown 
        
    :RETURNS:
        Nothing.
        
    :USAGE:
        @handlertry(''.join(["InvalidFileName:", 
                             "Error when attempting to open ", 
                             str(invalidfilename)])
        FH = open("invalidfilename, "r+", 0)

        ------------------------
        The above results in ...
        ------------------------

    1. Attempting to run the line of code 'FH = open("invalidfilename, "r+", 0)'

    2. Upon failure, control is passed to errorhandler.ErrorHandler()

    3. Based on the "InvalidFileName" in the message, control is passed to the
       InvalidFileName handler method. 

    4a.If the InvalidFileName handler can correct the issue, control is passed 
       back to the calling script, at the line BELOW the original code that 
       caused the error and code continues to run.
       
    4b.If the InvalidFileName handler CANNOT correct the issue, control is 
       passed to closure methods OR the original error is raised. 
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
            handler = CustomErrorHandler.err()

            cls = str(self.__class__.__name__)
            module = func.__name__

            success = False
            tally = 1
            while ((success is False) and (tally <= tries)): 
#                 print args #333
#                 print kwargs #333


                try:
                    result = func(self, *args, **kwargs)
                    success = True
    
                except Exception as err:
                    err = _dress_msg(cls, module, msg, err, args, kwargs)
                    args, kwargs, result = handler(self, 
                                     args, 
                                     kwargs, 
                                     err, 
                                     getmembers(self), 
                                     stack())
                    tally += 1
                    
            return result
            
        return wrapped

    return concrete_decorator          

def _dress_msg(cls, module, msg, err, args, kwargs):
   if not err.args: 
       err.args=('',)
   
   if len(args) == 0:      
       args = None

   if len(kwargs) == 0:    
       kw = None
   else:
       kw = ""
       for key in kwargs.keys():
           kw = kw + "'" + str(key) + ":" + str(kwargs[key]) + "', "
       kw = kw[:len(kw)-2]
                    
   err.args = (
               (cls + "." + module + ": " + msg + 
                "*args: " + str(args) + 
                "; **kwargs: " + str(kw) + "; " + 
                err.args[0],
                ) + 
               err.args[1:]
               )
   return err


if __name__ == "__main__":
    print "no test"