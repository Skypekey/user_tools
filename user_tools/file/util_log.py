#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @File    : util_log.py
# @Time    : 2021-06-10
# @Author  : Skypekey

"""Custom Log Class"""

import pathlib
import logging

LEVEL = ["debug", "info", "warning", "warn",
         "error", "fatal", "critical"]


class Pylog():
    def __init__(self, log_file, logger='', datefmt='%Y-%m-%d %H:%M:%S',
                 logfmt='%(asctime)s [%(levelname)s] %(message)s',
                 maxBytes=1024 * 1024 * 5, encoding="UTF-8",
                 backupCount=7) -> None:
        """
        params:
            log_file: Log file path.
            logger: logger objects to be inherited. Default is "".
            datefmt: Format of date and time in log file. Default is '%Y-%m-%d %H:%M:%S'.
            logfmt: Log file format. Default is '%(asctime)s [%(levelname)s] %(message)s'.
            maxBytes: The max size of log file. Default is 5MB.
            encoding: The encoding of log file. Default is UTF-8.
            backupCount: The count of backup file. Default is seven."""

        self.maxBytes = maxBytes
        self.encoding = encoding
        self.backupCount = backupCount
        self.log_file = log_file
        pathlib.Path(self.log_file).parent.mkdir(parents=True,
                                                 exist_ok=True)
        if logger:
            self.logger = logging.getLogger(logger)
        else:
            self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        self.fmt = logging.Formatter(logfmt, datefmt)

    def __console(self, message, level):
        """logging
        :params:
            level: The info level.
            msg: The info which will be logged.
        """

        file_handle = logging.handlers.TimedRotatingFileHandler(
            filename=self.log_file, mode='a', encoding=self.encoding,
            backupCount=self.backupCount, maxBytes=self.maxBytes,
            when='D')

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

    def logger_msg(self, level, msg):
        """Log directly, also can be use to log for functions with a return value of (LEVEL, "Output"). The LEVEL means one of LEVEL
        
        :params:
            level: The info level.
            msg: The info which will be logged.
        """

        if level not in LEVEL:
            self.__console(f"Level {level} is not correct, so use error! Message is {msg}", level="error")
        else:
            self.__console(msg, level=level)


if __name__ == "__main__":
    pass
