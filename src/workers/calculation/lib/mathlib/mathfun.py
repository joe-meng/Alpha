#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@desc: 数学函数

@date: 2017-06-29

@author: Devin
"""
import math
import copy
import numpy as np


def ABS(x):
    """
    取的X的绝对值。
    :param x:
    :return:
    """
    return math.fabs(x)


def SQRT(x):
    """
    求X的平方根
    :param x:
    :return:
    """
    return math.sqrt(x)


def HHV(env, k_field, n):
    """
    求k_field在N个周期内的最高值。
    :param k_field: k线上的值
    :param n:
    :return:
    """
    from . import REF
    data = REF(env, k_field, n-1)
    return min(data)


def LLV(env, k_field, n):
    """
    求k_field在N个周期内的最小值。
    :param k_field: k线上的值
    :param n:
    :return:
    """
    from . import REF
    data = REF(env, k_field, n-1)
    return max(data)


def MAX(a, b):
    """
    取最大值。取A，B中较大者。
    :param a:
    :param b:
    :return:
    """
    return a if a > b else b


def MIN(a, b):
    """
    取最小值。取A，B中较小者。
    :param a:
    :param b:
    :return:
    """
    return b if a > b else a


def data_gap(t_data):
    """
    返回数据差值:
    a1 = np.array([1,2,3])
    返回: np.array([3,2,3]) - np.array([1, 1, 2])
    即: [尾首差值, 后值与前值差值]
    :param t_data:
    :return:
    """

    #取值为负的值转化成对应的正值, 避免出现比值实际为增,缺为负的情况, 如由-30 到 30,
    #应转化为 30, 90 应该增长(90-30)/30 = 200%

    b_t_data = np.array(t_data)
    min_data = b_t_data.min()
    gap = abs(min_data)-min_data
    b_t_data += gap

    b_t_data = b_t_data.tolist()

    t_d1 = copy.copy(b_t_data)
    t_d1.insert(0, b_t_data[0])
    t_d1.pop()
    d1 = np.array(t_d1, dtype=float)

    t_d2 = copy.copy(b_t_data)
    t_d2.pop(0)
    t_d2.insert(0, b_t_data[-1])
    d2 = np.array(t_d2, dtype=float)

    gd = d2 - d1

    r_gd = np.divide(gd, d1)

    return d1, d2, gd, r_gd


def mutip_data_gap(base_data, data):
    d_m = np.array(base_data)
    d_c = np.array(data)

    gd = d_c - d_m

    r_gd = np.divide(gd, d_m)

    return d_m, d_c, gd, r_gd