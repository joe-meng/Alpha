# coding: utf-8
import logging
import traceback
from io import StringIO
from logging import StreamHandler
from timeout_decorator import timeout

from share.contrib import get_mysql_client
from workers.calculation.lib import mathlib
from workers.calculation.lib.utils import date_utils
from .check import security_check


logger = logging.getLogger('formula')
logger.setLevel(logging.DEBUG)


class ExecuteTimeout(Exception):
    pass


class ShareFormula(object):

    def __init__(self, id=None, formula=None, title=None, description=None, user_id=None):
        self.id = id
        self.formula = formula
        self.title = title
        self.description = description
        self.user_id = user_id
        self._varieties = None

    @property
    def varieties(self):
        if self._varieties is None:
            sql = 'select varieties_id from formula_varieties where formula_id = %s'
            with get_mysql_client() as cursor:
                cursor.execute(sql, (self.id,))
                result = cursor.fetchall()
            self._varieties = [item['varieties_id'] for item in result]
        return self._varieties


class BaseExecutor(object):

    def __init__(self, formula, env, out_logger=None):
        self.formula = formula
        self.env = env
        self.success = False
        self.chart_data = None
        self.io = None
        self.handler = None
        self.logger = self.get_logger(out_logger)

    def get_logger(self, outer_logger=None):
        if outer_logger:
            return outer_logger
        self.io = StringIO()
        self.handler = StreamHandler(self.io)
        fmt = logging.Formatter('%(levelname)s %(asctime)s '
                                '[%(lineno)d]: %(message)s')
        self.handler.setFormatter(fmt)
        logger.addHandler(self.handler)
        return logger

    def run(self):
        code = self.formula.formula
        try:
            # exec执行有风险
            self.exec(code)
            self.success = True
        except ExecuteTimeout:
            self.logger.error('公式运行超时，请检查您的代码。')
            self.success = False
        except:
            self.logger.error(str(traceback.format_exc()))
            self.success = False
        finally:
            if logger != self.logger:
                return
            self.logger.removeHandler(self.handler)
            execute_log = self.io.getvalue()
            self.io.close()
            return execute_log

    def alert(self, env, message, alert):
        raise NotImplemented

    def chart(self, env, price, contract='main_contract'):
        raise NotImplemented

    @property
    def globals_dict(self):
        return {}

    @property
    def locals_dict(self):
        return {'e': self.env,
                'logger': self.logger,
                'print': self.logger.info}

    def exec(self, code):
        exec(code, self.globals_dict, self.locals_dict)


class ApiFormulaExecutor(BaseExecutor):

    def exec(self, code):
        security_check(code)
        super().exec(code)

    def alert(self, env, message, alert=True):
        if alert:
            self.logger.info(message)

    def chart(self, env, price, contract='main_contract'):
        self.chart_data = {'variety': env.content_variety,
                           'price': price,
                           'contract': contract}

    @property
    def locals_dict(self):
        a = {attr: getattr(mathlib, attr) for attr in dir(mathlib) if not attr.startswith('__')}
        b = {attr: getattr(date_utils, attr) for attr in dir(date_utils) if not attr.startswith('__')}
        a.update(b)
        a.update({'e': self.env,
                  'logger': self.logger,
                  'print': self.logger.info,
                  'ALERT': self.alert,
                  'CHART': self.chart})
        return a


class WorkerFormulaExecutor(BaseExecutor):

    @timeout(10, use_signals=True, timeout_exception=ExecuteTimeout)
    def exec(self, code):
        super().exec(code)

    @property
    def locals_dict(self):
        a = {attr: getattr(mathlib, attr) for attr in dir(mathlib) if not attr.startswith('__')}
        b = {attr: getattr(date_utils, attr) for attr in dir(date_utils) if not attr.startswith('__')}
        a.update(b)
        a.update({'e': self.env,
                  'logger': self.logger,
                  'print': self.logger.info})
        return a
