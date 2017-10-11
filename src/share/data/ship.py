# coding: utf-8
import logging
from sqlbuilder.smartsql import Result, Q, T
from sqlbuilder.smartsql.dialects.mysql import compile as mysql_compile

from .abc import BaseData
from .proxy import ProxyData
from .exceptions import ShipNotExists
from share.contrib import get_mysql_client


class Ship(BaseData):

    def __init__(self, variety, price_code, serial='main_contract', start=None,
                 end=None, limit=None, offset=None, desc=False):
        self.variety = variety
        self.price_code = price_code
        self.serial = serial
        self.table = None
        self.column = None
        self.data_cls = None
        self.data_obj = None
        self.init()
        self.data_code = ProxyData.build_code(self)
        super().__init__(self.data_code, start, end, limit, offset, desc)
        self.data_obj = ProxyData(self.data_code, self.table, self.start,
                                  self.end, self.limit, self.offset, self.desc)

    def init(self):
        table = 'ref_ship'
        q = Q(T(table), result=Result(compile=mysql_compile)). \
            fields(T(table)['table_name'],
                   T(table)['column']).where((T(table)['varieties'] == self.variety) &
                                             (T(table)['price_code'] == self.price_code))
        sql, params = q.select()
        with get_mysql_client() as cursor:
            cursor.execute(sql, params)
            result = cursor.fetchone()
        if not result:
            raise ShipNotExists('varieties:%s,price_code:%s' % (self.variety, self.price_code))
        self.table = result['table_name']
        self.column = result['column']
        logging.info("获取数据SQL:%s, 参数:%s, 数据为:%s", sql, params, result)

    def get_all(self, timestamp=False):
        return self.data_obj.get_all(timestamp)

    def get_list(self, timestamp=False):
        return self.data_obj.get_list(timestamp)

    def count(self):
        return self.data_obj.count()

    @property
    def title(self):
        return self.data_obj.title

    @property
    def unit(self):
        return self.data_obj.unit


def ref_ship(variety, price_code, contract='main_contract', start=None,
             end=None, limit=None, offset=None, timestamp=False):
    data = Ship(variety, price_code, contract, start, end, limit, offset, desc=True)
    return data.get_list(timestamp)
