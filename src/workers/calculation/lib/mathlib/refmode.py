#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@desc: 引用机制

@date: 2017-06-29

@author: Devin
"""
import copy
import datetime

import re
from dateutil import relativedelta
from .constant import *


def REF(env, price, n=0, contract=MAIN_CONTRACT, **kwargs):
    """
    向前引用，取得前n根k线数据，返回一维数组，可以使用$
    :param c:
    :param n:
    :return:
    """
    from lib.datalib.dbdata import Source

    r_d = Source(env.content_variety).get_record(price, n + 1, contract,
                                                 env=env, **kwargs)
    r_d.reverse()
    return r_d


def REFD(env, price, n=0, contract=MAIN_CONTRACT, **kwargs):
    """
    向前引用,返回值带日期, 取得前一根k线数据，返回一维数组，可以使用$
    :param c:
    :return:
    """
    from lib.datalib.dbdata import Source
    from lib.utils.date_utils import timestamp2datetime

    r_d = Source(env.content_variety).get_record(price, n + 1, contract,
                                                 env=env, need_date=True,
                                                 **kwargs)
    data = list([(x[1], timestamp2datetime(x[0]/1000)) for x in r_d])
    data.reverse()
    return data

def ISCONTRACT(env, con_code, con_name):
    """
    是当前合约返回1，不是当前合约返回0。
    :param c: con_code: MAIN_CONTRACT,CON_CONTRACT_1
    :return: con_name: Cu1701
    """
    from . import REF
    is_current = 0
    con = REF(env, con_code)[0]
    if con and con[0] == con_name:
        is_current = 1
    return is_current


def WEEKDAY(env, r_date):
    """
    r_date datetime or date or "YYYY-DD-MM"
    取当天是星期几，返回0-6
    :param r_data:
    :return:
    """
    if type(r_date) == str:
        r_date = datetime.datetime.strptime(r_date, "%Y-%m-%d")
    return r_date.weekday()


def CURRENTDATE(env):
    """
    取当前年月日
    :param r_date:
    :return:
    """
    return datetime.datetime.today()


def GETPRICE(env, contract, field, date_from_str, date_end_str):
    """
    返回二维数组
    :param contract: 合约,类似SHFE_CU_1707
    :param field: K线上的值
    :param date_from_str: 取开始时间
    :param date_end_str: 取结束时间
    :return:
    """
    copy_env = copy.deepcopy(env)
    copy_env.contract = contract
    return REFD(copy_env, field, start_date=date_from_str,
                 end_date=date_end_str)


def DOMINANT(env):
    """
    取主力合约
    :return:
    """
    from . import MAIN_CONTRACT
    return REF(env, MAIN_CONTRACT, 0)[0]


def CONTCONTRACT(env, n=1):
    """
    获取连续合约的编码，参数表示连一、连二等，连一指的是离交割最近的月份
    :param n:
    :return:
    """
    con = MAIN_CONTRACT
    exec("con = REF(env, CON_CONTRACT_%s)"%n)
    return REF(env, con, 0)[0]


def DAYSTOEXPIRED(env, contract):
    """
    期货合约距最后交易日的天数。
    :param contract: 期货合约
    :return:
    """
    con = REF(env, contract)[0]
    expired_date = EXPIREDATE(env, con)[0]
    if isinstance(expired_date, datetime.datetime):
        expired_date = expired_date.date()
    delta = expired_date - datetime.date.today()
    return delta.days


def EXPIREDATE(env, contract):
    """
    返回期货合约的最后交易日
    :param contract:期货合约
    :return:
    """
    from lib.datalib.dbdata import Source
    from lib.mathlib import EXPIRE_DATE
    if not re.match("[a-zA-Z]{1,2}[0-9]{4}",contract):
        contract = REF(env, contract)[0]
    r_d = Source(env.content_variety).get_record(EXPIRE_DATE, 1, env=env,
                                                 contract=contract)
    r_d.reverse()
    return r_d


def ISHOLIDAY(env, date):
    """
    判断某日期是否是非交易日
    :param date:
    :return:
    """
    pass


def EXCHRATE(env):
    """
    获取汇率
    :return:
    """
    pass


def CONTRACTN(env, contract, n):
    """
    获取合约的相对第n个合约
    :param env:
    :param contract: 基准合约
    :param n:
    :return:
    """
    str_date = contract.upper()[len(env.content_variety):]
    base_date = datetime.datetime.strptime(str_date, "%y%m")
    n_date = base_date + relativedelta.relativedelta(months=int(n))
    return contract[:len(env.content_variety)] + datetime.datetime.strftime(
        n_date, "%y%m")
