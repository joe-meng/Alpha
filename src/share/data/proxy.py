# coding: utf-8
from .abc import BaseData
from .default import Default
from .kline import Kline, ContractKline
from .serial import Serial
from .symbol import Symbol
from .contract import Contract
from .math import Math
from .future import Future
from .tpl import Template

all_data_class_list = [Default, Kline, ContractKline, Serial, Symbol, Contract, Math, Future]
all_data_class_dict = {data_cls.table: data_cls for data_cls in all_data_class_list}


def data_class_factory(table=None):
    return all_data_class_dict.get(table, Default)


class ProxyData(BaseData):

    def __init__(self, data_code, table, start=None, end=None, limit=None, offset=None, desc=False):
        data_code = Template(data_code).render()
        data_cls = data_class_factory(table)
        if data_cls is Default:
            # data_code must be a column of the table
            data_code = '%s.%s' % (table, data_code)
        super().__init__(data_code, start, end, limit, offset, desc)
        self.data_cls = data_cls
        self.data_obj = self.data_cls(data_code, start, end, limit, offset, desc)
        self.data_code = self.data_obj.data_code

    def get_all(self, timestamp=False):
        return self.data_obj.get_all(timestamp)

    def get_list(self, timestamp=False):
        return self.data_obj.get_list(timestamp)

    def count(self):
        return self.data_obj.count()

    @classmethod
    def build_code(cls, ship):
        return data_class_factory(ship.table).build_code(ship)

    @property
    def Table(self):
        return self.data_obj.Table

    @property
    def Column(self):
        return self.data_obj.Column

    @property
    def Date(self):
        return self.data_obj.Date

    @property
    def column(self):
        return self.data_obj.column

    @property
    def table(self):
        return self.data_obj.table

    @property
    def date(self):
        return self.data_obj.date

    @property
    def unit(self):
        return self.data_obj.unit

    @property
    def title(self):
        return self.data_obj.title

    def join(self, data_obj):
        from .join import JoinData
        return JoinData((self, data_obj), self.start, self.end, self.limit, self.offset, self.desc)


def ref_proxy(data_code, table, start=None, end=None, limit=None, offset=None, timestamp=False):
    data = ProxyData(data_code, table, start, end, limit, offset, desc=True)
    return data.get_list(timestamp)


TableData, ref_table = ProxyData, ref_proxy
