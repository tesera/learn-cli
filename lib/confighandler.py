##############################################################################
# Removal of the "__license__" line or content from  "__license__", or removal 
# of "__author__" in this or any constituent # component or file constitutes a 
# violation of the licensing and copyright agreement. 
__author__      = "Mike Rightmire"
__copyright__   = "BioCom Software"
__license__     = "Tesera"
__license_file__= "Clause1.PERPETUAL_AND_UNLIMITED_LICENSING_TO_THE_CLIENT.py"
__version__     = "0.9.4.0"
__maintainer__  = "Mike Rightmire"
__email__       = "Mike.Rightmire@BiocomSoftware.com"
__status__      = "Development"
##############################################################################

from checks         import checkObject
from checks         import fileExists
from checks         import checklist
from ConfigParser   import SafeConfigParser
# from errorhandler   import handlertry
# from errorhandler   import raisetry
# from loghandler     import SetLogger
from loghandler     import log

import ConfigParser 
import inspect
import re
import types
import sys
from types import ModuleType

# class module(ModuleType):
#     """Automatically import objects from the modules."""
#     def __getattr__(self, name):
#         if name in object_origins:
#             module = __import__(object_origins[name], None, None, [name])
#             for extra_name in all_by_module[module.__name__]:
#                 setattr(self, extra_name, getattr(module, extra_name))
#             return getattr(module, name)
# #         elif name in attribute_modules:
# #             __import__('werkzeug.' + name)
#         return ModuleType.__getattribute__(self, name)


class GettattrWrapper(object):
    def __init__(self, wrapped):
        self.wrapped = wrapped
        
    def __getattr__(self, name):
        print "GettattrWrapper...searching ", name #333
        try:
            return self._config.__dict__[name]
        except (AttributeError, NameError), e:
            raise AttributeError        
    
