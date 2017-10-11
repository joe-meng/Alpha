# -- coding: utf-8 --
import datetime
import json
import logging
import re
import sys

from sqlalchemy import desc

if __name__ == '__main__':
    sys.path.append("../..")


from models.models import DayKline, MainContract, Session, CapitalFlowsMin, CapitalFlowsDay
from utils.cal_settings import MIN_INIT_PATA_MAP, MIN_RES_DEAL_MAP, COMMON_RES_DAEL_LIST
from common.ctp import BaseResPreprocess, BaseInitPreprocess, BasePreprocess
from send_ready_data import send_message_to_ready_queue
from utils.enums import *
from ctp_preprocess.day_handler import DayResPreProcess

_logger = logging.getLogger(__name__)

class MinPreProcess(BasePreprocess):
    """docstring for PreProcess."""
    def __init__(self, varieties, date, exchange, *args, **kwargs):
        super(MinPreProcess, self).__init__(*args, **kwargs)
        self.varieties = varieties
        self.date = date
        self.exchange = exchange





class MinInitPreProcess(BaseInitPreprocess):
    """初始化预处理对象"""

    def __init__(self, db, contract, varieties, date, exchange, *args, **kwargs):
        super(MinInitPreProcess, self).__init__(varieties, date, exchange,*args, **kwargs)
        self.pre_obj = MinPreProcess(varieties, date, exchange)
        self.pre_obj.db = db
        self.db = db
        self.pre_obj.contract = contract
        self.contract = contract
        # self.init_main_contract()

    def init_main_contract(self):
        """初始化主力合约数据"""
        contract_objs = self.db.query(MainContract).filter(MainContract.settlement_date == self.date[:10],
                                                      MainContract.varieties == self.varieties,
                                                      MainContract.exchange == self.exchange).all()
        if contract_objs:
            obj = contract_objs and contract_objs[0]
            self.pre_obj.main_contract = obj.to_dict()

            if 'init_serial_price_1_5_9' in MIN_INIT_PATA_MAP.get(self.varieties.lower()):
                today = datetime.datetime.today()
                contract1_5_9 = []
                for i in range(1, 13):
                    contract_name = 'serial_contract' + str(i)
                    if not self.pre_obj.main_contract[contract_name]:
                        continue
                    month = int(self.pre_obj.main_contract[contract_name][-2:])
                    if month in [1, 5, 9]:
                        contract1_5_9.append(self.pre_obj.main_contract[contract_name])
                if self.contract in contract1_5_9:
                    self.pre_obj.contract_n = str(contract1_5_9.index(self.contract)+1)
                    return
                else:
                    return 'exit'

            if 'init_serial_price_1_5_10' in MIN_INIT_PATA_MAP.get(self.varieties.lower()):
                today = datetime.datetime.today()
                contract1_5_10 = []
                for i in range(1, 13):
                    contract_name = 'serial_contract' + str(i)
                    if not self.pre_obj.main_contract[contract_name]:
                        continue
                    month = self.pre_obj.main_contract[contract_name][-2:]
                    if month in ['01', '05', '10']:
                        contract1_5_10.append(self.pre_obj.main_contract[contract_name])
                if self.contract in contract1_5_10:
                    self.pre_obj.contract_n = str(contract1_5_10.index(self.contract)+1)
                    return
                else:
                    return 'exit'

            for key, value in self.pre_obj.main_contract.items():
                if value == self.contract:
                    if key == "main_contract":
                        contract_n = "0"
                    else:
                        contract_n = key.replace("serial_contract", "")
                    if int(contract_n) in [0, 1, 2, 3, 6]:
                        self.pre_obj.contract_n = contract_n
                        return
                    else:
                        return 'exit'
            return 'exit'
        else:
            _logger.info('主力合约信息不存在')
            return 'exit'

    def init_serial_price(self):
        """初始化获取连一连二连三的价格"""
        # keys = ['serial_contract1', 'serial_contract2', 'serial_contract3', #'serial_contract4', 'serial_contract5',
        #         'serial_contract6']
        keys = [1, 2, 3, 6]
        if self.pre_obj.main_contract:
            for key in keys:
                contract = 'serial_contract' + str(key)
                # index = keys.index(key)+1
                if self.pre_obj.main_contract.get(contract):
                    dk_objs = self.db.query(DayKline).filter(DayKline.contract == self.pre_obj.main_contract[contract])\
                                        .order_by(desc(DayKline.date_time)).all()
                    if dk_objs:
                        # pre_obj.contract1_price = dk_objs[0].get('price_close')
                        setattr(self.pre_obj, 'contract'+str(key)+'_price', dk_objs[0].price_close)
                    else:
                        _logger.info('datetime::%s, contract::%s对应的day_kline数据不存在'%(self.date, self.pre_obj.main_contract[contract]))
                else:
                    _logger.info('%s:这一天的:%s: 合约不存在'%(self.date, contract))
        else:
            _logger.info('主力合约信息不存在')

    def init_serial_price_1_5_9(self):
        """初始化159合约的连一连二连三的价格"""
        date_time = self.pre_obj.date + ' 00:00:00'
        # month = today.month
        k = 0
        for i in range(1, 13):
            contract = 'serial_contract' + str(i)
            month = str(self.pre_obj.main_contract[contract])[-2:]
            if month in ['01', '05', '09']:
                k = k + 1
                contract = 'serial_contract' + str(i)
                dk_objs = self.db.query(DayKline).filter(DayKline.contract == self.pre_obj.main_contract[contract],
                                                         DayKline.date_time == date_time) \
                    .order_by(desc(DayKline.date_time)).all()
                if dk_objs:
                    # pre_obj.contract1_price = dk_objs[0].get('price_close')
                    setattr(self.pre_obj, 'contract' + str(k) + '_price', dk_objs[0].price_close)
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
                    setattr(self.pre_obj, 'contract' + str(k) + '_price', dk_objs[0].price_close)
                else:
                    _logger.info('datetime::%s, contract::%s对应的day_kline数据不存在' % (
                        self.date, self.pre_obj.main_contract[contract]))



