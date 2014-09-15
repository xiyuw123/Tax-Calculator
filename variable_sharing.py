'''
This file contains a mockup of a class that could be used to facilitate variable
sharing between functions as well as clarify where a particular variable is 
defined/coming from.

'''


class ParameterSet(object):
    """This is a mock-up implementation of a class to house parameters
    either read in from some file or created while running the taxcalc code.
    """
    def __init__(self, parameter_dict):
        # the idea here is that we pass a dictionary of parameters mapped
        # onto arrays with values and use these to generate object attributes.
        # We could potentially make this a bit more fancy and include some
        # file IO logic ()
        self.__dict__.update(parameter_dict)


# Here's how this would be used.

# Instead of the following code for the capital gains function
def CapGains():
    global _ymod
    global _ymod1
    global c02700
    global c23650
    global c01000
    c23650 = c23250 + e22250 + e23660 
    c01000 = np.maximum(-3000/_sep, c23650)
    c02700 = np.minimum(_feided, _feimax[2013-FLPDYR] * f2555) 
    _ymod1 = (e00200 + e00300 + e00600 + e00700 + e00800 + e00900 + c01000 
        + e01100 + e01200 + e01400 + e01700 + e02000 + e02100 + e02300 + e02600 
        + e02610 + e02800 - e02540)
    _ymod2 = e00400 + (0.50 * e02400) - c02900
    _ymod3 = e03210 + e03230 + e03240 + e02615
    _ymod = _ymod1 + _ymod2 + _ymod3


# we'd have something like this:
calc_vars = ParameterSet({})
puf_vars = ParameterSet(puf_dictionary_from_file)
planX_vars = ParameterSet(planX_dictionary_from_file)

def CapGains(puf_vars, planX_vars, calc_vars):
    calc_vars.c23650 = puf_vars.c23250 + puf_vars.e22250 + puf_vars.e23660 
    calc_vars.c01000 = np.maximum(-3000/calc_vars.sep, calc_vars.c23650)
    calc_vars.c02700 = np.minimum(calc_vars.feided, planX_vars.feimax[2013-FLPDYR] * f2555) 
    calc_vars.ymod1 = (
    puf_vars.e00200 + 
    puf_vars.e00300 + 
    puf_vars.e00600 + 
    puf_vars.e00700 + 
    puf_vars.e00800 + 
    puf_vars.e00900 + 
    puf_vars.c01000 + 
    puf_vars.e01100 + 
    puf_vars.e01200 + 
    puf_vars.e01400 + 
    puf_vars.e01700 + 
    puf_vars.e02000 + 
    puf_vars.e02100 + 
    puf_vars.e02300 + 
    puf_vars.e02600 + 
    puf_vars.e02610 + 
    puf_vars.e02800 - 
    puf_vars.e02540)
    ymod2 = e00400 + (0.50 * e02400) - c02900
    ymod3 = e03210 + e03230 + e03240 + e02615
    calc_vars.ymod = calc_vars.ymod1 + ymod2 + ymod3

    return calc_vars

# This also opens up possibilities to define functions like sum to try and
# calculations like ymod1 look a bit less hairy.