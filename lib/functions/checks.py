##############################################################################
# Removal of the "__license__" line or content from  "__license__", or removal 
# of "__author__" in this or any constituent # component or file constitutes a 
# violation of the licensing and copyright agreement. 
__author__      = "Mike Rightmire"
__copyright__   = "BioCom Software"
__license__     = "Tesera"
__license_file__= "Clause1.PERPETUAL_AND_UNLIMITED_LICENSING_TO_THE_CLIENT.py"
__version__     = "0.9.0.7"
__maintainer__  = "Mike Rightmire"
__email__       = "Mike.Rightmire@BiocomSoftware.com"
__status__      = "Development"
##############################################################################

import os.path
import re
import sys

def check(type, line, *args, **kwargs):
     
    if re.match("^.*path.*$", str(line).lower()):
        fullPathCheck(line) 

def fullPathCheck(line, *args, **kwargs):
    """
    INCOMPLETE
    """
    line = str(line)

    if ((line.endwith("\\")) or
        (line.endswith("/"))):
        endslash = True
        
    if (not checkPathFormat(line, endslash = endslash)): return False
    
        
def checkDict(_dict):
    try:
        _dict.keys()
        return True
    except (AttributeError):
        return False
    
def checklist(_list):
    try:
        _list.append("DELETEMELISTCHECKVARIABLE")
        _list.pop(len(_list)-1)
    except AttributeError, e:
        return False
    except Exception, e:
        raise
    return True

def checkObject(obj):
    if (
        ("object" in str(obj).lower()) or
        ("instance" in str(obj).lower())
         ):
        return True
    else:
        return False

def checkWindowsPathFormat(_path, endslash = False):
    _path = str(_path)

    wp = re.compile("^(([a-zA-Z]:\\\)|(\.\\\)|(\.\.\\\)).*$")

    if not re.match(wp, _path): return False

    if endslash:
        if _path[-1:] == "\\": return True
        else: return False

# Don't remember why this is here        
#     _path = str(_path).encode('string-escape')
    
def checkLinuxPathFormat(_path, endslash = False):
    _path = str(_path)
    
    lp = re.compile("^((\./)|(\.\./)|(/)).*$")

    if not re.match(lp, _path): return False
    
    #Must come after re.match
    if endslash:
        if _path[-1:] == "/": return True
        else: return False

# Don't remember why this is here        
#     _path = str(_path).encode('string-escape')

def checkPathFormat(_path, endslash = False):
    _path = str(_path)
    if   checkWindowsPathFormat(_path, endslash): return True
    elif checkLinuxPathFormat(_path, endslash)  : return True
    else: return False
    
def pathExists(_path):
    """
    Check that a full path exists when ONLY the full path is _path
    
    This differs from directoryExists, which checks (ONLY) that the full path 
    exists when _path is the full path PLUS THE FILENAME. 
    """
    if os.path.exists(_path): return True
    else: return False

def fullPathExists(_path, create = False):
    """
    :NAME:
        fullPathExists(path)

    :DESCRIPTION:
        Intended to check the existence of ONLY the path assuming a full path
        with filename included is passed.
        
        This differs from pathExists, which checks that the full path 
        exists when _path is the full path WITHOUT THE FILENAME.
        
        fullPathExists ONLY checks that the path exists. NOT the filename.
 

    :ARGUMENTS:
        path:    The full path WITH FILNEMAE I.e "/dir1/dir2/filename.ext"
        create:  (True/False) If path does NOT exist, but create is True,
                 path will be created and True returned. 
    :USAGE:
        if fullPathExists("/dir1/dir2/filename.ext"):
            print "The directory is there. I haven't check for the filename".
        else:
            print "'/dir1/dir2' does not exist."
    """
    _path = str(_path)
    _path = os.path.dirname(_path)
    
    if pathExists(_path):
        return True
    
    else:
        if create == True:
            try:
                os.makedirs(_path)
                return True

            except Exception as e:
                return False
#                 e.message = ''.join(["From 'checks.fullPathExists()': ", 
#                                      "Directory '", 
#                                      str(_path), 
#                                      "' does not exist and an error occurred ", 
#                                      "trying to create it. ", 
#                                      e.message])
#                 raise type(e)(e.message)                
            
        else:
            return False
        
#     return pathExists(_path)    
            
#=============================================================================
#=============================================================================
# DEPRICATED. USE fullPathExists            
def directoryExists(_path, create = False): # This name needs to be depricated
    """
    :NAME:
        directoryExists(path)

    :DESCRIPTION:
        Intended to check the existence of ONLY the path assuming a full path
        with filename included is passed.
        
        This differs from pathExists, which checks that the full path 
        exists when _path is the full path WITHOUT THE FILENAME.
        
        directoryExists ONLY checks that the path exists. NOT the filename.
 

    :ARGUMENTS:
        path:    The full path WITH FILNEMAE I.e "/dir1/dir2/filename.ext"
        create:  (True/False) If path does NOT exist, but create is True,
                 path will be created and True returned. 
    :USAGE:
        if directoryExists("/dir1/dir2/filename.ext"):
            print "The directory is there. I haven't check for the filename".
        else:
            print "'/dir1/dir2' does not exist."
    """
    _path = str(_path)
    _path = os.path.dirname(_path)
    
    if pathExists(_path):
        return True
    
    else:
        if create == True:
            try:
                os.makedirs(_path)
                return True

            except Exception as e:
                return False
#                 e.message = ''.join(["From 'checks.directoryExists()': ", 
#                                      "Directory '", 
#                                      str(_path), 
#                                      "' does not exist and an error occurred ", 
#                                      "trying to create it. ", 
#                                      e.message])
#                 raise type(e)(e.message)                
            
        else:
            return False
        
