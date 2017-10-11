# -- coding: utf-8 --
from datetime import datetime

import logging
import requests
from decimal import Decimal
from lxml import html

from spot.models import SpotExchangeRateDetail, SpotExchangeRateSummary

logger = logging.getLogger(__name__)


def crawl_boc():
    """
    中国银行外汇牌价 | 现汇买卖价、现钞买卖价、外管局中间价、银行报价
    http://www.bankofchina.com/sourcedb/whpj/index.html
    """
    url = 'http://srh.bankofchina.com/search/whpj/search.jsp'
    source = 'boc'
    currency = 'USD'
    USD_query_code = '1316'
    symbol = 'USE00043'

    logger.info('开始爬取 %s, url: %s' % (source, url))
    response = requests.post(url, data={'pjname': USD_query_code}, timeout=5)
    dom = html.fromstring(response.text)

    line = dom.xpath('//div[contains(@class, "BOC_main")]/table/tr')[1]
    SpotExchangeRateDetail.objects.update_or_create_all_envs(
        logger,
        currency=currency,
        date_time=datetime.strptime(line.getchildren()[7].text, '%Y.%m.%d %H:%M:%S'),
        source=source,
        symbol=symbol,
        defaults={
            'price_buy': Decimal(line.getchildren()[1].text) / 100,
            'price_sell': Decimal(line.getchildren()[3].text) / 100,
            'cash_buy': Decimal(line.getchildren()[2].text) / 100,
            'cash_sell': Decimal(line.getchildren()[4].text) / 100,
            'administration_price': Decimal(line.getchildren()[5].text) / 100,
            'price': Decimal(line.getchildren()[6].text) / 100,
        }
    )


def crawl_gov():
    """
    外管局外汇牌价 | 支持日级历史数据查询
    """
    url = 'http://www.safe.gov.cn/AppStructured/view/project!RMBQuery.action'
    source = 'gov'
    currency = 'USD'
    symbol = 'USE00044'

    logger.info('开始爬取 %s, url: %s' % (source, url))
    response = requests.get(url, timeout=5)
    dom = html.fromstring(response.text)

    SpotExchangeRateSummary.objects.update_or_create_all_envs(
        logger,
        currency=currency,
        date=datetime.strptime(dom.xpath('//table[@id="InfoTable"]//tr[2]//td[1]/text()')[0].strip(), '%Y-%m-%d'),
        source=source,
        duration_unit='d',
        symbol=symbol,
        defaults={
            'administration_price': Decimal(dom.xpath('//table[@id="InfoTable"]//tr[2]//td[2]/text()')[0]) / 100,
        }
    )
