# coding: utf-8
import logging
from sqlbuilder.smartsql import Result, Q
from sqlbuilder.smartsql.dialects.mysql import compile as mysql_compile

from .abc import BaseData
from .proxy import ProxyData
from share.contrib import get_mysql_client


class JoinData(BaseData):
    # 联表数据
    table = 'join'

    def __init__(self, data_objects, start=None, end=None, limit=None, offset=None, desc=False):
        self.data_objects = list(data_objects)
        data_code = '&'.join(['%s@%s' % (data_obj.data_code, data_obj.table) for data_obj in data_objects])
        super().__init__(data_code, start, end, limit, offset, desc)
        self._fields = None

    def get_list(self, timestamp=False):
        q = None
        std_obj = None
        for data_obj in self.data_objects:
            if q is None:
                std_obj = data_obj
                q = Q(std_obj.Table, result=Result(compile=mysql_compile)
                      ).fields(std_obj.Column)
            else:
                q = q.tables(q.tables() + data_obj.Table).\
                    on(std_obj.Date == data_obj.Date).\
                    fields(data_obj.Column)
        if timestamp:
            q = q.fields(std_obj.Date)
        if self.start:
            q = q.where(std_obj.Date >= self.start)
        if self.end:
            q = q.where(std_obj.Date <= self.end)
        if self.limit:
            q = q.limit(self.offset, self.limit)
        if self.desc:
            q = q.order_by(std_obj.Date.desc())
        else:
            q = q.order_by(std_obj.Date)
        sql, params = q.select()
        with get_mysql_client() as cursor:
            cursor.execute(sql, params)
            data = cursor.fetchall()
        result = [item.values() for item in data]
        logging.info("获取数据SQL:%s, 参数:%s, 数据为:%s", sql, params, result)
        return result

    def get_all(self, timestamp=False):
        data = super().get_all(timestamp)
        title = [data_obj.title for data_obj in self.data_objects]
        unit = [data_obj.unit for data_obj in self.data_objects]
        if timestamp:
            title.append('日期')
            unit.append('')
        data.update(title=title, unit=unit)
        return data

    def count(self):
        q = None
        std_obj = None
        for data_obj in self.data_objects:
            if q is None:
                std_obj = data_obj
                q = Q(std_obj.Table, result=Result(compile=mysql_compile)
                      ).fields(std_obj.Column.count().as_('count_value'))
            else:
                q = q.tables(q.tables() + data_obj.Table).\
                    on(std_obj.Date == data_obj.Date)
        if self.start:
            q = q.where(std_obj.Date >= self.start)
        if self.end:
            q = q.where(std_obj.Date <= self.end)
        sql, params = q.select()
        with get_mysql_client() as cursor:
            cursor.execute(sql, params)
            data = cursor.fetchone()
        result = data['count_value']
        logging.info("获取数据SQL:%s, 参数:%s, 数据为:%s", sql, params, result)
        return result

    @classmethod
    def build_code(cls, ship):
        return ship.column

    def join(self, data_obj):
        if data_obj not in self.data_objects:
            self.data_objects.append(data_obj)
        return self

    @classmethod
    def from_string(cls, data_code, start=None, end=None, limit=None, offset=None, desc=False):
        # data_code must be like cu.main_contract.price_open*day_kline&MA00001*symbol
        data_objects = []
        for item in data_code.split('&'):
            c, t = item.split('@')
            data_objects.append(ProxyData(c, t))
        return cls(data_objects, start, end, limit, offset, desc)


def ref_join(data_code, start=None, end=None, limit=None, offset=None, timestamp=False):
    data = JoinData.from_string(data_code, start, end, limit, offset, desc=True)
    return data.get_list(timestamp)
