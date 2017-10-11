# coding: utf-8
import time
import logging
from sqlbuilder.smartsql import Result, Q
from sqlbuilder.smartsql.dialects.mysql import compile as mysql_compile

from share.contrib import get_mysql_client


class BaseData(object):
    title = ''
    unit = ''
    data_code = None
    table = ''
    date = 'date_time'
    column = None

    def __init__(self, data_code, start=None, end=None, limit=None, offset=None, desc=False):
        self.data_code = data_code
        self.start = start
        self.end = end
        self.limit = limit
        self.offset = offset
        self.desc = desc

    def get_list(self, timestamp=False):
        q = Q(self.Table, result=Result(compile=mysql_compile)).\
            fields(self.Column, self.Date)
        if self.start:
            q = q.where(self.Date >= self.start)
        if self.end:
            q = q.where(self.Date <= self.end)
        if self.limit:
            q = q.limit(self.offset, self.limit)
        if self.desc:
            q = q.order_by(self.Date.desc())
        else:
            q = q.order_by(self.Date)
        sql, params = q.select()
        logging.info("获取数据SQL:%s, 参数:%s", sql, params)
        with get_mysql_client() as cursor:
            cursor.execute(sql, params)
            data = cursor.fetchall()
        if timestamp:
            result = [(int(time.mktime(item[self.date_alias].timetuple())) * 1000, item[self.column])
                      for item in data if item[self.column] is not None]
        else:
            result = [item[self.column] for item in data if item[self.column] is not None]
        # logging.info("数据为:%s", result)
        return result

    def get_all(self, timestamp=False):
        line = self.get_list(timestamp)
        return {'title': self.title,
                'unit': self.unit,
                'line': line,
                'line_type': self.table,
                'count': self.count(),
                'data_code': self.data_code}

    def count(self):
        q = Q(self.Table, result=Result(compile=mysql_compile)).fields(self.Column.count().as_('count_value'))
        if self.start:
            q = q.where(self.Date >= self.start)
        if self.end:
            q = q.where(self.Date <= self.end)
        sql, params = q.select()
        logging.info("获取数据SQL:%s, 参数:%s", sql, params)
        with get_mysql_client() as cursor:
            cursor.execute(sql, params)
            data = cursor.fetchone()
        result = data['count_value']
        logging.info("数据为:%s", result)
        return result

    @property
    def Table(self):
        raise NotImplemented

    @property
    def Column(self):
        return self.Table[self.column]

    @property
    def Date(self):
        return self.Table[self.date_alias]

    @classmethod
    def build_code(cls, ship):
        raise NotImplemented

    @property
    def date_alias(self):
        return self.date + '_alias'

    # 运算符重载技术
    def __add__(self, other):
        # 加法重载
        from ._math import Add
        return Add(self, other)

    def __radd__(self, other):
        from ._math import Add
        return Add(self, other)

    def __sub__(self, other):
        # 减法重载
        from ._math import Sub
        return Sub(self, other)

    def __rsub__(self, other):
        from ._math import Rsub
        return Rsub(self, other)

    def __mul__(self, other):
        # 乘法重载
        from ._math import Mult
        return Mult(self, other)

    def __rmul__(self, other):
        from ._math import Mult
        return Mult(self, other)

    def __truediv__(self, other):
        # 除法重载
        from ._math import Div
        return Div(self, other)

    def __rtruediv__(self, other):
        from ._math import Rdiv
        return Rdiv(self, other)

    def __mod__(self, other):
        # 求余重载
        from ._math import Mod
        return Mod(self, other)

    def __rmod__(self, other):
        from ._math import Rmod
        return Rmod(self, other)


class DataChart(object):

    def __init__(self):
        self.lines = []

    def add_line(self, line):
        if line not in self.lines:
            self.lines.append(line)

    def remove_line(self, line):
        if line in self.lines:
            self.lines.remove(line)

    def get_all(self):
        lines = []
        for line in self.lines:
            line_data = line.get_all(timestamp=True)
            lines.append(line_data)
        return lines
