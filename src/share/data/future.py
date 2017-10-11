# coding: utf-8
import logging
from sqlbuilder.smartsql import T, Q, Result, Field, Expr
from sqlbuilder.smartsql.dialects.mysql import compile as mysql_compile

from .abc import BaseData
from .exceptions import FutureCodeError
from share.contrib import get_mysql_client


class Future(BaseData):
    table = 'future'
    date = 'date_time'

    def __init__(self, future_code, start=None, end=None, limit=None, offset=None, desc=False):
        # data_code must be like 'variety.column' eg. 'cu.price_open'
        super().__init__(future_code, start, end, limit, offset, desc)
        self._ft = None
        code = future_code.split('.')
        if len(code) == 2:
            self.variety, self.column = code
        else:
            raise FutureCodeError('invalid future code: %s' % future_code)
        self.init()

    def init(self):
        mt = T('main_contract')
        q = Q(mt, result=Result(compile=mysql_compile))
        q = q.fields('*').where(mt['varieties'] == self.variety)
        q = q.order_by(mt['settlement_date'].desc()).limit(1)
        sql, params = q.select()
        logging.info("获取数据SQL:%s, 参数:%s", sql, params)
        with get_mysql_client() as cursor:
            cursor.execute(sql, params)
            result = cursor.fetchone()
        logging.info("数据为:%s", result)
        rows = []
        for i in range(1, 13):
            row = "select '%s' contract" % result.get('serial_contract' + str(i))
            rows.append(row)
        exp = ' union '.join(rows)
        ft = T(Expr(exp)).as_('future')
        self._ft = ft

    @property
    def Table(self):
        ft = self._ft
        ct = T('contracts')
        dt = T('day_kline')
        dq = Q(dt, result=Result(compile=mysql_compile))
        dq = dq.fields(Field(Expr('max(`day_kline`.`date_time`)')).as_('latest'), dt['contract'])
        dq = dq.group_by(dt['contract'])
        lt = dq.as_table('future_latest')
        q = Q(ft, result=Result(compile=mysql_compile))
        q = q.tables((q.tables() + ct)).on(ft['contract'] == ct['contract'])
        q = q.tables((q.tables() + lt)).on(ft['contract'] == lt['contract'])
        q = q.tables((q.tables() + dt)).on(ft['contract'] == dt['contract'])
        q = q.where(lt['latest'] == dt['date_time'])
        q = q.fields(dt[self.column], ct['expire_date'].as_(self.date_alias))
        return q.as_table(str(id(self)))
