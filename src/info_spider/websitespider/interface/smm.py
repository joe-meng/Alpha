# -*- coding: utf-8 -*-
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
    host = "https://www.smm.cn/"
    profile = {
        "20": "铜",
        "21": "铝",
        "22": "铅",
        "23": "锌",
        "24": "锡",
        "25": "镍",
        "26": "锰",
        "28": "硅",
        "29": "钴锂",
        "93": "锑",
        "97": "钨",
        "95": "铟镓锗",
        "188": "硒铋碲",
        "3": "小金属",
        "2": "贵金属",
        "30": "稀土",
        "78": "钢铁",
        "31": "废金属",
        "98": "再生",
        "32": "利源",
    }
    unix_time = int(time.time())
    url_list = [
        "https://platform.smm.cn/newscenter/news/list/直播/全部/1?page_limit=10",
        # "https://platform.smm.cn/newscenter/news/list/要闻/all/1?page_limit=10",
    ]
    for url in url_list:
        if "要闻" in url:
            website = "smm_news"
        else:
            website = "smm_live"
        response = requests.get(url)
        now = datetime.datetime.now()
        text = json.loads(str(response.text))
        code = text["code"]
        if code==100000:
            # 正确返回
            data = text["data"]
            for line in data:
                info = {}
                line_url = host.encode('utf-8') + line["ID"].encode('utf-8')
                _id = hashlib.sha256(line_url).hexdigest()
                if handler.check_exist("live", {"_id": _id}):
                    # 如果在数据库中已经存在  直接跳过
                    continue
                else:
                    key_words = line["KeyWords"]
                    info["_id"] = _id
                    info["url"] = line["URL"]
                    info["source"] = "上海有色网"
                    info["website"] = website
                    info["author"] = line["Author"]
                    info["pub_time"] = datetime.datetime.fromtimestamp(int(line["RenewDate"]))
                    info["craw_time"] = now
                    info["content_text"] = line["Profile"]
                    info["category"] = (profile.get(line["ProductType"], "") +','+ key_words).split(',')
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
