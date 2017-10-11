# -- coding: utf-8 --
import os
import re
import datetime
from share.utils import MysqlHnadler
from share.enums import *
class BaseHandler(object):
    """docstring for BaseHandler."""
    def __init__(self):
        self.db_handler = MysqlHnadler("main_contract")
        self.day = datetime.datetime.now().strftime("%Y-%m-%d")
        self.data = {}

    def init_all_metal(self):
        # 初始化内容
        all_data = self.db_handler.query({"settlement_date":self.day}, find_all=1)
        for data in all_data:
            if data["exchange"] not in self.data:
                # 市场不在
                self.data[data["exchange"]] = {}
            if data["varieties"] not in self.data[data["exchange"]]:
                # 品种不在
                self.data[data["exchange"]][data["varieties"]] = self.revert_dict(data)

    def revert_dict(self, data):
        return_dic = {}
        for k, v in data.items():
            if k in ["settlement_date", "exchange"]:
                continue
            if not v:
                continue
            if v not in return_dic:
                return_dic[v] = []
            return_dic[v].append(k.replace("main_contract", "0").replace("serial_contract", ""))
        return return_dic

    def check_change_day(self):
        # 检测是否改变要改变合约内容
        now_day = datetime.datetime.now().strftime("%Y-%m-%d")
        if not now_day==self.day:
            data = self.db_handler.query({"settlement_date": now_day})
            if len(data):
                self.day = now_day
                return 1
        return 0

    def reset_info(self):
        # 重置当天的合约信息
        self.day = datetime.datetime.now().strftime("%Y-%m-%d")
        self.init_all_metal()

    def get_main_contract(self, exchange, varieties, date_time=None):
        # 获取金属类别的主力合约
        table = self.db_handler.table
        self.db_handler.table = "main_contract"
        query_dict = {
            "exchange": exchange,
            "varieties": "varieties",
        }
        if date_time:
            query_dict["settlement_date"] = date_time
        info = self.db_handler.query(query_dict, find_all=0, order_by="date")
        self.db_handler.table = table
        return info["main_contract"]

    def get_contract_info(self, exchange, contract):
        # 获取该合约是主力合约  连续合约信息
        # return ["0", "1", "2"]
        replace_info = re.findall(r'(\d+)', contract)
        varieties = contract.replace(replace_info[0], "")
        if not varieties or varieties.lower() not in ACCEPT_METAL:
            return [], varieties
        return self.data[exchange][varieties].get(contract, []), varieties

    def get_contract_price(self, exchange, contract):
        # 获取该合约的最新报价
        table = self.db_handler.table
        self.db_handler.table = "day_kline"
        info = self.db_handler.query({
            "exchange":exchange, "contract":contract
        }, find_all=0, order_by="date_time")
        self.db_handler.table = table
        return info

    def get_exchange_price(self, currency="USD"):
        table = self.db_handler.table
        self.db_handler.table = "spot_exchange_summary"
        info = self.db_handler.query({
            "currency":currency,
            "source": "boc",
        }, find_all=0, order_by="date")
        self.db_handler.table = table
        return info

    def close():
        self.db_handler.close()


# base_handler = BaseHandler()
# base_handler.init_all_metal()


def main():
    pass

if __name__ == '__main__':
    main()
