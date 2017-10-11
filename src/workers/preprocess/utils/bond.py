# -- coding: utf-8 --
import sys
import json
import datetime
import requests
import pandas as pd
from tornado.ioloop import IOLoop
from apscheduler.schedulers.tornado import TornadoScheduler

sys.path.append("../..")

from share.utils import MysqlHnadler
from enums import *
def get_bond(now_str):
    url = "http://www.shfe.com.cn/data/instrument/ContractDailyTradeArgument%s.dat"%now_str
    print(url)
    bond = {}
    try:
        req = requests.get(url)
        data = json.loads(req.text)
        for line in data["ContractDailyTradeArgument"]:
            varieties = line["INSTRUMENTID"]
            var_bond = line["SPEC_LONGMARGINRATIO"]
            bond[varieties] = var_bond
    except:
        pass
    # print("shfe over", bond)
    # # 郑州交易所交易保证金
    # url = "http://www.czce.com.cn/portal/DFSStaticFiles/Future/%s/%s/FutureDataClearParams.txt"%(now_day.year, now_str)
    # try:
    #     req = requests.get(url)
    #     lines = req.text.split("\r\n")
    #     for line in lines:
    #         line = line.replace(" ", "")
    #         info_list = line.split("|")
    #         if len(info_list)<2:
    #             continue
    #         if info_list[3].isdigit():
    #             contract = info_list[0]
    #             var_bond = float(info_list[4])/100
    #             bond[contract] = var_bond
    # except:
    #     pass
    # print("czce over",bond)
    # # 大连交易所的保证金
    # df=pd.read_html('http://www.dce.com.cn/publicweb/notificationtips/queryDayTradPara.html')
    # df=df[0]
    # info = df.T[:2].to_dict()
    # for key, value in info.items():
    #     varieties = value[0]
    #     var_bond = value[1]
    #     try:
    #         var_bond = float(var_bond)
    #         bond[varieties] = var_bond
    #     except:
    #         pass
    # print("dce over")
    return bond

def save_bond(handler, now_str, bond):
    handler.table = "bond"
    if bond:
        for key, value in bond.items():
            handler.insert_table_info({
                "contract": key,
                "amount": value,
                "date": now_str
            })
        handler.commit()
        print("now_str", now_str)
    print("save_bond over")

def cal_fund_settlement(handler, varieties, settlement_date, bond):
    handler.table = 'main_contract'
    info = handler.query({"settlement_date":settlement_date,"varieties":varieties,"exchange":"shfe"}, find_all=0)
    handler.table = 'day_kline'
    all_price = 0
    for i in range(1,13):
        key = "serial_contract%s"%i
        if info[key]:
            # 获取该合约的信息
            day_info_list= handler.query({
                "contract": info[key],
                "exchange": info["exchange"],
                # "date_time": settlement_date,
            }, find_all=1, order_by="date_time", limit=2)
            day_info = day_info_list[0]
            last_info = day_info_list[1]
            # print(day_info,"day_info")
            # print(last_info, "last_info")
            openinterest = day_info["openinterest"] - last_info["openinterest"]
            settlement_price = day_info["price_close"]
            vol = HOLDING_NUM[info["varieties"]]["vol"]
            varieties_bond = bond[info[key]]
            # 持仓变动*最新价*每手数量*保证金比例
            price = openinterest*settlement_price*int(vol)*float(varieties_bond)
            all_price +=price
    return all_price

def main():
    now_day = datetime.datetime.now()
    now_str = now_day.strftime("%Y%m%d")
    handler = MysqlHnadler("bond")
    bond_info = handler.query({
        "date": now_day.strftime("%Y-%m-%d"),
    }, find_all=1)
    bond = {}
    price_list = []
    for info in bond_info:
        # print(info)
        bond[info["contract"]] = info["amount"]
    # all_varieties = ["ag","al","au","bu","cu","fu","hc","ni","pb","rb","ru","sn","wr","zn"]
    all_varieties = ["cu"]
    for varieties in all_varieties:
        price = cal_fund_settlement(handler, varieties, now_str, bond)
        price_list.append({"varieties": varieties, "amount": price, "date":now_day})
    handler.table = "min_fund_settlement"
    for insert_dict in price_list:
        handler.insert_table_info(insert_dict)
    handler.commit()
    handler.close()

if __name__ == '__main__':
    scheduler = TornadoScheduler()
    scheduler.add_job(main, 'cron', minute='*')

    scheduler.start()
    print('scheduler running...')

    try:
        IOLoop.instance().start()
    except (KeyboardInterrupt, SystemExit):
        pass
