import os
import sys
import json
import traceback
import datetime
import logging
import requests
import pandas as pd
sys.path.append("..")
from utils.db import MysqlHnadler
logger = logging.getLogger(__name__)

def trade_order():
    handler = MysqlHnadler("trade_order", db_name='alpha', host="140")
    now = datetime.datetime.now()
    try:
        # 上交所
        save_trade_order(handler, now.strftime("%Y%m%d"))
    except:
        logger.error("save_trade_order error")
    try:
        # 大商所
        save_dac_trade_order(handler, now)
    except:
        logger.error("save_dac_trade_order error")
    try:
        # 郑商所
        save_czce_trade(handler, now)
    except:
        logger.error("save_czce_trade error")
    handler.commit()
    handler.close()

def save_trade_order(handler, date_time):
    host = "http://www.shfe.com.cn/data/dailydata/kx/pm%s.dat"
    req = requests.get(host%date_time)
    data = json.loads(req.text)
    count_info = {}
    handler.table = "trade_order"
    for line in data["o_cursor"]:
        INSTRUMENTID = line["INSTRUMENTID"].strip()
        name = line["PRODUCTNAME"].strip()
        rank = line["RANK"]
        PARTICIPANTID2 = line["PARTICIPANTID2"].strip()
        PARTICIPANTID3 = line["PARTICIPANTID3"].strip()
        PARTICIPANTABBR2 = line["PARTICIPANTABBR2"].strip()
        PARTICIPANTABBR3 = line["PARTICIPANTABBR3"].strip()
        CJ2 = line["CJ2"]
        CJ3 = line["CJ3"]
        CJ2_CHG = line["CJ2_CHG"]
        CJ3_CHG = line["CJ3_CHG"]
        save_time = "%s-%s-%s"%(date_time[:4], date_time[4:6], date_time[6:])
        insert_dict = {
            "instrumentid": INSTRUMENTID,
            "name": name,
            "product_no": line["PRODUCTSORTNO"],
            "rank": rank,
            "participantid1": line["PARTICIPANTID1"].strip(),
            "participantid2": PARTICIPANTID2,
            "participantid3": PARTICIPANTID3,
            "participantabbr1": line["PARTICIPANTABBR1"].strip(),
            "participantabbr2": PARTICIPANTABBR2,
            "participantabbr3": PARTICIPANTABBR3,
            "cj1": line["CJ1"],
            "cj2": line["CJ2"],
            "cj3": line["CJ3"],
            "cj1_chg": line["CJ1_CHG"],
            "cj2_chg": line["CJ2_CHG"],
            "cj3_chg": line["CJ3_CHG"],
            "date_time": save_time,
        }
        if 0<line["RANK"]<21:
            if INSTRUMENTID not in count_info:
                count_info[INSTRUMENTID] = {}
            for broker in [PARTICIPANTABBR2, PARTICIPANTABBR3]:
                if broker not in count_info[INSTRUMENTID]:
                    count_info[INSTRUMENTID][broker] = {
                        "name": name,
                        "buy_volume": 0,
                        "buy_different": 0,
                        "sale_volume": 0,
                        "sale_different": 0,
                        "date_time": save_time
                    }
            # 处理多
            # print(CJ2, type(CJ2))
            count_info[INSTRUMENTID][PARTICIPANTABBR2]["buy_volume"] += CJ2 if CJ2 else 0
            count_info[INSTRUMENTID][PARTICIPANTABBR2]["buy_different"] += CJ2_CHG if CJ2_CHG else 0
            # 处理空
            count_info[INSTRUMENTID][PARTICIPANTABBR3]["sale_volume"] += CJ3 if CJ3 else 0
            count_info[INSTRUMENTID][PARTICIPANTABBR3]["sale_different"] += CJ3_CHG if CJ3_CHG else 0
        try:
            handler.insert_table_info(insert_dict)
        except:
            print("insert error")

    save_count_info(handler, count_info, "SHFE")

