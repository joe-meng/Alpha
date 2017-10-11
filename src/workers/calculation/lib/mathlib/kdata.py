#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@desc: K线数据

@date: 2017-06-29

@author: Devin
"""


def KOPEN(env):
    """
    获取K线图的开盘价
    :param k_data:K线图数据数组
    :return:
    """
    from . import REF, OPEN
    data = REF(env, OPEN, 0)[0]
    return data


def KCLOSE(env):
    """
    获取K线图的收盘价(env, 当天最后的一条收盘价)
    :param k_data:K线图数据数组
    :return: 收盘价
    """
    from . import REF, CLOSE
    data = REF(env, CLOSE, 0)[0]
    return data


def KHIGH(env):
    """
    获取K线图的最高价
    :param k_data:K线图数据数组
    :return:
    """
    from . import REF, HIGH
    data = REF(env, HIGH, 0)[0]
    return data


def KLOW(env):
    """
    获取K线图的最低价
    :param k_data:K线图数据数组
    :return:
    """
    from . import REF, LOW
    data = REF(env, LOW, 0)[0]
    return data


def KSETTLE(env):
    """
    获取k线图的结算价或者取得当时成交均价
    :param data:K线图数据数组
    :return:
    """
    from . import REF, SETTLE
    data = REF(env, SETTLE, 0)[0]
    return data


def KVOL(env):
    """
    取得K线图的成交量
    :param k_data:K线图数据数组
    :return:
    """
    from . import REF, VOL
    data = REF(env, VOL, 0)[0]
    return data


def KOPI(env):
    """
    获取K线图的持仓量
    :param k_data:K线图数据数组
    :return:
    """
    from . import REF, OPI
    data = REF(env, OPI, 0)[0]
    return data


def KSTOCK(env):
    """
    获取K线图 库存(env, 注意是每周)=仓单+不可交割库存
    :param k_data:K线图数据数组
    :return:
    """
    from . import REF, STOCK
    data = REF(env, STOCK, 0)[0]
    return data


def KWARRANT(env):
    """
    获取K线图 仓单(env, 注意是每周)
    :param k_data: K线图数据数组
    :return:
    """
    from . import REF, WARRANT
    data = REF(env, WARRANT, 0)[0]
    return data


def KCONTRACT(env):
    """
    获取K线图 当前合约名称
    :param k_data: K线图数据数组
    :return:
    """
    from . import REF, CONTRACT
    data = REF(env, CONTRACT, 0)[0]
    return data


def KFUTURES(env):
    """
    获取K线图 当前品种名称
    :param k_data: K线图数据数组
    :return:
    """
    from . import REF, FUTURES
    data = REF(env, FUTURES, 0)[0]
    return data


def KMARKET(env):
    """
    获取K线图 当前市场名称
    :param k_data: K线图数据数组
    :return:
    """
    from . import REF, MARKET
    data = REF(env, MARKET, 0)[0]
    return data


def KSPOT(env):
    """
    获取K线图 现货名称
    :param k_data: K线图数据数组
    :return:
    """
    from . import REF, SPOT
    data = REF(env, SPOT, 0)[0]
    return data


def KPD(env):
    """
    获取K线图 现货升贴水
    :param k_data: K线图数据数组
    :return:
    """
    from . import REF, PD
    data = REF(env, PD, 0)[0]
    return data

def KBUYVOL(env):
    """
    获取K线图 外盘（主动性买单）
    :param k_data: K线图数据数组
    :return:
    """
    from . import REF, BUYVOL
    data = REF(env, BUYVOL, 0)[0]
    return data

def KSELLVOL(env):
    """
    获取K线图 内盘(主动性卖单)
    :param k_data: K线图数据数组
    :return:
    """
    from . import REF, SELLVOL
    data = REF(env, SELLVOL, 0)[0]
    return data

def KCASHPREC(env):
    """
    获取K线图 资金沉淀
    :param k_data: K线图数据数组
    :return:
    """
    from . import REF, CASHPREC
    data = REF(env, CASHPREC, 0)[0]
    return data

def KCASHFLOW(env):
    """
    获取K线图 资金流向
    :param k_data: K线图数据数组
    :return:
    """
    from . import REF, CASHFLOW
    data = REF(env, CASHFLOW, 0)[0]
    return data

def KOPICHANGE(env):
    """
    获取K线图 日增仓
    :param env:
    :return:
    """
    from . import REF, OPICHANGE
    data = REF(env, OPICHANGE, 0)[0]
    return data