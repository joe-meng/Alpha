#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@date: 2017-07-11

@author: Devin
"""
import datetime
import inspect
import traceback

from sqlbuilder.smartsql import Q, T, Result
from sqlbuilder.smartsql.dialects.mysql import compile as mysql_compile

from lib.contrib import get_mysql_client
from settings import logger


class Variety(object):
    def get_record(self, name, limit=30, env=None, contract=None, **kwargs):
        sql, params = getattr(self, name)(limit=limit, env=env, contract=contract,  **kwargs)
        logger.debug("执行sql为: %s, params:%s", sql, params)
        conn = get_mysql_client()
        with conn.cursor() as cursor:
            try:
                cursor.execute(sql, tuple(params))
            except Exception as e:
                logger.error("执行错误:%s", traceback.format_exc())
                raise e
            result = cursor.fetchall()
            logger.debug("获取数据为:%s", result)
            return result

    def _add_date_limit(self, q, tb, date_column, **kwargs):
        start_date = kwargs.get("start_date", None)
        end_date = kwargs.get("end_date", None)

        if start_date:
            start_str = start_date
            if isinstance(start_date, datetime.datetime) or isinstance(
                    start_date, datetime.date):
                start_str = datetime.datetime.strftime(start_date, "%Y-%m-%d")
            q = q.where(getattr(tb, date_column) >= start_str)
        if end_date:
            end_str = end_date
            if isinstance(start_date, datetime.datetime) or isinstance(
                    start_date, datetime.date):
                end_str = datetime.datetime.strftime(end_date, "%Y-%m-%d")
            q = q.where(getattr(tb, date_column) < end_str)
        return q

    def EXCHANGE(self, env=None, limit=1, contract=None, **kwargs):
        _table_name = "future_exchange"
        _column = "price_sell"
        _currency = 'USD'
        _future = "1w"
        _description = "汇率"

        _desc = ["date"]
        _date_column = "date"

        _field_name = inspect.stack()[0].function

        tb = getattr(T, _table_name)
        cl = getattr(tb, _column).as_(_field_name)

        f_l = [cl]
        if kwargs.get("need_date", False):
            dl = getattr(tb, _date_column).as_("date")
            f_l.append(dl)

        q = Q(tb, result=Result(compile=mysql_compile)).fields(tuple(f_l)). \
            where(tb.currency == _currency).where(tb.future == _future).limit(
            limit).order_by(
            tb.date.desc())

        q = self._add_date_limit(q, tb, _date_column, **kwargs)

        return q.select()