#     return pathExists(_path)
#=============================================================================
#=============================================================================

def fileExists(_file):
    _file = str(_file)
    if os.path.isfile(_file): return True
    else: return False


def checkURL(URL):
    """"""
    URL = str(URL)
    def _runerror(URL):
        e = ("INTERR03: URL: '" + 
             str(URL) + 
             "' does not match expected format.")        
        raise NameError(e)
    
    URL = str(URL)
    URL = URL.lstrip()
    URL = URL.rstrip()
    
    pattern = ("^(https?){0,1}"        +               # http/https
                "(://){0,1}"            +               # ://
                "(\w+\.){0,}" +                  # Prefix [I.e. www.] (Optional)
                "((\w+)(\.\w\w+)"    +   # Server.xx (mandatory)
                "|" +                            # servername OR IP
                "(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))" + # OR IP (mandatory)  
                "(:\d+){0,1}" + # port (mandatory)
                "(\/\.*){0,}"    +   # remainder
               "$")
    pattern = re.compile(pattern, re.IGNORECASE)

    if pattern.match(URL):
        return True

    elif re.match("^\s*(https?://){0,1}localhost\s*[/\.]{0,}$", str(URL), re.IGNORECASE):
        return True
    
    else: 
        _runerror
        return False
    
def checkOS(os = None):
    """
    checkOS(['os'])
    
    DESCRIPTION
        checkOS returns either the OS platform (if called with no option), 
        or a True/False if the passed option matches the OS type.
        
    OPTIONS
        os = a STRING containing the name of the os to be identified. If the 
             platform matches the 'os', checkOS will return True, 
             otherwise it returns False.
             
            Acceptable 'os' parameters are:
                windows = T if windows OS
                win     = T if windows OS
                win32   = T if windows 32 bit specifically
                win64   = T if windows 64 bit specifically
                freebsd = T if FreeBSD specifically
                gnu     = T if GNU OS specifically
                linux   = T if linux, or GNU, or FreeBAD
                unix    = T if Solaris, or riscos, or FreeBSD
                *nix    = T if linux, or GNU, or FreeBAD, or Solaris, 
                          or riscos, or FreeBSD
                risc    = T is riscos
                atheos  = T is atheos
                solaris = T if solaris, or sunos
    """
    
    def _windows_os():
        if sys.platform.startswith('win'): return True
        else: return False
    
    def _linux_os():
        if sys.platform.startswith('linux'): return True
        else: return False
        
    def _osx_os():
        if sys.platform.startswith('darwin'): return True
        else: return False                
    
    def _cygwin_os():
        if sys.platform.startswith('cygwin'): return True
        else: return False
        
    def _os2_os():
        if sys.platform.startswith('os2'): return True
        else: return False
        
    def _os2emx_os():
        if sys.platform.startswith('os2emx'): return True
        else: return False
        
    def _riscos_os():
        if sys.platform.startswith('riscos'): return True
        else: return False
        
    def _atheos_os():
        if sys.platform.startswith('atheos'): return True
        else: return False                

    def _sun_os():
        if sys.platform.startswith('sunos'): return True
        else: return False
                
    def _freebsd_os():
        if sys.platform.startswith('freebsd'): return True
        else: return False

    def _gnu_os():
        if sys.platform.startswith('gnu'): return True
        else: return False
                                
    def _unknown_os():
        return sys.platform    

    _os = str(os).lower()
    
    if os is None: return sys.platform
    
    elif sys.platform == _os: return True
    
    elif ((_os == "win") or (_os == "w") or (_os == "windows")): 
        return _windows_os()

    elif ((_os == "g") or (_os == "gnu")):
        return _gnu_os()

    elif ((_os == "lin") or (_os == "l") or (_os == "linux")):
        if _linux_os() or _gnu_os() or _freebsd_os(): 
            return True
        else:
            return False
    
    elif ((_os == "freebsd") or (_os == "free") or (_os == "bsd")):
          return _freebsd_os()
     
    elif ((_os == "mac") or (_os == "osx") or (_os == "darwin") or 
          (_os == "dar") or (_os == "apple")):
        return _osx_os()

    elif ((_os == "cygwin") or (_os == "cyg") or (_os == "c")):
        return _cygwin_os()
      
    elif ((_os == "os2emx") or (_os == "emx")):
        return _os2emx_os()

    elif ((_os == "os2")):
        return _os2_os()

    elif ((_os == "risc") or (_os == "riscos")):
        return _riscos_os()

    elif ((_os == "atheos") or (_os == "athe") or (_os == "ath")):    
        return _atheos_os()        
    
    elif ((_os == "solaris") or (_os == 'sol') or (_os == 'sun')):
        return _sun_os()
    
    elif ((_os == 'unix')):
        if _freebsd_os() or _sun_os() or _riscos_os(): 
            return True
        else:
            return False

    elif ((_os == 'nix') or (_os == '*nix')):
        if (_freebsd_os() or _sun_os() or _riscos_os() or 
            _linux_os() or _gnu_os()): 
            return True
        else:
            return False
        
    elif ((_os == "win32") or (_os == "w32") or (_os == "x32") or 
          (_os == "windows32") ):
        if str(sys.platform) == "win32": 
            return True
        else:
            return False

    elif ((_os == "win64") or (_os == "w64") or (_os == "x64") or
          (_os == "ia64") or (_os == "windows64") ):
        if str(sys.platform) == "win64": 
            return True
        else:
            return False
        
    else: return False
    
if __name__ == "__main__":
    print checkURL('https://127.0.0.1/./')
    