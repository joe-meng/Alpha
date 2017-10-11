import pprint
from datetime import datetime, date

import logging

import requests
from decimal import Decimal
from lxml import html

from future.models import FutureBWDSummary

logger = logging.getLogger(__name__)


def crawl_enanchu():
    """
    南储商务网
    铜、铝、锌
    """
    url = 'http://www.enanchu.com/ajaxQuoteRecordsToday.action?tabId=1'
    source = 'enanchu'
    metal_commodity_mapping = {
        'Cu': {
            'bwd': 20,
            'symbol': 'USE00001',
        },
        'Al': {
            'bwd': 8,
            'symbol': 'USE00002',
        },
        'Zn': {
            'bwd': 459,
            'symbol': 'USE00003',
        }
    }

    logger.info('开始爬取 %s, url: %s' % (source, url))
    response = requests.get(url, timeout=5).json()['records']

    for metal, mapping in metal_commodity_mapping.items():
        try:
            item = list(filter(lambda i: i['commodityId'] == mapping['bwd'], response))[0]
        except Exception as e:
            logger.error('%s 解析错误: %s' % (metal, e.args[0]))
            continue

        FutureBWDSummary.objects.update_or_create_all_envs(
            logger,
            varieties=metal,
            source=source,
            date=datetime.strptime(item['quotationTimeFormatString'], '%Y-%m-%d'),
            duration_unit='d',
            future='1m',
            symbol=mapping['symbol'],
            defaults={
                'price_high': item['highPrice'],
                'price_low': item['lowPrice'],
                'price': (Decimal(item['highPrice']) + Decimal(item['lowPrice'])) / 2,
            }
        )


