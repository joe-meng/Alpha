#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import wraps
import pymysql

from settings import mysql


def singleton(func):
    # 单例模式装饰器：用于函数
    instance_list = []

    @wraps(func)
    def instance(*args, **kwargs):
        try:
            _instance = instance_list[0]
        except IndexError:
            _instance = func(*args, **kwargs)
            instance_list.append(_instance)
        return _instance

    return instance


class Connection(pymysql.connections.Connection):

    def cursor(self, *args, **kwargs):
        # when connection closed, reconnect.
        self.ping(reconnect=True)
        return super(Connection, self).cursor(*args, **kwargs)


@singleton
def get_mysql_client():
    return Connection(host=mysql.get('host'),
                      user=mysql.get('user'),
                      port=mysql.get('port', 3306),
                      password=mysql.get('password'),
                      db=mysql.get('db'),
                      charset=mysql.get('charset'),
                      connect_timeout=mysql.get('timeout'),
                      cursorclass=pymysql.cursors.DictCursor)
