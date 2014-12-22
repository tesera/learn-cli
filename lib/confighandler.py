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

from checks import checkObject as obj
from checks import fileExists
from ConfigParser import SafeConfigParser
from errorlogger import errorLogger
from errorhandler import errorhandler

import ConfigParser 
import errorhandler
import sys

class configHandler(object):
    def __init__(self, 
                 config_file,
                 screendump = False, 
                 debug = False, 
                 ):

        self.config_file    = config_file
        self.screendump     = screendump 
        self.debug          = debug 
        
        with errorLogger('configHandler', 
                         screendump = screendump, 
                         debug = debug) as self.errorlog:

            self.errorlog.write("confighandler.ConfigHandler: started.")
                        
#             # Set errorhandler ----------------------------------------------------
#             self.CustomErrorHandler = errorhandler.errorhandler(self.log)
#             self.err = self.CustomErrorHandler.err()

            # Set config handler --------------------------------------------------
            self.config_file    = config_file
            self.screendump     = screendump 
            self.debug          = debug

            self.errorlog.write(("config_file = " + str(self.config_file)))            
            self.errorlog.write(("screendump  = " + str(self.screendump)))
            self.errorlog.write(("debug       = " + str(self.debug))) 

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
        self.verify_file()
        self.errorlog.write(("Opening " + str(self.config_file)))
        self.config = SafeConfigParser()
        self.config.read(self.config_file)
        
    def load_vars(self, callobj, section = None):
        for section_name in self.config.sections():
            if ((section_name.lower() == str(section).lower()) or 
                (section is None)):
                self.errorlog.write(("Loading section: " + str(section_name)))                
                for name, value in self.config.items(section_name):
                    callobj.__dict__[name] = value
    
    def verify_file(self):
        """"""
        self.errorlog.write(("Verfiying " + str(self.config_file)))
        # Check config file exists since parser will not error if you 
        # attempt to open a non-existent file
        if not fileExists(self.config_file):
            e = ''.join(["ConfigFileNotFound(", 
                         str(self.config_file),"):"])
            raise IOError(e) # Remove me and active self.err line

if __name__ == "__main__":

    class forttest(object):
        def __init__(self):
            self.vartest= 1
                    
    obj = forttest()

    config = configHandler(config_file = "./test.conf",
                           screendump = True, 
                           debug = True 
                           )
    
    config.load_vars(obj)
    print vars(obj)
