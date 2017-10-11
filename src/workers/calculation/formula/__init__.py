#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@date: 2017-07-05

@author: Devin
"""
from formula.base import warrant_con_down, lme_stock_con_up, \
    lme_stock_con_down, warrant_daily_up, warrant_daily_down, \
    warrant_con_up, DOJI_STAR, exchange_lme, con1_con2_abs, \
    con2_con3_abs, con1_con3_abs, opi_monthly_con_up, \
    warrant_monthly_con_up,smm_spot_daily_up, smm_spot_daily_down,\
    smm_bwd_con_down, smm_bwd_con_up, smm_spot_week_down, smm_spot_week_up
from formula.cu_al import cu_al_smm_bwd_con_down,\
    cu_al_smm_bwd_con_up, cu_al_smm_spot_daily_down, cu_al_smm_spot_daily_up,\
    cu_al_smm_spot_week_down,cu_al_smm_spot_week_up

formula_list = [
    (warrant_daily_up, 1, "吨"),
    # (warrant_daily_down, 2, "吨"),
    # (warrant_con_up, 3, "吨"),
    # (warrant_con_down, 4, "吨"),
    # (lme_stock_con_up, 5, "吨"),
    # (lme_stock_con_down, 6, "吨"),
    # (cu_al_smm_spot_daily_up, 7, "元"),
    # (cu_al_smm_spot_daily_down, 8, "元"),
    # (cu_al_smm_bwd_con_up, 9, "元"),
    # (cu_al_smm_bwd_con_down, 10, "元"),
    # (cu_al_smm_spot_week_up, 11, "元"),
    # (cu_al_smm_spot_week_down, 12, "元"),
    # (DOJI_STAR, 13, ""),
    # (exchange_lme, 14, "元"),
    # (opi_monthly_con_up, 15, "手"),
    # (warrant_monthly_con_up, 16, "吨"),
    # (con1_con2_abs, 17, "元"),
    # (con2_con3_abs, 18, "元"),
    # (con1_con3_abs, 19, "元"),
    # (smm_spot_daily_up, 20, "元"),
    # (smm_spot_daily_down, 21, "元"),
    # (smm_bwd_con_up, 22, "元"),
    # (smm_bwd_con_down, 23, "元"),
    # (smm_spot_week_up, 24, "元"),
    # (smm_spot_week_down, 25, "元"),
]

__all__ = ['formula_list']
