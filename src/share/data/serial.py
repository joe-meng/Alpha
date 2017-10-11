# coding: utf-8
import datetime
from sqlbuilder.smartsql import Result, Q, T
from sqlbuilder.smartsql.dialects.mysql import compile as mysql_compile

from .abc import BaseData
from .exceptions import SerialCodeError


serial_dict = {'main_contract': '主力',
               'index_contract': '指数',
               'serial_contract1': '连一',
               'serial_contract2': '连二',
               'serial_contract3': '连三',
               'serial_contract4': '连四',
               'serial_contract5': '连五',
               'serial_contract6': '连六',
               'serial_contract7': '连七',
               'serial_contract8': '连八',
               'serial_contract9': '连九',
               'serial_contract10': '连十',
               'serial_contract11': '连十一',
               'serial_contract12': '连十二',
               'index': '指数',
               'default': '未知列'}


class Serial(BaseData):
    table = 'main_contract'
    date = 'settlement_date'

    def __init__(self, serial_code, start=None, end=None, limit=None, offset=None, desc=False):
        # example: 'cu.main_contract'
        # format: 'variety.column'
        super().__init__(serial_code, start, end, limit, offset, desc)
        code = serial_code.split('.')
        if len(code) != 2:
            raise SerialCodeError('serial code(%s) must be like: variety.column' % serial_code)
        self.variety, self.column = code

    @property
    def Table(self):
        t = T(self.table)
        return Q(t, result=Result(mysql_compile)).fields(t[self.column], t[self.date].as_(self.date_alias)).\
            where((t['varieties'] == self.variety) &
                  (t[self.date] <= datetime.date.today())).as_table(str(id(self)))

    @classmethod
    def build_code(cls, ship):
        return '%s.%s' % (ship.variety, ship.column)

    @property
    def title(self):
        serial_name = serial_dict.get(self.column, 'default')
        t = self.variety + serial_name
        return t


def ref_serial(serial_code, start=None, end=None, limit=None, offset=None, timestamp=False):
    data = Serial(serial_code, start, end, limit, offset, desc=True)
    return data.get_list(timestamp)
