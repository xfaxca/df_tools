# _err_check.py

"""
This module provides functions for error checking to use either for other
df_tools modules or otherwise.

Functions:
check_ls, check_eq_ls_len, check_numeric, check_int, check_string, check_bool,
check_dfs, param_exists_in_set, check_threshold, parent_fn_mod_2step, parent_fn_mod_3step.

Please see the doc strings of individual functions for further information.
"""

from inspect import *
import pandas as pd
import numpy as np
import sys

__all__ = ['check_ls',
           'check_eq_ls_len',
           'check_numeric',
           'check_int',
           'check_string',
           'check_bool',
           'check_dfs',
           'param_exists_in_set',
           'check_threshold',
           'parent_fn_mod_2step',
           'parent_fn_mod_3step']


def check_ls(ls):
    """
    This function checks if an object is a list. If not, it returns an error, noting that a list is required.

    Parameters:
    :param ls: Object to check. A list is expected.
    :return: Nothing.
    """
    if isinstance(ls, list):
        pass
    else:
        main_module, main_fn, main_lineno = parent_fn_mod_3step()
        calling_module, calling_fn, calling_lineno = parent_fn_mod_2step()
        print('On line %i in function %s of module %s' % (main_lineno, main_fn, main_module))
        print('     Error on line %i in module %s' % (calling_lineno, calling_module))
        print('         Invalid input for function %s' % calling_fn)
        sys.exit('          ERROR: A list is required.')

    return 0


def check_eq_ls_len(list_ls=[]):
    """
    This function checks a list of lists to ensure that they are all the same length. If they are not, an error is
        returned, and the script is exited.

    Parameters:
    :param list_ls: A list of lists in which each member's length will be compared to the others.
    :return: Nothing.
    """
    for ls_no in range(0, len(list_ls)-1):
        if len(list_ls[ls_no]) == len(list_ls[ls_no + 1]):
            pass
        else:
            main_module, main_fn, main_lineno = parent_fn_mod_3step()
            calling_module, calling_fn, calling_lineno = parent_fn_mod_2step()
            print('On line %i in function %s of module %s' % (main_lineno, main_fn, main_module))
            print('     Error on line %i in module %s' % (calling_lineno, calling_module))
            print('         Invalid input for function %s' % calling_fn)
            sys.exit('          ERROR: Length of at least 2 lists are unequal.')

    return 0


def check_numeric(values=[]):
    """
    This function checks to see if all values in a list are numerical. It passed tests with nans and strings. If a
        non-numerical value is found (by type cast to integer), then it an error is returned and the script stops. The
        resulting error will indicate the calling module, function and line number within the calling module.

    Parameters:
    :param values: A list of values to check to ensure that they are numeric. If they are not, an error is returned,
        and the script is exited.
    :return: Nothing.
    """
    # Todo: The following numpy types were not being recognized at a certain point during testing. The cause is
    # todo: unknown since they were initially working fine. Will work to re-implement them in future versions.
    # Problematic types: np.int128, no.float80, np.float96, np.float128, np.float256, np.uint128, np.int128

    numeric_types = (int, float, complex, np.int, np.int8, np.int16, np.int32, np.int64, np.float,
                     np.float16, np.float32, np.float64, np.uint8, np.uint16, np.uint32, np.uint64)
    for val, valnum in zip(values, range(len(values))):
        if isinstance(val, numeric_types):
            pass
        else:
            main_module, main_fn, main_lineno = parent_fn_mod_3step()
            calling_module, calling_fn, calling_lineno = parent_fn_mod_2step()
            print('On line %i in function %s of module %s' % (main_lineno, main_fn, main_module))
            print('     Error on line %i in module %s' % (calling_lineno, calling_module))
            print('         Non-numeric value "%s" found list at index %i!' % (val, valnum))
            sys.exit('         ERROR: All values must be of numerical type (int, float, complex, numpy.*.')
    return 0


def check_int(values=[]):
    """
    This function checks if every item in a list is an integer. Otherwise, it returns an error and exits the script.

    Parameters:
    :param values: List of values/objects that will be tested as to whether or not they are integers. If any are not,
        an error is returned, and the script is exited.
    :return: Nothing.
    """
    for val, valnum in zip(values, range(len(values))):
        if isinstance(val, int):
            pass
        else:
            main_module, main_fn, main_lineno = parent_fn_mod_3step()
            calling_module, calling_fn, calling_lineno = parent_fn_mod_2step()
            print('On line %i in function %s of module %s' % (main_lineno, main_fn, main_module))
            print('     Error on line %i in module %s' % (calling_lineno, calling_module))
            print('         Non-integer frame object "%s" found list at index %i!' % (val, valnum))
            sys.exit('         ERROR: All values must be integers.')
    return 0


def check_string(values=[]):
    """
    This function checks if every item in a list is an integer. Otherwise, it returns an error and exits the script.

    Parameters:
    :param values: List of values/objects that will be tested as to whether or not they are strings. If any are not,
        an error is returned and the script is exited.
    :return: Nothing.
    """
    for val, valnum in zip(values, range(len(values))):
        if isinstance(val, str):
            pass
        else:
            main_module, main_fn, main_lineno = parent_fn_mod_3step()
            calling_module, calling_fn, calling_lineno = parent_fn_mod_2step()
            print('On line %i in function %s of module %s' % (main_lineno, main_fn, main_module))
            print('     Error on line %i in module %s' % (calling_lineno, calling_module))
            print('         Non-string frame object "%s" found list at index %i!' % (val, valnum))
            sys.exit('         ERROR: All values must be strings.')
    return 0