class ConfigHandler(object):
    """
    :NAME:
        ConfigHandler(config_file = '/path/path/filename.conf', 
                      [global=True/False], 
                      [app_name   = "MyApp"], 
                      [logfile    = "/path/path/MyAppLog.log"],
                      [log_level  = <int>],
                      [screendump = True/False],
                      [config_file = "/path/path/MyApp.conf"], 
                      [pidfile = "/var/run/MyApp.pid"],
                    )    
        
    :DESCRIPTION:
        ConfigHandler() is a 'suite' configuration handler. It is intended to be 
        called by a class's "__init__" and set the configuration parameters 
        throughout an entire software package (I.e. the same configuration 
        information for every class object that is instantiated in association 
        with a complete piece of functional software).
        
        The primary goal with ConfigHandler is to load a single, consistent
        configuration environment to be passed amongst ALL objects within a 
        package.
        
        ConfigHandler is a SINGLETON, meaning once instantiated, THE SAME OBJECT
        will be returned to every class object calling it. 
        
        ConfigHandler ALSO INITIATES the "loghandler"  (which is ALSO  a 
        singleton and ALSO intended to be a consistent single logging object 
        passed amongst all instantiated objects of a package. 
        
        IF YOU CALL ConfigHandler, YOU DO NOT NEED TO SET THE LOGGER, however 
        doing so will not break anything. 
         
        
    :ARGUMENTS:
        config_file:    <full path with filename>
        
            MANDATORY
            
            Tell ConfigHandler where to find the configuration file. 
            
            If the file does not exist, error is raised.
            
            The default config file example has the details about 
            creating a config file. It is based on Python's ConfigParser
            module and uses that format. 
            
            I.e.
            
            parameter = string 
            
            While ConfigHandler also handles the logging module, if 
            a config file is not desired, just use the 'loghandler.log'
            @classmethod to manually instantiate the logger (see 
            LogHandler's help page for details.
            
            I.e.
                    
            from loghandler import log
            
            log.info(
                "I automatically instantiate the logging object.", 
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
                       
        
        global:     True/False
        
            OPTIONAL
            
            True inserts the config file's parameter definitions into 
            'callobj' (the object calling confighandler) AS WELL AS
            the confighandler object that's getting returned. 
            
            DEFAULTS TO: True
                    
        app_name   = <str>

            OPTIONAL

            Sets the 'app_name' variable for the LogHandler. See the 
            LogHandler help or 'loghandler.py' for details.  

        logfile    <full path with filename>

            OPTIONAL

            Sets the 'logfile' variable for the LogHandler. See the 
            LogHandler help or 'loghandler.py' for details.  

        log_level  = <int>

            OPTIONAL

            Sets the 'log_level' variable for the LogHandler. See the 
            LogHandler help or 'loghandler.py' for details.  
        
        screendump = True/False
        
            OPTIONAL

            Sets the 'screendump' variable for the LogHandler. See the 
            LogHandler help or 'loghandler.py' for details.  
                
                      
        *args, **kwargs: 
            Numerous parameters can be passed into the ConfigHandler object.
            
            Using args/kwargs for even the one mandatory parameter was chosen 
            to allow for future flexibility.  
            
    
    :VARIABLES:
        No userspace mutable variables. 
        
    :METHODS:
        No userspace mutable methods...although future version of this will 
        have methods for setting and getting variables as well as manipulating 
        the overall config environment including making changes to the config 
        file and reloading config parameters. 

    :RETURNS:
        self as callingobject._config
        
    :USAGE:
        <myClass>
            def __init__(self):
                self.config_var = ConfigHandler(config_file = "./my.conf)
                
    :EXAMPLE:
        <configuration.conf>
        # ---------------------------------------------------------------------
        # Class configuration file 
        # ---------------------------------------------------------------------
        #######################################################################
        #  THIS FILE SHOULD ONLY BE USED TO SET SIMPLE CONFIGURATION VALUES. 
        # NOT AS A REPLACEMENT FOR SETTING VARIABLES PROPERLY WITHIN A CLASS!! 
        #
        # THE PARAMETERS SET BY CONFIGHANDLER USING THIS FILE ARE SET DIRECTLY 
        # IN THE CALLING CLASS'S "self". PLEASE BE AWARE WHEN CREATING THIS 
        # CONFIG FILE 
        #######################################################################
        #
        #  I.e. The line "option = 1" in this file creates 
        #       "callingobject.self.option = 1" 
        #       AND 
        #       "callingobject.self._config.option = 1". 
        #
        #  class some_python_class(object):
        #    def __init__(self):
        #      ConfigHandler(self, config_file = "/dir/dir/file.conf")
        # 
        #  print self.option
        #  1
        #   
        #  print self._config.option
        #  1
        #
        # SECTIONS:
        #  Each [SECTION] defines a specific set of option-value pairs. The 
        # SECTION name is userspace and arbitrary. 
        #
        # OPTIONS:
        #  option=value
        #   Each option within a section will create a variable BY THE SAME 
        #   NAME AS THE 'OPTION' in the instantiated ConfigHandler OBJECT with 
        # its value set to "value". 
        # I.e.
        #  "name=Hydrogen" creates a variable called "self.name" in the 
        #  ConfigHandler object with the value of "Hydrogen". 
        #  This is the same as if the line of code 'self.name = str("Hydrogen")' 
        #  had been written directly into the calling objects code.  
        #
        #   Caveats:
        #     - Spaces after the "=" are ignored.
        #
        #     - ALL VALUES ARE A STRING...so they MAY have to be converted for 
        #       use. At instantiation, ConfigHandler attempts to convert floats, 
        #       integers and boolean - but be prepared to check for this. 
        #
        #     - Numbers will be returned as floats or int...never bools. 
        #
        #     - Quotes around values will be returned as part of the string. 
        #
        #  
        # FORMAT:
        #  [section_name]
        #    option=value
        #
        #  - Lines starting with "#" are ignored. 
        #
        #  - Lines with "#" AFTER DATA ARE *NOT* IGNORED. 
        #    I.e. name=Hydrogen # This comment will be included in name's value
        #
        #  - Do NOT use quotes for text values. 
        # ---------------------------------------------------------------------
        [LOGGING]
        logfile             = MyPackage.log
        log_path            = /shared/MyPackage/var/log/
        app_name            = MyPackageName 
        log_level           = 10 
        screendump          = True
        create_paths        = True         
    """
    __exists = False
    
