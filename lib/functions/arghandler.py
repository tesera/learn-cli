
from errorhandler   import handlertry
from errorhandler   import raisetry

@handlertry("FATAL: rhandler._override_with_kw_vars")
def override_kw_vars(self, kwargs):
    for key in kwargs.keys():
        self.config.__dict__[key] =  kwargs[key]
    return True

def set_mandatory_defaults(self, _dict):
    """
    In the event the config file does not have the mandatory variables, 
    and they are not passed in as __init__ variables, they can be set here.
    These defaults can be modified. The order of setting defaults should be:
    1. config file
    2. __init__ parameters
    3. Here (_set_mandatory_defaults) 
    """
    for key in _dict.keys():
        if key not in self.config.__dict__.keys():
            self.config.__dict__[key] = _dict[key]
    return
