#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @File    : util_check.py
# @Time    : 2021-07-23
# @Author  : Skypekey

"""Some check method."""

import traceback
from typing import Any, Union, List, Dict

from user_tools.exception import util_exception


def check_arg(arg: Any, arg_type: str, arg_format: Union[Dict, List] = [],
              type: str = "") -> Union[bool, str]:
    """Check whether the parameters are correct.

    :param arg(Any): The parameter.
    :param arg_format(Dict|list): 
        Format for each parameter.
        The key of the dict is the parameter name.
        The value is a dict or a list. 
            When only the verification type is required, it's a list, otherwise it's dict.
            For dict, it has three key: type, exist, isnull, format.
                The type is a str, means the type of parameter. Depends on the official standard of Python.
                The exist is a bool, means whether the parameter is required. default is True.
                The isnull is a bool, means whether the parameter can be null, default is False.
                The value type of format is depends on the type. Default is None, means no format check.
                    for str, it is a dict, it has two key: start, end
                    for bool, it is None or an empty string.
                    for dict, it is a dict, it has two key: arg_list, arg_format. means judge again by this method.
                    for float or int, it is a dict, it has three key: min, max, decimal(means number of decimal places)
    :param type(str): When the types are consistent, use this parameter.

    :return(bool|str): The result of check or the error info.
    """

    try:
        def check_type(ct_str, ct_type):
            if ct_type == 'int':
                ct_type = int
            elif ct_type == 'float':
                ct_type = float
            elif ct_type == 'bool':
                ct_type = bool
            elif ct_type == 'complex':
                ct_type = complex
            elif ct_type == 'str':
                ct_type = str
            elif ct_type == 'list':
                ct_type = list
            elif ct_type == 'tuple':
                ct_type = tuple
            elif ct_type == 'set':
                ct_type = set
            elif ct_type == 'dict':
                ct_type = dict
            else:
                raise util_exception.ParameterException(f'{ct_type} is not a standard data type!')
            
            if isinstance(ct_str, ct_type):
                return True
            else:
                return False

        def check_null(ct_str, ct_type):
            checknum = ct_type not in ("int", "float", "bool", "complex")
            if checknum and not ct_str:
                return False
            else:
                return True

        if arg_format == []:
            if check_type(arg, arg_type) and check_null(arg, arg_type):
                return True
            else:
                return False
        elif arg_type != 'dict':
            raise util_exception.ParameterException('arg only supports str, list, dict!')

        if check_type(arg, 'str'):
            pass
        elif check_type(arg, 'list'):
            pass
        else:
            pass

    except Exception as e:
        return f'check_arg has an exception: {traceback.format_exc().strip()}!'


if __name__ == "__main__":
    pass
