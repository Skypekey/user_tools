# -*- coding: UTF-8 -*-
# @Author: coinren
# @Filename: util_network
# @Time: 2022-11-24 13:53:40

import re
import socket
import threading
import traceback
from typing import Tuple, Any

FILENAME = 'util_network'


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


def check_port(IP, Port, protocol="tcp", timeout=1) -> Tuple[bool, Any]:
    """Check whether the Port on IP is open.

    :param IP(str): The IP that needs to be checked.\n
    :param Port(int): The Port on IP that needs to be checked.\n
    :param timeout(int): Timeout period.

    :return Tuple[bool, Any]: If there is no error, return (True, ""),
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
        result = traceback.format_exc().strip()
    finally:
        threadlock.release()
        conn.close()
        return (flag, result)


if __name__ == "__main__":
    pass
