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


def crawl_smm():
    """
    smm 报价
    """
    metal_mappings = {
        'Cu': {
            'match': 'SMM 1#电解铜',
            'symbol': 'USE00147',
        },
        'Al': {
            'match': 'SMM A00铝',
            'symbol': 'USE00148',
        },
        'Ni': {
            'match': 'SMM 1#电解镍',
            'symbol': 'USE00149',
        },
        'Zn': {
            'match': 'SMM 0#锌锭',
            'symbol': 'USE00150',
        },
    }
    url = 'https://www.smm.cn/'
    source = 'smm'

    logger.info('开始爬取 %s, url: %s' % (source, url))
    response = requests.get(url, timeout=5)
    dom = html.fromstring(response.text)

    date_string = dom.xpath('//span[@class="content-left-first-pirce-index-date"]/text()')[0]  # 格式：07-22
    date_string = '%s-%s' % (date.today().year, date_string)

    for metal, mapping in metal_mappings.items():
        try:
            line = dom.xpath('//a[text()="%s"]/ancestor::tr' % mapping['match'])[0].getchildren()
            price_low, price_high = map(lambda i: Decimal(i), line[1].text.split('-'))
            price = line[2].text.strip()
        except Exception as e:
            logger.error('%s 解析错误: %s' % (metal, e.args[0]))
            continue

        SpotPriceSummary.objects.update_or_create_all_envs(
            logger,
            varieties=metal,
            source='smm',
            date=datetime.strptime(date_string, '%Y-%m-%d'),
            duration_unit='d',
            symbol=mapping['symbol'],
            defaults={
                'price_low': price_low,
                'price_high': price_high,
                'price': price,
            }
        )


def crawl_smm_al():
    """
    smm 报价 | 铝
    """
    metal = 'Al'
    url = 'http://hq.smm.cn/lv'
    source = 'smm_无锡'

    logger.info('开始爬取 %s, url: %s' % (source, url))
    response = requests.get(url, timeout=5)
    dom = html.fromstring(response.text)

    match_text = '无锡 A00铝'
    date_string = dom.xpath(
        '//span[@class="value1" and text()="%s"]/parent::div/parent::div/div[@class="itemDateTime"]/text()' % match_text)[
        0]  # 格式：6月22日
    month, day = map(int, re.match(r'(\d+)月(\d+)日', date_string).groups())
    price_low, price_high = dom.xpath('//span[text()="%s"]/parent::div/span[2]/text()' % match_text)[0].split('-')
    SpotPriceSummary.objects.update_or_create_all_envs(
        logger,
        varieties=metal,
        source='smm_无锡',
        date=date(datetime.today().year, month, day),
        duration_unit='d',
        symbol='USE00047',
        defaults={
            'price_low': price_low,
            'price_high': price_high,
            'price': dom.xpath('//span[text()="%s"]/parent::div/span[3]/text()' % match_text)[0],
        }
    )


def crawl_smm_cu_huabei():
    """
    smm 报价 | 铜
    """
    source = 'smm_华北'
    metal = 'Cu'
    url = 'http://hq.smm.cn/spot_data/8/全部类别/华北地区'

    logger.info('开始爬取 %s, url: %s' % (source, url))
    response = requests.get(url, timeout=5).json()['products'][0]

    SpotPriceSummary.objects.update_or_create_all_envs(
        logger,
        varieties=metal,
        source=source,
        date=datetime.strptime(response['SpotDetail']['RenewDate'], '%Y-%m-%d'),
        duration_unit='d',
        symbol='USE00049',
        defaults={
            'price': response['SpotDetail']['Average'],
            'price_high': response['SpotDetail']['Highs'],
            'price_low': response['SpotDetail']['Low'],
        }
    )


def crawl_ccmn_长江现货():
    """
    ccmn 长江现货报价 | 铜、铝、锌、镍
    """

    source = 'ccmn_长江现货'
    metal_mappings = {
        'Cu': {
            'match': '1#铜',
            'symbol': 'USE00050',
        },
        'Al': {
            'match': 'A00铝',
            'symbol': 'USE00051',
        },
        'Ni': {
            'match': '1#镍',
            'symbol': 'USE00052',
        },
        'Zn': {
            'match': '0#锌',
            'symbol': 'USE00053',
        },
    }
    url = 'http://www.ccmn.cn/historyprice/cjxh_1/'

    logger.info('开始爬取 %s, url: %s' % (source, url))
    response = requests.get(url, timeout=5)
    dom = html.fromstring(response.text)

    for metal, mapping in metal_mappings.items():
        try:
            line = dom.xpath('//td[text()="%s"]/ancestor::tr' % mapping['match'])[0]
            price_low, price_high = line.xpath('td[position()=3]/text()')[0].split('—')
            date_string = '%s-%s' % (datetime.today().year, line.xpath('td[position()=7]/text()')[0])
        except Exception as e:
            logger.error('%s 解析错误: %s' % (metal, e.args[0]))
            continue

        SpotPriceSummary.objects.update_or_create_all_envs(
            logger,
            varieties=metal,
            source=source,
            date=datetime.strptime(date_string, '%Y-%m-%d'),
            duration_unit='d',
            symbol=mapping['symbol'],
            defaults={
                'price': line.xpath('td[position()=4]/text()')[0],
                'price_high': price_high,
                'price_low': price_low,
            }
        )


