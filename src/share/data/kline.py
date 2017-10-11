# coding: utf-8
import datetime
from sqlbuilder.smartsql import Result, Q, T, Field, Expr
from sqlbuilder.smartsql.dialects.mysql import compile as mysql_compile

from .abc import BaseData
from .serial import serial_dict
from .exceptions import SerialNotExists, KlineCodeError


column_dict = {'default': {'name': '未知列', 'unit': '单位未知'},
               'price_open': {'name': '开盘价', 'unit': '元/吨'},
               'price_close': {'name': '收盘价', 'unit': '元/吨'},
               'price_high': {'name': '最高价', 'unit': '元/吨'},
               'price_low': {'name': '最低价', 'unit': '元/吨'},
               'volumn': {'name': '累计成交量', 'unit': '手'},
               'openinterest': {'name': '持仓量', 'unit': '手'},
               'settlement_price': {'name': '结算价', 'unit': '元/吨'}}


class ContractKline(BaseData):
    table = 'contract_kline'
    date = 'date_time'

    def __init__(self, contract_code, start=None, end=None, limit=None, offset=None, desc=False):
        # example: 'cu9999.price_open', 'LCPS.price_open'
        # contract code format: 'contract.column'
        super().__init__(contract_code, start, end, limit, offset, desc)
        code = contract_code.split('.')
        if len(code) != 2:
            raise KlineCodeError('contract kline code(%s) must be like: contract.column')
        self.contract, self.column = code
        self._handle = None

    @classmethod
    def build_code(cls, ship):
        return ship.column

    @property
    def Table(self):
        t = T('day_kline')
        if self.column == 'settlement_price':
            exp = 'if(`day_kline`.`settlement_price`, `day_kline`.`settlement_price`, `day_kline`.`price_close`)'
            field = Field(Expr(exp)).as_(self.column)
        else:
            field = t[self.column]
        return Q(t, result=Result(mysql_compile)).fields(field, t[self.date].as_(self.date_alias)).\
            where(t['contract'] == self.contract).as_table(str(id(self)))

    @property
    def title(self):
        column_info = column_dict.get(self.column) or column_dict.get('default')
        t = '%s%s' % (self.contract, column_info['name'])
        return t

    @property
    def unit(self):
        column_info = column_dict.get(self.column) or column_dict.get('default')
        return column_info['unit']


def ref_contract_kline(contract_code, start=None, end=None, limit=None, offset=None, timestamp=False):
    data = ContractKline(contract_code, start, end, limit, offset, desc=True)
    return data.get_list(timestamp)


class Kline(BaseData):
    table = 'day_kline'
    date = 'settlement_date'

    def __init__(self, kline_code, start=None, end=None, limit=None, offset=None, desc=False):
        # example: 'cu.main_contract.price_open'
        # kline code format: 'variety.serial.column'
        super().__init__(kline_code, start, end, limit, offset, desc)
        code = kline_code.split('.')
        if len(code) != 3:
            raise KlineCodeError('kline code(%s) must be like: variety.serial.column')
        self.variety, self.serial, self.column = code
        self._main = None
        if self.serial not in serial_dict:
            exc = 'serial:%s' % self.serial
            raise SerialNotExists(exc)

    @property
    def Table(self):
        if self.serial == 'main_contract' or self.serial == 'index_contract':
            return self.main.Table
        t_c = 'main_contract'
        t_k = 'day_kline'
        q = Q(T(t_c), result=Result(compile=mysql_compile))
        q = q.tables((q.tables() + T(t_k)).on(T(t_c)[self.date] == T(t_k)['date_time']))
        if self.column == 'settlement_price':
            exp = 'if(`day_kline`.`settlement_price`, `day_kline`.`settlement_price`, `day_kline`.`price_close`)'
            field = Field(Expr(exp)).as_(self.column)
        else:
            field = T(t_k)[self.column]
        q = q.fields(T(t_c)[self.date].as_(self.date_alias), field)
        q = q.where(T(t_c)['varieties'] == self.variety)
        q = q.where(T(t_c)[self.serial] == T(t_k)['contract'])
        q = q.where(T(t_c)[self.date] <= datetime.date.today())
        return q.as_table(str(id(self)))

    @property
    def Column(self):
        if self.serial == 'main_contract':
            return self.main.Column
        return super().Column

    @property
    def Date(self):
        if self.serial == 'main_contract':
            return self.main.Date
        return super().Date

    @classmethod
    def build_code(cls, ship):
        return '%s.%s.%s' % (ship.variety, ship.serial, ship.column)

    @property
    def unit(self):
        column_info = column_dict.get(self.column) or column_dict.get('default')
        return column_info['unit']

    @property
    def title(self):
        column_info = column_dict.get(self.column) or column_dict.get('default')
        t = '%s%s%s' % (self.variety, serial_dict.get(self.serial), column_info['name'])
        return t

    @property
    def main(self):
        if not self._main:
            if self.serial == 'main_contract':
                code = '%s9999.%s' % (self.variety, self.column)
            else:
                code = '%s8888.%s' % (self.variety, self.column)
            self._main = ContractKline(code, self.start, self.end, self.limit, self.offset, self.desc)
        return self._main


def ref_kline(kline_code, start=None, end=None, limit=None, offset=None, timestamp=False):
    data = Kline(kline_code, start, end, limit, offset, desc=True)
    return data.get_list(timestamp)
