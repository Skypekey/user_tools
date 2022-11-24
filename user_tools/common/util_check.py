#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @File    : util_check.py
# @Time    : 2021-07-23
# @Author  : Skypekey

"""Some check method."""

import traceback
from typing import Any, Union, List

from user_tools.exception import util_exception

FILENAME = 'util_check'


def check_arg(arg: Any, arg_format: Union[str, object, List[str, object]], method: str = "type") -> Union[bool, str]:
    """Check the parameters.

    :param arg(Any): The parameter.
    :param arg_format(str|object|list[object|str]):
        arg_format can be an object, a str or a list whose element is an object or a str, means arg type belong to arg_format or means arg is not null

    :return(flag, strings):
        flag(bool): means success or failure.
        strings(str): if flag is True, means the check successfully, otherwise means error or exception info."""

    try:
        def _check_type(ct_str, ct_type):
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
            elif isinstance(ct_type, object):
                ct_type = ct_type
            else:
                raise util_exception.ParameterException(
                    f'{ct_type} is not a standard data type!')

            if isinstance(ct_str, ct_type):
                return True
            else:
                return False

        def _check_null(cn_str, cn_type):
            if not _check_type(cn_str, cn_type):
                raise util_exception.ParameterException(
                    f'{cn_str} is not {cn_type} object.')

            if isinstance(cn_type, object):
                cn_type = cn_type.__name__

            # When it is a number, no matter what it is, return True
            checknum = cn_type not in ("int", "float", "bool", "complex")
            if checknum and not cn_str:
                return False
            else:
                return True

        def _check(method, arg, arg_format):
            if method == 'type':
                return _check_type(arg, arg_format)
            elif method == "null":
                return _check_null(arg, arg_format)
        
        result = True

        if method not in ('type', 'null'):
            raise util_exception.ParameterException("method must be type or null.")

        if _check_type(arg_format, list):
            for i in arg_format:
                if not (_check_type(i, object) and _check_type(i, str)):
                    raise util_exception.ParameterException(
                        "when arg_format is a list, element of arg_format must be an object, a str or a list.")
                elif not _check(method, arg, i):
                    result = False
                    break

        elif not (_check_type(arg_format, object) and _check_type(arg_format, str)):
            raise util_exception.ParameterException(
                "arg_format must be an object, a str or a list.")
        else:
            result = _check(method, arg, arg_format)

        return (True, result)
    except Exception as e:
        return (False, f'[{FILENAME}]:check_arg has an exception: {traceback.format_exc().strip()}!')


if __name__ == "__main__":
    pass
