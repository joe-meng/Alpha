#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@desc: 走势函数

@date: 2017-06-29

@author: Devin
"""

import numpy as np

from settings import logger


def ISDOWN(env):
    """
    判断该周期是否收阴
    :param t_data:该周期数据,类数组
    :return:
    """
    from . import KOPEN, KCLOSE
    open_price = KOPEN(env)
    close_price = KCLOSE(env)
    gap = close_price - open_price
    return gap < 0, [gap]


def ISEQUAL(env):
    """
    判断该周期是是否平盘,即十字星
    :param t_data:该周期数据,类数组
    :return:
    """
    from . import KOPEN, KCLOSE, data_gap, REF, DOJI_STAR_THRESHOLD
    threshold = REF(env, DOJI_STAR_THRESHOLD)[0]
    open_price = KOPEN(env)
    close_price = KCLOSE(env)
    data = [open_price, close_price]
    d1, d2, gd, r_gd = data_gap(data)
    logger.info("开盘价:%s, 收盘价:%s, 差值:%s, 差值比:%s", d1, d2, gd, r_gd)
    result = (threshold - abs(r_gd)) >= 0
    return result.all().tolist(), ["%.6f" % r_gd[0]], threshold


def ISUP(env):
    """
    判断该周期是否收阳
    :param t_data:该周期数据,类数组
    :return:
    """
    from . import KOPEN, KCLOSE
    open_price = KOPEN(env)
    close_price = KCLOSE(env)
    gap = close_price - open_price
    return gap > 0, [gap]


def ISCONTUP(t_data, interval_rate=None, all_rate=None, isge=True):
    """
    是否持续上升
    :param t_data:该周期数据,类数组
    :param interval_rate:相临数据间的比率,
    :param all_rate:首尾数据比率
    :param isge:是否大于等于比率/否则小于等于比率
    :return:
    """
    from . import data_gap
    d1, d2, gd, rate = data_gap(t_data)

    if all_rate != None and interval_rate != None:
        inter_list = np.ones(len(t_data), dtype=float) * interval_rate
        inter_list[0] = all_rate
        if isge:
            result_list = (rate - inter_list) >= 0
        else:
            result_list = (rate - inter_list) <= 0
        return result_list.all().tolist(), gd.tolist()

    if all_rate != None:
        if isge:
            return (rate[1] >= all_rate).tolist(), gd[:1].tolist()
        else:
            return (rate[1] <= all_rate).tolist(), gd[:1].tolist()

    if interval_rate != None:
        inter_list = np.ones((len(t_data) - 1), dtype=float) * interval_rate
        if isge:
            result_list = (rate[1:] - inter_list) >= 0
        else:
            result_list = (rate[1:] - inter_list) <= 0
        return result_list.all().tolist(), gd[1:].tolist()


def ISCONTDOWN(t_data, interval_rate=None, all_rate=None, isge=True):
    """
    是否持续下降
    :param t_data:该周期数据,类数组
    :param interval_rate:相临数据间的比率,
    :param all_rate:首尾数据比率
    :param isge:是否大于等于比率/否则小于等于比率
    """
    from . import data_gap
    d1, d2, gd, rate = data_gap(t_data)
    gd = -gd
    rate = -rate

    if all_rate != None and interval_rate != None:
        inter_list = np.ones(len(t_data), dtype=float) * interval_rate
        inter_list[0] = all_rate
        if isge:
            result_list = (rate - inter_list) >= 0
        else:
            result_list = (rate - inter_list) <= 0
        return result_list.all().tolist(), gd.tolist()

    if all_rate != None:
        if isge:
            return (rate[1] >= all_rate).tolist(), gd[:1].tolist()
        else:
            return (rate[1] <= all_rate).tolist(), gd[:1].tolist()

    if interval_rate != None:
        inter_list = np.ones((len(t_data) - 1), dtype=float) * interval_rate
        if isge:
            result_list = (rate[1:] - inter_list) >= 0
        else:
            result_list = (rate[1:] - inter_list) <= 0
        return result_list.all().tolist(), gd[1:].tolist()

def ISCONTCHANGE(t_data, interval_rate=None, all_rate=None, isge=True):
    """
    是否持续改变
    :param t_data:该周期数据,类数组
    :param interval_rate:相临数据间的比率,
    :param all_rate:首尾数据比率
    :param isge:是否大于等于比率/否则小于等于比率
    """
    is_con_up, up_data = ISCONTUP(t_data, interval_rate, all_rate, isge)
    is_con_down, down_data = ISCONTDOWN(t_data, interval_rate, all_rate, isge)
    return is_con_up or is_con_down, up_data

def ISCONTUPABS(t_data, interval_abs=None, all_abs=None, isge=True):
    """
    是否持续上升
    :param t_data:该周期数据,类数组
    :param interval_abs:相临数据间的差值,
    :param all_abs:首尾数据差值
    :param isge:是否大于等于差值/否则小于等于差值
    :return:
    """
    from . import data_gap
    d1, d2, gd, rate = data_gap(t_data)

    if all_abs != None and interval_abs != None:
        inter_list = np.ones(len(t_data), dtype=float) * interval_abs
        inter_list[0] = all_abs
        if isge:
            result_list = (gd - inter_list) >= 0
        else:
            result_list = (gd - inter_list) <= 0
        return result_list.all().tolist(), gd.tolist()

    if all_abs != None:
        if isge:
            return (gd[1] >= all_abs).tolist(), gd[:1].tolist()
        else:
            return (gd[1] <= all_abs).tolist(), gd[:1].tolist()

    if interval_abs != None:
        inter_list = np.ones((len(t_data) - 1), dtype=float) * interval_abs
        if isge:
            result_list = (gd[1:] - inter_list) >= 0
        else:
            result_list = (gd[1:] - inter_list) <= 0
        return result_list.all().tolist(), gd[1:].tolist()


def ISCONTDOWNABS(t_data, interval_abs=None, all_abs=None, isge=True):
    """
    是否持续上升
    :param t_data:该周期数据,类数组
    :param interval_abs:相临数据间的差值,
    :param all_abs:首尾数据差值
    :param isge:是否大于等于差值/否则小于等于差值
    :return:
    """
    from . import data_gap
    d1, d2, gd, rate = data_gap(t_data)
    gd = -gd
    rate = -rate

    if all_abs != None and interval_abs != None:
        inter_list = np.ones(len(t_data), dtype=float) * interval_abs
        inter_list[0] = all_abs

        if isge:
            result_list = (gd - inter_list) >= 0
        else:
            result_list = (gd - inter_list) <= 0
        return result_list.all().tolist(), gd.tolist()

    if all_abs != None:
        if isge:
            return (gd[1] >= all_abs).tolist(), gd[:1].tolist()
        else:
            return (gd[1] <= all_abs).tolist(), gd[:1].tolist()

    if interval_abs != None:
        inter_list = np.ones((len(t_data) - 1), dtype=float) * interval_abs
        if isge:
            result_list = (gd[1:] - inter_list) >= 0
        else:
            result_list = (gd[1:] - inter_list) <= 0
        return result_list.all().tolist(), gd[1:].tolist()


def ISCONTCHANGEABS(t_data, interval_abs=None, all_abs=None, isge=True):
    """
    是否持续改变绝对值
    :param t_data:该周期数据,类数组
    :param interval_abs:相临数据间的差值,
    :param all_abs:首尾数据差值
    :param isge:是否大于等于差值/否则小于等于差值
    """
    is_con_up, up_data = ISCONTUPABS(t_data, interval_abs, all_abs, isge)
    is_con_down, down_data = ISCONTDOWNABS(t_data, interval_abs, all_abs, isge)
    return is_con_up or is_con_down, up_data


def CONTUPDETAIL(base_data, comp_data, interval_abs=0):
    """
    获取持续上升具体数据
    :param base_data: 基数数组
    :param comp_data: 被对比的数据
    :param interval_abs: 差值
    :return:
    """
    from . import mutip_data_gap
    d1, d2, gd, rate = mutip_data_gap(base_data, comp_data)
    r_l = gd > interval_abs

    con_up_count = 0
    for i in range(-1, -1-len(r_l), -1):
        if r_l[i]:
            con_up_count += 1
        else:
            break
    return d1, d2, con_up_count, gd[-con_up_count:], rate[-con_up_count:]


def COUNTGT(d_list, number=0):
    """
    返回持续
    :param d_list:
    :return:
    """
    con_up_count = 0
    for i in range(-1, -1-len(d_list), -1):
        if d_list[i] >= number:
            con_up_count += 1
        else:
            break
    return con_up_count

