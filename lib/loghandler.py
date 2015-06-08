##############################################################################
# Removal of the "__license__" line or content from  "__license__", or removal 
# of "__author__" in this or any constituent # component or file constitutes a 
# violation of the licensing and copyright agreement. 
# from cgi import logfile
# NOTES:

from cgi import logfile
from __builtin__ import True
__author__      = "Mike Rightmire"
__copyright__   = "BioCom Software"
__license__     = "Tesera"
__license_file__= "Clause1.PERPETUAL_AND_UNLIMITED_LICENSING_TO_THE_CLIENT.py"
__version__     = "0.9.5.0"
__maintainer__  = "Mike Rightmire"
__email__       = "Mike.Rightmire@BiocomSoftware.com"
__status__      = "Development"
##############################################################################

"""
LogHandler IS USED BY BOTH ConfigHandler and ErrorHandler. 
AS SUCH, NEITHER CAN BE IMPLEMENTED IN THESE CLASSES WITHOUT WREAKING HAVOC 
"""
from checks  import checkPathFormat
from checks  import directoryExists
from checks  import fileExists
from inspect import stack 

import datetime
import time
import inspect
import logging
import os
import re
import sys


class log(object):
    """
    :NAME:
    loghanlder.log('message', [KW-params])

    :DESCRIPTION:
    'log' is an interface and controller for the Python module 'logging'. It 
    functions using the same basic interface as the 'logging', but handles the 
    instantiation and management blindly in the backend.

    from loghandler import log
    
    log.info( "I automatically instantiate the logging object.", 
              app_name   = "MyApplication", 
              logfile    = "./MyApplication.log",
              log_level  = 10,
              screendump = True,
              formatter  = '%(asctime)s-%(name)s-%(levelname)s-%(message)s',
              create_paths = True
             )  
                 
    log.critical('message')
    log.error('message')
    log.warning('message')
    log.info('message')
    log.debug('message')

    log.debug("I alter the existing logging object's parameters.", 
              app_name   = "MyApp", 
              logfile    = "./DiffLogName.log",
             )  
   

    :ARGUMENTS:
    app_name:     The friendly name of the application actually instantiating a log 
                  object. This is the name used to create a python "logging.logger"
                  instance, and the name that will appear next to the data in 
                  the log file to identify what application generated the log 
                  information.
               
                  MANDATORY: No default at this time, however does not need to 
                          be set if the setLogger object exists and is called by 
                          a child script or process. 
               
               
                  DEFAULTS TO: loghandler
                  
    screendump:   If True, all lines dumped to the logfile will also 
                  appear on the screen (stderr).
                  
                  DEFAULTS TO: False
                 
    formatter:    A string which is passed TO the Python logging 
                  formatter object.
                  
                  DEFAULTS TO: 
                  '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                 
    create_paths: If True, an attempt to change the logfile to a 
                  directory/fle path that does not exist will cause 
                  the loghandler object to silently create the path and 
                  filename.
                  
                  DEFAULTS TO: True
                   
    logfile:      The FUL PATH (fully qualified path and fielname) where
                  log data will be written to disk. If a file name only 
                  is given, the existing path of the calling applicaiton 
                  is used AFTER being converted to the fully qualified 
                  path.
                  
                  DEFAULTS TO: ./loghandler.log  
                                 
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
               
    :METHODS:
    None.
        
    :RETURNS:
    Nothing. 'log' is never instantiated as an object, and will error if the 
    attempt is made.     
    
    :USAGE:
    'log' is imported and used directly via @classmethods.
     
    Anytime parameters are passed in addition to the message to be logged, 
    these parameters are used to instantiate or change the object behind 
    the scenes.

    from loghandler import log
    
    var = 1
    
    log.info( "I instantiate the logging object", 
              app_name   = "MyApplication", 
              logfile    = "./MyApplication.log",
              log_level  = 10,
              screendump = True,
             )            
      
    log.info("var was set to " + str(var))
    
    log.info( "I change the app name.", 
              app_name   = "MyApp", 
             )            
    
    (MyApp.log)
    2014-12-23 15:35:42,510 - MyApplication - INFO - I instantiate the logging object
    2014-12-23 15:35:42,511 - MyApplication - INFO - var was set to 1
    2014-12-23 15:35:43,000 - MyApp - INFO - I change the app name.

    """
    
    @classmethod
    def _setLogger(self, *args, **kwargs):
        """
        This determines if a logging singleton has been created, if not it
        creates one...and then returns the (possibly modified) kwargs 
        for use by the Python logger call. 
        """
        # Regardless of instance status, kwargs still needs to be stripped of 
        # the loghandler keywords.  
        app_name = kwargs.pop('app_name', None)
        logfile = kwargs.pop('logfile', None)
        log_level = kwargs.pop('log_level', None)
        screendump = kwargs.pop('screendump', None)
        formatter = kwargs.pop('formatter', None)
        create_paths = kwargs.pop('create_paths', None)
        
