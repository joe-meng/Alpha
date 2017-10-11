# -*- coding: utf-8 -*-
import os
import sys
sys.path.append("..")
import time
import json
import datetime
import hashlib
import requests
from utils.db import MongoHandler


def main():
    name = "wallstreet_live"
    handler = MongoHandler()
    host = "https://wallstreetcn.com/live/"
    unix_time = int(time.time())
    url_list = [
        "https://api-prod.wallstreetcn.com/apiv1/content/lives?channel=global-channel&client=pc&limit=20",
    ]
    profile ={
        "global-channel": "全球",
        "gold-forex-channel": "A股",
        "gold-channel": "外汇",
        "us-stock-channel": "美股",
    }
    for url in url_list:
        website = "wallstreet_live"
        source = "华尔街见闻"
        response = requests.get(url)
        now = datetime.datetime.now()
        text = json.loads(str(response.text))
        code = text["code"]
        if code==20000:
            # 正确返回
            data = text["data"]["items"]
            for line in data:
                info = {}
                line_url = host + str(line["id"])
                line_url = line_url.encode("utf-8")
                _id = hashlib.sha256(line_url).hexdigest()
                if handler.check_exist("live", {"_id": _id}):
                    # 如果在数据库中已经存在  直接跳过
                    continue
                else:
                    # key_words = line["KeyWords"]
                    info["_id"] = _id
                    info["source"] = source
                    info["website"] = website
                    info["content_html"] = line["content"] + "\n".join(["<img src='%s' class='zoomer__img'>"%img for img in line["image_uris"]])
                    info["pub_time"] = datetime.datetime.fromtimestamp(int(line["display_time"]))
                    info["craw_time"] = now
                    info["content_text"] = line["content_text"]
                    info["category"] = [profile.get(key, "") for key in line["channels"]]
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
