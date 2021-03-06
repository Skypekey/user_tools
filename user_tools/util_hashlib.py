#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Some functions related to hash operations."""
import os
import hashlib
import user_tools.util_check as uc


def get_str_md5(string):
    """Returns the MD5 value of a string.

    :param string(str): String to get the MD5 value.\n
    :return(str): The MD5 value of string.
        If string is empty, the MD5 value is empty."""

    md5name = ""
    if not string:
        tmp_md5 = hashlib.md5(string)
        md5name = tmp_md5.hexdigest().upper()
    return md5name


def get_file_md5(file_path):
    """Returns the MD5 value of a file.

    :param file_path(str): File path to get MD5 value.\n
    :return(str): the MD5 value of file_path.
        If the MD5 value is empty, it may be the following:
            file_path not file; file_path not exist; file_path is null."""

    md5name = ""
    expr1 = uc.is_not_null(file_path)
    expr2 = uc.file_or_dir(file_path) == "file"
    if expr1 and expr2:
        with open(file_path, "rb") as f:
            tmp_md5 = hashlib.md5()
            while True:
                tmp_file = f.read(8096)
                if not tmp_file:
                    break
                tmp_md5.update(tmp_file)
            md5name = tmp_md5.hexdigest().upper()
    return md5name
