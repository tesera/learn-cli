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

from checks         import checkObject as obj
from checks         import fileExists
from ConfigParser   import SafeConfigParser
from errorhandler   import handlertry
from errorhandler   import raisetry
from loghandler     import SetLogger 

import ConfigParser 
# import Errorhandler
import sys

class ConfigHandler(object):
    def __init__(self, callobj, config_file):
        """"""
        self._setlog()

        self.config_file    = config_file
        self.callobj        = callobj
        self.log.debug("ConfigHandler called with " + str(self.config_file))

        self._initial_var_load()

        # This is a special function of the confighandler
        # If the full path for the logfile in the config file is different than 
        # what's currently being used, migrate the log. 
        self._migrate_log()

    #__________________________________________________________________________
    # PRIVATE METHODS
    def _initial_var_load(self):
        """"""
        self.open_file()
        self.load_vars()
    
    def _migrate_log(self):
        """
        This is a special migrate log method that should only be used within 
        confighandler. It actually migrating anything is a rarity.
        """
        # callobj is the self for which the confighandler is setting variables
        # 'configured_full_log_path' is the path as set by the config file

        configured_full_log_path = self.log.set_full_log_path(
                                                        self.callobj.log_path, 
                                                        self.callobj.logfile
                                                        )

        # self.log is the logging singleton object
        # If the full_log_path in the current logging object is NOT the same
        # as configured_full_log_path, then migrate the log to the new 
        if self.log.full_log_path != configured_full_log_path:
            self.log.debug(''.join(["Logfile changed by configuration file. ", 
                                    "Migrating..."]))
            # loghandler's migrate method
            # Remember, the migrate method automagically resets the handler's
            # self.full_log_path to 'dest'
            self.log.migrate(
                    dest = configured_full_log_path, # the log path from config  
                    source = self.log.full_log_path, # Current
                    create_paths = True)
                        
        else:
            self.log.debug(''.join(["Continuing with original log file : '", 
                                    str(self.log.full_log_path), 
                                    "' ."]))
        
    @raisetry("confighandler.ConfigHandler: Failed at SetLogger()")
    def _setlog(self):
        """"""
        self.log = SetLogger()
        return 

    #__________________________________________________________________________
    # PUBLIC METHODS
    @raisetry("ConfigHandler.getatttr: ")    
    def getattr(self, section = None, valuename = None, default = None):
        """"""
#         try:
        # FUTURE: if section is none, search all the sctions and return 
        #         either the first instance, or a list of all
        if ((section is None) or (len(section) < 1)):
            e = "Parameter 'section' cannot be empty or None."
            raise ConfigParser.NoSectionError(e)
        

        # FUTURE: if valuename is none, return a list of all values
        if ((valuename is None) or (len(valuename) < 1)):
            e = "Parameter 'valuename' cannot be empty or None."
            raise ConfigParser.NoOptionError(e)
    
        return self.config.get(section, valuename)
    
#         except ConfigParser.NoSectionError, e:
#             e=''.join(["ConfigFileParseError(",str(self.config_file),
#                        "):", str(section), ") Section not found."])
# #             self.err(e, getmembers(self), stack())
#             raise IOError(e)
#     
#         except ConfigParser.NoOptionError, e:
#             e=''.join(["ConfigFileNoOption(",str(self.config_file),
#                        ":", str(section), ":", str(valuename), 
#                        ") option not found."])
# #             self.err(e, getmembers(self), stack())
#             raise IOError(e)
#             
#             if (("err" in str(default).lower()) or
#                 ('rais' in str(default).lower())):
#                 raise IOError(e)
#             else:
#                 return default

    @raisetry("ConfigHandler.setatttr: ")    
    def setattr(self, section = None, valuename = None, persist = False):
        """
        setattr will be used to change a config setting on the fly. 
        By default it only makes the change in the active software
        If persist = True, the change will also be permanently made in the 
        config file parameter "self.config_file" 
        """
        raise NotImplementedError
            
    def open_file(self):
        self.verify_file()
        self.log.debug(("Opening " + str(self.config_file)))
        self.config = SafeConfigParser()
        self.config.read(self.config_file)
        
    def load_vars(self, section = None):
        for section_name in self.config.sections():
            if ((section_name.lower() == str(section).lower()) or 
                (section is None)):
                self.log.debug(("Loading section: " + str(section_name)))                
                for name, value in self.config.items(section_name):
                    self.callobj.__dict__[name] = value
    
    def verify_file(self):
        """"""
        self.log.debug(("Verfiying " + str(self.config_file)))
        # Check config file exists since parser will not error if you 
        # attempt to open a non-existent file
        if not fileExists(self.config_file):
            e = ''.join(["ConfigFileNotFound(", 
                         str(self.config_file),"):"])
            raise IOError(e) # Remove me and active self.err line

if __name__ == "__main__":
    from loghandler import SetLogger
    
    class forttest(object):
        def __init__(self):
            self.log = SetLogger(app_name = "myapp", 
                                 logfile = "confighandlerTest.log",
                                 log_path = "../log", 
                                 log_level = 10, 
                                 screendump = True,
                                 create_paths = False )

            self.log.debug("myapp log file created.")

            self.config = ConfigHandler(self, "../etc/XIterativeVarSel.py.conf")

    obj = forttest()

