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


class CustomError(Exception):
    """
    Base user extensible exception class
    Baseclass for dealing with unhandled errors
    Extends class Exception
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


class FatalException(CustomError):
    """
    raise FatalSocketError
    Returns default error + the attached string message
    "Socket encountered a fatal condition. "
    
    EVENTUALLY this needs to cleanly close out the current processes, and 
    return the user to the start GUI. For now, it creates program halt.   
    """
    def __init__(self, message = None):
        self.message = ("")
        CustomError.__init__(self, self.message)
