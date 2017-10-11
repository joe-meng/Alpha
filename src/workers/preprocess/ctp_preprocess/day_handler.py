# -- coding: utf-8 --
import traceback

import logs
import os
import sys
import json
import datetime
import re
import logging
import when
sys.path.append("../..")
# from share.mq import channel

from sqlalchemy import desc
# from send_ready_data import send_message_to_ready_queue
# from share.utils import MysqlHnadler
from send_ready_data import send_message_to_ready_queue
from utils.enums import MIN_PARA_MODEL_MAP, MIN_VARIEYIES_DICT, \
                            DAY_VARIEYIES_DICT, ALLOW_EXCHANGE, \
                            ALLOW_VARIETIES, PRE_SYMBOL, DAY_PARA_MODEL_MAP
from models.models import Session, DayKline, MainContract, MinPreprocess, DayPreprocess, CapitalFlowsDay, CapitalFlowsMin
from utils.cal_settings import DAY_INIT_PATA_MAP, DAY_RES_DEAL_MAP, COMMON_RES_DAEL_LIST, COMMON_INIT_LIST
from common.ctp import BasePreprocess, BaseInitPreprocess, BaseResPreprocess
from check import check

init_check = os.environ.get('init_check', None)
_logger = logging.getLogger(__name__)
# _logger = None
# db = Session()
# from share.base import base_handler


def cal_day(ch, method, properties, body):
    info = body.decode('utf8').split(",")
    exchange = info[1]
    if exchange not in ALLOW_EXCHANGE:
        return
    day_min = info[2]
    contract = info[0]
    date = info[3].split(" ")[0]
    replace_info = re.findall(r'(\d+)', contract)
    varieties = contract.replace(replace_info[0], "")
    if varieties.lower() not in ALLOW_VARIETIES:
        return
    try:
        cal_day_info(varieties, exchange, date)
    except:
        logging.error("cal_day 数据异常, 数据:%s, 异常:%s", info, traceback.format_exc())


class DayPreProcess(BasePreprocess):
    """日数据预处理对象,保存计算公式"""

    def __init__(self, varieties, date, exchange, *args, **kwargs):
        super(DayPreProcess, self).__init__(*args, **kwargs)
        self.varieties = varieties
        self.date = date
        self.exchange = exchange
        self.basic_1_2 = 0
        self.basic_1_3 = 0
        self.basic_2_3 = 0
        self.contract1_price = 0
        self.contract2_price = 0
        self.contract3_price = 0


    @property
    def calculation_basic_rate(self):
        """计算基差比值"""
        if not self.contract1_price:
            self.calculation_basic
        price_1 = self.contract1_price
        price_2 = self.contract2_price
        price_3 = self.contract3_price
        if not price_1:
            basic_1_2_rate = 0
            basic_1_3_rate = 0
        else:
            basic_1_2_rate = round((price_1 - price_2) / price_1, 4)
            basic_1_3_rate = round((price_1 - price_3) / price_1, 4)
        if not price_2:
            basic_2_3_rate = 0
        else:
            basic_2_3_rate = round((price_2 - price_3) / price_2, 4)
        res = {
            "basic_1_2_rate": basic_1_2_rate,
            "basic_1_3_rate": basic_1_3_rate,
            "basic_2_3_rate": basic_2_3_rate,
        }
        return res


    # @property
    # def calculation_basic(self):
    #     self.basic_1_2 = self.contract1_price - self.contract2_price
    #     self.basic_1_3 = self.contract1_price - self.contract3_price
    #     self.basic_2_3 = self.contract2_price - self.contract3_price
    #     return {
    #         'basic_1_2': self.basic_1_2,
    #         'basic_1_3': self.basic_1_3,
    #         'basic_2_3': self.basic_2_3,
    #     }



