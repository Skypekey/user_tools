#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @File    : util_xlsx.py
# @Time    : 2022-10-22
# @Author  : Skypekey


import openpyxl
from typing import Union, List
from pathlib import Path
from user_tools.file import util_file


def xlsx2json(file_path: Union[str, Path], encoding: str = "GBK") -> Union[None, str]:
    """Convert the contents of the Excel file to data in json format.

    :param file_path(str): The path of the file which to be read.\n
    :param encoding(str): Encoding format to write csv file, default is "GBK".\n

    :return(flag, strings):
        flag(bool): means success or failure.
        strings(str): if flag is True, means the content of Excel is in json mode, otherwise means error or exception info.
    """

    try:

        return (True, )
    except Exception as e:
        return (False, f' has an exception: {str(e)}!')


def jsonlist2xlsx(jsonlist: List, file_path: Union[str, Path], fieldnames: List = [],
                  encoding: str = "UTF-8") -> Union[None, str]:
    """Write the contents of jsonlist to file_path.

    :param file_path(str): File to be written.\n
    :param jsonlist(list): What will be written to the file_path.\n
    :param encoding(str): Encoding format to write csv file, default is "UTF-8".\n
    :return(None|str): No return value of the error info."""

    try:
        hp_result = util_file.handle_path(file_path, 'c_exist')
        if hp_result.count(True) != 2:
            return f'File creation failed: {hp_result[1]}!'
        if jsonlist == [] and fieldnames == []:
            return 'Both jsonlist and fieldnames are empty!'

    except Exception as e:
        return f'jsonlist2csv has an exception: {str(e)}!'


if __name__ == "__main__":
    pass
