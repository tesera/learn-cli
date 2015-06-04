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

def _format_original_error(e):
    return "".join([str(e), ". "])
#         return "".join(["[Original error: ", str(e), "]"])

def _log_error(message, e):
    # Format message
    e = "".join([str(_format_original_error(e)), message])
    # Send to log
    log.error(e)
    return