class MinResPreProcess(BaseResPreprocess):
    
    persis_obj_map = MIN_PARA_MODEL_MAP
    varieties_map = MIN_VARIEYIES_DICT
    
    def __init__(self, db, pre_obj, *args, **kwargs):
        super(MinResPreProcess, self).__init__(*args, **kwargs)
        self.db = db
        self.res = {}
        self.pre_obj = pre_obj

    # def in_and_out(self):
    #     """进出口"""
    #     contract_n = self.pre_obj.contract_n
    #     insert_dict = {}
    #     if contract_n == '0':
    #         # 处理主力合约
    #         self.pre_obj.cal_main_contract()
    #         insert_dict = self.pre_obj.get_main_contract_value()
    #     elif contract_n == "1":
    #         self.pre_obj.cal_1m_contract()
    #         insert_dict = self.pre_obj.get_1m_value()
    #     elif contract_n == "2":
    #         # 处理连二合约
    #         self.pre_obj.cal_2m_contract()
    #         insert_dict = self.pre_obj.get_2m_value()
    #     elif contract_n == "3":
    #         # 处理连三合约
    #         self.pre_obj.cal_3m_contract()
    #         insert_dict = self.pre_obj.get_3m_value()
    #     elif contract_n == "6":
    #         self.pre_obj.cal_6m_contract()
    #         insert_dict = self.pre_obj.get_6m_value()
    #
    #     self.res.update(insert_dict)


    def in_and_out(self):
        """进出口"""
        contract_n = self.pre_obj.contract_n
        if contract_n == '0':
            self.res.update({'change': self.pre_obj.change})
            self.res.update(self.pre_obj.cal_import_cost)
            self.res.update(self.pre_obj.cal_domestic_price)
            self.res.update(self.pre_obj.cal_cur_rate)
            self.res.update(self.pre_obj.cal_profit)
            self.get_hulun_rate()
        elif contract_n == '1':
            self.res.update(self.pre_obj.cal_change_1m)
            self.res.update(self.pre_obj.cal_import_cost_1m)
            self.res.update(self.pre_obj.cal_domestic_price_1m)
            self.res.update(self.pre_obj.cal_1m_rate)
            self.res.update(self.pre_obj.cal_profit_1m)
        elif contract_n == '2':
            self.res.update(self.pre_obj.cal_change_2m)
            self.res.update(self.pre_obj.cal_import_cost_2m)
            self.res.update(self.pre_obj.cal_domestic_price_2m)
            self.res.update(self.pre_obj.cal_2m_rate)
            self.res.update(self.pre_obj.cal_profit_2m)
        elif contract_n == '3':
            self.res.update(self.pre_obj.cal_change_3m)
            self.res.update(self.pre_obj.cal_import_cost_3m)
            self.res.update(self.pre_obj.cal_domestic_price_3m)
            self.res.update(self.pre_obj.cal_3m_rate)
            self.res.update(self.pre_obj.cal_profit_3m)
        elif contract_n == '6':
            self.res.update(self.pre_obj.cal_change_6m)
            self.res.update(self.pre_obj.cal_import_cost_6m)
            self.res.update(self.pre_obj.cal_domestic_price_6m)
            self.res.update(self.pre_obj.cal_6m_rate)
            self.res.update(self.pre_obj.cal_profit_6m)


    def update_capital_value(self):
        """日数据更新资金流动"""
        date = self.pre_obj.date + str(datetime.datetime.now())[10:]
        obj = CapitalFlowsMin
        self.common_update_capital_value(date, obj)
        self.common_update_capital_value(self.pre_obj.date, CapitalFlowsDay)


