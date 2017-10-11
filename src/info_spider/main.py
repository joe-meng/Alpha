#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import datetime
import subprocess

from tornado.ioloop import IOLoop
from apscheduler.schedulers.tornado import TornadoScheduler

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')

DEBUG = False
all_topic = [
    "今日有色",
    "海通有色",
    "南储商务网",
    "文韬武略话有色",
    "对冲研投",
    "方正中期期货有限公司",
    "扑克投资家",
    "大宗商品交易中心",
    "富宝有色",
    "阿拉丁铝产业链服务平台",
    "上海金属网",
    "中粮期货工业品部",
    "买卖宝",
    "付鹏的财经世界",
    "产业在线",
    "咩咩说",
    "华尔街见闻",
]

def get_smm_interface():
    # 上海有色网直播和要闻
    subprocess.call('cd {0}/websitespider/interface && python smm.py'.format(SRC_DIR), shell=True)

def get_wallstreet_interface():
    # 华尔街直播接口
    subprocess.call('cd {0}/websitespider/interface && python wallstreet.py'.format(SRC_DIR), shell=True)

def get_cailian_interface():
    # 财联社直播接口
    subprocess.call('cd {0}/websitespider/interface && python cailian.py'.format(SRC_DIR), shell=True)

def get_topic():
    length = len(all_topic)
    now = datetime.datetime.now()
    if now.hour>len(all_topic):
        return ""
    position = now.hour%(len(all_topic)+1)
    topic = all_topic[0] if position<1 else all_topic[position-1]
    return topic

def crawl_wechat():
    # 微信公众号爬虫
    log_file = os.path.join(LOG_DIR, 'wechat.log')
    topic = get_topic()
    if topic:
        subprocess.call('cd {0}/wechat && scrapy crawl wechat -a username={1} --logfile={2}'.format(SRC_DIR, topic , log_file), shell=True)

def crawl_cnmn():
    # 中国有色网爬虫
    log_file = os.path.join(LOG_DIR, 'cnmn.log')
    subprocess.call('cd {0}/websitespider && scrapy crawl cnmn --logfile={1}'.format(SRC_DIR, log_file), shell=True)

def crawl_smm():
    # 上海有色网爬虫
    log_file = os.path.join(LOG_DIR, 'smm.log')
    subprocess.call('cd {0}/websitespider && scrapy crawl smm --logfile={1}'.format(SRC_DIR, log_file), shell=True)

def crawl_wallstreet():
    # 上海有色网爬虫
    log_file = os.path.join(LOG_DIR, 'wallstreet.log')
    subprocess.call('cd {0}/websitespider && scrapy crawl wallstreet --logfile={1}'.format(SRC_DIR, log_file), shell=True)

def crawl_jinrong():
    # 金融界爬虫
    log_file = os.path.join(LOG_DIR, 'jinrongjie.log')
    subprocess.call('cd {0}/websitespider && scrapy crawl jinrongjie --logfile={1}'.format(SRC_DIR, log_file), shell=True)

def crawl_enanchu():
    # 南储商务网爬虫
    log_file = os.path.join(LOG_DIR, 'enanchu.log')
    subprocess.call('cd {0}/websitespider && scrapy crawl enanchu --logfile={1}'.format(SRC_DIR, log_file), shell=True)

def crawl_shmet():
    # 上海金属网爬虫
    log_file = os.path.join(LOG_DIR, 'shmet.log')
    subprocess.call('cd {0}/websitespider && scrapy crawl shmet --logfile={1}'.format(SRC_DIR, log_file), shell=True)

def crawl_guba():
    # 股吧爬虫
    log_file = os.path.join(LOG_DIR, 'guba.log')
    subprocess.call('cd {0}/websitespider && scrapy crawl guba --logfile={1}'.format(SRC_DIR, log_file), shell=True)


if __name__ == '__main__':
    # -c scray_wechat
    scheduler = TornadoScheduler()
    # cnmn 中国有色网 的爬虫 一分钟
    scheduler.add_job(crawl_cnmn, 'cron', minute="1-59", hour="*")
    # wechat 微信公众号 的爬虫 一分钟
    scheduler.add_job(crawl_wechat, 'cron', minute="1", hour="*")
    # 上海有色网 的接口  30s
    scheduler.add_job(get_smm_interface, 'interval', seconds=30)
    # 华尔街见闻 的接口  30s
    scheduler.add_job(get_wallstreet_interface, 'interval', seconds=30)
    # 财联社直播  每分钟
    scheduler.add_job(get_cailian_interface, 'cron', minute="*", hour="*")
    # 股吧
    scheduler.add_job(crawl_guba, 'cron', minute="5", hour="*")
    # 华尔街见闻新闻
    scheduler.add_job(crawl_wallstreet, 'cron', minute="4", hour="*")
    # 金融界咨询
    scheduler.add_job(crawl_jinrong, 'cron', minute="2", hour="*")
    # 南储商务网
    scheduler.add_job(crawl_enanchu, 'cron', minute="3", hour="*")
    # 上海有色网
    scheduler.add_job(crawl_smm, 'cron', minute="6", hour="*")
    # 上海金属网
    scheduler.add_job(crawl_shmet, 'cron', minute="7", hour="*")


    # # 上海金属网 网站爬虫 一分钟  属性信息不一致 且大部分需要登录  暂不使用
    # scheduler.add_job(crawl_wechat, 'cron', minute=0, hour="*")
    scheduler.start()
    print('scheduler running...')

    try:
        IOLoop.instance().start()
    except (KeyboardInterrupt, SystemExit):
        pass
