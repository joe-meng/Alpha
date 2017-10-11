# coding: utf-8
import logging
from sqlbuilder.smartsql import T, Q, Result
from sqlbuilder.smartsql.dialects.mysql import compile as mysql_compile

from .exceptions import SymbolNotExists, SymbolCodeError
from .abc import BaseData
from share.contrib import get_mysql_client


class Symbol(BaseData):

    attr_list = ('table_name', 'unit', 'title', 'source', 'varieties',
                 'duration_unit', 'column', 'benchmark', 'date_column')
    table = 'symbol'
    date = 'date'

    def __init__(self, symbol_code, start=None, end=None, limit=None, offset=None, desc=False):
        # example: 'S0116880'
        # symbol_code format: 'symbol.column'
        super().__init__(symbol_code, start, end, limit, offset, desc)
        code = symbol_code.split('.')
        self._convert = True
        if len(code) == 1:
            self.symbol = symbol_code
            self.column = None
        elif len(code) == 2:
            self.symbol, self.column = code
            self._convert = False
        else:
            raise SymbolCodeError('symbol code(%s) must be like: symbol.column' % symbol_code)
        self.init()

    def init(self):
        sql, params = Q(T('symbol'), result=Result(compile=mysql_compile)).\
            fields('*').where(T('symbol')['symbol'] == self.symbol).select()
        with get_mysql_client() as cursor:
            cursor.execute(sql, params)
            data = cursor.fetchone()
        if not data:
            raise SymbolNotExists('symbol(%s) not exists!' % self.symbol)
        for attr in self.attr_list:
            if attr == 'column':
                self.column = self.column or data.get(attr) or 'amount'
            elif attr == 'date_column':
                self.date = data.get(attr) or self.date
            else:
                setattr(self, attr, data.get(attr))
        logging.info("获取数据SQL:%s, 参数:%s, 数据为:%s", sql, params, data)
        return data

    @property
    def Table(self):
        t = T(self.table_name)
        if self._convert:
            field = (t[self.column] * self.benchmark).as_(self.column)
        else:
            field = t[self.column]
        return Q(t, result=Result(mysql_compile)).fields(field, t[self.date].as_(self.date_alias)).\
            where(t['symbol'] == self.symbol).as_table(str(id(self)))

    @classmethod
    def build_code(cls, ship):
        return ship.column


def ref_symbol(symbol_code, start=None, end=None, limit=None, offset=None, timestamp=False):
    data = Symbol(symbol_code, start, end, limit, offset, desc=True)
    return data.get_list(timestamp)
