# -*- coding: utf-8 -*-
import os
import sys
sys.path.append("..")
import time
import json
import datetime
import hashlib
import requests
# os.path.join(os.path.dirname("__file__"),os.path.pardir)
# print(os.path.pardir)
from utils.db import MongoHandler


def main():
    name = "smm_live"
    handler = MongoHandler()
    host = "http://www.cailianpress.com/"

    unix_time = int(time.time())
    url_list = [
        "http://www.cailianpress.com/v2/article/get_roll?type=-1&count=30"
    ]
    for url in url_list:
        website = "cailian_live"
        response = requests.get(url)
        now = datetime.datetime.now()
        text = json.loads(str(response.text))
        code = text["errno"]
        if code==0:
            # 正确返回
            data = text["data"]
            for line in data:
                info = {}
                line_url = host.encode('utf-8') + line["time"].encode('utf-8')
                _id = hashlib.sha256(line_url).hexdigest()
                if handler.check_exist("live", {"_id": _id}):
                    # 如果在数据库中已经存在  直接跳过
                    continue
                else:
                    info["_id"] = _id
                    info["url"] = host+line["time"]
                    info["source"] = "财联社"
                    info["website"] = website
                    info["author"] = line["author"]
                    info["pub_time"] = datetime.datetime.fromtimestamp(int(line["ctime"]))
                    info["craw_time"] = now
                    info["content_text"] = line["content"]
                    _id = handler.insert_one('live', info)
        else:
            # 错误返回 什么都不做
            info = {"_id":1}

def timestamp_datetime(value):
    format_str = '%Y-%m-%d %H:%M:%S'
    # value为传入的值为时间戳(整形)，如：1332888820
    value = time.localtime(value)
    ## 经过localtime转换后变成
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    # 最后再经过strftime函数转换为正常日期格式。
    dt = time.strftime(format_str, value)
    return dt

if __name__ == '__main__':
    main()
