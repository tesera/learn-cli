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

from checks         import checkObject
from checks         import fileExists
from checks         import checklist
from ConfigParser   import SafeConfigParser
from errorhandler   import handlertry
from errorhandler   import raisetry

from loghandler     import SetLogger

import ConfigParser 
import re
# import Errorhandler
import sys

class ConfigHandler(object):
    __exists = False
    
    def __new__(cls,                  
#                 callobj, 
#                 config_file = None, 
#                 log_level   = None,
#                 screendump  = None, 
                *args, 
                **kwargs
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
            cls.instance = super(ConfigHandler, cls).__new__(cls)
            return cls.instance

        # Else if an instance does exist, set a flag since
        # __init__is called, but flag halts completion (just returns)           
        else:
            cls.instance.__exists = True
            return cls.instance

    def __init__(self, 
#                 config_file    = None, 
#                  log_level      = None,
#                  screendump     = None, 
                *args, 
                **kwargs
                 ):
        """"""
        # Here, we do not give the option of changing the ConfigHandler 
        # parameters. One log file, determined by the main application
        # This can be changed to match SetLogger...but is not recommended.
        if self.__exists: return

        try:
            self.log_level = kwargs["log_level"]
        except (KeyError, AttributeError), e:
            self.log_level = 40

        try:
            self.screendump = kwargs["screendump"]
        except (KeyError, AttributeError), e:
            self.screendump = False
        
        self.log = SetLogger(
                             app_name = "configparser", 
                             logfile = "configparser.log",
                             log_path = "./", 
                             log_level = self.log_level, 
                             screendump = self.screendump, 
                             create_paths = False 
                             )


        try:
            self.config_file    = kwargs["config_file"]
        except (KeyError, AttributeError), e:
            e = ''.join(["Parameter 'config_file' ", 
                         "MUST be passed at first object instantiation.", 
                         str(e)])
            raise ValueError(e)

        self.log.info("ConfigHandler called with " + str(self.config_file))

        self._load_all_vars()

#         # Override config file vars. This needs to come AFTER loding the config 
#         # file but BEFORE the final SetLogger to allow for config file vars 
#         # to be manually overidden  
#         if log_level    is not None: self.log_level = log_level
#         if screendump   is not None: self.screendump = screendump

        self._override_with_kw_vars(kwargs)

        self._set_mandatory_defaults({"app_name":"configparser", 
                                      "logfile":"configparser.log", 
                                      "log_path":"./", 
                                      "create_paths":False} 
                                     )

        self.log = SetLogger(
                             app_name = self.app_name, 
                             logfile = self.logfile,
                             log_path = self.log_path, 
                             log_level = self.log_level, 
                             screendump = self.screendump, 
                             create_paths = self.create_paths 
                             )
        

    #__________________________________________________________________________
    # PRIVATE METHODS

    @handlertry("PassThroughException: rhandler._set_mandatory_defaults")
    def _set_mandatory_defaults(self, _dict):
        """
        """
        for key in _dict.keys():
            if key not in self.__dict__.keys():
                self.__dict__[key] = _dict[key]
        return

    def _load_all_vars(self):
        """"""
        self.open_file()
        self.loadattr()

    @handlertry("FATAL: rhandler._override_with_kw_vars")
    def _override_with_kw_vars(self, kwargs):
        for key in kwargs.keys():
            self.__dict__[key] =  kwargs[key]
        return True
        
#     @handlertry("PassThroughException: rhandler._set_mandatory_defaults")

    
#     def _migrate_log(self):
#         """
#         This is a special migrate log method that should only be used within 
#         confighandler. It actually migrating anything is a rarity.
#         """
#         # callobj is the self for which the confighandler is setting variables
#         # 'configured_full_log_path' is the path as set by the config file
# 
#         configured_full_log_path = self.log.set_full_log_path(
#                                                         self.log_path, 
#                                                         self.logfile
#                                                         )
# 
#         # self.log is the logging singleton object
#         # If the full_log_path in the current logging object is NOT the same
#         # as configured_full_log_path, then migrate the log to the new 
#         if self.log.full_log_path != configured_full_log_path:
#             self.log.debug(''.join(["Logfile changed by configuration file. ", 
#                                     "Migrating..."]))
#             # loghandler's migrate method
#             # Remember, the migrate method automagically resets the handler's
#             # self.full_log_path to 'dest'
#             self.log.migrate(
#                     dest = configured_full_log_path, # the log path from config  
#                     source = self.log.full_log_path, # Current
#                     create_paths = True)
#                         
#         else:
#             self.log.debug(''.join(["Continuing with original log file : '", 
#                                     str(self.log.full_log_path), 
#                                     "' ."]))
        
    #__________________________________________________________________________
    # PUBLIC METHODS

    @handlertry("PassThroughException: ConfigHandler.getatttr;  ")    
    def getattr(self, varname, default = None):
        """
        Retrieves the attribute from ConfigHandlers "self"
        """
        # If the first attempt to return a self var fails, control 
        # should pass to @handlertry where corrections can be set 
        # For now this is just a passthrough, which will drop control
        # to the second line, which returns the default
        return self.__dict__[varname]
        return default

    @raisetry("ConfigHandler.getatttr;  ")    
    def setattr(self, varname, value, default = None):
        """
        Sets an attribute from ConfigHandlers "self"
        """
        self.__dict__[str(varname)] = value
        return True

    @raisetry("ConfigHandler.setatttr: ")    
    def configattr(self, section = None, valuename = None, persist = False):
        """
        configattr will be used to change a config setting on the fly. 
        By default it only makes the change in the active software
        If persist = True, the change will also be permanently made in the 
        config file parameter "self.config_file" 
        """
        raise NotImplementedError

    @handlertry("ConfigFileParseError: ")
    def open_file(self):
        self.verify_file()
        self.log.debug(("Opening " + str(self.config_file)))
        self.config = SafeConfigParser()
        self.config.optionxform = str
        self.config.read(self.config_file)
        return True
    
    @handlertry(''.join(["ConfigFileNoOption: ConfigHandler.load_var; "]))        
    def loadattr(self, varname = None, section = None):
        """
        Retrieves a variable from the CONFIG FILE (not self)
        """
        _found = False
        for section_name in self.config.sections():

            if ((section_name.lower() == str(section).lower()) or 
                (section is None)):
                
                for name, value in self.config.items(section_name):
                    if ({"LOADALL":True, None:True, name:True}.get(varname)):
                        value = self._convert_string_values(value)
                        self.__dict__[name] = value
#                         self.log.debug(''.join(["set '", str(name), 
#                                                 "' to '", str(value),
#                                                 "'."]))
                        _found = True

                        if varname is not None: return value

        if not _found: raise AttributeError(''.join(["Unable to find variable '",
                                                    str(varname), 
                                                    "' in section '", 
                                                    str(section), 
                                                    "' of config_file '", 
                                                    str(self.config_file), 
                                                    "'. "
                                                    ]))
            
    
    def verify_file(self):
        """"""
        self.log.debug(("Verfiying " + str(self.config_file)))
        # Check config file exists since parser will not error if you 
        # attempt to open a non-existent file
        if not fileExists(self.config_file):
            e = ''.join(["ConfigFileNotFound(", 
                         str(self.config_file),"):"])
            raise IOError(e) # Remove me and active self.err line

    def _convert_string_values(self, value):
        """"""
        @raisetry(''.join(["ConfigHandler._convert_values; checking value of '", 
                           str(value), "'."]))
        def _convertit(self, value):
            # Check for boolean text, return actual bool
            if (re.match("^true$", str(value).lower())) : return True
            if (re.match("^false$", str(value).lower())): return False

            # Check for INT and float 
            if (re.match("^[0-9]+\.[0-9]*$", value)):   return float(value)
            if (re.match("^[0-9]+$", value)):           return int(value)

            # Otherwise just return original string, no conversion            
            return value 
        
        result = _convertit(self, value)

        return result
            
        
if __name__ == "__main__":
    from loghandler import SetLogger
     
    class forttest(object):
        def __init__(self):
#             self.log = SetLogger(app_name = "myapp", 
#                                  logfile = "confighandlerTest.log",
#                                  log_path = "../log", 
#                                  log_level = 10, 
#                                  screendump = True,
#                                  create_paths = False )

            self.config = ConfigHandler(
#                                         self, 
                                        log_level = 10,
                                        screendump = True,
                                        config_file = "../etc/MRAT.conf"
                                        )

    obj = forttest()
    
#     for i in obj.config.__dict__.keys():
#         print i,":", obj.config.__dict__[i]
         
    print obj.config.getattr("log_level")
    print obj.config.getattr("nadadadad")
    