#     def __new__(cls, callobj, *args, **kwargs): 
    def __new__(cls, *args, **kwargs): 
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
        
        # This grabs the calling object, so var can be loaded into it
        callobj = inspect.stack()[1][0].f_locals['self']

        if not hasattr(cls, 'instance'):
            cls.instance = super(ConfigHandler, cls).__new__(cls)
            callobj._config = cls.instance
            return cls.instance

        # Else if an instance does exist, set a flag since
        # __init__is called, but flag halts completion (just returns)
        else:
            cls.instance.__exists = True
            callobj._config = cls.instance
            return cls.instance

    def __init__(self, *args, **kwargs):
        """"""
        # This grabs the calling object, so var can be loaded into it
        self.callobj = inspect.stack()[1][0].f_locals['self']

        # Forgot what this does ;-)
        sys.modules[self.callobj.__class__.__module__] = GettattrWrapper(sys.modules[self.callobj.__class__.__module__])
#         sys.modules[__name__] = ModuleWrapper(sys.modules[__name__])

        # Singleton. If confighandler object exists, do not re-run __init__, 
        # just return         
        if self.__exists:
            return
        
        # MANDATORY DEFAULTS dict
        # The following mandatory parameters must exist. If they do not exist 
        # in the config file AND have not been passed to the __init__, 
        # these will be used. 
        self.MANDATORY_DEFAUTS = {
                             "app_name":"configparser", 
                             "logfile":"configparser.log", 
                             "log_path":"./", 
                             "create_paths":True
                             }
        
        ### These params check for loghandler object params
        # Get log_level from kwargs or set to default 40
        self.log_level  = kwargs.pop("log_level", 40)
        # Get screendump from kwargs or set default False
        self.screendump = kwargs.pop("screendump", False)
        # Get global from kwargs or set default True
        self.GLOBAL = kwargs.pop("global", True)

        # Set temp logger to monitor confighandler
        app_name = "configparser"
        logfile = "./configparser.log"
        log_level = self.log_level 
        screendump = self.screendump 
        create_paths = True 

        msg = ''.join(['Initiating logger with ',
                       'app_name:', str(app_name), 
                       ', logfile: ', str(logfile), 
                       ', log_level: ', str(log_level), 
                       ', screendump: ', str(screendump), 
                       ', create_paths: ', str(create_paths), 
                       '.'])
        
        # Actually creates the loghandler object.
        log.debug(  msg,
                    app_name = app_name, 
                    logfile = logfile,
                    log_level = self.log_level, 
                    screendump = self.screendump, 
                    create_paths = create_paths 
                    )

        # Check for the config file param. Absence of config_file raises err
        # Defaults to None if KW does not exist
        self.config_file  = kwargs.pop("config_file", None)
        # Checks validity of config_file param. None raises error. 
        self._check_config_file(self.config_file)
        log.info("ConfigHandler called with " + str(self.config_file))

        # Load the config file avriables into self and self._config
        self._load_all_vars(*args, **kwargs)

        # Set the perm logger config based on settings in the config file
        log.debug("Setting logger's permanent configuration",
                             app_name = self.app_name, 
                             logfile = self.logfile,
#                              log_path = self.log_path, 
                             log_level = self.log_level, 
                             screendump = self.screendump, 
                             create_paths = self.create_paths 
                             )
        
    
    #__________________________________________________________________________
    # PRIVATE METHODS
    #@handlertry("InvalidConfigurationFile:")    
    def _check_config_file(self, conf):
        """"""
        err = ''.join(["Invalid 'config_file' parameter set as '",
              str(conf),
              "'. "  
              "Configuration file name MUST be passed at object ", 
              "instantiation as a string."]) 

        if (conf is None):              raise ValueError(err)
        if (not fileExists(str(conf))): raise ValueError(err)
                
    #@handlertry("PassThroughException:")    
    def _convert_string_values(self, value):
        """"""
        #@raisetry(''.join(["ConfigHandler._convert_values; checking value of '", 
