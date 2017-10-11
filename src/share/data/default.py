# coding: utf-8
from sqlbuilder.smartsql import Result, Q, T
from sqlbuilder.smartsql.dialects.mysql import compile as mysql_compile

from .abc import BaseData
from .exceptions import DefaultCodeError


class Default(BaseData):

    data_code = None
    table = 'default'
    date = 'date'
    column = None

    def __init__(self, data_code, start=None, end=None, limit=None, offset=None, desc=False):
        # example: 'data_wind.amount'
        # data code format: 'table.column'
        super().__init__(data_code, start, end, limit, offset, desc)
        code = data_code.split('.')
        if len(code) != 2:
            raise DefaultCodeError('data code(%s) must be like: table.column' % data_code)
        self.table, self.column = code

    @property
    def Table(self):
        t = T(self.table)
        return Q(t, result=Result(mysql_compile)).fields(t[self.column], t[self.date].as_(self.date_alias)).as_table(str(id(self)))

    @classmethod
    def build_code(cls, ship):
        return '%s.%s' % (ship.table, ship.column)

    @property
    def title(self):
        return self.data_code


def ref_default(data_code, start=None, end=None, limit=None, offset=None, timestamp=False):
    data = Default(data_code, start, end, limit, offset, desc=True)
    return data.get_list(timestamp)
