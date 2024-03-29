#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @File    : util_mysql.py
# @Time    : 2021-12-14
# @Author  : Skypekey


"""A custom object for MySQL, to operate the MySQL database."""

import traceback
import pymysql
from user_tools.common import util_method


class User_MySQL():
    def __init__(self, info, method="host") -> None:
        """
        :param method(str): Method used for database authentication. Only host and socket.
        :param info(Dict): Database authentication information.\n
            The format of info:\n
                info = {
                    # required, where use host to access database.
                    "host": "host",
                    "user": "user", # required
                    "password": "password", # required
                    "port": 3306, # optional, default is 3306
                    "database": "mysql", # optional
                    # required, where use socket to access database.
                    "socket": "/tmp/mysql.sock"
                }
        """

        self.info = info
        self.method = method

    def __verify(self):
        """Initialize database authentication information.

        :return tuple(bool, db_conn|str, db_cur|None): If there is no error, return the database connection handle and cursor handle, otherwise an error message is returned."""

        arg_list = ["host", "user", "password",
                    "port", "database", "socket"]
        connect_info = self.info.copy()
        err_info = ""

        for i in self.info.keys():
            if i not in arg_list:
                err_info = f"Illegal parameter {i}, only the following parameters are allowed: \n{''.join(arg_list)}"
                break
        if self.method not in ["host", "socket"]:
            err_info = "Only host and socket methods are allowed"
        elif not isinstance(self.info, dict):
            err_info = "info must be a dict object"
        elif "user" not in self.info or not self.info["user"]:
            err_info = "info must contain user and cannot be empty"
        elif "password" not in self.info or not self.info["password"]:
            err_info = "info must contain password and cannot be empty"
        elif "database" not in self.info or not self.info["database"]:
            err_info = "info must contain database and cannot be empty"
        elif self.method == "host":
            if "host" not in self.info or not self.info["host"]:
                err_info = f"When using {self.method} authentication,\
                             host is required"
            elif "port" not in self.info or not self.info["port"]:
                connect_info["port"] = 3306
        elif self.method == "socket":
            if "socket" not in self.info or not self.info["socket"]:
                err_info = f"When using {self.method} authentication,\
                             socket is required"

        return util_method.return_boolinfo(err_info, connect_info)

    def __connect(self):
        """Connect to database."""

        try:
            flag, result = self.__verify()
            if flag:
                self.db_conn = pymysql.connect(**result)
                self.db_cur = self.db_conn.cursor(pymysql.cursors.DictCursor)
            else:
                return (flag, result)
        except Exception as e:
            return f"Database connection error, exception info is:\n{traceback.format_exc().strip()}"

    def __close(self):
        self.db_cur.close()
        self.db_conn.close()

    def __check(self, sql, isquery=True):
        err_info = self.__connect()
        if not err_info:
            isselect = sql.lower().startswith("select")
            into = "into" in sql.lower().split(" ")
            if isquery and (not isselect or into):
                err_info = "Only Select sql statement is supported when use query method."
            elif not isquery and isselect and not into:
                err_info = "Sql statement must contains into when use noquery method and use select sql statement."

        return util_method.return_boolinfo(err_info, "")

    def Query(self, sql):
        """Query data from the database.

        :param sql(str): It's a sql statement."""

        err_info = ""
        data = ""

        flag, err_info = self.__check(sql)
        if flag:
            try:
                self.db_cur.execute(sql)
                data = self.db_cur.fetchall()
            except Exception as e:
                err_info = f"sql statement is {sql}.\n exception info is:\n{traceback.format_exc().strip()}"
            finally:
                self.__close()
        return util_method.return_boolinfo(err_info, data)

    def NoQuery(self, sql):
        """Change the data in the database.

        :param sql(str): It's a sql statement."""

        err_info = ""
        data = ""

        flag, err_info = self.__check(sql, False)
        if flag:
            try:
                self.db_cur.execute(sql)
                self.db_conn.commit()
            except Exception as e:
                self.db_conn.rollback()
                err_info = f"sql statement is {sql}.\n exception info is:\n{traceback.format_exc().strip()}"
            finally:
                self.__close()

        return util_method.return_boolinfo(err_info, data)


if __name__ == "__main__":
    pass
