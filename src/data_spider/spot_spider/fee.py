# -- coding: utf-8 --
import logging

import re
from datetime import date, datetime

import requests
from lxml import html

from enums import FeeTypes
from varieties.models import Fee

logger = logging.getLogger(__name__)


def crawl_smm_zn():
    """
    smm 加工费报价 | 锌
    """
    source = 'smm'
    metal = 'Zn'
    url = 'http://hq.smm.cn/xin'

    logger.info('开始爬取 %s, url: %s' % (source, url))
    response = requests.get(url, timeout=5)
    dom = html.fromstring(response.text)

    match_text = '国产锌精矿T/C'
    date_string = dom.xpath('//span[text()="%s"]/parent::div/following-sibling::*[2]/text()' % match_text)[
        0]  # 格式：6月22日
    month, day = map(int, re.match(r'(\d+)月(\d+)日', date_string).groups())

    source = 'smm'
    price = dom.xpath('//span[text()="%s"]/parent::div/span[3]/text()' % match_text)[0]
    price_low, price_high = dom.xpath('//span[text()="%s"]/parent::div/span[2]/text()' % match_text)[0].split('-')
    Fee.objects.update_or_create_all_envs(
        logger,
        varieties=metal,
        source=source,
        date=date(datetime.today().year, month, day),
        type=FeeTypes.domestic_processing_fee.value,
        symbol='USE00045',
        defaults={
            'price': price,
            'price_low': price_low,
            'price_high': price_high,
        }
    )

    match_text = '进口锌精矿T/C'
    date_string = dom.xpath('//span[text()="%s"]/parent::div/following-sibling::*[2]/text()' % match_text)[
        0]  # 格式：6月22日
    month, day = map(int, re.match(r'(\d+)月(\d+)日', date_string).groups())
    price = dom.xpath('//span[text()="%s"]/parent::div/span[3]/text()' % match_text)[0]
    price_low, price_high = dom.xpath('//span[text()="%s"]/parent::div/span[2]/text()' % match_text)[0].split('-')
    Fee.objects.update_or_create_all_envs(
        logger,
        varieties=metal,
        source=source,
        date=date(datetime.today().year, month, day),
        type=FeeTypes.import_processing_fee.value,
        symbol='USE00046',
        defaults={
            'price': price,
            'price_low': price_low,
            'price_high': price_high,
        }
    )


def crawl_smm_pb():
    """
    smm 加工费报价 | 铅
    """
    source = 'smm'
    metal = 'Pb'
    url = 'http://hq.smm.cn/qian'

    logger.info('开始爬取 %s, url: %s' % (source, url))
    response = requests.get(url, timeout=5)
    dom = html.fromstring(response.text)

    match_text = '国产铅精矿T/C'
    date_string = dom.xpath('//span[text()="%s"]/parent::div/following-sibling::*[2]/text()' % match_text)[
        0]  # 格式：6月22日
    month, day = map(int, re.match(r'(\d+)月(\d+)日', date_string).groups())

    source = 'smm'
    price = dom.xpath('//span[text()="%s"]/parent::div/span[3]/text()' % match_text)[0]
    price_low, price_high = dom.xpath('//span[text()="%s"]/parent::div/span[2]/text()' % match_text)[0].split('-')
    Fee.objects.update_or_create_all_envs(
        logger,
        varieties=metal,
        source=source,
        date=date(datetime.today().year, month, day),
        type=FeeTypes.domestic_processing_fee.value,
        symbol='USE00157',
        defaults={
            'price': price,
            'price_low': price_low,
            'price_high': price_high,
        }
    )

    match_text = '进口铅精矿T/C'
    date_string = dom.xpath('//span[text()="%s"]/parent::div/following-sibling::*[2]/text()' % match_text)[
        0]  # 格式：6月22日
    month, day = map(int, re.match(r'(\d+)月(\d+)日', date_string).groups())
    price = dom.xpath('//span[text()="%s"]/parent::div/span[3]/text()' % match_text)[0]
    price_low, price_high = dom.xpath('//span[text()="%s"]/parent::div/span[2]/text()' % match_text)[0].split('-')
    Fee.objects.update_or_create_all_envs(
        logger,
        varieties=metal,
        source=source,
        date=date(datetime.today().year, month, day),
        type=FeeTypes.import_processing_fee.value,
        symbol='USE00158',
        defaults={
            'price': price,
            'price_low': price_low,
            'price_high': price_high,
        }
    )
