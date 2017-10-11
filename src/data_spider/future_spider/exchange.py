# -- coding: utf-8 --
import pprint
from datetime import datetime

import logging
import requests
from decimal import Decimal
from lxml import html

from future.models import FutureExchangeRate


logger = logging.getLogger(__name__)


def crawl_boc():
    """
    中国银行外汇牌价 | 期货
    http://www.bankofchina.com/sourcedb/ffx/
    """
    url = 'http://www.bankofchina.com/sourcedb/ffx/'
    source = 'boc'
    currency = 'USD'
    future_mappings = {
        '1w': {
            'match': '一周',
            'symbol': 'USE00020',
        },
        '20d': {
            'match': '二十天',
            'symbol': 'USE00021',
        },
        '1m': {
            'match': '一个月',
            'symbol': 'USE00022',
        },
        '2m': {
            'match': '两个月',
            'symbol': 'USE00023',
        },
        '3m': {
            'match': '三个月',
            'symbol': 'USE00024',
        },
        '4m': {
            'match': '四个月',
            'symbol': 'USE00025',
        },
        '5m': {
            'match': '五个月',
            'symbol': 'USE00026',
        },
        '6m': {
            'match': '六个月',
            'symbol': 'USE00027',
        },
        '7m': {
            'match': '七个月',
            'symbol': 'USE00028',
        },
        '8m': {
            'match': '八个月',
            'symbol': 'USE00029',
        },
        '9m': {
            'match': '九个月',
            'symbol': 'USE00030',
        },
        '10m': {
            'match': '十个月',
            'symbol': 'USE00031',
        },
        '11m': {
            'match': '十一个月',
            'symbol': 'USE00032',
        },
        '12m': {
            'match': '十二个月',
            'symbol': 'USE00033',
        },
    }

    logger.info('开始爬取 %s, url: %s' % (source, url))
    response = requests.get(url, timeout=5)
    dom = html.fromstring(response.content.decode())

    for future, mapping in future_mappings.items():
        try:
            line = dom.xpath('//tr[td[text()="{0}"] and td[text()="{1}"]]'.format(currency, mapping['match']))[0].getchildren()
        except Exception as e:
            logger.error('%s 解析错误: %s' % (future, e.args[0]))
            continue

        FutureExchangeRate.objects.update_or_create_all_envs(
            logger,
            currency=currency,
            future=future,
            source=source,
            date=datetime.strptime(line[6].text, '%Y-%m-%d'),
            symbol=mapping['symbol'],
            defaults={
                'price_buy': Decimal(line[3].text) / 100,
                'price_sell': Decimal(line[4].text) / 100,
                'price': Decimal(line[5].text) / 100,
            }
        )
