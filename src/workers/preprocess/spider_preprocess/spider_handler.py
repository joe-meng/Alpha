# -- coding: utf-8 --
import os
import sys
import json
import datetime

sys.path.append("../..")
# from share.mq import channel

from share.utils import MysqlHnadler
from send_ready_data import send_message_to_ready_queue
from utils.enums import *
# from share.base import base_handler

def cal_spider_queue(info):
    # 计算爬虫给的消息流
    if info["type"]=="stock":
        # 库存数据更新
        queue_dict = {"type": "spider", "data": "stock"}
        send_message_to_ready_queue(json.dumps(queue_dict))
    elif info["type"]=="warehouse_receipt":
        # 仓单的数据更新
        queue_dict = {"type": "spider", "data": "warehouse_receipt"}
        send_message_to_ready_queue(json.dumps(queue_dict))
    elif info["type"]=="nanchu":
        # 南储数据更新
        queue_dict = {"type": "spider", "data": "nanchu"}
        send_message_to_ready_queue(json.dumps(queue_dict))
    else:
        # 暂时不需要处理的内容
        pass

if __name__ == '__main__':
    cal_spider_queue(info)
