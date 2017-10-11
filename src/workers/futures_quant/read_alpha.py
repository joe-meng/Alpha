# -*- coding: utf-8 -*-
from __future__ import division
from sqlalchemy import create_engine

import pandas as pd
import numpy as np
import sys
import os
from settings import logger

quant_path = os.path.dirname(os.path.abspath(__file__))
workers_path = os.path.dirname(quant_path)
src_path = os.path.dirname(workers_path)
if src_path not in sys.path:
    sys.path.append(src_path)

from share.conf import mysql

address = 'mysql+pymysql://%s:%s@%s:%s/%s' % (mysql.get('user'),
                                              mysql.get('password'),
                                              mysql.get('host'),
                                              mysql.get('port'),
                                              mysql.get('db'))
conn = create_engine(address)


def read_day_kline(varieties, start_date, end_date):
    contractname = varieties + '9999'  # 主力合约

    sql = 'select date_time,contract,price_open,price_low,price_high,price_close from alpha.day_kline\
            where contract="' + contractname + '" and date_time  between "' + start_date + '" and "' + end_date + '"'

    day_kline_data = pd.read_sql(sql, conn)

    t_close = np.array(day_kline_data['price_close'][1:])
    y_close = np.array(
        day_kline_data['price_close'][0:len(day_kline_data) - 1])
    rise = (t_close - y_close) / y_close
    b = np.insert(rise, 0, 'NaN')
    day_kline_data['rise'] = b
    day_kline_data['varieties'] = varieties

    return day_kline_data


def read_last_history(varieties):
    sql = 'select max(date) from alpha.cross_star_history where  varieties = "' + varieties + '"'
    date = pd.read_sql(sql, conn)

    return date['max(date)'][0]


def to_cross_star_history(dataset):
    if isinstance(dataset, pd.DataFrame) and not dataset.empty:
        try:
            logger.info("品类%s 日期%s历史写入数据到表cross_star_history",dataset['varieties'][0],dataset['date'].tolist())
            dataset.to_sql("cross_star_history", conn, if_exists='append',
                           index=False)
        except:
            logger.error("表cross_star_history中内容已存在,写入失败")
        else:
            logger.info("表cross_star_history数据写入成功")


def to_cross_star_threshold(dataset):
    if isinstance(dataset, pd.DataFrame) and not dataset.empty:
        try:
            logger.info("品类%s 日期%s阀值写入数据到表cross_star_threshold",dataset['varieties'][0],dataset['date'].tolist())
            dataset.to_sql("cross_star_threshold", conn, if_exists='append',
                           index=False)
        except:
            logger.error("表cross_star_threshold内容已存在,写入失败")
        else:
            logger.info("表cross_star_threshold数据写入成功")
