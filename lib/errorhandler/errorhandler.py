#!/usr/bin/python

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


from loghandler import log
from handlers import Handlers
import inspect
# import functools
# import handlers 
import re
import subprocess
import sys
import types

        
class ErrorHandler(object):
    """
    class_obj = ErrorHandler()
    
    DESCRIPTION:
        errorhandler is a class to control, and attempt to fix, exceptions 
        generated in scripts. 
    
        ErrorHandler should NEVER be called or included within a user script. 
        This class is called ESXCLUSIVELY by the trywrappers.handlertry
        decorator.  
    
    USAGE:
        <myclass>
            @handlertry("TriggerMessage: ", tries = 2)
            def myMethod(self, args, kwargs):
                FH = open(filename, "w+", 0)
                return FH
            
            Some code here
            Some more code here
            FH = self.myMethod("Non_Existent_Filename")
            After ErrorHandler attempts fix, control returns here regardless 

    METHODS:
        customErr(e, source, frame)
            e = The MODIFIED string passed out from the exception. Normal usage
                dictates the string be pre-pended with the name of the error
                handling method (see above). 
            
            source = The 'getmembers(self)' call found in the self.err call above
            
            frame = The 'stack()' call found in the self.err call above
            
        err(e, source, frame)
            Simply a smaller pointer to customErr()
            
        None of these methods are intended or recommended to be user callable.  
    """

    def __init__(self): #, log):
        pass

    def err(self):
        def _err(callobj, args, kwargs, e, source, frame):
            return self.customErr(callobj, args, kwargs, e, source, frame)
        return _err
            
    def customErr(self, callobj, args, kwargs, e, source, frame):
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
            _log_error(self, message, e)
                     
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
#         import handlers 
        #333

        # This calls the proper handler method from 'handlers'
        # NOTE: The error keyword MUST MATCH THE METHOD NAME
        # NOTE: A string search is used to match the method name to contents 
        #       of the error string passed in.
        #       THIS MEANS if you have two methods, 'ERR1' AND 'ERR10', 'ERR1'
        #       will always be the one found...SO IT IS RECOMMENDED YOU NAME
        #       THE METHODS VERY UNIQUELY AND CAREFULLY.
        #       I.e. 'StringNotFoundInLogError' 
        for key in Handlers.__dict__.keys():
            if (str(key).lower() in str(e).lower()):
                return Handlers.__dict__[key](callobj, args, kwargs, e)
        return Handlers.UnknownException(callobj, args, kwargs, e)
        
        
        