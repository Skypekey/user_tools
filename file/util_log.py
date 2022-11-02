#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @File    : util_log.py
# @Time    : 2021-06-10
# @Author  : Skypekey


import pathlib
import logging
from functools import wraps


LEVEL = ["debug", "info", "warning", "warn",
         "error", "fatal", "critical"]


class Pylog():

    def __init__(self, log_file, logger='', datefmt='%Y-%m-%d %H:%M:%S',
                 logfmt='%(asctime)s [%(levelname)s] %(message)s') -> None:

        self.log_file = log_file
        pathlib.Path(self.log_file).parent.mkdir(parents=True,
                                                 exist_ok=True)
        if logger:
            self.logger = logging.getLogger(logger)
        else:
            self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        self.fmt = logging.Formatter(logfmt, datefmt)

    def __console(self, message, maxBytes=1024 * 1024 * 5, level='',
                  encoding="UTF-8", backupCount=1):
        file_handle = logging.handlers.RotatingFileHandler(
            filename=self.log_file, mode='a', encoding=encoding,
            backupCount=backupCount, maxBytes=maxBytes)

        file_handle.setFormatter(self.fmt)
        if(level.lower() == "debug"):
            file_handle.setLevel(logging.DEBUG)
        else:
            file_handle.setLevel(logging.INFO)
        self.logger.addHandler(file_handle)

        if level == 'info':
            self.logger.info(message)
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'warning' or level == 'warn':
            self.logger.warn(message)
        elif level == 'error':
            self.logger.error(message)
        elif level == 'fatal' or level == 'critical':
            self.logger.critical(message)
        self.logger.removeHandler(file_handle)
        file_handle.close()

    def logger_tuple(self, func):
        """Used to log for functions with a return value of (True/False, "Output")."""

        @wraps(func)
        def with_logging(*args, **kwargs):
            result = func(*args, **kwargs)
            print(result)
            if result[0]:
                self.__console(result[1])
            else:
                self.__console(result[1], level='error')
            return result
        return with_logging

    def logger_msg(self, level, msg):
        """Log directly"""

        if level not in LEVEL:
            self.__console(f"Level {level} is not correct!", level="error")
        else:
            self.__console(msg, level=level)


if __name__ == "__main__":
    pass
