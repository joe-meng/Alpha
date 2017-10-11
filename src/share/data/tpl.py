# coding: utf-8
import re
import datetime
from collections import ChainMap
from sqlbuilder.smartsql import T, Q, Result
from sqlbuilder.smartsql.dialects.mysql import compile as mysql_compile

from share.contrib import get_mysql_client

pattern = r"""
    %(delim)s(?:
      (?P<escaped>%(delim)s) |   # Escape sequence of two delimiters
      (?P<named>[\w\.\|:\+\-]+)      |   # delimiter and a Python identifier
      {(?P<braced>[\w\.\|:\+\-]+)}   |   # delimiter and a braced identifier
      (?P<invalid>)              # Other ill-formed delimiter exprs
    )
    """


class Filter(object):

    def filter(self, origin, arg):
        pass


class FilterNotExist(Exception):
    pass


class Template(object):

    delimiter = '$'
    tp = re.compile(pattern % {'delim': re.escape(delimiter)}, re.IGNORECASE | re.VERBOSE)
    filters = {}

    def __init__(self, template):
        self.template = template

    @classmethod
    def add_filter(cls, name):

        def decorate(flt):
            cls.filters[name] = flt
            return flt

        return decorate

    @classmethod
    def remove_filter(cls, name):

        def decorate(flt):
            if name in cls.filters:
                cls.filters.pop(name)
            return flt

        return decorate

    @property
    def context(self):
        return {'now': datetime.datetime.now()}

    def render(self, **kwargs):
        if self.delimiter not in self.template:
            return self.template
        mapping = ChainMap(kwargs, self.context)

        def convert(mo):
            named = mo.group('named') or mo.group('braced')
            if named is not None:
                named = named.strip()
                result = None
                for i, word in enumerate(named.split('|')):
                    if i == 0:
                        result = mapping[word] if word in mapping else word
                    else:
                        flt, arg = word.split(':')
                        flt_cls = self.filters.get(flt)
                        if not flt_cls:
                            raise FilterNotExist('filter %s not exist' % flt)
                        result = flt_cls().filter(result, arg)
                return str(result)
            if mo.group('escaped') is not None:
                return self.delimiter
            raise ValueError('Unrecognized named group in pattern',
                             self.tp)

        return self.tp.sub(convert, self.template)


@Template.add_filter('date')
class DateFilter(Filter):

    def filter(self, date, fmt):
        return date.strftime(fmt)


@Template.add_filter('serial')
class SerialFilter(Filter):

    def filter(self, variety, serial):
        if serial == '0':
            _serial = 'main_contract'
        else:
            _serial = 'serial_contract' + serial
        mt = T('main_contract')
        q = Q(mt, result=Result(compile=mysql_compile))
        q = q.fields(mt[_serial].as_('serial'))
        q = q.where((mt['varieties'] == variety) & (mt[_serial] != None )).order_by(mt['settlement_date'].desc()).limit(1)
        sql, params = q.select()
        with get_mysql_client() as cursor:
            cursor.execute(sql, params)
            contract = cursor.fetchone()['serial']
        return contract


@Template.add_filter('back')
class BackFilter(Filter):

    def filter(self, contract, years):
        ct = T('contracts')
        q = Q(ct, result=Result(compile=mysql_compile))
        q = q.fields(ct['expire_date']).where(ct['contract'] == contract).limit(1)
        sql, params = q.select()
        with get_mysql_client() as cursor:
            cursor.execute(sql, params)
            expire_date = cursor.fetchone()['expire_date']
        origin = expire_date.strftime('%y%m')
        new = str(expire_date.year + int(years))[-2:] + str(expire_date.month).zfill(2)
        return contract.replace(origin, new)


@Template.add_filter('ref')
class RefFilter(Filter):

    def filter(self, code, data_type):
        from .proxy import ref_proxy
        data = ref_proxy(code, data_type, limit=1)
        return data[0] if data else '暂无'
