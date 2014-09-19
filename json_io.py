# coding: utf-8
''' This file provides functionality for reading properties files and updating
them.
'''

# we need numpy and json libraries as well as regex support
import numpy as np
import json
import re

# local aliases for json functions
dump = json.dump
loads = json.loads

COMMENT_REGEX = re.compile('(?:#|//).*')


def load_commented_json(file_name, comment_rgx=COMMENT_REGEX):
    '''This function allows us to load JSON files containing both python
    and JavaScript inline comments.
    comment_rgx can optionally be set to something else.
    Returns serialized python object.
    '''
    with open(file_name) as json_file:
        file_str = json_file.read()
    no_comments = comment_rgx.sub('', file_str)
    return loads(no_comments, object_hook=list_to_array)


def read_plans(planX_file_name, planY_file_name=None):
    '''Given file names for the plan X and plan Y files reads them both in 
    (assuming they're formatted in JSON), prints which parameters differ
    between the two and updates plan X with parameters from plan Y.
    '''
    # load planX
    planX = load_commented_json(planX_file_name)

    if planY_file_name:
        # if given, load planY and proceed accordingly
        planY = load_commented_json(planY_file_name)

        print_different_params(planX, planY)
        # incorporate planY into planX
        return dict(planX, **planY)
    else:
        print 'No plan Y given.'
        return planX


# we define the function for converting lists to numpy arrays
def list_to_array(obj_dict):
    '''Takes dictionary read from json file and sets all values that are lists
    to numpy arrays.

    Example usage is given below.
    >>> json_str = ('{"retain_amtys" : [112500, 150000, 75000, 112500, 150000, 75000],'
    ... '"cphase" :[75000, 110000, 55000, 75000, 75000, 55000],'
    ... '"rt6" : 0.35}')
    >>> smpl_py_obj = json.loads(json_str, object_hook=list_to_array)
    >>> print smpl_py_obj #doctest: +NORMALIZE_WHITESPACE
    {u'retain_amtys': array([112500, 150000,  75000, 112500, 150000,  75000]),
    u'cphase': array([ 75000, 110000,  55000,  75000,  75000,  55000]), 
    u'rt6': 0.35}
    '''
    # for every in dictionary
    for key in obj_dict:
        # check if corresponding value is a list
        if isinstance(obj_dict[key], list):
            # if it is, set it to numpy array
            obj_dict[key] = np.array(obj_dict[key])
    return obj_dict


def print_different_params(planX, user_planY):
    '''Given plan X and plan Y (which can contain user modifications), prints 
    the differing parameters.
    '''
    message = 'User passed different param "{param}". Default is {default}'
    if not user_planY:
        print 'Seems like PlanY has no entries at all.'

    for param in planY:
        if planX[param] != user_planY[param]:
            print message.format(param=param, default=planX[param])
    print ("Done comparing. "
        "If you didn't see any messages, none of the user-defined parameters "
        "differed from their defaults.")


# class for converting json "lists" into numpy arrays
class NumpyArrayJSON(json.JSONEncoder):
    """This class allows us to serialize numpy arrays to JSON.
    It is currently very simple (I've seem more sophisticated code posted online)
    but it gets the job done for now.
    """
    def default(self, obj):
        # if obj is an numpy's ndarray type, make it a list
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        # otherwise return regular JSONEncoder default method
        return super(NumpyArrayJSON, self).default(obj)     


if __name__ == '__main__':
    # if module is run on its own (as opposed to being imported), run doctest
    import doctest
    doctest.testmod()
    