##############################################################################
# Removal of the "__license__" line or content from  "__license__", or removal 
# of "__author__" in this or any constituent # component or file constitutes a 
# violation of the licensing and copyright agreement. 
__author__      = "Mike Rightmire"
__copyright__   = "BioCom Software"
__license__     = "Jeff Wright"
__license_file__= "Clause1.PERPETUAL_AND_UNLIMITED_LICENSING_TO_THE_CLIENT.py"
__version__     = "0.9.0.0"
__maintainer__  = "Mike Rightmire"
__email__       = "Mike.Rightmire@BiocomSoftware.com"
__status__      = "Development"
##############################################################################

from checks import checkObject as obj
from checks import fileExists
from ConfigParser import SafeConfigParser
from loghandler import checkLogger

import ConfigParser 
import errorhandler

class ConfigHandler(object):
    def __init__(self, config_file, log = ""):

        # Set logger ----------------------------------------------------------
        self.log = checkLogger(log, 
                               callingobj = self, 
                               log_path = "" )

        # Set errorhandler ----------------------------------------------------
        self.CustomErrorHandler = errorhandler.errorhandler(self.log)
        self.err = self.CustomErrorHandler.err()

        # Set config handler --------------------------------------------------
        self.config_file = config_file
        self.log.debug(''.join(["Config file:", str(self.config_file)]))
        self.verify_file()
        self.open_file()

    def readvalue(self, section, valuename, default = None):
        try:
            return self.config.get(section, valuename)
    
        except ConfigParser.NoSectionError, e:
            e=''.join(["ConfigFileParseError(",str(self.config_file),
                       "):", str(self.conf_section), ") Section not found."])
#             self.err(e, getmembers(self), stack())
            raise IOError(e)
    
        except ConfigParser.NoOptionError, e:
            e=''.join(["ConfigFileNoOption(",str(self.config_file),
                       ":", str(self.conf_section), ":", str(valuename), 
                       ") option not found."])
#             self.err(e, getmembers(self), stack())
            raise IOError(e)
            
            if (("err" in str(default).lower()) or
                ('rais' in str(default).lower())):
                raise IOError(e)
            else:
                return default
            
    def open_file(self):
#         self.log.debug(''.join(["Reading config file..."]))
        self.config = SafeConfigParser()
        self.config.read(self.config_file)
#         self.log.debug(''.join(["Good."]))
        
    
    def load_vars(self, callobj, section):
        for section_name in self.config.sections():
            if section_name.lower() == str(section).lower():
#                 self.log.debug(''.join(["Loading config file '", 
#                                         str(self.config_file),
#                                         "' section '", 
#                                         str(section_name), "'."]))
                for name, value in self.config.items(section_name):
                    callobj.__dict__[name] = value
    
    def verify_file(self):
        # Check config file exists since parser will not error if you 
        # attempt to open a non-existent file
#         self.log.debug(''.join(["Verifying config file..."]))
        if not fileExists(self.config_file):
            e = ''.join(["ConfigFileNotFound(", 
                         str(self.config_file),"):"])
    #             self.err(e, getmembers(self), stack())
            raise IOError(e) # Remove me and active self.err line
#         self.log.debug(''.join(["Good."]))
