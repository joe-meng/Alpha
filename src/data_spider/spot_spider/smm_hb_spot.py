# -- coding: utf-8 --
import pprint
from datetime import datetime, date

import re

import logging
import requests
from decimal import Decimal
from lxml import html

from spot.models import SpotPriceSummary

logger = logging.getLogger(__name__)

def crawl_smm_Ni_huabei():
    """
    smm 华北现货价格 | 镍
    """
    source = 'smm_华北'
    metal = 'Ni'
    name_commodity_mapping = {
        '高镍生铁8-12%': {
            'symbol': 'USE00169',
        },
        '低镍生铁1.5-1.7%': {
            'symbol': 'USE00170',
        },
        '红土镍矿（CIF）Ni1.8%,Fe15-20%进口': {
            'symbol': 'USE00171',
        },
        '红土镍矿（CIF）Ni0.9%,Fe49%进口': {
            'symbol': 'USE00172',
        },
        '红土镍矿（CIF）Ni1.5%,Fe15-25%进口': {
            'symbol': 'USE00173',
        },
        '红土镍矿（FOB）Ni1.5%,Fe15-25%': {
            'symbol': 'USE00174',
        },
        '红土镍矿（FOB）Ni0.9%,Fe49%': {
            'symbol': 'USE00175',
        },
        '红土镍矿（FOB）Ni1.8%,Fe15-20%': {
            'symbol': 'USE00176',
        },
        '红土镍矿1.4-1.6%': {
            'symbol': 'USE00177',
        },
        '红土镍矿1.6-1.7%': {
            'symbol': 'USE00178',
        },
        '红土镍矿1.7-1.8%': {
            'symbol': 'USE00179',
        },
        '红土镍矿1.8-1.9%': {
            'symbol': 'USE00180',
        },
        '红土镍矿1.9-2.0%': {
            'symbol': 'USE00181',
        },
        '红土镍矿0.9-1.0%0.9-1.0%': {
            'symbol': 'USE00182',
        },
    }
    url = 'http://hq.smm.cn/spot_data/18/全部类别/全国地区'

    logger.info('开始爬取 %s, url: %s' % (source, url))
    response = requests.get(url, timeout=5).json()['products']
    for name, mapping in name_commodity_mapping.items():
        try:
            item = list(filter(lambda i: i['SpotDetail']['ProductName'] + i['SpotDetail']['ProductSpec'] + i['SpotDetail']['BrandMark'] == name, response))[0]
        except Exception as e:
            logger.error('%s 解析错误: %s' % (metal, e.args[0]))
            continue

        SpotPriceSummary.objects.update_or_create_all_envs(
            logger,
            varieties=metal,
            source='smm_华北',
            date=item['SpotDetail']['RenewDate'],
            duration_unit='d',
            symbol=mapping['symbol'],
            defaults={
                'price_low': item['SpotDetail']['Low'],
                'price_high': item['SpotDetail']['Highs'],
                'price': item['SpotDetail']['Average'],
            }
        )

def crawl_smm_Pb_huabei():
    """
    smm 华北现货价格 | 铅
    """
    source = 'smm_华北'
    metal = 'Pb'
    name_commodity_mapping = {
        '废起动型汽车电池白壳': {
            'symbol': 'USE00183',
        },
        '废起动型汽车电池黑壳': {
            'symbol': 'USE00184',
        },
    }
    url = 'http://hq.smm.cn/spot_data/12/全部类别/全国地区'

    logger.info('开始爬取 %s, url: %s' % (source, url))
    response = requests.get(url, timeout=5).json()['products']
    for name, mapping in name_commodity_mapping.items():
        try:
            item = list(filter(lambda i: i['SpotDetail']['ProductName'] + i['SpotDetail']['ProductSpec'] == name, response))[0]
        except Exception as e:
            logger.error('%s 解析错误: %s' % (metal, e.args[0]))
            continue

        SpotPriceSummary.objects.update_or_create_all_envs(
            logger,
            varieties=metal,
            source='smm_华北',
            date=item['SpotDetail']['RenewDate'],
            duration_unit='d',
            symbol=mapping['symbol'],
            defaults={
                'price_low': item['SpotDetail']['Low'],
                'price_high': item['SpotDetail']['Highs'],
                'price': item['SpotDetail']['Average'],
            }
         )



def crawl_smm_Al_huabei():
    """
    smm 华北现货价格 | 铝
    """
    source = 'smm_华北'
    metal = 'Al'
    name_commodity_mapping = {
        '氧化铝进口': {
            'symbol': 'USE00185',
        },
        '铝土矿6.0≤Al/Si＜7.0山西': {
            'symbol': 'USE00186',
        },
        '铝土矿4.5≤Al/Si＜5.5山西': {
            'symbol': 'USE00187',
        },
        '铝土矿6.0≤Al/Si＜7.0河南': {
            'symbol': 'USE00188',
        },
        '铝土矿4.5≤Al/Si＜5.5河南': {
            'symbol': 'USE00189',
        },
        '铝土矿6.5≤Al/Si＜7.5广西': {
            'symbol': 'USE00190',
        },
        '铝土矿5.5≤Al/Si＜6.5广西': {
            'symbol': 'USE00191',
        },
        '铝土矿6.5≤Al/Si＜7.5贵州': {
            'symbol': 'USE00192',
        },
        '铝土矿5.5≤Al/Si＜6.5贵州': {
            'symbol': 'USE00193',
        },
    }
    url = 'http://hq.smm.cn/spot_data/10/全部类别/全国地区'

    logger.info('开始爬取 %s, url: %s' % (source, url))
    response = requests.get(url, timeout=5).json()['products']
    for name, mapping in name_commodity_mapping.items():
        try:
            item = list(filter(lambda i: i['SpotDetail']['ProductName'] + i['SpotDetail']['ProductSpec']+ i['SpotDetail']['BrandMark'] == name, response))[0]
        except Exception as e:
            logger.error('%s 解析错误: %s' % (metal, e.args[0]))
            continue

        SpotPriceSummary.objects.update_or_create_all_envs(
            logger,
            varieties=metal,
            source='smm_华北',
            date=item['SpotDetail']['RenewDate'],
            duration_unit='d',
            symbol=mapping['symbol'],
            defaults={
                'price_low': item['SpotDetail']['Low'],
                'price_high': item['SpotDetail']['Highs'],
                'price': item['SpotDetail']['Average'],
            }
        )

