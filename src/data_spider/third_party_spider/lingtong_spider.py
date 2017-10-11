# -*- coding: utf-8 -*-
import logging
from datetime import datetime

import requests
from decimal import Decimal

from s_common import Spider
from symbols.models import Symbol
from third_party_data.models import LingtongData

logger = logging.getLogger(__name__)


class LingtongSpider(Spider):
    """
    灵通报价
    """

    def _run(self):
        url = 'http://www.enanchu.com/ajaxQuoteRecordsToday.action?tabId=11'
        resp = requests.get(url, timeout=5)
        resp = resp.json()

        for item in resp["records"]:
            day = datetime.strptime(item['quotationTimeFormatString'], '%Y-%m-%d').date()
            symbol = 'LTBJ_%s' % item['commodityId']
            price = (Decimal(item['highPrice']) + Decimal(item['lowPrice'])) / 2

            # symbol 是否存在, 若不存在则新建
            symbol_obj = Symbol.objects.filter(symbol=symbol)
            if not symbol_obj:
                logger.info('symbol %s not exist, adding to symbol...' % symbol)
                symbol_obj = Symbol(
                    title=item['commodityName'],
                    symbol=symbol,
                    table_name='data_lingtong',
                    source='南储接口:灵通报价',
                    duration_unit='d',
                )
                symbol_obj.save()

            record = LingtongData.objects.filter(symbol=symbol, date=day).first()
            if record:
                logger.info('%s %s 已在数据库，跳过' % (symbol, day))
                continue
            else:
                logger.info('%s 数据库无数据, 全部保存到数据库' % symbol)
                LingtongData.objects.update_or_create_all_envs(
                    logger,
                    price_high=item['highPrice'],
                    price_low=item['lowPrice'],
                    price=price,
                    change=item['priceRate'],
                    symbol=symbol,
                    date=day
                )