#                            str(value), "'."]))
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
            
    #@handlertry("")    
    def _load_all_vars(self, *args, **kwargs):
        """"""
        self.open_file()
        self.loadattr()
        # Override config file vars.
        # This overwrites variables set from the config file, with any identical
        # variables that were passed into the __init__. This way, config file
        # params can be selectively overrided at runtime.   
        # This needs to come AFTER loding the config 
        # file but BEFORE the final SetLogger to allow for config file vars 
        # to be manually overidden  
        self._override_with_kw_vars(kwargs)

        # Should th following mandatory parameters not exist in the config 
        # file AND not have been passed to the __init__, create them here 
        # using set defauls
        self._set_mandatory_defaults(self.MANDATORY_DEFAUTS)

        # All the configuration is first set into the ConfigHandler 
        # object (self). THEN, if GLOBAL is true, they are passed into the 
        # calling object as well
        # self.GLOBAL defaults to True
        if self.GLOBAL: self.callobj.__dict__.update(self.__dict__) 

    #@handlertry("FATAL:")
    def _override_with_kw_vars(self, kwargs):
        for key in kwargs.keys():
            self.__dict__[key] =  kwargs[key]
        return True
        
        
    #__________________________________________________________________________
    # PUBLIC METHODS

    #@handlertry("PassThroughException: rhandler._set_mandatory_defaults")
    def _set_mandatory_defaults(self, _dict):
        """
        """
        for key in _dict.keys():
            if key not in self.__dict__.keys():
                self.__dict__[key] = _dict[key]
        return

    #@handlertry("PassThroughException:")    
    def get(self, varname, default = None):
        """
        Retrieves the attribute from ConfigHandlers "self"
        """
        # If the first attempt to return a self var fails, control 
        # should pass to @handlertry where corrections can be set 
        # For now this is just a passthrough, which will drop control
        # to the second line, which returns the default
        return self.__dict__[varname]
        return default

    #@handlertry("PassThroughException:")    
    def set(self, varname, value, default = None):
        """
        Sets an attribute from ConfigHandlers "self"
        """
        self.__dict__[str(varname)] = value
        return True

    #@handlertry("PassThroughException:")    
    def getconfig(self, section = None, valuename = None, persist = False):
        """
        """
        raise NotImplementedError

    #@handlertry("PassThroughException:")    
    def setconfig(self, section = None, valuename = None, persist = False):
        """
        """
        raise NotImplementedError
    
    #@handlertry("ConfigFileParseError: ")
    def open_file(self):
        self.verify_file()
        log.debug(("Opening " + str(self.config_file)))
        self.config = SafeConfigParser()
        self.config.optionxform = str
        self.config.read(self.config_file)
        return True
    
    #@handlertry(''.join(["ConfigFileNoOption:"]))        
    def loadattr(self, varname = None, section = None):
        """
        Retrieves a variable from the CONFIG FILE (not self)
        """
        _found = False
        for section_name in self.config.sections():
#             print "confighandler: loading section name: " + section_name #333

            if ((section_name.lower() == str(section).lower()) or 
                (section is None)):

                # ConfigParser.InterpolationMissingOptionError as handlertry error message
                for name, value in self.config.items(section_name):
                    if ({"LOADALL":True, None:True, name:True}.get(varname)):
#                         print "adding var '" + str(name) + "' with value '" + 
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
            
    #@handlertry("PassThroughException:")    
    def verify_file(self):
        """"""
        log.debug(("Verfiying " + str(self.config_file)))
        # Check config file exists since parser will not error if you 
        # attempt to open a non-existent file
        if not fileExists(self.config_file):
            e = ''.join(["ConfigFileNotFound(", 
                         str(self.config_file),"):"])
            raise IOError(e) # Remove me and active self.err line

        
if __name__ == "__main__":
    class forttest(object):
        def __init__(self):

            self.config = ConfigHandler(
                                        self, 
                                        log_level = 10,
                                        screendump = True,
                                        config_file = "../etc/QRNote.conf"
                                        )

    obj = forttest()
    print obj.instantiate_default
    print obj._config.instantiate_default
    