def crawl_ccmn_长江有色网():
    """
    ccmn 长江有色网报价 | 铜、铝、锌、镍
    """

    source = 'ccmn_长江有色网'
    metal_mappings = {
        'Cu': {
            'match': '1#铜',
            'symbol': 'USE00054',
        },
        'Al': {
            'match': 'A00铝',
            'symbol': 'USE00055',
        },
        'Ni': {
            'match': '1#镍',
            'symbol': 'USE00056',
        },
        'Zn': {
            'match': '0#锌',
            'symbol': 'USE00057',
        },
    }
    url = 'http://www.ccmn.cn/historyprice/cjysw_1/'

    logger.info('开始爬取 %s, url: %s' % (source, url))
    response = requests.get(url, timeout=10)
    dom = html.fromstring(response.text)

    for metal, mapping in metal_mappings.items():
        try:
            line = dom.xpath('//td[text()="%s"]/ancestor::tr' % mapping['match'])[0]
            price_low, price_high = line.xpath('td[position()=3]/text()')[0].split('—')
            date_string = '%s-%s' % (datetime.today().year, line.xpath('td[position()=7]/text()')[0])
        except Exception as e:
            logger.error('%s 解析错误: %s' % (metal, e.args[0]))
            continue

        SpotPriceSummary.objects.update_or_create_all_envs(
            logger,
            varieties=metal,
            source=source,
            date=datetime.strptime(date_string, '%Y-%m-%d'),
            duration_unit='d',
            symbol=mapping['symbol'],
            defaults={
                'price': line.xpath('td[position()=4]/text()')[0],
                'price_high': price_high,
                'price_low': price_low,
            }
        )


def crawl_enanchu():
    """
    南储商务网
    铜、铝、镍、锌、进出口铝
    """
    url = 'http://www.enanchu.com/ajaxQuoteRecordsToday.action?tabId=1'
    source = 'enanchu'
    metal_commodity_mapping = {
        'Cu': {
            'price': 18,
            'symbol': 'USE00058',
        },
        'Al': {
            'price': 22,
            'symbol': 'USE00059',
        },
        'Ni': {
            'price': 31,
            'symbol': 'USE00060',
        },
        'Zn': {
            'price': 24,
            'symbol': 'USE00061',
        }

    }
    logger.info('开始爬取 %s, url: %s' % (source, url))
    response = requests.get(url, timeout=5).json()['records']

    for metal, mapping in metal_commodity_mapping.items():
        try:
            item = list(filter(lambda i: i['commodityId'] == mapping['price'], response))[0]
        except Exception as e:
            logger.error('%s 解析错误: %s' % (metal, e.args[0]))
            continue

        SpotPriceSummary.objects.update_or_create_all_envs(
            logger,
            varieties=metal,
            source=source,
            date=datetime.strptime(item['quotationTimeFormatString'], '%Y-%m-%d'),
            duration_unit='d',
            symbol=mapping['symbol'],
            defaults={
                'price_high': item['highPrice'],
                'price_low': item['lowPrice'],
                'price': (Decimal(item['highPrice']) + Decimal(item['lowPrice'])) / 2,
            }
        )


def crawl_shmet():
    """
    上海金属网 现货报价
    """
    url = 'http://www.shmet.com/Template/_Template.html?viewName=_HomeSpotPrice&metalid=10133,10131,10132,10002,10003,10134,10135'
    source = 'shmet'
    metal_mappings = {
        'Cu': {
            'match': '1# 电解铜',
            'symbol': 'USE00062'
        },
        'Al': {
            'match': 'A00 铝',
            'symbol': 'USE00063'
        },
        'Pb': {
            'match': '1# 铅',
            'symbol': 'USE00064'
        },
        'Zn': {
            'match': '0# 锌',
            'symbol': 'USE00065'
        },
        'Ni': {
            'match': '1# 电解镍',
            'symbol': 'USE00066'
        },
    }

    logger.info('开始爬取 %s, url: %s' % (source, url))
    response = requests.get(url, timeout=5)
    dom = html.fromstring(response.text)

    for metal, mapping in metal_mappings.items():
        try:
            line = dom.xpath('//td[position()=1][contains(.,"%s")]/ancestor::tr' % mapping['match'])[0].getchildren()
            date_string = '%s-%s' % (date.today().year, line[4].text)
            price_low, price_high = map(Decimal, line[1].text.split('-'))
        except Exception as e:
            logger.error('%s 解析错误: %s' % (metal, e.args[0]))
            continue

        SpotPriceSummary.objects.update_or_create_all_envs(
            logger,
            varieties=metal,
            source=source,
            date=datetime.strptime(date_string, '%Y-%m-%d').date(),
            duration_unit='d',
            symbol=mapping['symbol'],
            defaults={
                'price_high': price_high,
                'price_low': price_low,
                'price': (price_high + price_low) / 2,
            }
        )