def check_bool(values=[]):
    """
    This function checks whether or not a list of values are boolean. If not, returns an error, echos to the terminal
        and exits the script.
        
    Parameters:
    :param values: Values to check whether or not they are boolean (i.e., True/False)
    :return: Nothing
    """
    for val, valnum in zip(values, range(len(values))):
        if isinstance(val, bool):
            pass
        else:
            main_module, main_fn, main_lineno = parent_fn_mod_3step()
            calling_module, calling_fn, calling_lineno = parent_fn_mod_2step()
            print('On line %i in function %s of module %s' % (main_lineno, main_fn, main_module))
            print('     Error on line %i in module %s' % (calling_lineno, calling_module))
            print('         Non-bool object "%s" found list at index %i!' % (val, valnum))
            sys.exit('         ERROR: All values must be boolean (True/False).')

    return 0


def check_dfs(values=[]):
    """
    This function checks if every item in a list is a pandas DataFrame. If any are not, an error is returned, and the
        script is exited.
    
    Parameters:
    :param values: List of values/objects that will be tested as to whether or not they are pandas DataFrames.
    :return: Nothing.
    """
    for val, valnum in zip(values, range(len(values))):
        if isinstance(val, pd.DataFrame):
            pass
        else:
            main_module, main_fn, main_lineno = parent_fn_mod_3step()
            calling_module, calling_fn, calling_lineno = parent_fn_mod_2step()
            print('On line %i in function %s of module %s' % (main_lineno, main_fn, main_module))
            print('     Error on line %i in module %s' % (calling_lineno, calling_module))
            print('         Non-DataFrame object "%s" found in list at index %i!' % (val, valnum))
            sys.exit('         ERROR: All values must be pandas DataFrames.')
    return 0


def param_exists_in_set(value, val_set=[]):
    """
    This function checks if the passed value exists in a set of values
    :param value: The value to check for in the set.
    :param val_set: Set of values in which to check for parameter, value
    :return: Nothing
    """
    if value in val_set:
        pass
    else:
        main_module, main_fn, main_lineno = parent_fn_mod_3step()
        calling_module, calling_fn, calling_lineno = parent_fn_mod_2step()
        print('On line %i in function %s of module %s' % (main_lineno, main_fn, main_module))
        print('     Error on line %i in module %s' % (calling_lineno, calling_module))
        print('         Value "%s" not found in set: %s. Please use one of these values as input.' % (value, val_set))
        sys.exit('         ERROR: Incorrect parameter value.')

    return 0


def check_threshold(values=[], thresh=1.0, how='under'):
    """
    This function checks to see whether or not a numeric value is less than/equal to or greater than/equal to a
     given threshold value. If any are not, an error is returned, and the script is exited.

    Parameters:
    :param values: Values to check whether or not they are under or over a threshold, depending on the parameter 'how'
    :param thresh: A numerical threshold to which to compare each value in values.
    :param how: An option to test whether the values are 'under' (less than/equal to) or 'over' (greater than/equal to).
    :return:
    """
    # Check to make sure the arguments values and thresh are numeric (using check_numeric function in _err_check.py),
    # and that how is a string value, with 'over' or 'under' as the value.
    check_numeric(values=values)
    check_numeric(values=[thresh])
    check_string(values=[how])
    param_exists_in_set(value=how, val_set=['under', 'over'])

    for val in values:
        if how == 'under':
            if val <= thresh:
                pass
            else:
                main_module, main_fn, main_lineno = parent_fn_mod_3step()
                calling_module, calling_fn, calling_lineno = parent_fn_mod_2step()
                print('On line %i in function %s of module %s' % (main_lineno, main_fn, main_module))
                print('     Error at line %i in module %s' % (calling_lineno, calling_module))
                print('         Value (%0.2f) is over the maximum value of %0.2f' % (val, thresh))
                sys.exit('         ERROR: Parameter over maximum threshold.')
        elif how == 'over':
            if val >= thresh:
                pass
            else:
                main_module, main_fn, main_lineno = parent_fn_mod_3step()
                calling_module, calling_fn, calling_lineno = parent_fn_mod_2step()
                print('On line %i in function %s of module %s' % (main_lineno, main_fn, main_module))
                print('     Error at line %i in module %s' % (calling_lineno, calling_module))
                print('         Value (%0.2f) is under the minimum value of %0.2f' % (val, thresh))
                sys.exit('         ERROR: Parameter under minimum threshold.')

    return 0


def parent_fn_mod_2step():
    """
    This function finds the calling module, file, and line number 2 steps prior to the current function.

    Parameters:
    :return: calling module name, function name, and line number for 2 previous function calls ('2step')
    """
    return stack()[2].filename, stack()[2].function, stack()[2].lineno


def parent_fn_mod_3step():
    """
    This function finds the calling module, file and line number 3 steps prior to the current function.

    Parameters:
    :return: calling module name, function name, and line number for 3 previous function calls ('3step')
    """
    return stack()[3].filename, stack()[3].function, stack()[3].lineno