#         try: print ' app_name=', app_name
#         except: print 'no app_name'#:True,   None:True}.get(app_name))   and 
#         try: print 'logfile=', logfile #:True,    None:True}.get(logfile))    and
#         except:  print 'no logfile'#:True,   None:True}.get(app_name))   and 
# #         try: print 'log_path = ', log_path#:True,   None:True}.get(log_path))   and
# #         except:  print 'no log_path'#:True,   None:True}.get(app_name))   and 
#         try: print 'log_level=', log_level#:True,  None:True}.get(log_level))  and
#         except:  print 'no log_level'#:True,   None:True}.get(app_name))   and 
#         try: print 'formatter=', formatter#:True,  None:True}.get(format))  and
#         except:  print 'no formatter'#:True,   None:True}.get(app_name))   and 
#         try: print 'screendump=', screendump#:True, None:True}.get(screendump))
#         except:  print 'no screendump'#:True,   None:True}.get(app_name))   and 
        

#         # Now that the loghandler keywords have been stripped out of kwargs, 
#         # see if singleton instance exists by calling
#         # setlogger with no params and checking for instance
#         # if one exists, just set it and we're done
#         logger = SetLogger(instantiate = False)
#         if logger is not None: return logger, kwargs
             
        # Otherwise, create a new instance with the set parameters from kwargs, 
        # or the defaults if a parameter is None
        # Pass KWARGS (only) to make a logging instance
        # Be sure instantiate is sent as True
        logger = SetLogger(                
                            app_name     = app_name, 
                            logfile      = logfile,
                            log_level    = log_level, 
                            screendump   = screendump, 
                            formatter    = formatter,
                            create_paths = create_paths, 
                            instantiate  = True # MUST BE TRUE
                            )
        

#         if logfile is not None:
#             logger.logfile(logfile) 
            
        
                
        return logger, kwargs

    # LOGGING OVERRIDES========================================================    

    @classmethod
    def critical(self,message, *args, **kwargs):
        """"""
        logger, kwargs = log._setLogger(*args, **kwargs)
        return logger.critical(message, *args, **kwargs)               
  
    @classmethod
    def error(self,message, *args, **kwargs):
        """"""
        logger, kwargs = log._setLogger(*args, **kwargs)
        return logger.error(message, *args, **kwargs)               
      
    @classmethod
    def warning(self,message, *args, **kwargs):
        """"""
        logger, kwargs = log._setLogger(*args, **kwargs)
        return logger.warning(message, *args, **kwargs)               
      
    @classmethod
    def info(self,message, *args, **kwargs):
        """"""
        logger, kwargs = log._setLogger(*args, **kwargs)
        return logger.info(message, *args, **kwargs)               

    @classmethod
    def debug(self,message, *args, **kwargs):
        """"""
        #####
        # Use these later to improve formatting
        # Allowing different caller files to be listd in the log line
#         curframe = inspect.currentframe()
#         calframe = inspect.getouterframes(curframe, 2)
#         print 'caller name:', calframe[1][1]
        logger, kwargs = log._setLogger(*args, **kwargs)         
        return logger.debug(message, *args, **kwargs)               

