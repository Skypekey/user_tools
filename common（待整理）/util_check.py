#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @File    : util_check.py
# @Time    : 2021-07-23
# @Author  : Skypekey


"""Some checks on files or directories."""

import re
from typing import Dict, List, Tuple, Union
import threading
import socket
from user_tools.exception import util_exception


def check_ip(ip: str) -> bool:
    """Test whether the IP is valid.

    :param ip(str): The IP that needs to be judged.\n
    :return(bool): Returns whether url is valid.\n
        Return False, if the IP is not legal."""

    ip_rex = r'(?=(\b|\D))(((\d{1,2})|(1\d{1,2})|(2[0-4]\d)|(25[0-5]))\.)' + \
        r'{3}((\d{1,2})|(1\d{1,2})|(2[0-4]\d)|(25[0-5]))(?=(\b|\D))'

    is_legal = re.match(re.compile(ip_rex), ip)
    if is_legal:
        return True
    else:
        return False


def check_url(url: str, style: str = "http") -> bool:
    """Test whether url is valid.

    :params url(str): The url that needs to be judged.\n
    :return(bool): Returns whether url is valid.\n
        Return False, if the style is not web or git.
    """

    result = False
    if style == "http":
        result = True if re.match(r'^https?:/{2}\w.+$', url) else False
    elif style == "git":
        result = True if re.match(
            r'^(http(s)?:\/\/([^\/]+?\/){2}|git@[^:]+:[^\/]+?\/).*?.git$', url
        ) else False
    return result


def check_arg(arg_list: List, arg_format_dict: Dict) -> Tuple(bool, Union[bool, str]):
    """Check whether the parameters are correct.

    :param arg_list(List): List of parameters.
    :param arg_format_dict(Dict): 
        Format for each parameter.
        The key of the dict is the parameter name.
        The value is also a dict. It has three key: exist, type, isnull, format.
            The exist is a bool, means whether the parameter is required. default is True.
            The type is a str, means the type of parameter. Depends on the official standard of Python.
            The isnull is a bool, means whether the parameter can be null.
            The value type of format is depends on the type. The format can be None, means no format check.
                for str, it is a dict, it has two key: start, end
                for bool, it is None or an empty string.
                for dict, it is a dict, it has two key: arg_list, arg_format_dict. means judge again by this method.
                for float or int, it is a dict, it has three key: min, max, decimal(means number of decimal places)

    :return Tuple(bool, Any): 
        If there is no error, return (True, True),
        otherwise False and an error message is returned.
    """

    try


def check_port(IP, Port, protocol="tcp", timeout=1):
    """Check whether the Port on IP is open.

    :param IP(str): The IP that needs to be checked.\n
    :param Port(int): The Port on IP that needs to be checked.\n
    :param timeout(int): Timeout period.

    :return Tuple(bool, Any): If there is no error, return (True, ""),
        otherwise False and an error message is returned."""

    threadlock = threading.Lock()
    flag = False
    result = ""
    socket.setdefaulttimeout(timeout)
    try:
        if protocol.lower() == "tcp":
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif protocol.lower() == "udp":
            conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            return (False, "The protocol only can be TCP or UDP")
        conn.connect((IP, Port))
        threadlock.acquire()
        flag = True
    except Exception as e:
        threadlock.acquire()
        result = str(e)
    finally:
        threadlock.release()
        conn.close()
        return (flag, result)


if __name__ == "__main__":
    pass