def crawl_ccmn_长江现货():
    """
    ccmn 长江现货报价 | 铜、铝
    """

    source = 'ccmn_长江现货'
    metal_mappings = {
        'Cu': {
            'match': '铜升贴水',
            'symbol': 'USE00004',
        },
        'Al': {
            'match': '铝升贴水',
            'symbol': 'USE00005',
        }
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

        FutureBWDSummary.objects.update_or_create_all_envs(
            logger,
            varieties=metal,
            source=source,
            date=datetime.strptime(date_string, '%Y-%m-%d'),
            duration_unit='d',
            future='1m',
            symbol=mapping['symbol'],
            defaults={
                'price': line.xpath('td[position()=4]/text()')[0],
                'price_high': price_high.replace('b', '+').replace('c', '-'),
                'price_low': price_low.replace('b', '+').replace('c', '-'),
            }
        )


def crawl_ccmn_长江有色网():
    """
    ccmn 长江有色网升贴水 | 铜、铝
    """

    source = 'ccmn_长江有色网'
    metal_mappings = {
        'Cu': {
            'match': '铜升贴水',
            'symbol': 'USE00006',
        },
        'Al': {
            'match': '铝升贴水',
            'symbol': 'USE00007',
        }
    }
    url = 'http://www.ccmn.cn/historyprice/cjysw_1/'

    logger.info('开始爬取 %s, url: %s' % (source, url))
    response = requests.get(url, timeout=5)
    dom = html.fromstring(response.text)

    for metal, mapping in metal_mappings.items():
        try:
            line = dom.xpath('//td[text()="%s"]/ancestor::tr' % mapping['match'])[0]
            price_low, price_high = map(
                lambda i: i.replace('b', '').replace('c', '-'),
                line.xpath('td[position()=3]/text()')[0].split('—')
            )
            date_string = '%s-%s' % (datetime.today().year, line.xpath('td[position()=7]/text()')[0])
        except Exception as e:
            logger.error('%s 解析错误: %s' % (metal, e.args[0]))
            continue

        FutureBWDSummary.objects.update_or_create_all_envs(
            logger,
            varieties=metal,
            source=source,
            date=datetime.strptime(date_string, '%Y-%m-%d'),
            duration_unit='d',
            future='1m',
            symbol=mapping['symbol'],
            defaults={
                'price': line.xpath('td[position()=4]/text()')[0],
                'price_high': price_high,
                'price_low': price_low,
            },
        )


def crawl_shmet_lme():
    """
    SHMET LME BWD
    """
    source = 'shmet_lme'
    metal_mappings = {
        'Cu': {
            'match': '铜',
            'symbol': 'USE00164',
        },
        'Al': {
            'match': '铝',
            'symbol': 'USE00165',
        },
        'Pb': {
            'match': '铅',
            'symbol': 'USE00166',
        },
        'Zn': {
            'match': '锌',
            'symbol': 'USE00167',
        },
        'Ni': {
            'match': '镍',
            'symbol': 'USE00168',
        },
    }
    url = 'http://www.shmet.com/Template/_Template.html?viewName=_HomeLme&metalid=10191,10198,10199,10200,10201,10202'

    logger.info('开始爬取 %s, url: %s' % (source, url))
    response = requests.get(url, timeout=5)
    dom = html.fromstring(response.text)

    for metal, mapping in metal_mappings.items():
        try:
            line = dom.xpath('//td[position()=1][contains(.,"%s")]/ancestor::tr' % mapping['match'])[0].getchildren()
            date_string = '%s-%s' % (date.today().year, line[4].text)
            price_low, price_high = map(lambda i: i.replace('c', '-').replace('b', '').replace('level', '0' or None),
                                        line[3].text.split('/'))
        except Exception as e:
            logger.error('%s 解析错误: %s' % (metal, e.args[0]))
            continue

        FutureBWDSummary.objects.update_or_create_all_envs(
            logger,
            varieties=metal,
            future='3m',
            source=source,
            date=datetime.strptime(date_string, '%Y-%m-%d').date(),
            duration_unit='d',
            symbol=mapping['symbol'],
            defaults={
                'price_high': price_high,
                'price_low': price_low,
                'price': (Decimal(price_low) + Decimal(price_high)) / 2,
            }
        )


def crawl_shmet_bonded():
    """
    SHMET 保税区溢价
    """
    source = 'shmet_bonded'
    metal_mappings = {
        'Cu': {
            'match': '铜',
            'symbol': 'USE00008',
        },
        'Al': {
            'match': '铝',
            'symbol': 'USE00009',
        },
        'Pb': {
            'match': '铅',
            'symbol': 'USE00010',
        },
        'Zn': {
            'match': '锌',
            'symbol': 'USE00011',
        },
        'Ni': {
            'match': '镍',
            'symbol': 'USE00012',
        },
    }
    url = 'http://www.shmet.com/Template/_Template.html?viewName=_HomeOuter&metalid=10149,10150,10151,10152,10170'

    logger.info('开始爬取 %s, url: %s' % (source, url))
    response = requests.get(url, timeout=5)
    dom = html.fromstring(response.text)

    for metal, mapping in metal_mappings.items():
        try:
            line = dom.xpath('//td[position()=1][contains(.,"%s")]/ancestor::tr' % mapping['match'])[0].getchildren()
            date_string = '%s-%s' % (date.today().year, line[4].text)
            price_low, price_high = map(lambda i: i or None, line[1].text.split('-'))
            if not price_low or not price_high:
                continue
        except Exception as e:
            logger.error('%s 解析错误: %s' % (metal, e.args[0]))
            continue

        FutureBWDSummary.objects.update_or_create_all_envs(
            logger,
            varieties=metal,
            source=source,
            date=datetime.strptime(date_string, '%Y-%m-%d').date(),
            duration_unit='d',
            change=line[3].text,
            future='1m',
            symbol=mapping['symbol'],
            defaults={
                'price_high': price_high,
                'price_low': price_low,
                'price': line[2].text,
            }
        )


def crawl_shmet():
    """
    现货 bwd
    """
    source = 'shmet'
    metal_mappings = {
        'Cu': {
            'match': '1# 电解铜',
            'symbol': 'USE00013'
        },
        'Al': {
            'match': 'A00 铝',
            'symbol': 'USE00014'
        },
        'Pb': {
            'match': '1# 铅',
            'symbol': 'USE00015'
        },
        'Zn': {
            'match': '0# 锌',
            'symbol': 'USE00016'
        },
        'Ni': {
            'match': '1# 电解镍',
            'symbol': 'USE00017'
        },
        'Ni_Russia': {
            'match': '俄罗斯镍',
            'symbol': 'USE00018'
        },
    }
    url = 'http://www.shmet.com/Template/_Template.html?viewName=_HomeSpotPrice&metalid=10133,10131,10132,10002,10003,10135,10213'

    logger.info('开始爬取 %s, url: %s' % (source, url))
    response = requests.get(url, timeout=5)
    dom = html.fromstring(response.text)

    for metal, mapping in metal_mappings.items():
        try:
            line = dom.xpath('//td[position()=1][contains(.,"%s")]/ancestor::tr' % mapping['match'])[0].getchildren()
            date_string = '%s-%s' % (date.today().year, line[4].text)
            price_low, price_high = map(lambda i: i.replace('c', '-').replace('b', '').replace('level', '0' or None),
                                        line[3].text.split('/'))
        except Exception as e:
            logger.error('%s 解析错误: %s' % (metal, e.args[0]))
            continue

        FutureBWDSummary.objects.update_or_create_all_envs(
            logger,
            varieties=metal,
            source=source,
            date=datetime.strptime(date_string, '%Y-%m-%d').date(),
            duration_unit='d',
            future='1m',
            symbol=mapping['symbol'],
            defaults={
                'price_high': price_high,
                'price_low': price_low,
                'price': (Decimal(price_low) + Decimal(price_high)) / 2,
            }
        )


def crawl_smm_cu_huabei():
    """
    smm 华北升贴水 | 铜
    """
    source = 'smm_华北'
    metal = 'Cu'
    url = 'http://hq.smm.cn/spot_data/8/全部类别/华北地区'
    symbol = 'USE00019'

    logger.info('开始爬取 %s, url: %s' % (source, url))
    response = requests.get(url, timeout=5).json()['products'][0]

    FutureBWDSummary.objects.update_or_create_all_envs(
        logger,
        varieties=metal,
        source=source,
        date=datetime.strptime(response['PremiumDetail'][0]['RenewDate'], '%Y-%m-%d'),
        duration_unit='d',
        future='1m',
        symbol=symbol,
        defaults={
            'price': response['SpotDetail']['Average'],
            'price_high': response['SpotDetail']['Highs'],
            'price_low': response['SpotDetail']['Low'],
        }

    )


def crawl_smm():
    """
    smm 升贴水 | 铜
    """
    source = 'smm'
    url = 'https://www.smm.cn/'
    logger.info('开始爬取 %s' % url)
    metal_mappings = {
        'Cu': {
            'match': 'SMM 1#电解铜',
            'symbol': 'USE00145',
        },
        'Al': {
            'match': 'SMM A00铝',
            'symbol': 'USE00146',
        }
    }

    response = requests.get(url, timeout=5)
    dom = html.fromstring(response.text)

    for metal, mapping in metal_mappings.items():
        try:
            date_string = dom.xpath('//a[text()="%s"]/ancestor::tr/td/text()' % mapping['match'])[-1]  # 格式：07-22
            date_string = '%s-%s' % (date.today().year, date_string)
            line = dom.xpath('//a[text()="%s"]/ancestor::tr/following-sibling::tr' % mapping['match'])[0].getchildren()
            price_low, price_high = map(lambda i: Decimal(i.replace('(', '').replace(')', '').replace(' ', '').replace('贴', '-').replace('升', '').replace('平水', '0')), line[1].text.strip('( )').split('-'))
        except Exception as e:
            logger.error('%s 解析错误: %s' % (metal, e.args[0]))
            continue

        FutureBWDSummary.objects.update_or_create_all_envs(
            logger,
            varieties=metal,
            source=source,
            date=datetime.strptime(date_string, '%Y-%m-%d'),
            duration_unit='d',
            future='1m',
            symbol=mapping['symbol'],
            defaults={
                'price': (price_high + price_low) / 2,
                'price_high': price_high,
                'price_low': price_low,
            }
        )