class DayInitPreProcess(BaseInitPreprocess):
    """日数据预处理对象初始化"""


    def __init__(self, db, varieties, date, exchange, *args, **kwargs):
        super(DayInitPreProcess, self).__init__(varieties, date, exchange, *args, **kwargs)
        self.pre_obj = DayPreProcess(varieties, date, exchange)
        self.db = db
        # self.init_main_contract()

    def init_symbol(self):
        """初始化最新分钟数据"""
        for pre_code in PRE_SYMBOL:
            obj = MIN_PARA_MODEL_MAP.get(pre_code)
            if not obj:
                continue
            symbol = MIN_VARIEYIES_DICT.get(self.varieties.lower()) + PRE_SYMBOL[pre_code]
            model_objs = self.db.query(obj).filter(obj.symbol == symbol,
                                              obj.date.like(self.date + "%")).order_by(desc(obj.date)).all()
            if not model_objs:
                continue
            model_obj = model_objs[0]
            setattr(self.pre_obj, symbol, model_obj.amount)


    def init_serial_price(self):
        """初始化获取连一连二连三,连六的价格"""
        # keys = ['serial_contract1', 'serial_contract2', 'serial_contract3', #'serial_contract4', 'serial_contract5',
        #         'serial_contract6']
        keys = [1, 2, 3, 6]
        if self.pre_obj.main_contract:
            for key in keys:
                # index = keys.index(key) + 1
                contract = 'serial_contract'+ str(key)
                if self.pre_obj.main_contract.get(contract):
                    dk_objs = self.db.query(DayKline).filter(DayKline.contract == self.pre_obj.main_contract[contract],
                                                             DayKline.date_time == self.pre_obj.date) \
                                                                .order_by(desc(DayKline.date_time)).all()
                    if dk_objs:
                        # pre_obj.contract1_price = dk_objs[0].get('price_close')
                        if dk_objs[0].settlement_price:
                            setattr(self.pre_obj, 'contract' + str(key) + '_price', dk_objs[0].settlement_price)
                        elif dk_objs[0].price_close:
                            setattr(self.pre_obj, 'contract' + str(key) + '_price', dk_objs[0].price_close)
                    else:
                        _logger.info('datetime::%s, contract::%s对应的day_kline数据不存在' % (
                        self.date, self.pre_obj.main_contract[contract]))
                else:
                    _logger.info('%s:这一天的:%s: 合约不存在' % (self.date, self.pre_obj.main_contract[contract]))
        else:
            _logger.info('主力合约信息不存在')


    def init_serial_price_1_5_9(self):
        """初始化159合约的连一连二连三的价格"""
        date_time = self.pre_obj.date + ' 00:00:00'
        k = 0
        # month = today.month
        for i in range(1, 13):
            # month = (when._add_time(today, months=i)).month
            contract = 'serial_contract' + str(i)
            if not self.pre_obj.main_contract[contract]:
                continue
            month = str(self.pre_obj.main_contract[contract])[-2:]
            if month in ['01', '05', '09']:
                k = k + 1
                # contract = 'serial_contract' + str(i)
                dk_objs = self.db.query(DayKline).filter(DayKline.contract == self.pre_obj.main_contract[contract],
                                                         DayKline.date_time == date_time) \
                    .order_by(desc(DayKline.date_time)).all()
                if dk_objs:
                    # pre_obj.contract1_price = dk_objs[0].get('price_close')
                    price = dk_objs[0].settlement_price or dk_objs[0].price_close or 0.0
                    setattr(self.pre_obj, 'contract' + str(k) + '_price', price)
                else:
                    _logger.info('datetime::%s, contract::%s对应的day_kline数据不存在' % (
                        self.date, self.pre_obj.main_contract[contract]))


    def init_serial_price_1_5_10(self):
        """初始化1,5, 10, 合约的连一连二连三的价格"""
        date_time = self.pre_obj.date + ' 00:00:00'
        # month = today.month
        k = 0
        for i in range(1, 13):
            contract = 'serial_contract' + str(i)
            month = str(self.pre_obj.main_contract[contract])[-2:]
            if month in ['01', '05', '10']:
                k = k + 1
                contract = 'serial_contract' + str(i)
                dk_objs = self.db.query(DayKline).filter(DayKline.contract == self.pre_obj.main_contract[contract],
                                                         DayKline.date_time == date_time) \
                    .order_by(desc(DayKline.date_time)).all()
                if dk_objs:
                    # pre_obj.contract1_price = dk_objs[0].get('price_close')
                    price = dk_objs[0].settlement_price or dk_objs[0].price_close or 0.0
                    setattr(self.pre_obj, 'contract' + str(k) + '_price', price)
                else:
                    _logger.info('datetime::%s, contract::%s对应的day_kline数据不存在' % (
                        self.date, self.pre_obj.main_contract[contract]))