def save_dac_trade_order(handler, date_time):
    for varieties in ["a", "b", "bb", "c", "cs", "fb", "i", "j", "jd", "jm", "l", "m", "p", "pp", "v", "y"]:
        try:
            count_info = {}
            url = "http://www.dce.com.cn/publicweb/quotesdata/memberDealPosiQuotes.html?memberDealPosiQuotes.variety=%s&memberDealPosiQuotes.trade_type=0&year=%s&month=%s&day=%s&contract.contract_id=all&contract.variety_id=%s"%(
                varieties, date_time.year, date_time.month-1, date_time.day, varieties
            )
            handler.table = "trade_order"
            info = pd.read_html(url)
            print(varieties, "url ok")
            total = info[0].T
            detail = info[1].T
            # 处理综合内容
            for i in total:
                line = total[i]
                if "期货" in line[0]:
                    # 处理期货公司综合
                    insert_dict = {
                        "name": varieties,
                        "participantabbr1": line[0].strip(),
                        "participantabbr2": line[0].strip(),
                        "participantabbr3": line[0].strip(),
                        "cj1": line[1],
                        "cj1_chg": line[2],
                        "cj2": line[3],
                        "cj2_chg": line[4],
                        "cj3": line[5],
                        "cj3_chg": line[6],
                        "date_time": date_time
                    }
                    handler.insert_table_info(insert_dict)
            # 处理详细的期货公司数据
            for i in detail:
                if i>0:
                    line = detail[i]
                    participantabbr2 = line[5].strip() if not pd.isnull(line[5]) else ""
                    participantabbr3 = line[9].strip() if not pd.isnull(line[9]) else ""
                    cj2 = line[6] if not pd.isnull(line[6]) else 0
                    cj2_chg = line[7] if not pd.isnull(line[7]) else 0
                    cj3 = line[10] if not pd.isnull(line[10]) else 0
                    cj3_chg = line[11] if not pd.isnull(line[11]) else 0
                    if pd.isnull(line[0]) or "总计" in line[0]:
                        continue
                    insert_dict = {
                        "name": varieties,
                        "rank": line[0],
                        "participantabbr1": line[1].strip() if not pd.isnull(line[1]) else "",
                        "participantabbr2": participantabbr2,
                        "participantabbr3": participantabbr3,
                        "cj1": line[2] if not pd.isnull(line[2]) else 0,
                        "cj1_chg": line[3] if not pd.isnull(line[3]) else 0,
                        "cj2": cj2,
                        "cj2_chg": cj2_chg,
                        "cj3": cj3,
                        "cj3_chg": cj3_chg,
                        "date_time": date_time
                    }
                    try:
                        handler.insert_table_info(insert_dict)
                    except:
                        print("insert error")

                    if varieties not in count_info:
                        count_info[varieties] = {}
                    for broker in [participantabbr2, participantabbr3]:
                        if broker not in count_info[varieties]:
                            count_info[varieties][broker] = {
                                "name": varieties,
                                "buy_volume": 0,
                                "buy_different": 0,
                                "sale_volume": 0,
                                "sale_different": 0,
                                "date_time": date_time
                            }
                    # 处理多
                    # print(CJ2, type(CJ2))
                    count_info[varieties][participantabbr2]["buy_volume"] += int(cj2)
                    count_info[varieties][participantabbr2]["buy_different"] += int(cj2_chg)
                    # 处理空
                    count_info[varieties][participantabbr3]["sale_volume"] += int(cj3)
                    count_info[varieties][participantabbr3]["sale_different"] += int(cj3_chg)

            save_count_info(handler, count_info, "DCE")
        except:
            print(varieties, date_time)

def save_czce_trade(handler, date_time):

    url = "http://www.czce.com.cn/portal/DFSStaticFiles/Future/%s/%s/FutureDataHolding.htm"%(date_time.year, date_time.strftime("%Y%m%d"))
    req = requests.get(url)
    info = req.text.encode("ISO-8859-1").decode("gbk")
    data_info = pd.read_html(info)

    data = data_info[1].T
    name = ""
    contract = ""
    count_info = {}
    for i in data:
        line = data[i]
        if "名次" in line[0]:
            continue
        if "日期" in line[0]:
            # 处理合计
            if "品种" in line[0]:
                name_list = line[0].split(" ")
                name = name_list[0].replace("品种：", "")
                contract = ""
            else:
                str_list = line[0].split(" ")
                contract = str_list[0].replace("合约：", "")
                name = contract[:2]
            # 初始化统计信息内容
            if contract:
                varieties = contract
            else:
                varieties = name
            if varieties not in count_info:
                count_info[varieties] = {}
        else:
            if "合计" in line[0]:
                rank = 999
            else:
                rank = line[0]
            participantabbr1 = line[1] if not pd.isnull(line[1]) else ""
            participantabbr2 = line[4] if not pd.isnull(line[4]) else ""
            participantabbr3 = line[7] if not pd.isnull(line[7]) else ""
            cj1 = line[2] if not pd.isnull(line[2]) else 0
            cj1_chg = line[3] if not pd.isnull(line[3]) else 0
            cj2 = line[5] if not pd.isnull(line[5]) else 0
            cj2_chg = line[6] if not pd.isnull(line[6]) else 0
            cj3 = line[8] if not pd.isnull(line[8]) else 0
            cj3_chg = line[9] if not pd.isnull(line[9]) else 0
            insert_dict = {
                "instrumentid": contract,
                "name": name,
                "rank": rank,
                "participantabbr1": participantabbr1,
                "cj1": cj1,
                "cj1_chg": cj1_chg,
                "participantabbr2": participantabbr2,
                "cj2": cj2,
                "cj2_chg": cj2_chg,
                "participantabbr3": participantabbr3,
                "cj3": cj3,
                "cj3_chg": cj3_chg,
                "date_time": date_time,
                "exchange": "CZCE",
            }
            handler.table = "trade_order"
            handler.insert_table_info(insert_dict)
            if rank != 999 and participantabbr2 != "-" and participantabbr3 != "-":
                # 处理统计信息
                for broker in [participantabbr2, participantabbr3]:
                    if broker not in count_info[varieties]:
                        count_info[varieties][broker] = {
                            "name": varieties,
                            "buy_volume": 0,
                            "buy_different": 0,
                            "sale_volume": 0,
                            "sale_different": 0,
                            "date_time": date_time
                        }
                # 处理多
                count_info[varieties][participantabbr2]["buy_volume"] += int(str(cj2).replace("-", "0"))
                count_info[varieties][participantabbr2]["buy_different"] += int(str(cj2_chg).replace("-", "0"))
                # 处理空
                count_info[varieties][participantabbr3]["sale_volume"] += int(str(cj3).replace("-", "0"))
                count_info[varieties][participantabbr3]["sale_different"] += int(str(cj3_chg).replace("-", "0"))

    save_count_info(handler, count_info, "CZCE")

def save_count_info(handler, count_info, exchange):
    handler.table = "trade_count"
    for contract in count_info.keys():
        for broker in count_info[contract].keys():
            if not broker:
                continue
            insert_dict = count_info[contract][broker]
            insert_dict.update({"contract": contract, "broker": broker, "exchange": exchange})
            handler.insert_table_info(insert_dict)
