#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @File    : util_file.py
# @Time    : 2021-07-23
# @Author  : Skypekey


"""Some functions related to file operations."""
import datetime
from pathlib import Path
import pathlib
from typing import List, Union
from user_tools.common import util_time
from user_tools.exception import util_exception


def write_file(file_path: Union[str, Path],
               msg: str, mode: str = "a", encoding: str = "UTF-8") -> None:
    """Write the contents of msg to file_path.

    :param file_path(str): File to be written.\n
    :param msg(str): What will be written to the file_path.\n
    :param mode(str): How to write file, default is "a".\n
        Character Meaning\n
            'w'   open for writing, create if not exists.
                  truncating the file first.\n
            'x'   create a new file and open it for writing\n
            'a'   open for writing, create if not exists.
                  appending to the end of the file (default).\n
            'b'   binary mode.
                  If you use this, no encoding parameter is required\n
            't'   text mode (default).
            '+'   open a disk file for updating (reading and writing)\n
    :param encoding(str): Encoding format to write file, default is "UTF-8".\n
    :return(None): No return value."""

    if "b" not in mode:
        with open(file_path, mode, encoding=encoding) as f:
            f.write(msg)
    else:
        with open(file_path, mode) as f:
            f.write(msg)


def read_file(file_path: Union[str, Path], need_list: bool = False,
              binary: bool = False, encoding: str = "UTF-8") -> List[bool, Union[List, str]]:
    """Return the content of file_path.

    :param file_path(str): File to be read.\n
    :param binary(bool): How to read file, True means return bytes, otherwise return text.
    :param encoding(str): Encoding format to read file, default is "UTF-8".\n
    :return(list): The result contains two elements.
        The type of the first element is bool, means success or failure.
        The type of the second element is a string. The first element is True, means the contents of file_path, otherwise means exception info.
    """

    try:
        result = [True, ""]
        basepath = pathlib.Path(file_path)
        if handle_path(basepath, "type")[1] == "file":
            if binary:
                result[1] = basepath.read_bytes()
            else:
                msg = basepath.read_text(encoding=encoding)
                if need_list:
                    result[1] = []
                    for line in msg.split('\n'):
                        result[1].append(line.strip())
                else:
                    result[1] = msg
        else:
            raise util_exception.ParameterException(f'Path {file_path} is not a file path!')
    except Exception as e:
        return [False, f'handle_path has an exception: {str(e)}']


def handle_path(path: Union[str, Path], method: str) -> List[bool, Union[str, bool, List, int, float]]:
    """Handle path.

    :param path(str|Path): The path that needs to be judged.\n
    :param method(str): 
        exist: Test whether path exists.
        c_exist: Test whether path exists. if not exist, then create file.
        suffix: Return the suffix of path.
        type: Test whether path is file or dir.
        null: Test whether path is not null. If the path is directory and only have some empty directory, return True means is null.
        size: Return the size of path.
        ctime: Platform dependent:
            Return the time of most recent metadata change on Unix,
            Return the time of creation on Windows, expressed in seconds.
        atime: Return the last access time of path.
        mtime: Return the last modify time of path.

    :return(list): The result contains two elements.
        The type of the first element is bool, means success or failure.
        The type of the second element depends on method when the first element is True, otherwise it is a string means exception info.
        if method is exist, c_exist or null. it's bool.
        if method is suffix or type. it's string.
        if method is size. it's int.
        if method is ctime, atime or mtime. it's float
    """
    
    try:
        basepath = pathlib.Path(path)
        result = [True, ""]
        is_exist = basepath.exists()
        is_dir = basepath.is_dir()
        is_file = basepath.is_file()
        suffix = basepath.suffixes


        if method == 'exist':
            result[1] = is_exist
        elif method == 'c_exist':
            basepath.touch()
            result[1] = True
        elif method == 'suffix':
            result[1] = suffix
        elif method in ('type', 'null', 'size', 'ctime', 'atime', 'mtime'):
            if is_exist:
                stat = basepath.stat()
                if method == 'type':
                    if is_dir:
                        result[1] = 'dir'
                    elif is_file:
                        result[1] = 'file'
                    else:
                        raise util_exception.ParameterException(f'Type of {path} is not file or dir!')
                elif method == 'size':
                    result[1] = stat.st_size
                elif method == 'null':
                    result[1] = True if stat.st_size else False
                elif method == 'ctime':
                    result[1] = stat.st_ctime_ns
                elif method == 'atime':
                    result[1] = stat.st_atime_ns
                elif method == 'mtime':
                    result[1] = stat.st_mtime_ns
            else:
                raise util_exception.ParameterException(f'Path {path} is not exist!')
        else:
            raise util_exception.ParameterException(f'Method {method} is not exist!')
        return result
    except Exception as e:
        return [False, f'handle_path has an exception: {str(e)}']


def clear_file(logpath: Path, filename, format_str="%Y%m%d",
               lasttime=7, firsttime=30):
    """Clean up log files with time format. eg: get_vmax_info_20210204.log

    :param logpath(str): The path where the log file is located.\n
    :param filename(str): Distinguished name of the log file.\n
    :param format_str(str): Time format used to format time.\n
        Default is '%Y-%m-%d %H:%M:%S'.\n
        Commonly used format codes:\n
            %Y: Year with century as a decimal number.\n
            %m: Month as a decimal number [01,12].\n
            %d: Day of the month as a decimal number [01,31].\n
            %H: Hour (24-hour clock) as a decimal number [00,23].\n
            %M: Minute as a decimal number [00,59].\n
            %S: Second as a decimal number [00,61].\n
            %z: Time zone offset from UTC.\n
            %a: Locale's abbreviated weekday name.\n
            %A: Locale's full weekday name.\n
            %b: Locale's abbreviated month name.\n
            %B: Locale's full month name.\n
            %c: Locale's appropriate date and time representation.\n
            %I: Hour (12-hour clock) as a decimal number [01,12].\n
            %p: Locale's equivalent of either AM or PM.\n
    :param lasttime(int): log file retention time.\n
    :param firsttime(int): The date of the oldest file to look for.\n

    :return(str): Log file cleanup results.\n
        Empty string means success, Else failure"""

    error = "日志清理正常"
    try:
        for i in range(lasttime, lasttime + firsttime):
            basetime = datetime.datetime.now() - datetime.timedelta(days=i)
            ago_day = datetime.datetime.timestamp(basetime)
            timestr = util_time.format_time(ago_day, format_str=format_str)
            old_log_file = logpath / f"{filename}_{timestr}.log"
            if handle_path(old_log_file, 'exist').count(True) == 2:
                old_log_file.unlink()
    except Exception as e:
        error = f"日志清理出错，异常信息为{str(e)}"
    return error


if __name__ == "__main__":
    pass
