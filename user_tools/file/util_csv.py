#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @File    : util_csv.py
# @Time    : 2022-10-22
# @Author  : Skypekey

"""Some functions related to csv file operations."""

import csv
import traceback
from typing import List, Tuple, Union
from pathlib import Path

from user_tools.exception import util_exception
from user_tools.file import util_file


def csv2list(arg_filepath: Union[str, Path]) -> Tuple[bool, Union[str, List]]:
    """Convert the contents of the csv file to data in json format.

    :param arg_filepath(str): The path of the file which to be read.\n

    :return(flag, strings):
        flag(bool): means success or failure.
        strings(str|list): if flag is True, means the content of csv is in json mode, otherwise means error or exception info."""

    try:
        if not (isinstance(arg_filepath, Path) and isinstance(arg_filepath, str)):
            raise util_exception.ParameterException(f"{arg_filepath} is not str or pathlib.Path")
        
        csvlist = []
        with open(arg_filepath,'rt') as f: 
            rows = csv.DictReader(f)
            for row in rows:
                csvlist.append(row)
        return (True, csvlist)

    except Exception as e:
        return (False, f'csv2list has an exception: {traceback.format_exc().strip()}!')


def list2csv(listinfo: List, arg_filepath: Union[str, Path], fieldnames: List = [],
             encoding: str = "UTF-8", not_exist: bool = True) -> Union[None, str]:
    """Write the contents of listinfo to arg_filepath.

    :param listinfo(list): What will be written to the arg_filepath.\n
    :param arg_filepath(str): File to be written.\n
    :param fieldnames(list): header of csv.\n
    :param encoding(str): Encoding format to write csv file, default is "UTF-8".\n
    :param not_exist(bool): Whether to overwrite the file when it exists.\n

    :return(None|str): No return value or the error info."""

    try:
        # verify args
        if isinstance(listinfo, list):
            if listinfo and not isinstance(listinfo[0], dict):
                return "Elements in listinfo must be dict."
        else:
            return "listinfo must be list."
        if not (isinstance(arg_filepath, Path) and isinstance(arg_filepath, str)):
            return f"{arg_filepath} is not str or pathlib.Path"

        if not isinstance(fieldnames, list):
            return "listinfo must be list."
        
        if not isinstance(encoding, str):
            return "encoding must be str."

        if util_file.handle_path(arg_filepath, "exist").count(True) == 2 and not_exist:
            return "File exists and not_exist is True, overwrite not allowed."

        if listinfo and fieldnames:
            if fieldnames != listinfo[0].keys():
                return f"If the keys of the first dict in listinfo and fieldnames is different, the file will not be written"
        elif listinfo:
            fieldnames = fieldnames
        elif fieldnames:
            fieldnames = listinfo[0].keys()
        else:
            return 'Both listinfo and fieldnames are empty!'

        with open(arg_filepath, 'w', newline='', encoding=encoding) as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(listinfo)

    except Exception as e:
        return f'list2csv has an exception: {traceback.format_exc().strip()}!'


if __name__ == "__main__":
    print(csv.list_dialects())
    pass
