#!/usr/bin/env python
# -*- coding: utf-8 -*-


# 在这个方法中编写任何的初始化逻辑。e对象将会在你的算法策略的任何方法之间做传递。
# 你选择的品目数据更新将会触发此段逻辑
data = REF(e, PD, 3)
e.alert, e.result = ISCONTDOWN(data, 0)

e_variety = e.ch_variety
e.introduction = "%sSMM升贴水连续下跌3天" % e_variety

logger.info(e.introduction)
