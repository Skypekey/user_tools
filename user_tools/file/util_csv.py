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

from user_tools.file import util_file


def csv2list(filepath: Union[str, Path]) -> Tuple[bool, Union[str, List]]:
    """Convert the contents of the csv file to data in json format.

    :param file_path(str): The path of the file which to be read.\n

    :return(flag, strings):
        flag(bool): means success or failure.
        strings(str|list): if flag is True, means the content of csv is in json mode, otherwise means error or exception info."""

    try:
        csvlist = []
        with open(filepath,'rt') as f: 
            cr = csv.DictReader(f)
            for row in cr:
                csvlist.append(row)
        return (True, csvlist)
    except Exception as e:
        return (False, f'csv2list has an exception: {traceback.format_exc().strip()}!')


def list2csv(listinfo: List, file_path: Union[str, Path], fieldnames: List = [],
                 encoding: str = "UTF-8") -> Union[None, str]:
    """Write the contents of listinfo to file_path.

    :param file_path(str): File to be written.\n
    :param listinfo(list): What will be written to the file_path.\n
    :param encoding(str): Encoding format to write csv file, default is "UTF-8".\n
    :return(None|str): No return value or the error info."""

    try:
        hp_result = util_file.handle_path(file_path, 'c_exist')
        if hp_result.count(True) != 2:
            return f'File creation failed: {hp_result[1]}!'
        if listinfo == [] and fieldnames == []:
            return 'Both listinfo and fieldnames are empty!'
        
        if listinfo != []:
            fieldnames = fieldnames if fieldnames != [] and fieldnames == listinfo[0].keys() else listinfo[0].keys()

        with open(file_path, 'w', newline='', encoding=encoding) as csvfile:
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(listinfo)
    except Exception as e:
        return f'list2csv has an exception: {traceback.format_exc().strip()}!'


if __name__ == "__main__":
    print(csv.list_dialects())
    pass
