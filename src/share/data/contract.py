# coding: utf-8
from sqlbuilder.smartsql import Result, Q, T
from sqlbuilder.smartsql.dialects.mysql import compile as mysql_compile

from .abc import BaseData
from .exceptions import ContractCodeError


class Contract(BaseData):
    table = 'contracts'
    date = 'expire_date'

    def __init__(self, data_code, start=None, end=None, limit=None, offset=None, desc=False):
        super().__init__(data_code, start, end, limit, offset, desc)
        code = data_code.split('.')
        if len(code) != 2:
            raise ContractCodeError('contract code must be like contract.column:%s' % data_code)
        self.contract, self.column = code

    @property
    def Table(self):
        t = T(self.table)
        return Q(t, result=Result(mysql_compile)).fields(t[self.column], t[self.date].as_(self.date_alias)).\
            where(t['contract'] == self.contract).as_table(str(id(self)))

    @classmethod
    def build_code(cls, ship):
        return '%s.%s' % (ship.serial, ship.column)


def ref_contract(data_code, start=None, end=None, limit=None, offset=None, timestamp=False):
    data = Contract(data_code, start, end, limit, offset, desc=True)
    return data.get_list(timestamp)
