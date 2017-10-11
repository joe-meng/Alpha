#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@date: 2017-08-17

@author: Devin
"""
from sqlbuilder.smartsql import Q, T, Result
from sqlbuilder.smartsql.dialects.mysql import compile as mysql_compile

from .base import Base


class Formula(Base):
    def list(self, variety, price_code=[], result_type=dict, **kwargs):
        f_tb = T.formula
        fv_tb = T.formula_varieties
        vr_tb = T.varieties_record

        tbs = ((f_tb + fv_tb).on(f_tb.id == fv_tb.formula_id) & vr_tb).on(
            fv_tb.varieties_id == vr_tb.id)

        q = Q(tbs, result=Result(compile=mysql_compile)). \
            fields(f_tb.formula, f_tb.id, f_tb.unit). \
            where(vr_tb.code == variety).where(f_tb.enable == 1)

        for code in price_code:
            t_code = "%" + code + ",%"
            q = q.where(vr_tb.trigger_price_code.like(t_code))

        data = self.get_record(*q.select(), **kwargs)
        if result_type == tuple:
            data = [(x["formula"], x["id"], x["unit"]) for x in data]
        return data

