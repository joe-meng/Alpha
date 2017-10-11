#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@date: 2017-08-17

@author: Devin
"""
import traceback

from lib.contrib import get_mysql_client
from settings import logger


class Base(object):
    def get_record(self, sql, params, **kwargs):
        logger.debug("执行sql为: %s, params:%s", sql, params)
        with get_mysql_client() as cursor:
            try:
                cursor.execute(sql, tuple(params))
            except Exception as e:
                logger.error("执行错误:%s", traceback.format_exc())
                raise e
            result = cursor.fetchall()
            logger.debug("获取数据为:%s", result)
            return result
