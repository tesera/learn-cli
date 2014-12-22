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

from checks import fileExists

import datetime
import logging
import os

class errorLogger(object):
    """
    :NAME:
        errorLogger
        
    :DESCRIPTION:
        errorLogger is EXCLUSIVELY for writing errors to file located IN THE
        SAME DIRECTORY AS THE SCRIPT CALLING IT. It is intended to capture 
        debug output BEFORE A COMPREHENSIVE LOG OBJECT can be created. I.e.
        within the loghandler itself. 
        
        For all other logging, please use the loghandler object. 
        
    :ARGS:
        caller: This is the name of the calling script or object. 
                Functionally, all this does is set the filename as 
                'caller.error.log' in the local directory.
                
        debug:  Global setting as to whether the logger should leave the 
                logfile in place upon close() [debug mode] or delete the file 
                upon close() [normal mode]. 
                
                The global debug can be set to ensure the logfile persists, 
                however since the logfile is in the same directory as the
                script this can cause unexpected file glut.  
                
                If a fatal error occurs while running a script using errorLogger
                it SHOULD ALWAYS BE be closed with "close(debug=True)" which 
                will override the global debug variable and leave the logfile 
                intact for further analysis. 
                
                 
        screendump: (True/False). True means each line will be dumped to the 
                    screen, as well as self.logfile. This is not to be confused 
                    with the screendump() method which dupm the content of the
                    current logfile to the screen on demand.  
                
    :METHODS:
        __init__: This set the self.logfile variable only. 
        
        start():         Opens the 'self.logfile' for writing.

        close(debug):    Closes the 'self.logfile' for writing.

                         If 'debug' is true...only closes the file...but leaves 
                         if intact.
                         
                         If 'debug' is false, file is deleted.  

                If a fatal error occurs while running a script using errorLogger
                it SHOULD ALWAYS BE be closed with "close(debug=True)" which 
                will override the global debug variable and leave the logfile 
                intact for further analysis. 
        
        screendump:      Dumps the content of the logfile to the STDOUT.
        
        read:            Returns a list object with each line of the logfile as 
                         an element.
                         
        write(message):  Writes 'message' to the logfile.
        
    :RETURNS:
    
        An object by which a message can be written to a logfile. 
        
        The method read() returns a list object with each line of the logfile as 
        an element.
        
        There are no other returns.
        
    :USAGE:
        log = errorLogger(name_of_calling_script, 
                          [debug = True/False, screendump = True/False]
                          )

        ...OR...
        
        with  errorLogger(name_of_calling_script, 
                          [debug = True/False, screendump = True/False]
                          ) as log:                          
        
                          
        log.write(message_text)
        list_object = log.read()
        log.screendump()
        log.close() # Removes logfile 
    """
    # ________________________________________________________________________
    # __init__
    def __init__(self, 
                 caller, 
                 debug      = False, 
                 screendump     = False, 
                 ):
        """
        """
        self.caller     = caller
        self.logfile    = ''.join(["./", str(caller), ".error.log"])
        self.screen     = screendump
        self.debug      = debug
        self.closed = False
        
        self._start()
        
    # ________________________________________________________________________
    # _cleanup
    def _cleanup(self, debug = False):
        """
        Always pass 'debug' specifically so it can be 
        overridden in error situations. 

        If debug is true...do nothing (leave the file). 
        """        
        if self.closed is False:
            if debug is False:
                try:
                    os.remove(self.logfile)
    
                except Exception, e:
                    pass
    
            else:
                self.write(("Retaining errorLogger temp log file " + 
                            self.logfile))
                self.write("errorlogger.errorLogger object terminated")
                    
            try:
                if self.caller in logging.Logger.manager.loggerDict.keys():
                    del logging.Logger.manager.loggerDict[self.caller]
            except Exception, e:
                pass
            
            # Flag just to get rid of annoying multiple close reports
            # Aesthetic only
            self.closed = True 

    # ________________________________________________________________________
    # __del__
    def __del__(self):
        self.close()
        
    # ________________________________________________________________________
    # __enter__
    def __enter__(self):
        return self
    
    # ________________________________________________________________________
    # __exit__
    def __exit__(self, type, value, traceback):
        self.close()
        
    # ________________________________________________________________________
    # _read (private method for internals only)
    def _read(self):
        """"""
        _list = open(self.logfile, "r", 0).read().splitlines()
        return _list

    # ________________________________________________________________________
    # _start
    def _start(self):
        try:    
            # create self.logger with 'spam_application'
            self.logger = logging.getLogger(self.caller)
            self.logger.setLevel(level=10)  # Always debug
            self.formatter = logging.Formatter(
                        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
            # create file handler which logs even debug messages
            self.fh = logging.FileHandler(self.logfile)
            self.fh.setLevel(level=10) # Always debug
            self.fh.setFormatter(self.formatter)

            # create console handler with a higher log level
            if self.screen:
                self.ch = logging.StreamHandler()
                self.ch.setLevel(level=10)  # Always debug
                self.ch.setFormatter(self.formatter)
            else:
                self.ch = False
                    
            # add the handlers to the logger
            if self.fh: self.logger.addHandler(self.fh)
            if self.ch: self.logger.addHandler(self.ch)

        except Exception, e:
                e = ''.join(["Unable to open errorlog: '", 
                            str(self.logfile), 
                            ". ", 
                            str(e)]
                            )
                raise IOError(e)
        
    # ________________________________________________________________________
    # close() 
    def close(self, debug = None):
        ## Option for debug override at close
        if debug is not None:
            self._cleanup(debug)
        else:
            self._cleanup(self.debug)

    # ________________________________________________________________________
    # screendump()
    def screendump(self):
        try:
            errorlist = self._read()
            for line in errorlist:
                print str(line)
                 
        except Exception, e:
            e = ''.join(["Unable to dump errorlog: '", 
                        str(self.logfile), 
                        " to screen. ", 
                        str(e)]
                        )
            raise IOError(e)
            
    # ________________________________________________________________________
    # read()
    def read(self):
        """
        Always returns a list. 
        Each element is a line from the file. 
        """
        _list = self._read()
        return _list
    

    # ________________________________________________________________________
    # write()
    def write(self, message):
        """
        """
        self.logger.debug(str(message))
                
#test
if __name__ == "__main__":
    print; print "Creating errorLogger object with screen and file output..."
    o = errorLogger('errorLogger', screendump=True)
    print "Done."

    print; print "errorLogger.write()..."
    o.write("This is a test.")
    o.write("This is a test AGAIN.")
    import time
    time.sleep(0.5)
    print "Done."        
    
    print; print "errorLogger.screendump()..." 
    print "-------------------------------------------------------"    
    o.screendump()
    print "-------------------------------------------------------"    

            
    print; print "errorLogger.read()..."
    l = o.read()
    print "result: ", l
    print "Done." 

    print; print "Closing errorLogger object (removing file)..."
    o.close()
    print "Done." 
               