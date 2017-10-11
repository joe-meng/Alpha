# -- coding: utf-8 --
import re
import logging
import requests
from collections import OrderedDict
from datetime import datetime, date

import execjs

from future.models import FuturePriceDetail
from third_party_data.models import DataSinaDayKLine


logger = logging.getLogger(__name__)


def crawl_sina_lme():
    """
    新浪财经 lme 报价 | 铜、铝、镍、锌、铅
    """
    metal_lme_mapping = OrderedDict((
        ('Al', {
            'match': 'hf_AHD',
            'symbol': 'USE00038'
        }),
        ('Cu', {
            'match': 'hf_CAD',
            'symbol': 'USE00039'
        }),
        ('Ni', {
            'match': 'hf_NID',
            'symbol': 'USE00040'
        }),
        ('Pb', {
            'match': 'hf_PBD',
            'symbol': 'USE00041'
        }),
        ('Zn', {
            'match': 'hf_ZSD',
            'symbol': 'USE00042'
        }),
    ))
    ids = [i['match'] for i in metal_lme_mapping.values()]
    url = 'http://hq.sinajs.cn/?list=%s' % ','.join(ids)
    source = 'sina_lme'

    logger.info('开始爬取 %s, url: %s' % (source, url))
    response = requests.get(url, timeout=5)
    response = re.findall(r'"(.*)"', response.text)

    for i, metal in enumerate(metal_lme_mapping):
        line = response[i].split(',')
        FuturePriceDetail.objects.update_or_create_all_envs(
            logger,
            varieties=metal,
            future='3m',
            date_time=datetime.strptime('%s %s' % (line[12], line[6]), '%Y-%m-%d %H:%M:%S'),
            source=source,
            symbol=metal_lme_mapping[metal]['symbol'],
            defaults={
                'price': line[0],
            }
        )



def crawl_sina_lme_day():
    """
    新浪财经 lme 报价 | 铜、铝、镍、锌、铅
    http://stock2.finance.sina.com.cn/futures/api/jsonp.php/var _AHD2017_8_28=/GlobalFuturesService.getGlobalFuturesDailyKLine?symbol=AHD
    """
    metal_lme_mapping = OrderedDict((
        ('Al', {
            'match': 'AHD',
            'symbol': 'USE00152'
        }),
        ('Cu', {
            'match': 'CAD',
            'symbol': 'USE00153'
        }),
        ('Ni', {
            'match': 'NID',
            'symbol': 'USE00154'
        }),
        ('Pb', {
            'match': 'PBD',
            'symbol': 'USE00155'
        }),
        ('Zn', {
            'match': 'ZSD',
            'symbol': 'USE00156'
        }),
    ))

    today = date.today().strftime('%Y_%m_%d')
    source = 'sina_lme'
    exchange = 'LME'
    for metal, mapping in metal_lme_mapping.items():
        sina_code = mapping['match']
        url = f'http://stock2.finance.sina.com.cn/futures/api/jsonp.php/var%20_{sina_code}{today}=/GlobalFuturesService.getGlobalFuturesDailyKLine?symbol={sina_code}'

        logger.info('开始爬取 %s, url: %s' % (source, url))
        response = requests.get(url, timeout=5)
        response = re.findall(r'\((.*)\)', response.text)[0]
        day_kline = execjs.eval(response)

        latest_day_kline = DataSinaDayKLine.objects.filter(symbol=mapping['symbol']).order_by('-date').first()
        latest_day = latest_day_kline.date if latest_day_kline else date(2000, 1, 1)

        for kline in filter(lambda kline: datetime.strptime(kline['date'], '%Y-%m-%d').date() >= latest_day, day_kline):
            DataSinaDayKLine.objects.update_or_create_all_envs(
                logger,
                varieties=metal,
                symbol=mapping['symbol'],
                exchange=exchange,
                date=datetime.strptime(kline['date'], '%Y-%m-%d'),
                defaults={
                    'price_low': kline['low'],
                    'price_high': kline['high'],
                    'price_open': kline['open'],
                    'price_close': kline['close'],
                    'volume': kline['volume'],
                }
            )



def crawl_sina_shfe_day():
    """
    新浪财经 shfe 报价 | 铜、铝、镍、锌、铅
    http://stock2.finance.sina.com.cn/futures/api/jsonp.php/var _AHD2017_8_28=/GlobalFuturesService.getGlobalFuturesDailyKLine?symbol=AHD
    """
    metal_lme_mapping = OrderedDict((
        ('Al', {
            'match': 'AL0',
            'symbol': 'USE00159'
        }),
        ('Cu', {
            'match': 'CU0',
            'symbol': 'USE00160'
        }),
        ('Ni', {
            'match': 'NI0',
            'symbol': 'USE00161'
        }),
        ('Pb', {
            'match': 'PB0',
            'symbol': 'USE00162'
        }),
        ('Zn', {
            'match': 'ZN0',
            'symbol': 'USE00163'
        }),
    ))

    today = date.today().strftime('%Y_%m_%d')
    source = 'sina_shfe'
    exchange = 'SHFE'
    for metal, mapping in metal_lme_mapping.items():
        sina_code = mapping['match']
        url = f'http://stock2.finance.sina.com.cn/futures/api/jsonp.php/var%20_{sina_code}{today}=/InnerFuturesNewService.getDailyKLine?symbol={sina_code}'
        logger.info('开始爬取 %s, url: %s' % (source, url))
        response = requests.get(url, timeout=5)
        response = re.findall(r'\((.*)\)', response.text)[0]
        day_kline = execjs.eval(response)

        latest_day_kline = DataSinaDayKLine.objects.filter(symbol=mapping['symbol']).order_by('-date').first()
        latest_day = latest_day_kline.date if latest_day_kline else date(2000, 1, 1)

        for kline in filter(lambda kline: datetime.strptime(kline['d'], '%Y-%m-%d').date() >= latest_day, day_kline):
            DataSinaDayKLine.objects.update_or_create_all_envs(
                logger,
                varieties=metal,
                symbol=mapping['symbol'],
                exchange=exchange,
                date=datetime.strptime(kline['d'], '%Y-%m-%d'),
                defaults={
                    'price_low': kline['l'],
                    'price_high': kline['h'],
                    'price_open': kline['o'],
                    'price_close': kline['c'],
                    'volume': kline['v'],
                }
            )


