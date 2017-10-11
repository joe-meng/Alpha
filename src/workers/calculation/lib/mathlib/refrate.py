#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@date: 2017-07-21

@author: Devin
"""
import copy
import datetime
import decimal

import numpy as np

from lib.utils.date_utils import next_day
from settings import logger

"""
DOJI_STAR = "DOJI_STAR" #十字星
OPI_MONTH_RATE = "OPI_MONTH" #持仓比
WARRANT_MONTH_RATE = "WARRANT_MONTH_RATE" #仓单比
SHFE_LME_DIFF = "SHFE_LME_DIFF" #沪伦差值
CON1_CON2_DIFF_RATE = "CON1_CON2_DIFF_RATE" #连一连二比
CON1_CON3_DIFF_RATE = "CON1_CON3_DIFF_RATE" #连一连三比
CON2_CON3_DIFF_RATE = "CON2_CON3_DIFF_RATE" #连二连三比

"""


def rate_DOJI_STAR(env, n=0, contract=None, **kwargs):
    """
    十字星
    :param c:
    :param n:
    :return:
    """
    from . import REFD, OPEN, CLOSE, mutip_data_gap, REF, DOJI_STAR_THRESHOLD
    rate = REF(env, DOJI_STAR_THRESHOLD)[0]
    open_price = REFD(env, OPEN, n - 1, contract, **kwargs)
    close_price = REFD(env, CLOSE, n - 1, contract, **kwargs)

    open_array = np.swapaxes(np.array(open_price), 0, 1)
    close_array = np.swapaxes(np.array(close_price), 0, 1)

    d1, d2, gd, r_gd = mutip_data_gap(open_array[0], close_array[0])

    logger.info("开盘价:%s, 收盘价:%s, 差值:%s, 差值比:%s, 预警值:%s", d1, d2, gd, r_gd,
                rate)
    result = (rate - abs(r_gd)) >= 0

    return [result.tolist(), r_gd.tolist(), open_array[1].tolist()]


def rate_warrant_month(env, n=0, contract=None, **kwargs):
    """
    仓单环比
    :param env:
    :param n:取值
    :param kwargs: 可能包含start_date, end_date
    :return:
    """
    from . import REFD, WARRANT
    from lib.utils.date_utils import all_month_end

    cur_num = n - 1
    copy_kwargs = copy.deepcopy(kwargs)
    copy_kwargs["start_date"] = None
    warrant_array = REFD(env, WARRANT, cur_num + 30, contract, **copy_kwargs)

    cut_off_month_dt = all_month_end(warrant_array[0][1], warrant_array[-1][1])

    d_m, d_c, gd, r_gd, m_date, c_date = _rate_month(warrant_array,
                                                     cut_off_month_dt, n=n,
                                                     **kwargs)
    return [(r_gd >= 0).tolist(), r_gd.tolist(), c_date.tolist(), gd.tolist(),
            d_m.tolist(), d_c.tolist()]


def rate_shfe_lme(env, n=0, contract=None, **kwargs):
    """
    泸伦差价
    SHFE_LME_DIFF
    :param env:
    :param n:
    :param kwargs:
    :return:
    """
    from . import REFD, SETTLE, FUTURE_LME, EXCHANGE
    shfe_settle_price = REFD(env, SETTLE, n - 1, **kwargs)
    lme_settle_price = REFD(env, FUTURE_LME, n - 1, **kwargs)
    exchange = REFD(env, EXCHANGE, n - 1, **kwargs)

    shfe_settle_array = np.swapaxes(np.array(shfe_settle_price), 0, 1)
    lme_settle_array = np.swapaxes(np.array(lme_settle_price), 0, 1)
    exchange_array = np.swapaxes(np.array(exchange), 0, 1)

    gap_price = np.array([decimal.Decimal(x) for x in shfe_settle_array[0]]) - \
                np.array([decimal.Decimal(x) for x in
                          lme_settle_array[0]]) * decimal.Decimal(1.17) * \
                exchange_array[0]

    result = gap_price >= -300

    return [result.tolist(), gap_price.tolist(), shfe_settle_array[1].tolist()]


def rate_con1_con2(env, n=0, contract=None, **kwargs):
    """
    连1连2价并
    CON1_CON2_DIFF_RATE
    SHFE_LME_DIFF
    :param env:
    :param n:
    :param kwargs:
    :return:
    """
    from . import CON_CONTRACT_1, CON_CONTRACT_2
    return _rate_con_con(env, CON_CONTRACT_1, CON_CONTRACT_2, n, **kwargs)


def rate_con1_con3(env, n=0, contract=None, **kwargs):
    """
    连1连3价并
    CON1_CON2_DIFF_RATE
    SHFE_LME_DIFF
    :param env:
    :param n:
    :param kwargs:
    :return:
    """
    from . import CON_CONTRACT_1, CON_CONTRACT_3
    return _rate_con_con(env, CON_CONTRACT_1, CON_CONTRACT_3, n, **kwargs)


def rate_con2_con3(env, n=0, contract=None, **kwargs):
    """
    连1连2价并
    CON1_CON2_DIFF_RATE
    SHFE_LME_DIFF
    :param env:
    :param n:
    :param kwargs:
    :return:
    """
    from . import CON_CONTRACT_3, CON_CONTRACT_2
    return _rate_con_con(env, CON_CONTRACT_2, CON_CONTRACT_3, n, **kwargs)


def _rate_con_con(env, conx, cony, n=0, **kwargs):
    from . import REFD, CLOSE

    copy_env_x = copy.deepcopy(env)
    copy_env_x.contract = conx

    conx_close = REFD(copy_env_x, CLOSE, n - 1, conx, **kwargs)

    copy_env_y = copy.deepcopy(env)
    copy_env_y.contract = cony

    cony_close = REFD(copy_env_y, CLOSE, n - 1, cony, **kwargs)

    conx_close_array = np.swapaxes(np.array(conx_close), 0, 1)
    cony_close_array = np.swapaxes(np.array(cony_close), 0, 1)

    gap_close = conx_close_array[0] - cony_close_array[0]

    alert_price = conx_close_array[0] * 0.005

    rate_close = np.divide(gap_close, alert_price)

    result = abs(rate_close) >= 1

    logger.info("alert_price:%s, gap_close:%s, rate:%s, result:%s",
                alert_price,
                rate_close, gap_close, result)

    r_l = [result.tolist(), rate_close.tolist(), conx_close_array[1].tolist()]
    return r_l


def rate_opi_month(env, n=0, contract=None, **kwargs):
    """
    持仓环比
    :param env:
    :param n:
    :param kwargs:可能包含start_date, end_date
    :return:
    """
    from . import CON_CONTRACT_1, REFD, OPI

    # 需要多一个月的数据来进行环比
    cur_num = n - 1
    copy_kwargs = copy.deepcopy(kwargs)
    copy_kwargs["start_date"] = None
    con1_opi = REFD(env, OPI, cur_num + 30, CON_CONTRACT_1, **copy_kwargs)
    con1_array = REFD(env, CON_CONTRACT_1, cur_num + 30, **copy_kwargs)

    cut_off_month_dt = []

    # 获取交割日期
    for i in range(len(con1_array) - 1):
        if con1_array[i][0] != con1_array[i + 1][0]:
            cut_off_month_dt.append(con1_array[i][1])

    d_m, d_c, gd, r_gd, m_date, c_date = _rate_month(con1_opi,
                                                     cut_off_month_dt, n=n,
                                                     **kwargs)
    return [(r_gd >= 0).tolist(), r_gd.tolist(), c_date.tolist(), gd.tolist(),
            d_m.tolist(), d_c.tolist()]


def _rate_month(data_list, cut_date_list, n=0, **kwargs):
    """
    获取环比数据
    :param con1_opi: 处理的数据 [(111, datetime),(222, datetime)]
    :param cut_off_month_dt: [datetime, datetime]
    :param n: 选取多少条
    :param kwargs: 可能包含start_date  end_date
    :return:环比数据,  当前数据,  差值, 差值比, 环比数据日期, 当前数据日期
    """
    from . import mutip_data_gap

    # 按交割日期分割数据
    cut_off_month_data = _split_data_by_dt(data_list, cut_date_list)

    # 获取对齐数据
    current_data_array, month_data_array = _align_data(cut_off_month_data)

    k_s_dt = kwargs.get("start_date", None)
    k_e_dt = kwargs.get("end_date", next_day(datetime.date.today()))

    # 根据条件清理数据(limit, start_date, end_date)

    # 0. 三维数组合并成二维数组:
    current_data_array = _flatten_data(current_data_array)
    month_data_array = _flatten_data(month_data_array)

    # 1. 清理日期
    min_i, max_i = _clean_data_index(current_data_array)
    current_data_array = current_data_array[min_i: max_i + 1]
    month_data_array = month_data_array[min_i: max_i + 1]

    # 2. 清理limit
    current_data_array = _clean_data_limit(current_data_array, n)
    month_data_array = _clean_data_limit(month_data_array, n)
    logger.info("当前月数据取值%s, 环比数据取值:%s", current_data_array, month_data_array)

    # 环比数值
    current_data_array = np.swapaxes(np.array(current_data_array), 0, 1)
    month_data_array = np.swapaxes(np.array(month_data_array), 0, 1)

    d_m, d_c, gd, r_gd = mutip_data_gap(month_data_array[0],
                                        current_data_array[0])

    logger.info(
        "获取数据限制条数limit:%s, 开始日期:%s, 结束日期:%s, 差值:%s, 差值比率:%s", n,
        k_s_dt, k_e_dt, gd, r_gd)
    return d_m, d_c, gd, r_gd, month_data_array[1], current_data_array[1]


def _split_data_by_dt(split_data, cut_off_month_dt):
    """
    按交割日期分割数据
    split_data: 要分离的数据[(111, datetime.datetime.now()), (....), ;;;]
    cut_off_month_dt: 分离数据的日期[(111, datetime.datetime.now()), (...), ...)]
    cut_off_month_opi: 分离好的数据[[(111, datetime.datetime.now()), (...)],[ ...]]
    :return:
    """
    split_data = copy.deepcopy(split_data)
    dt_index = 0
    tmp_list = []
    last_list = []
    splited_data = []
    for opi, dt in split_data:
        if dt.strftime("%Y-%m-%d") <= cut_off_month_dt[dt_index].strftime(
                "%Y-%m-%d"):
            tmp_list.append((opi, dt))
        elif len(cut_off_month_dt) > dt_index + 1:
            splited_data.append(copy.copy(tmp_list))
            tmp_list = [(opi, dt)]
            dt_index += 1
        else:
            last_list.append((opi, dt))
    else:
        if tmp_list:
            splited_data.append(copy.copy(tmp_list))
        if last_list:
            splited_data.append(copy.copy(last_list))
    return splited_data


def _align_data(data_list):
    """
    对齐数组
    data_list :[ [(111,datetime), (222, datetime)], [(112, datetime)], [(223, datetime), (334, datetime)]]
    :return: [[(112, datetime)], [(223, datetime), (334, datetime)]]
            [[(111,datetime)], [(112, datetime),(112, datetime)]]
    """
    data_list = copy.deepcopy(data_list)
    current_data_array = []
    month_data_array = []
    for i in range(-1, -len(data_list), -1):
        c_array = copy.deepcopy(data_list[i])
        m_array = copy.deepcopy(data_list[i - 1])

        current_data_array.insert(0, c_array)

        lcd = len(c_array)
        lmd = len(m_array)
        if lcd < lmd:
            m_array = m_array[:lcd]
        elif lcd > lmd:
            [m_array.insert(0, m_array[0]) for x in range(lcd - lmd)]

        month_data_array.insert(0, m_array)

    return current_data_array, month_data_array


def _clean_data_index(index_data, start_date=None, end_date=None):
    """

    :param clean_data: [(111, datetime), (2222, datetime), (231, datetime)]
    :param start_date: datetime
    :param end_date: datetime
    :return: min_i, max_i
    """
    copy_data = copy.deepcopy(index_data)
    min_i = 0
    max_i = len(copy_data) - 1
    for i in range(len(copy_data)):
        dt = copy_data[i][1]
        if start_date and start_date.strftime("%Y-%m-%d") >= dt.strftime(
                "%Y-%m-%d"):
            min_i = i
        if end_date and end_date.strftime("%Y-%m-%d") > dt.strftime(
                "%Y-%m-%d"):
            max_i = i
    return min_i, max_i


def _clean_data_limit(data_list, limit):
    """
    :return:
    """
    data_list = copy.deepcopy(data_list)
    len_data = len(data_list)
    if len_data > limit:
        g_n = len_data - limit
        data_list = data_list[g_n:]
    return data_list


def _flatten_data(copy_data):
    copy_data = copy.deepcopy(copy_data)
    new_data = []
    [new_data.extend(copy.deepcopy(x)) for x in copy_data]
    return new_data
