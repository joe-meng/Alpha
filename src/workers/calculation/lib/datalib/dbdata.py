#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@date: 2017-07-05

@author: Devin
"""
import contextlib
import copy

from lib.mathlib.constant import MAIN_CONTRACT
from lib.vo import DBPreProcess
from settings import logger, ref_ship


@contextlib.contextmanager
def prehandle_data(varieties):
    logger.info("算法分析开始处理预处理队列中数据varieties: %s", varieties)
    context = DBPreProcess(varieties=varieties)
    yield copy.deepcopy(context)
    logger.info("算法分析结束处理预处理队列中数据varieties: %s", varieties)


class Source(object):
    def __init__(self, varieties):
        self.varieties = varieties

    def get_record(self, price, limit=None, contract=MAIN_CONTRACT, env=dict(),
                   need_date=False, **kwargs):
        start = kwargs.get("start_date", None)
        end = kwargs.get("end_date", None)
        timestamp = need_date

        data = ref_ship(self.varieties, price, contract=contract, start=start,
                        end=end, limit=limit, offset=None, timestamp=timestamp)

        return data
