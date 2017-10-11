#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import json

import re


class FormulaEnv(object):
    """
    公式内部参数定义
    """

    def __init__(self, id=None, unit="", pre_data=None):
        # 公式编号
        self.id = id
        # 预处理的数据
        self.pre_data = pre_data
        # 介绍
        self.introduction = ""
        # 品目
        self.varieties = None
        # 合约
        self.contract = None
        # 是否警告
        self.alert = False
        # 数据
        self.result = []
        # 指标
        self.price = None
        # 单位
        self.unit = unit

    @property
    def tuple(self):
        return self.id, self.alert, self.introduction

    @property
    def pub_msg_dict(self):
        if self.alert:
            message = "【有色在线】" + datetime.date.today().strftime(
                "%Y-%m-%d") + self.introduction
            # if self.result:
            #     message += "(" + ",".join([str(x) + self.unit for x in self.result]) + ")"
        else:
            message = ""

        return dict(
            chart=dict(variety=self.content_variety, price=self.price,
                       contract=self.contract),
            alert=dict(enable=self.alert, message=message),
            formula=dict(id=self.id)
        )

    @property
    def content_variety(self):
        return self.pre_data.varieties.lower()

    @property
    def ch_variety(self):
        return self.pre_data.get_ch_varieties()

    def is_main_contract(self):
        from lib.mathlib import MAIN_CONTRACT
        if not self.contract:
            self.contract = MAIN_CONTRACT
        return self.contract == MAIN_CONTRACT

    def is_contract_N(self):
        return re.match("^CON\_CONTRACT\_\d{1,2}$", self.contract)

    def is_corrp_formula(self):
        """
        判断该公式是否适用于content_varieties运算
        :return:
        """
        c_v = self.content_variety
        if type(self.varieties) == str:
            return self.varieties.lower() == c_v.lower()
        return any([x.lower() == self.content_variety.lower() for x in
                    self.varieties])

    def __str__(self):
        return "公式编号:%s, 预处理的数据:%s, 介绍:[%s], 品目:%s,合约:%s," \
               "是否警告:%s,数据:%s,指标:%s, 单位:%s" % (
                   self.id, self.pre_data, self.introduction, self.varieties,
                   self.contract, self.alert, self.result,
                   self.price, self.unit)


class PreProcessMessage(object):
    """
    预处理传过来的消息
    """

    def __init__(self, text):
        self.text = text
        self.json = json.loads(text)

    @property
    def insert_id(self):
        return self.json.get('insert_id')

    @property
    def varieties(self):
        return self.json.get('varieties')


class DBPreProcess(object):
    """
    数据库表preprocess_data的一条数据
    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        # 编号
        self.id = kwargs.get("id", "null")
        # 品目
        self.varieties = kwargs.get("varieties")

    def get_ch_varieties(self):
        from .mathlib import variety_chinese
        v = self.varieties.lower()
        if v in variety_chinese:
            return variety_chinese.get(v)
        return v

    def get_variety(self):
        return self.varieties

    def __str__(self):
        return "编号:%s, 品目%s, 其它:%s" % (self.id, self.varieties, self.kwargs)
