#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@date: 2017-06-30

@author: Devin
"""

from .constant import *
from .kdata import *
from .mathfun import *
from .refmode import *
from .refrate import *
from .trendfun import *


def CHART(e, price, contract=MAIN_CONTRACT):
    """
    警告图
    :param e:环境
    :param price: 警告图显示的code
    :param contract: 警告图显示的合约
    :return:
    """
    e.price = price
    e.contract = contract


def ALERT(e, message, alert=True):
    """
    警告信息
    :param e:环境
    :param message:警告包含的信息
    :param enable: 是否警告
    :return:
    """
    e.introduction = message
    e.alert = alert
