#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @File    : util_json.py
# @Time    : 2021-07-23
# @Author  : Skypekey

"""Some functions related to json file operations."""

import json
import traceback
from pathlib import Path
from typing import Any, Dict, Union, Tuple

from user_tools.file import util_file
from user_tools.exception import util_exception


def read_json(json_file: Union[str, Path]) -> Tuple[bool, Union[str, Dict]]:
    """Return the contents of json_file.

    :param json_file(str): Json file to be read.\n
    :return(flag, strings):
        flag(bool): means success or failure.
        strings(str): if flag is True, means the content of json_file, otherwise means error or exception info."""

    try:
        json_dict = {}
        hp_result = util_file.handle_path(json_file, 'exist')
        if hp_result.count(True) != 2:
            raise util_exception.ParameterException(f'File not exists: {hp_result[1]}')
        with open(json_file, "r", encoding="UTF-8") as f:
            json_dict = json.load(f)
        return (True, json_dict)
    except Exception as e:
        return (False, f'read_json has an exception: {traceback.format_exc().strip()}!')


def write_json(json_file: Union[str, Path], json_dict: Dict[Any, Any]) -> Union[None, str]:
    """Write the contents of json_dict to json_file.

    :param json_file(str): Json file to be written.\n
    :param json_dict(str): What will be written to the json file.\n

    :return(None|str): No return value or the error info."""

    try:
        with open(json_file, "w", encoding="UTF-8") as f:
            # ensure_ascii = False is to display Chinese,
            # if not written, it will be displayed as unicode encoding.
            # indent is to format the json file,
            # otherwise it will be displayed on one line.
            json.dump(json_dict, f, ensure_ascii=False, indent=4)
    except Exception as e:
        return f'write_json has an exception: {traceback.format_exc().strip()}!'


if __name__ == "__main__":
    pass
