#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@date: 2017-07-14

@author: Devin
"""
import os.path

import sys

base_path = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../"))
calcu_path = os.path.normpath(os.path.join(base_path, "workers/calculation"))

sys.path.insert(0, calcu_path)

print(sys.path)

from lib.vo import FormulaEnv, DBPreProcess
from lib.mathlib import *


def test_cu_close():
    env = FormulaEnv(id=2, unit="",
                     pre_data=DBPreProcess(id=1, varieties='cu'))
    env.introduction = ""
    env.price = CLOSE
    data = REF(env, CLOSE, 10, CON_CONTRACT_1)
    print("data: %s", data)

    data = REFD(env, CLOSE, 10)
    print("data_d: %s", data)

def test_pd():
    env = FormulaEnv(id=2, unit="",
                     pre_data=DBPreProcess(id=1, varieties='cu'))
    # env.introduction = "SMM升贴水连续下跌3天"
    data = REF(env, PD, 10)
    # d1, d2, gd, rate = data_gap(data)
    print("升贴水data: %s", data)
    # print("差值:", d1, d2, gd, rate)

    data = REFD(env, PD, 10)
    print("升贴水带日期data: %s", data)


def test_lme_warrant():
    env = FormulaEnv(id=2, unit="",
                     pre_data=DBPreProcess(id=1, varieties='cu'))
    # env.introduction = "SMM升贴水连续下跌3天"
    data = REF(env, LME_WARRANT, 10)
    # d1, d2, gd, rate = data_gap(data)
    print("LME仓单data: %s", data)
    # print("差值:", d1, d2, gd, rate)

    data = REFD(env, LME_WARRANT, 10)
    print("LME仓单带日期data: %s", data)

def test_nanchu_in():
    env = FormulaEnv(id=2, unit="",
                     pre_data=DBPreProcess(id=1, varieties='cu'))
    # env.introduction = "SMM升贴水连续下跌3天"
    data = REF(env, NANCHU_IN, 10)
    # d1, d2, gd, rate = data_gap(data)
    print("南储仓电解铜入库data: %s", data)
    # print("差值:", d1, d2, gd, rate)

    data = REFD(env, NANCHU_IN, 10)
    print("南储仓电解铜入库带日期data: %s", data)


def test_nanchu_out():
    env = FormulaEnv(id=2, unit="",
                     pre_data=DBPreProcess(id=1, varieties='cu'))
    # env.introduction = "SMM升贴水连续下跌3天"
    data = REF(env, NANCHU_OUT, 10)
    # d1, d2, gd, rate = data_gap(data)
    print("南储仓电解铜出库data: %s", data)
    # print("差值:", d1, d2, gd, rate)

    data = REFD(env, NANCHU_OUT, 10)
    print("南储仓电解铜出库带日期data: %s", data)


def test_nanchu_stock():
    env = FormulaEnv(id=2, unit="",
                     pre_data=DBPreProcess(id=1, varieties='cu'))
    # env.introduction = "SMM升贴水连续下跌3天"
    data = REF(env, NANCHU_STOCK, 10)
    # d1, d2, gd, rate = data_gap(data)
    print("广东铜社会库存data: %s", data)
    # print("差值:", d1, d2, gd, rate)

    data = REFD(env, NANCHU_STOCK, 10)
    print("广东铜社会库存带日期data: %s", data)

def test_stock():
    env = FormulaEnv(id=2, unit="",
                     pre_data=DBPreProcess(id=1, varieties='cu'))
    # env.introduction = "SMM升贴水连续下跌3天"
    data = REF(env, STOCK, 10)
    # d1, d2, gd, rate = data_gap(data)
    print("铜总库存data: %s", data)
    # print("差值:", d1, d2, gd, rate)

    data = REFD(env, STOCK, 10)
    print("铜总库存带日期data: %s", data)

def test_stock_sh():
    env = FormulaEnv(id=2, unit="",
                     pre_data=DBPreProcess(id=1, varieties='cu'))
    # env.introduction = "SMM升贴水连续下跌3天"
    data = REF(env, STOCK_WS, 10)
    # d1, d2, gd, rate = data_gap(data)
    print("铜总库存data: %s", data)
    # print("差值:", d1, d2, gd, rate)

    data = REFD(env, STOCK_WS, 10)
    print("铜总库存带日期data: %s", data)

def test_lem_future():
    env = FormulaEnv(id=2, unit="",
                     pre_data=DBPreProcess(id=1, varieties='cu'))
    env.introduction = "SMM升贴水连续下跌3天"
    # env.contract = MAIN_CONTRACT
    # env.varieties = Cu
    # env.exchange = SHFE
    env.price = FUTURE_LME

    data = REF(env, FUTURE_LME, 10)
    print("data: %s", data)

    data = REFD(env, FUTURE_LME, 10)
    print("带日期data: %s", data)

def test_doji_star_threshold():
    env = FormulaEnv(id=2, unit="",
                     pre_data=DBPreProcess(id=1, varieties='cu'))
    env.introduction = "SMM升贴水连续下跌3天"
    # env.contract = MAIN_CONTRACT
    # env.varieties = Cu
    # env.exchange = SHFE
    # env.price = FUTURE_LME

    data = REF(env, DOJI_STAR_THRESHOLD, 10)
    print("data: %s", data)

    data = REFD(env, DOJI_STAR_THRESHOLD, 10)
    print("带日期data: %s", data)



def test_open_price():
    env = FormulaEnv(id=2, unit="",
                     pre_data=DBPreProcess(id=1, varieties='cu'))
    env.introduction = "沪铜开盘价连续下跌3天"
    env.contract = CON_CONTRACT_1
    env.varieties = Cu
    env.exchange = SHFE
    env.price = OPEN

    data = REFD(env, OPEN, 10)
    # d1, d2, gd, rate = data_gap(data)
    print("data: %s", data)
    # print("差值:", d1, d2, gd, rate)

    # data = REFD(env, OPEN, 10)
    # print("带日期data: %s", data)


def test_cross_star():
    """
    十字星
    :return:
    """
    env = FormulaEnv(id=2, unit="",
                     pre_data=DBPreProcess(id=1, varieties='cu'))
    env.introduction = "沪铜十字星"
    env.contract = MAIN_CONTRACT
    env.varieties = Cu
    env.exchange = SHFE
    env.price = CROSS_STAR

    data = REFD(env, CROSS_STAR, n=10)
    print("十字星data: ", data)


def test_warrant_monthly_rate():
    """
    仓单比
    :return:
    """
    env = FormulaEnv(id=2, unit="",
                     pre_data=DBPreProcess(id=1, varieties='cu'))
    env.introduction = "沪%s交割月%s合约持仓：仓单环比连续上涨%s天"
    # env.varieties = Cu
    # env.source = SHFE
    env.price = WARRANT_MONTH_RATE

    data = REFD(env, WARRANT_MONTH_RATE, n=5)
    print("仓单环比data: ", data)


def test_con1_con2_rate():
    env = FormulaEnv(id=2, unit="",
                     pre_data=DBPreProcess(id=1, varieties='cu'))
    env.introduction = "沪%s连1-连2合约高于预警指数%s元"
    # env.varieties = Cu
    # env.contract = CON_CONTRACT_1
    # env.exchange = SHFE
    env.price = CON1_CON2_DIFF_RATE

    data = REFD(env, CON1_CON2_DIFF_RATE, n=3)
    print("连1-连2差价:", data)


def test_con1_con3_rate():
    env = FormulaEnv(id=2, unit="",
                     pre_data=DBPreProcess(id=1, varieties='zn'))
    env.introduction = "沪%s连1-连3合约高于预警指数%s元"
    env.varieties = Zn
    env.contract = CON_CONTRACT_1
    env.exchange = SHFE
    env.price = CON1_CON3_DIFF_RATE

    data = REFD(env, CON1_CON3_DIFF_RATE, n=3)
    print("连1-连3差价:", data)


def test_con2_con3_rate():
    env = FormulaEnv(id=2, unit="",
                     pre_data=DBPreProcess(id=1, varieties='cu'))
    env.introduction = "沪%s连2-连3合约高于预警指数%s元"
    # env.varieties = Cu
    # env.contract = CON_CONTRACT_2
    # env.exchange = SHFE
    env.price = CON1_CON3_DIFF_RATE

    data = REFD(env, CON2_CON3_DIFF_RATE, n=10)
    print("连2-连3差价:", data)


def test_opi_monthly_rate():
    """
    持仓比
    :return:
    """
    env = FormulaEnv(id=2, unit="",
                     pre_data=DBPreProcess(id=1, varieties='cu'))
    env.introduction = "沪%s交割月%s合约持仓：仓单环比连续上涨%s天"
    # env.varieties = Cu
    # env.exchange = SHFE
    # env.contract = CON_CONTRACT_1
    env.price = OPI_MONTH_RATE

    data = REFD(env, OPI_MONTH_RATE, n=2)
    print("持仓data: ", data)

    # con1, con1_date = REFD(env, CON_CONTRACT_1)[0]
    # print("交割月%s, date:%s", con1, con1_date)


def test_exchange_rate():
    """
    持仓比
    :return:
    """
    env = FormulaEnv(id=2, unit="",
                     pre_data=DBPreProcess(id=1, varieties='cu'))
    env.introduction = "汇率"
    env.varieties = Cu
    env.exchange = SHFE
    env.contract = CON_CONTRACT_1
    env.price = EXCHANGE

    data = REFD(env, EXCHANGE, n=10)
    print("汇率data: ", data)


def test_shfe_lme_rate():
    """
    持仓比
    :return:
    """
    e = FormulaEnv(id=2, unit="",
                     pre_data=DBPreProcess(id=1, varieties='cu'))
    main_con = REF(e, MAIN_CONTRACT)
    e.result = REF(e, SHFE_LME_DIFF)

    if e.result and  e.result[0] >= -300:
        e.alert = True

    e_variety = e.content_varieties_ch

    e.chart = SHFE_LME_DIFF
    print("持仓比主力合约: ", main_con)
    print("e.result: ", e.result)


def test_spot_zn():
    env = FormulaEnv(id=2, unit="",
                     pre_data=DBPreProcess(id=1, varieties='zn'))


    # env.introduction = "沪%s交割月%s合约持仓：仓单环比连续上涨%s天"
    env.varieties = Zn
    # env.exchange = SHFE
    # env.source = SHMET
    # env.contract = CON_CONTRACT_1
    env.price = SPOT

    data = REFD(env, SPOT, 3)
    print("现货价格data: ", data)

def test_warrant_cu():
    env = FormulaEnv(id=2, unit="",
                     pre_data=DBPreProcess(id=1, varieties='cu'))


    # env.introduction = "沪%s交割月%s合约持仓：仓单环比连续上涨%s天"
    # env.varieties = Zn
    # env.exchange = SHFE
    # env.source = SHMET
    # env.contract = CON_CONTRACT_1
    # env.price = SPOT

    data = REFD(env, WARRANT, 3)
    print("现货价格data: ", data)

def test_CON_CONTRACT_4():

    env = FormulaEnv(id=2, unit="",
                     pre_data=DBPreProcess(id=1, varieties='cu'))


    # env.introduction = "沪%s交割月%s合约持仓：仓单环比连续上涨%s天"
    # env.varieties = Zn
    # env.exchange = SHFE
    # env.source = SHMET
    # env.contract = CON_CONTRACT_1
    # env.price = SPOT

    data = REFD(env, CON_CONTRACT_1, 3)
    print("铜连四data: ", data)


def test_DAYSTOEXPIRED():
    env = FormulaEnv(id=2, unit="",
                     pre_data=DBPreProcess(id=1, varieties='zn'))
    DAYSTOEXPIRED(env,CON_CONTRACT_1)


def test_attri():
    from lib import mathlib
    from lib.utils import date_utils
    a = {attr: getattr(mathlib, attr) for attr in dir(mathlib) if not attr.startswith('__')}
    b = {attr: getattr(date_utils, attr) for attr in dir(date_utils) if not attr.startswith('__')}
    a.update(b)
    print(a)

if __name__ == "__main__":
    # test_cross_star()
    # test_warrant_monthly_rate()
    # test_con1_con2_rate()
    # test_con1_con3_rate()
    # test_con2_con3_rate()
    # test_opi_monthly_rate()
    # test_lem_future()
    # test_exchange_rate()
    # test_shfe_lme_rate()
    # test_zn_close()
    # test_spot_zn()
    # test_open_price()
    # test_cu_close()
    # test_pd()
    # test_lme_warrant()
    # test_warrant_cu()
    # test_nanchu_in()
    # test_nanchu_out()
    # test_nanchu_stock()
    # test_stock()
    # test_stock_sh()
    # test_doji_star_threshold()
    # test_CON_CONTRACT_4()
    # test_opi_monthly_rate()
    # test_DAYSTOEXPIRED()
    test_attri()
