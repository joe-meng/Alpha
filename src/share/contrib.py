# coding: utf-8
from importlib import import_module
from functools import wraps
import threading
import pymysql

from . import conf


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


def thread_singleton(func):
    # 线程单例
    instance_dict = {}

    @wraps(func)
    def instance(*args, **kwargs):
        thread_id = threading.current_thread().ident
        _instance = instance_dict.get(thread_id)
        if not _instance:
            _instance = func(*args, **kwargs)
            instance_dict[thread_id] = _instance
        return _instance

    return instance


class Connection(pymysql.connections.Connection):

    def cursor(self, *args, **kwargs):
        # when connection closed, reconnect.
        self.ping(reconnect=True)
        return super(Connection, self).cursor(*args, **kwargs)


# @singleton
@thread_singleton
def get_mysql_client():
    # 多线程共用一个连接有问题，暂定解决方案为各线程独占一个连接，最优解决方案为多线程共用一个连接池
    return Connection(host=conf.mysql.get('host'),
                      port=conf.mysql.get('port'),
                      user=conf.mysql.get('user'),
                      password=conf.mysql.get('password'),
                      db=conf.mysql.get('db'),
                      charset=conf.mysql.get('charset'),
                      connect_timeout=conf.mysql.get('timeout'),
                      cursorclass=pymysql.cursors.DictCursor)


def import_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError as err:
        raise ImportError("%s doesn't look like a module path" % dotted_path) from err

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError as err:
        raise ImportError('Module "%s" does not define a "%s" attribute/class' % (
            module_path, class_name)
        ) from err