def cal_contract_vals(db, varieties, contract, date, exchange):
    """数据处理"""
    now = date + str(datetime.datetime.now())[10:]
    init_obj = MinInitPreProcess(db, contract, varieties, date, exchange)
    init_list = MIN_INIT_PATA_MAP.get(varieties, [])
    for para in init_list:
        init_res = getattr(init_obj, para)()
        if init_res == "exit":
            # db.roll_back()
            db.close()
            return
    res_obj = MinResPreProcess(db, init_obj.pre_obj)
    deal_list = MIN_RES_DEAL_MAP.get(varieties, []) + COMMON_RES_DAEL_LIST
    for deal in deal_list:
        getattr(res_obj, deal)()
    print(res_obj.res)
    res_obj.save_symbol_data(res_obj.res, now)
    day_res_obj = DayResPreProcess(db, init_obj.pre_obj)
    day_res_obj.save_symbol_data(res_obj.res, date)
    send_message_to_ready_queue(json.dumps({"varieties": varieties}))


def cal_min(ch, method, properties, body):
    print(body)
    info = body.decode('utf8').split(",")
    print("info", info)
    exchange = info[1]
    day_min = info[2]
    contract = info[0]
    date = info[3].split(" ")[0]
    # if exchange not in ALLOW_EXCHANGE:
    #     return
    replace_info = re.findall(r'(\d+)', contract)
    varieties = contract.replace(replace_info[0], "")
    if varieties.lower() not in ALLOW_VARIETIES:
        return
    db = Session()
    cal_contract_vals(db, varieties, contract, date, exchange)
    db.close()



if __name__ == '__main__':
    # varieties, contract_n, date, exchange
    # for i in range(7):
    #     print('================%s'%i)
    db = Session()
    cal_contract_vals(db, "ni", 'ni1801', '2017-08-28', 'SHFE')
    # cal_contract_vals("cu", '6', '2017-08-08', 'SHFE')
    # cal_min(None, None, None, 'al1712,SHFE,Day,2017-08-10 00:00:00,16305,16595,16100,16425,37694,3087957300,57264,0,16190,19883,17811')
# b'IH1709,CFFEX,Day,2017-08-28 00:00:00,2728,2775.2,2723.4,2740.4,10330,8522320680,18208,0,2709.8,5226,5104'
# info ['IH1709', 'CFFEX', 'Day', '2017-08-28 00:00:00', '2728', '2775.2', '2723.4', '2740.4', '10330', '8522320680', '18208', '0', '2709.8', '5226', '5104']
# b'zn8888,SHFE,Day,2017-08-28 00:00:00,26520,26520,26520,25735,593842,76060520650,536406,0,0,0,0'
# info ['zn8888', 'SHFE', 'Day', '2017-08-28 00:00:00', '26520', '26520', '26520', '25735', '593842', '76060520650', '536406', '0', '0', '0', '0']