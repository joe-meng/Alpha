#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@date: 2017-08-15

@author: Devin
"""
#品目
Cu = "cu"
Al = "al"
Zn = "zn"
Pb = "pb"
Ni = "ni"
Pvc = "pvc"

variety_chinese = {
    Cu:"铜",
    Al:"铝",
    Zn:"锌",
    Pb:"铅",
    Ni:"镍",
    Pvc:"PVC"
}

#有效的PRICE CODE铜的取值
OPEN = "OPEN"  # 开盘价
CLOSE = "CLOSE"  # 收盘价
HIGH = "HIGH"  # 最高值
LOW = "LOW"  # 最低值
SETTLE = "SETTLE"  # 结算价
VOL = "VOL"  # 累计成交量
YEAL_SALE="YEAL_SALE" #年累计消费量
OPI = "OPI"  # 持仓量
BUYVOL = "BUYVOL" #外盘 (主动性买单)
SELLVOL = "SELLVOL" #内盘(主动性卖单)
CASHPREC="CASHPREC" #资金沉淀
CASHFLOW="CASHFLOW" #资金流向
STOCK = "STOCK"  # SHFE库存
WARRANT = "WARRANT"  # 仓单
CONTRACT = "CONTRACT"  # 合约名称
FUTURES = "FUTURES"  # 合约名称
MARKET = "MARKET"  # 当前市场
SPOT = "SPOT"  # 现货价格
PD = "PD"  # 现货升贴水
STOCK_SH = "STOCK_SH"  # 上海地区库存
STOCK_JS = "STOCK_JS"  # 江苏地区库存
STOCK_ZJ = "STOCK_ZJ"  # 浙江地区库存
STOCK_BS = "STOCK_BS"  # 保税商品库存
STOCK_WS = "STOCK_WS"  # 完税商品库存
STOCK_LME = "STOCK_LME"  # LME库存
MAIN_CONTRACT = "main_contract"  # 主力合约
INDEX_CONTRACT = "index_contract"  # 指数合约
CON_CONTRACT_1 = "serial_contract1"  # 连1合约
CON_CONTRACT_2 = "serial_contract2"  # 连2合约
CON_CONTRACT_3 = "serial_contract3"  # 连3合约
CON_CONTRACT_4 = "serial_contract4"  # 连4合约
CON_CONTRACT_5 = "serial_contract5"  # 连5合约
CON_CONTRACT_6 = "serial_contract6"  # 连6合约
CON_CONTRACT_7 = "serial_contract7"  # 连7合约
CON_CONTRACT_8 = "serial_contract8"  # 连8合约
CON_CONTRACT_9 = "serial_contract9"  # 连9合约
CON_CONTRACT_10 = "serial_contract10"  # 连10合约
CON_CONTRACT_11 = "serial_contract11"  # 连11合约
CON_CONTRACT_12 = "serial_contract12"  # 连12合约
LME_WARRANT = "LME_WARRANT"  # LME仓单
FUTURE_LME = "FUTURE_LME" #LME铜3月价格
NANCHU_IN = "NANCHU_IN"  # 南储仓电解铜入库
NANCHU_OUT = "NANCHU_OUT"  # 南储仓电解铜出库
NANCHU_STOCK = "NANCHU_STOCK"  # 广东铜社会库存
DOJI_STAR_THRESHOLD="DOJI_STAR_THRESHOLD" #十字星阀值
EXPIRE_DATE = "EXPIRE_DATE" #期货合约交割日期
EXCHANGE = "EXCHANGE"  # 汇率

DOJI_STAR_RATE = "DOJI_STAR_RATE" #十字星比值(收盘-开盘)/开盘(日)
DOJI_STAR = "DOJI_STAR" #十字星
OPI_MONTH_RATE = "OPI_MONTH_RATE" #持仓比
WARRANT_MONTH_RATE = "WARRANT_MONTH_RATE" #仓单环比
SHFE_LME_DIFF = "SHFE_LME_DIFF" #沪伦差值(日)
CON1_CON2_DIFF_RATE = "CON1_CON2_DIFF_RATE" #连一连二差值比
CON1_CON3_DIFF_RATE = "CON1_CON3_DIFF_RATE" #连一连三差值比
CON2_CON3_DIFF_RATE = "CON2_CON3_DIFF_RATE" #连二连三差值比
CON1_CON2_DIFF = "CON1_CON2_DIFF" #连一连二差值
CON1_CON3_DIFF = "CON1_CON3_DIFF" #连一连三差值
CON2_CON3_DIFF = "CON2_CON3_DIFF" #连二连三差值
WEEK_SPOT_DIFF = "WEEK_SPOT_DIFF" #现货周差(日)
OPICHANGE = "OPICHANGE" #日增仓 (今天-昨天)OPI
PD_MONTH_DIFF = "PD_MONTH_DIFF" #交割月升贴水同期对比差
WEEK_SPOT_RATE = "WEEK_SPOT_RATE" #现货周差(分钟)
WEEK_SPOT_RATE_D = "WEEK_SPOT_RATE_D" #现货周差(日)
WARRANT_MONTH_DIFF = "WARRANT_MONTH_DIFF" #仓单月差
OPI_MONTH_DIFF = "OPI_MONTH_DIFF" #持仓月差


#期货交易所(期货)
LME = "LME"
SHFE = "SHFE"
COMEX = "COMEX"
CFFEX = "CFFEX"
CZCE = "CZCE"
DCE = "DCE"

#现货价格来源
SHMET = "shmet" #上海金属网
CCMN_CJXH = "ccmn_长江现货"
SMM = "smm"
E_NANCHU = "enanchu"
SMM_HB = "smm_华北"
CCMN_CJYS = "ccmn_长江有色网"
SMM_WX = "smm_无锡"

SINA_LME = "sina_lme"
SHMET_LME = "shmet_lme"