class DayResPreProcess(BaseResPreprocess):
    """日数据结果获取对象"""

    persis_obj_map = DAY_PARA_MODEL_MAP
    varieties_map = DAY_VARIEYIES_DICT

    def __init__(self, db, pre_obj, *args, **kwargs):
        self.db =db
        self.pre_obj = pre_obj
        self.varieties = pre_obj.varieties
        self.date = pre_obj.date
        self.res = {}
        self.persis_map = DAY_PARA_MODEL_MAP #持久化对象对应关系
        self.persis_map = DAY_PARA_MODEL_MAP #持久化对象对应关系
        self.varieties_map = DAY_VARIEYIES_DICT #获取品类对应的symbol映射
        super(DayResPreProcess, self).__init__(*args, **kwargs)


    def translate_from_min(self):
        """根据分钟数据生成日数据"""
        for pre_code in PRE_SYMBOL:
            obj = MIN_PARA_MODEL_MAP.get(pre_code)
            if not obj:
                continue
            symbol = MIN_VARIEYIES_DICT.get(self.varieties.lower())+PRE_SYMBOL[pre_code]
            if not hasattr(self.pre_obj, symbol):
                continue
            amount = getattr(self.pre_obj, symbol)
            day_symbol = DAY_VARIEYIES_DICT.get(self.varieties.lower()) + PRE_SYMBOL[pre_code]
            day_obj = DAY_PARA_MODEL_MAP.get(pre_code)
            day_model_objs = self.db.query(day_obj).filter(day_obj.symbol == day_symbol,
                                                      day_obj.date == self.date).all()
            if day_model_objs:
                day_model_objs[0].amount = amount
            else:
                new_day_obj = day_obj(date=self.date, symbol=day_symbol, amount=amount)
                self.db.add(new_day_obj)
        self.db.commit()


    def update_capital_value(self):
        """日数据更新资金流动"""
        date = self.pre_obj.date
        obj = CapitalFlowsDay
        self.common_update_capital_value(date, obj)


    def in_and_out(self):
        """进出口"""
        self.res.update({'change': self.pre_obj.change,})
        self.res.update(self.pre_obj.cal_change_1m)
        self.res.update(self.pre_obj.cal_change_2m)
        self.res.update(self.pre_obj.cal_change_3m)
        self.res.update(self.pre_obj.cal_change_6m)
        self.res.update(self.pre_obj.cal_import_cost)
        self.res.update(self.pre_obj.cal_import_cost_1m)
        self.res.update(self.pre_obj.cal_import_cost_2m)
        self.res.update(self.pre_obj.cal_import_cost_3m)
        self.res.update(self.pre_obj.cal_import_cost_6m)
        self.res.update(self.pre_obj.cal_domestic_price)
        self.res.update(self.pre_obj.cal_domestic_price_1m)
        self.res.update(self.pre_obj.cal_domestic_price_2m)
        self.res.update(self.pre_obj.cal_domestic_price_3m)
        self.res.update(self.pre_obj.cal_domestic_price_6m)
        self.res.update(self.pre_obj.cal_cur_rate)
        self.res.update(self.pre_obj.cal_1m_rate)
        self.res.update(self.pre_obj.cal_2m_rate)
        self.res.update(self.pre_obj.cal_3m_rate)
        self.res.update(self.pre_obj.cal_6m_rate)
        self.res.update(self.pre_obj.cal_profit)
        self.res.update(self.pre_obj.cal_profit_1m)
        self.res.update(self.pre_obj.cal_profit_2m)
        self.res.update(self.pre_obj.cal_profit_3m)
        self.res.update(self.pre_obj.cal_profit_6m)
        self.get_hulun_rate()


    def get_in_and_out_other(self):
        """159等非全年活跃合约进出口"""
        self.res.update({'change': self.pre_obj.change,})
        self.res.update(self.pre_obj.cal_change_2m)
        self.res.update(self.pre_obj.cal_change_3m)
        # self.res.update(self.pre_obj.cal_change_6m)
        self.res.update(self.pre_obj.cal_import_cost)
        self.res.update(self.pre_obj.cal_import_cost_1m)
        self.res.update(self.pre_obj.cal_import_cost_2m)
        self.res.update(self.pre_obj.cal_import_cost_3m)
        # self.res.update(self.pre_obj.cal_import_cost_6m)
        self.res.update(self.pre_obj.cal_domestic_price)
        self.res.update(self.pre_obj.cal_domestic_price_1m)
        self.res.update(self.pre_obj.cal_domestic_price_2m)
        self.res.update(self.pre_obj.cal_domestic_price_3m)
        # self.res.update(self.pre_obj.cal_domestic_price_6m)
        self.res.update(self.pre_obj.cal_cur_rate)
        self.res.update(self.pre_obj.cal_1m_rate)
        self.res.update(self.pre_obj.cal_2m_rate)
        self.res.update(self.pre_obj.cal_3m_rate)
        # self.res.update(self.pre_obj.cal_6m_rate)
        self.res.update(self.pre_obj.cal_profit)
        self.res.update(self.pre_obj.cal_profit_1m)
        self.res.update(self.pre_obj.cal_profit_2m)
        self.res.update(self.pre_obj.cal_profit_3m)
        # self.res.update(self.pre_obj.cal_profit_6m)
        self.get_hulun_rate()



