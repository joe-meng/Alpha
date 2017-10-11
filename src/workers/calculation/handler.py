#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import traceback

from lib.datalib.model.formula import Formula
from lib.vo import FormulaEnv
from pubmsg import pub
from settings import logger, ShareFormula, WorkerFormulaExecutor


class CalcMessageHandler(object):
    def __init__(self):
        self.formula = Formula()

    def formulas(self, variety, price_code=[]):
        formulas_list = self.formula.list(variety, price_code, result_type=tuple)
        return formulas_list

    def do_handle(self, pre_data):
        for f, db_id, unit in self.formulas(pre_data.get_variety()):
            env = FormulaEnv(db_id, unit, pre_data)
            share_formula = ShareFormula(db_id, f)
            executor = WorkerFormulaExecutor(share_formula, env, out_logger=logger)
            try:
                executor.run()
                self._pub_alert_msg(env)
            except Exception as e:
                logger.error("公式%s出现了异常%s, 上下文是%s", db_id,
                             traceback.format_exc(), env)
                continue

    def _pub_alert_msg(self, env):
        logger.info("警告消息为:%s", env.pub_msg_dict)
        pub_msg_str = json.dumps(env.pub_msg_dict)
        pub(pub_msg_str)