#     @property
#     def logfile(self):
#         print 'In property logfile'#333
#         logger, kwargs = log._setLogger()
#         return logger.logfile
#     
#     @logfile.setter
#     def logfile(self, value):
#         print 'In property logfile.setter'#333
#         logger, kwargs = log._setLogger()
#         logger._change_logfile(value)
        
    
class SetLogger(object):
    """
    :NAME:
    SetLogger( app_name, 
               [logfile, 
                log_level, 
                screendump, 
                create_paths]) 

    :DESCRIPTION:
    setLogger is a log object manager intended to handle the details of 
    creating and altering a logger. 
    
    The setLogger class is a singleton, meaning once an object is created by a 
    calling script, all CHILD SCRIPTS attempting to instantiate a setLogger 
    object will - in actuality - receive the existing object. 
    
    The advantage of this is that each object, function or 
    child process of the original script can simply call setLogger once and 
    in-the-blind to continue logging appropriately.
    
    SetLogger IS ONLY INTENDED TO BE CALLED BY THE ABOVE 'log' class.   
     
    :ARGUMENTS:
    app_name:     The friendly name of the application actually instantiating a log 
                  object. This is the name used to create a python "logging.logger"
                  instance, and the name that will appear next to the data in 
                  the log file to identify what application generated the log 
                  information.
               
                  MANDATORY: No default at this time, however does not need to 
                          be set if the setLogger object exists and is called by 
                          a child script or process. 
               
               
                  DEFAULTS TO: loghandler
                  
    screendump:   If True, all lines dumped to the logfile will also 
                  appear on the screen (stderr).
                  
                  DEFAULTS TO: False
                 
    formatter:    A string which is passed TO the Python logging 
                  formatter object.
                  
                  DEFAULTS TO: 
                  '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                 
    create_paths: If True, an attempt to change the logfile to a 
                  directory/fle path that does not exist will cause 
                  the loghandler object to silently create the path and 
                  filename.
                  
                  DEFAULTS TO: True
                   
    logfile:      The FUL PATH (fully qualified path and fielname) where
                  log data will be written to disk. If a file name only 
                  is given, the existing path of the calling applicaiton 
                  is used AFTER being converted to the fully qualified 
                  path.
                  
                  DEFAULTS TO: ./loghandler.log  
                                 
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
               
    instantiate: Used noly by the 'log' class above. A call to SetLogger with 
                 instantiate=False means either the existing SetLogger object 
                 OR NONE will be returned. This is intended to test for the 
                 existance of an object. 
                 
                 DEFAULTS TO: True
                   
    :METHODS:
        :Name: 
            change(param, value) 
        :Description: 
            Alters the loghandler object's persistent parameters including:
                app_name
                log_level    
                screendump
                formatter
                create_paths
                logfile

            These changes are made in the existing, singleton object and IS 
            USED BY THE INTERNAL WORKINGS OF LOGHANDLER AND CONFIGHANDLER to 
            instantiate and modify itself. Any chenges made here should oly 
            be completed with an understanding of the impact it may have on 
            the larger, supported methods. 
        :Parameters:
            param:    The actual, inflexible variable name used internally by
                      the loghanlder class.
                      
            value:    The new value to be assigned to param.     

        :Name: 
            screendump()
        :Description: 
            Will dump the contents of the current logfile to STD_OUT.
        :Parameters:
            None
        
        :Name: 
            purge()
        :Description: 
            Will erase the contents of the existing logfile, with a post-erase 
            marker to identify that an erase has been performed. 
        :Parameters:
            None
    
    :RETURNS:
        None. Used as classmethods. 
    
    :USAGE:
        The loghandler.SetLogger  object is used ONLY by the 'log' class above. 
        logger = SetLogger(                
                            app_name     = app_name, 
                            logfile      = logfile,
                            log_level    = log_level, 
                            screendump   = screendump, 
                            formatter    = formatter,
                            create_paths = create_paths, 
                            instantiate  = True # MUST BE TRUE to create object
                           )
        
        def childMethod(self, var = None):
            log.info("I will log to the same file as ParentClass objects.")
            log.info("var was set to " + str(var))
            log.debug("I will only log if PARAM "log_level" was "DEBUG")

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
                app_name     = None, # DO NOT CHANGE FROM None
                logfile      = None, # DO NOT CHANGE FROM None
                log_level    = None, # DO NOT CHANGE FROM None 
                screendump   = None, # DO NOT CHANGE FROM None 
                formatter    = None, # DO NOT CHANGE FROM None
                create_paths = None, # DO NOT CHANGE FROM None 
                instantiate  = True # DO NOT CHANGE FROM True
                ):
        """
        This is a singleton class. 
         
        The __new__ method is called prior to instantiation with __init__. 
        If there's already an instance of the class, the existing object is 
        returned. If it doesn't exist, a new object is instantiated with 
        the __init__.
        """

#         try: print ' app_name=', app_name
#         except: print 'no app_name'#:True,   None:True}.get(app_name))   and 
#         try: print 'logfile=', logfile #:True,    None:True}.get(logfile))    and
#         except:  print 'no logfile'#:True,   None:True}.get(app_name))   and 
#         try: print 'log_level=', log_level#:True,  None:True}.get(log_level))  and
#         except:  print 'no log_level'#:True,   None:True}.get(app_name))   and 
#         try: print 'formatter=', formatter#:True,  None:True}.get(format))  and
#         except:  print 'no formatter'#:True,   None:True}.get(app_name))   and 
#         try: print 'screendump=', screendump#:True, None:True}.get(screendump))
#         except:  print 'no screendump'#:True,   None:True}.get(app_name))   and 


        # __init__ is called no matter what, so...
        # If there is NOT an instance, just create an instance 
        # This WILL run __init__
        # Do NOT set self.__exists here, since if _-exists == True, __init__ is 
        # cancelled (it must still run at the first instantiation)
        if not hasattr(cls, 'instance'):
            if instantiate: 
                cls.instance = super(SetLogger, cls).__new__(cls)
                return cls.instance
            else:
                return None
 
        # Else if an instance does exist, set a flag since
        # __init__is called, but flag halts completion (just returns)           
        else:
            cls.instance.__exists = True
            return cls.instance
        
    def __init__(self, 
                app_name     = None, # DO NOT CHANGE FROM None 
                logfile      = None, # DO NOT CHANGE FROM None
                log_level    = None, # DO NOT CHANGE FROM None 
                screendump   = None, # DO NOT CHANGE FROM None 
                formatter    = None, # DO NOT CHANGE FROM None
                create_paths = None, # DO NOT CHANGE FROM None 
                instantiate  = None, # DO NOT CHANGE FROM None
                ):

#         try: print ' app_name=', app_name
#         except: print 'no app_name'#:True,   None:True}.get(app_name))   and 
#         try: print 'logfile=', logfile #:True,    None:True}.get(logfile))    and
#         except:  print 'no logfile'#:True,   None:True}.get(app_name))   and 
#         try: print 'log_level=', log_level#:True,  None:True}.get(log_level))  and
#         except:  print 'no log_level'#:True,   None:True}.get(app_name))   and 
#         try: print 'formatter=', formatter#:True,  None:True}.get(format))  and
#         except:  print 'no formatter'#:True,   None:True}.get(app_name))   and 
#         try: print 'screendump=', screendump#:True, None:True}.get(screendump))
#         except:  print 'no screendump'#:True,   None:True}.get(app_name))   and 
#         try: print 'create_paths=', create_paths
#         except: print 'no create_paths'#:True,   None:True}.get(app_name))   and 
# 
#         try: print ' self.app_name=', self.app_name
#         except: print 'no self.app_name'#:True,   None:True}.get(app_name))   and 
#         try: print 'self.logfile=', self.logfile #:True,    None:True}.get(logfile))    and
#         except:  print 'no self.logfile'#:True,   None:True}.get(app_name))   and 
#         try: print 'self.log_level=', self.log_level#:True,  None:True}.get(log_level))  and
#         except:  print 'no self.log_level'#:True,   None:True}.get(app_name))   and 
#         try: print 'self.formatter=', self.formatter#:True,  None:True}.get(format))  and
#         except:  print 'no self.formatter'#:True,   None:True}.get(app_name))   and 
#         try: print 'self.screendump=', self.screendump#:True, None:True}.get(screendump))
#         except:  print 'no self.screendump'#:True,   None:True}.get(app_name))   and 
#         
                
        if self.__exists:
            # Changes need to come in a certain order
            # so change_list MUST be a list, to preserve this order. 
            change_list = []
            if ((app_name is not None) and (app_name != self.app_name)):
                change_list.append({'app_name':app_name})
            
            if ((log_level != None) and (log_level != self.log_level)):
                change_list.append({'log_level':log_level})

            if ((screendump != None) and (screendump != self.screendump)):
                change_list.append({'screendump':screendump})

            if ((formatter != None) and (formatter != self.formatter)):
                change_list.append({'formatter':formatter})

            if ((create_paths != None) and (create_paths != self.create_paths)):
                change_list.append({'create_paths':create_paths})

            if ((logfile != None) and (logfile != self.logfile)):
                change_list.append({'logfile':logfile})

            for change in change_list:
                for param in change.keys():
                    self.change(param, change[param])

            return # Leave __init__ as singleton has been returned

        self.app_name_default     = 'loghandler', 
        self.logfile_default      = './loghandler.log'
        self.log_level_default    = 40
        self.screendump_default   = False 
        self.formatter_default    = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        self.create_paths_default = True 
        self.instantiate_default  = True
                
        self.create_paths = self._check_create_paths(create_paths)
        self.app_name   = self._check_app_name(app_name)
        self.log_level  = self._check_log_level(log_level)
        self.formatter  = self._check_formatter(formatter)
        self.screendump = self._check_screendump(screendump)
        self.logfile    = self._check_logfile(logfile)

#         try: print ' self.app_name=', self.app_name
#         except: print 'no self.app_name'#:True,   None:True}.get(app_name))   and 
#         try: print 'self.logfile=', self.logfile #:True,    None:True}.get(logfile))    and
#         except:  print 'no self.logfile'#:True,   None:True}.get(app_name))   and 
#         try: print 'self.log_level=', self.log_level#:True,  None:True}.get(log_level))  and
#         except:  print 'no self.log_level'#:True,   None:True}.get(app_name))   and 
#         try: print 'self.formatter=', self.formatter#:True,  None:True}.get(format))  and
#         except:  print 'no self.formatter'#:True,   None:True}.get(app_name))   and 
#         try: print 'self.screendump=', self.screendump#:True, None:True}.get(screendump))
#         except:  print 'no self.screendump'#:True,   None:True}.get(app_name))   and 
        
        self.handlers = [] #333 maybe dont need this

        # Start the log
        self._set_logger()

    ##################################################################3333
    ### fix this at some point to work for all OSs ###################3333

    def _getSyslog(self): 
        # For now cheat and just give the PI syslog
        return '/var/log/messages'

    def critical(self, message, *args, **kwargs): # OVERRIDES_________________
        return self.logger.critical(message, *args, **kwargs)
  
    def error(self, message, *args, **kwargs):
        return self.logger.error(message, *args, **kwargs)
      
    def warning(self, message, *args, **kwargs):
        return self.logger.warning(message, *args, **kwargs)
      
    def info(self, message, *args, **kwargs):
        return self.logger.info(message, *args, **kwargs)
      
    def debug(self, message, *args, **kwargs):
        return self.logger.debug(message, *args, **kwargs)                

    #__________________________________________________________________________
    # PUBLIC METHODS            

    def delete(self, app_name):# PUBLIC METHODS_______________________________
        """"""
        raise NotImplementedError
#         self._remove_logger(app_name)
        
    def formatter(self, format):
        """
        NOT YET IMPLEMENTED
        Intended to change the log formatting of the existing handlers
        """
        raise NotImplementedError
 
    def level(self, level = 40):
        """
        NOT YET IMPLEMENTED
        Intended to change the logging level of the existing handlers
        """
        raise NotImplementedError

    def change(self, param, value):
        """
        :NAME:
            loghandler.change(param, value)
        :DESCRIPTION:
            change() alters the loghandler object's persistent parameters 
            including:
                app_name
                log_level    
                screendump
                formatter
                create_paths
                logfile
        
            These changes are made in the existing, singleton object and IS 
            USED BY THE INTERNAL WORKINGS OF LOGHANDLER AND CONFIGHANDLER to 
            instantiate and modify itself. Any chenges made here should oly 
            be completed with an understanding of the impact it may have on 
            the larger, supported methods. 
            
        :ARGUMENTS:
            param:    The actual, inflexible variable name used internally by
                      the loghanlder class.
                      
            value:    The new value to be assigned to param. 
            
        :VARIABLES:
            app_name:     The application which is making calls to the instant
                          -iated loghanlder object. This ppears in the logging
                          lines which are dumped to the logfile and screendump.
                         
                          DEFAULTS TO: loghandler
                          
            log_level:    The logging level (see the Python 'logging' man pages.
            
                          DEFAULTS TO: 40
                          
            screendump:   If True, all lines dumped to the logfile will also 
                          appear on the screen (stderr).
                          
                          DEFAULTS TO: False
                         
            formatter:    A string which is passed TO the Python logging 
                          formatter object.
                          
                          DEFAULTS TO: 
                          '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                         
            create_paths: If True, an attempt to change the logfile to a 
                          directory/fle path that does not exist will cause 
                          the loghandler object to silently create the path and 
                          filename.
                          
                          DEFAULTS TO: True
                           
            logfile:      The FUL PATH (fully qualified path and fielname) where
                          log data will be written to disk. If a file name only 
                          is given, the existing path of the calling applicaiton 
                          is used AFTER being converted to the fully qualified 
                          path.
                          
                          DEFAULTS TO: ./loghandler.log  

        :RETURNS:
            None
            
        :USAGE:
            from loghandler import log
            log.error(app_name   = "MyApplication", 
                      logfile    = "./MyApplication.log",
                      log_level  = 10,
                      screendump = True,
                     )            
            change('app_name', 'MyApp')
            change('logfile', '/var/log/apps/DifferentLogName.log')
            
        """
        if param == 'app_name'     : self._change_app_name(value)
        if param == 'log_level'    : self._change_log_level(value)
        if param == 'screendump'   : self._change_screendump(value)
        if param == 'formatter'    : self._change_formatter(value)
        if param == 'create_paths' : self._change_create_paths(value)
        if param == 'logfile'      : self._change_logfile(value)
            
    def purge(self):
        """
        Deletes the current contents of the logfile on disk. 
        WARNING: Security risk. 
                 Ensure the purge process if verified as authorized and 
                 that successful purges are written to the start of the new log. 
        """
        self.logger.critical(''.join(["Attempting to purge '", 
                                      str(self.logfile), "'. "]))

        if fileExists(self.logfile): 
            os.remove(self.logfile)
            with open(self.logfile, 'w', 0):
                os.utime(self.logfile, datetime.datetime.now())

        self.logger.critical(''.join(["Successfully purged '", 
                                      str(self.logfile), "'. "]))

    def dump(self):
        """
        Dumps the current logfile contents to std out.
        """
        _list = self._read()
        for line in _list:
            print line

    #__________________________________________________________________________
    # PRIVATE METHODS            

    def _change_app_name(self, new_app_name):
        """"""
        orig = self.app_name
        self._remove_all_loggers()
        self.app_name   = self._check_app_name(new_app_name)
        self._set_logger()
        msg = ''.join(["Parameter 'app_name' changed from '", 
               str(orig), 
               "' to '", 
               str(self.app_name), 
               "'."])
        self.logger.info(msg)
        return True

    def _change_create_paths(self, create_paths):
        """"""
        orig = self.create_paths
        self.create_paths = self._check_create_paths(create_paths)
        msg = ''.join(["Parameter 'create_paths' changed from '", 
               str(orig), 
               "' to '", 
               str(self.create_paths), 
               "'."])
        self.logger.info(msg)
        return True
            
    def _change_formatter(self, formatter):
        """"""
        orig = self.formater
        self._remove_all_loggers()
        self.formatter  = self._check_formatter(formatter)
        self._set_logger()
        msg = ''.join(["Parameter 'formatter' changed from '", 
                       str(orig), 
                       "' to '", 
                       str(self.formatter), 
                       "'."])
        self.logger.info(msg)
        return True
        
    def _change_logfile(
                        self, 
                        logfile, 
                        migrate = True, 
                        create_paths = None
                       ):
        """
        Intended to change the current logfile of the existing handler
        """
        self.logger.info(''.join(["Attempting to change logfile from '", 
                                  self.logfile, 
                                  "' to '", 
                                  str (logfile),
                                  "'. "
                                  ])) 
#         except NameError, e:
#             pass
        
        create_paths = self._check_create_paths(create_paths)
        source = self.logfile # current

        migrated = False
        if migrate == True:
            # Returns true of false
            migrated = self._migrate_log_data(logfile, 
                                              create_paths = create_paths)

        # Set new logger
        self._remove_handler(self.logfile)                
        self.logfile = logfile
        self._set_filehandler(self.logfile) 
#         self._set_logger()
        
        if migrated:
            self.logger.info(''.join(["Logfile migrated from '", 
                                      source, 
                                      "' to '", 
                                      self.logfile, 
                                      "'. "
                                      ]))
        
        else:
            self.logger.info(''.join(["Unable to migrate Logfile. ", 
                                      "Previous logfile exists at '", 
                                      source, 
                                      "'. "
                                      ])) 
            
    def _change_log_level(self, log_level):
        """"""
        orig = self.screendump
        self._remove_all_loggers()
        self.log_level  = self._check_log_level(log_level)
        self._set_logger()
        msg = ''.join(["Parameter 'log_level' changed from '", 
               str(orig), 
               "' to '", 
               str(self.log_level), 
               "'."])
        self.logger.info(msg)
        return True
    
    def _change_screendump(self, screendump):
        """"""
        orig = self.screendump
#         self.screendump = self._check_boolean(screendump)
        self.screendump = self._check_screendump(screendump)
        self._set_screendump()
        msg = ''.join(["Parameter 'screendump' changed from '", 
               str(orig), 
               "' to '", 
               str(self.screendump), 
               "'."])
        self.logger.info(msg)
        return True
            
    def _check_app_name(self, app_name):
        """"""
        # Verify string and clean
        # This can deliver nonsense if a nonsense object is passed in as 
        # app_name, but it will be functional nonsense
        app_name = (''.join(c for c in str(app_name) 
                            if re.match("[a-zA-z0-9]", c)))

        if self.__exists:
            if ((app_name != self.app_name) and 
                (app_name is not None)):
#                 e = ''.join(["Changing an existing loghandler object's ", 
#                              "app_name is not yet supported."]) 
#                 raise NotImplementedError(e)
                return app_name
#                 self._set_logger()
            
        else:
            if ((app_name is None) or (app_name == '')):
                return 'loghandler'
            else:
                return app_name

    def _check_create_paths(self, create_paths):
        if type(create_paths) is not bool:
            try:
                return self.create_paths
            except (NameError, AttributeError):
                return self.create_paths_default
        else:
            return create_paths

    def _check_formatter(self, format = None):
        if format is None:
            return logging.Formatter(self.formatter_default)
        
        else:
            return str(format) # Put check in place???

#     def _check_boolean(self, screendump):
#         if screendump is None:
#             try:
#                 return self.screendump
#             except AttributeError, e:
#                 return False
#  
#         # Check for strings instead of proper bool            
#         if (("t" in str(screendump).lower())): 
#             return True
#  
#         if (("f" in str(screendump).lower())): 
#             return False
#  
#         # Check for numbers instead of proper bool                        
#         try:
#             if int(screendump) == 1: return True
#             if int(screendump) == 0: return False
#         except ValueError, e:
#             return False
#  
#         # Check for proper bool
#         if isinstance(screendump, bool):
#             return screendump
#         else:
#             e = "Parameter 'screendump' must be boolean (True/False)"
#             raise TypeError(e)

    def _check_logfile_format(self, logfile = None):
        """"""
        if logfile is None:
            try:
                return self.logfile
            except (NameError, AttributeError):
                return self.logfile_default
                       
        # Keyword 'None', 'No', or 'void' (spelled out as text, 
        # not the Python keyword None) means
        # No logging. 
        if (('none' in str(logfile).lower()) or
            ('void' in str(logfile).lower())):
            return 'void'

        # If key word 'syslog' obtain and use the systems syslog
        if 'syslog' in logfile.lower():
            return self._getSyslog()
        
        # If here, the logfile passed is a path and/or filename
        # Strip illegal characters
        # This automatically converts what was passed into a string
        logfile = (''.join(c for c in str(logfile) if re.match("[a-zA-z0-9 -_./\\ ]", c)))

        # logfile must start with either '/' or './'
        # If it has neither, we assume local directory
        if not re.match('^\s*[./|/].*$', logfile): 
            logfile = './' + logfile
         
        # If logfile ends with '/', then its just a path
        # Use the path, and add the default logfilename     
        if logfile.endswith('/'):
            logfile = logfile + self.logfile_default
        
        # logfile is a full path, including filename, and must end in .log    
        if not logfile.lower().endswith('.log'):
            logfile = logfile + '.log'
        
        # Check that directory exists and, if not, create it
        if not directoryExists(logfile, create = self.create_paths):
            err = ''.join([
                           "The logfile directory '", 
                           str(logfile), 
                           "' does not exist and creating it either ", 
                           "failed or is prohibited by the 'create_paths' ", 
                           " parameter (currently set as '", 
                           str(self.create_paths),
                           "')."
                           ])
            raise AttributeError(err)
        
        return os.path.abspath(logfile)
                        
    def _check_logfile(self, logfile):
        """"""
        if ((logfile is None) or (logfile == '')):
            if self.__exists: 
                return self.logfile
            else: 
                return self.logfile_default
        else:
            return self._check_logfile_format(logfile)
            
    def _check_log_level(self, log_level = None):
        #Level
        if log_level is None: 
            try:
                return self.log_level
            except (NameError, AttributeError):
                return self.log_level_default

        # IS NOT NONE
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

    def _check_screendump(self, screendump):
        if type(screendump) is not bool:
            try:
                return self.screendump
            except (NameError, AttributeError):
                return self.screendump_default
            return False
        else:
            return screendump
                
    def _isExistingHandler(self, path):
        """"""
        if re.match("^(\s){0,}(<){0,1}stderr(>){0,1}(\s){0,}$", str(path).lower()):
            path = "<stderr>"
        else:
            path = self._check_logfile_format(path) # returns full path
            
        for handler in self.logger.handlers:
            if path == handler.__dict__['stream'].name:
                return True
        
        return False
    
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
        # If source is None, then source is existing path
        if source is None:
            source = self.logfile
            
        # Format the destination
        dest = self._check_logfile_format(dest)
            
        # If source and dest are identical, just return
        if source == dest:
            return True

        self.logger.info(''.join(["Moving '", 
                                  source, 
                                  "' to '", 
        #                                       str(log_path), "/",
                                  dest,
                                  "'. "
                                  ])) 
        
        # If create_paths is not passed, use the object's current setting
        if create_paths is None: 
            try:
                create_paths = self.create_paths
            except (NameError, AttributeError):
                create_paths = True # Assume True if unknown
                
        # Raises error if None or ""
        err = ''.join(['loghandler._migrate_log_data: ', 
                       'Destination parameter (', 
                       str(dest), 
                       ') is invalid.'])
        # Raises ValueError if dest < 1 or len(dest) chokes
        try:
            if len(dest) < 1: raise ValueError
        except Exception as e:
            self.logger.error(err)
            return False
#             raise type(e)(err + ' (' + e.message + ')')
        
        # Check the dir is already there
        if not directoryExists(dest): 
            if create_paths:
                os.mkdir(os.path.dirname(dest))
            else:
                err = ''.join(['loghandler._migrate_log_data: ',
                           "Destination parameter ('", 
                           str(dest),
                           "') does not exist. Settings prevent creation."])
                self.logger.error(err)
                return False 
#                 raise AttributeError(err)

        try:
            with open(source, "r", 0) as IN:
                with open(dest, "a+", 0) as OUT:
                    for line in IN: OUT.write(line)

            if not fileExists(dest):
                raise Exception
            
        except Exception, e:
            err = ''.join(["Unable to complete log migration from '", 
                           str(source), 
                           "' to '", 
                           str(dest), 
                           "'. Retaining original log file. "
                           ])
            return False

        # Upon success, set self.logfile to new path
#         self.logfile = dest
#         self.log_path = os.path.dirname(dest)
#         self.logfile  = os.path.basename(dest)
        if not self._remove_file(source):
            err = ''.join(["Unable to remove original log file '", 
                           str(source), 
                           "'. Retaining."])
            self.logger.error(err)

        return True
        
    def _read(self):
        """"""
        _list = open(self.logfile, "r", 0).read().splitlines()
        return _list

    def _remove_all_loggers(self):
        keys = logging.Logger.manager.loggerDict.keys()
        for key in keys:
            self._remove_logger(key)
                
    def _remove_handler(self, handle = None):
        """"""
        if re.match("^(\s){0,}(<){0,1}stderr(>){0,1}(\s){0,}$", str(handle).lower()):
            handle = "<stderr>"
            
        elif handle is not None: 
            handle = self._check_logfile_format(handle) # returns full path
        
        else:
            handle = self.logfile_default
        
        msg = ''.join(["Removing handler '", 
                       str(handle), 
                       "'."])    
        self.logger.info(msg)
            
        for h in list(logging.Logger.manager.loggerDict[self.app_name].handlers):
            if h.__dict__['stream'].name == handle:
                logging.Logger.manager.loggerDict[self.app_name].removeHandler(h)

    def _remove_file(self, _file):
        try:
            os.remove(_file)
            return True
        except Exception:
            return False
 
    def _remove_logger(self, app_name):
        if self._isExistingLogger(app_name):
            for h in list(logging.Logger.manager.loggerDict[app_name].handlers):
                logging.Logger.manager.loggerDict[app_name].removeHandler(h)
            del logging.Logger.manager.loggerDict[app_name]

    def _set_filehandler(self, logfile = None, level = None, formatter = None):
        """"""        
        # Logfile
        logfile = self._check_logfile_format(logfile) # returns full path
        fh = logging.FileHandler(logfile)

        #Level
        level = self._check_log_level(level)
        fh.setLevel(level)

        # Format
        formatter = self._check_formatter(formatter)
        fh.setFormatter(formatter)
        
        if not self._isExistingHandler(logfile):
            self.logger.addHandler(fh)
            msg = ''.join(["Added filehandler '", 
                           str(logfile), 
                           "'."])
            self.logger.info(msg)
            self.handlers.append(fh) #333 aybe dont need this
        else:
            msg = ''.join(["Filehandler '", 
                           str(logfile), 
                           "' already exists. Skipping."])
            self.logger.info(msg)
            
    def _set_logger(self):
        """
        ALL the 'self' variables need to be set at this point, or this 
        will FAIL.
        """
        
        # Create the logger agent        
        self.logger = logging.getLogger(self.app_name)
        
        # Set the logger defaul level
        self.logger.setLevel(level=self.log_level)

        # Set the base handlers
        self._set_screendump()
        self._set_filehandler(self.logfile)
        
    def _set_screendump(self, setting = None, level = None, formatter = None):
        """"""
        self.screendump = self._check_screendump(setting)
        # If a boolean is passed, reset self.screendump to new setting
        # Otherwise use system defaut
        if self.screendump: #True
            if self._isExistingHandler('stderr'):
                msg = "Screendump is already set to 'True'"
                self.logger.info(msg)
            else:
                # handler object
                ch = logging.StreamHandler()

                #Level
                level = self._check_log_level(level)
                ch.setLevel(level=level)
        
                # Format
                formatter = self._check_formatter(formatter)
                ch.setFormatter(self.formatter)

                #Set                 
                self.logger.addHandler(ch)
                self.handlers.append(ch) #333 maybe dont need this
                
                msg = ''.join(["Added screenhandler ", 
                               '(logger.stream to <stderr>).'])
                self.logger.info(msg)                
                
        else:
            if self._isExistingHandler('stderr'):
                msg = "Turning off Screendump"
                self.logger.info(msg)
                self._remove_handler('stderr')

                msg = ''.join(["Removed screenhandler ", 
                               '(logger.stream to <stderr>).'])
                self.logger.info(msg)                

if __name__ == "__main__":
    
    log = SetLogger(
                    app_name   = "QRNote", 
                    logfile    = "./qrnote.log",
                    log_level  = 10,
                    screendump = True,
                    )
    
#     log.debug("This is a log test of log.debug")
#     log.info("This is a log test of log.info")
#     log.warning("This is a log test of log.warning")
#     log.error("This is a log test of log.error")
#     log.critical("This is a log test of log.critical")
# 
#     log.migrate(dest = "/shared/GitHub/Tesera/MRAT_Refactor/log/migrated.log", 
#                 source = "/shared/GitHub/Tesera/MRAT_Refactor/log/test.log", 
#                 create_paths = False)

#     log.debug("--------------------------------------")
#     log.debug("This is line one in migradted")
#     log.debug("This is line two in migradted")
# 
#     log = SetLogger(app_name = "NEWrealAppName", 
# #                     logfile = "NEWtest.log",
# #                     log_path = "/shared/GitHub/Tesera/MRAT_Refactor/log", 
#                     log_level = 20, 
# #                     screendump = True, 
#                     )
# 
#     log.debug("This is line one in new set")
#     log.debug("This is line two in new set")
#     
#     log = SetLogger(app_name = "NEWrealAppName", 
#                     logfile = "NEWtest.log",
#                     log_path = "/shared/GitHub/Tesera/MRAT_Refactor/log", 
#                     log_level = 10, 
# #                     screendump = True, 
#                     )
#  
#     log.debug("This is line one in SECOND new set")
#     log.debug("This is line two in SECOND new set")
#     