def cal_day_info(varieties, date, exchange):
    db = Session()
    init_obj = DayInitPreProcess(db, varieties, date, exchange)
    init_list = COMMON_INIT_LIST + DAY_INIT_PATA_MAP.get(varieties, [])
    for para in init_list:
        init_res = getattr(init_obj, para)()
        if init_res == "exit":
            # db.roll_back()
            db.close()
            return
    res_obj = DayResPreProcess(db, init_obj.pre_obj)
    deal_list = DAY_RES_DEAL_MAP.get(varieties, []) + COMMON_RES_DAEL_LIST
    for deal in deal_list:
        getattr(res_obj, deal)()
    res = res_obj.res
    res_obj.save_symbol_data(res, date)
    # print(res_obj.res, date)
    _logger.info('完成计算 res: %s, 日期: %s, 品类: %s'%(res_obj.res, date, res_obj.varieties))
    if init_check:
        check(init_obj, init_list)
    send_message_to_ready_queue(json.dumps({"varieties": varieties}))
    db.commit()
    db.close()



if __name__ == '__main__':
    # import sys
    # import os
    # os.environ['ALPHA_ENV'] = 'test'
    # 计算日数据入口
    # date = "2017-08-22"
    date = "2017-09-13"
    # v_list = ["cu", "al", "pb", "zn", "ni"]
    # v_list = ["pp"]
    # for varieties in v_list:
    #     cal_day_info("hc", date, "shfe")
    # cal_day_info("pp", date, "dce")
    cal_day_info("cu", date, "shfe")
