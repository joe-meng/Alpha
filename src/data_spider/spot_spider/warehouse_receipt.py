# -- coding: utf-8 --
from collections import OrderedDict
from datetime import date, datetime

import logging
import requests
from lxml import html
import json
import re

from spot.models import SpotWarehouseReceipt
from django.db import transaction

METAL_TYPES = ('铜', '铝', '锌', '天然橡胶', '燃料油', '黄金', '螺纹钢', '线材', '铅', '白银', '沥青仓库', '沥青厂库')

METAL_MAPPINGS = {
    '铜': 'Cu',
    '铝': 'Al',
    '铅': 'Pb',
    '锌': 'Zn',
    '镍': 'Ni',
    '锡': 'Sn',
    '天然橡胶': 'Ru',
    '燃料油': 'Fu',
    '黄金': 'Au',
    '螺纹钢': 'Rb',
    '线材': 'Wr',
    '白银': 'Ag',
    '沥青仓库': 'Bu_warehouse',
    '沥青厂库': 'Bu_factory',
    '沥青': 'Bu',
    '热轧卷板': 'Hc',
}

logger = logging.getLogger(__name__)


def strip_eng(string):
    return re.findall(r'(.*)\$\$.*', string)[0]


def crawl_lme():
    """
    lme 库存 | 铜、铝、镍、锌
    """
    metal_lme_mapping = OrderedDict((
        ('Al', {
            'match': 'aluminium',
            'symbol': 'USE00104'
        }),
        ('Cu', {
            'match': 'copper',
            'symbol': 'USE00105'
        }),
        ('Ni', {
            'match': 'nickel',
            'symbol': 'USE00106'
        }),
        ('Zn', {
            'match': 'zinc',
            'symbol': 'USE00107'
        }),
    ))
    source = 'lme'

    for metal, mapping in metal_lme_mapping.items():
        url = 'http://www.lme.com/metals/non-ferrous/%s/' % mapping['match']
        logger.info('开始爬取 %s, url: %s' % (source, url))

        try:
            response = requests.get(url, timeout=5)
            dom = html.fromstring(response.text)
            date_string = re.findall(r'(.*) for (.*)', dom.xpath('//div[contains(@class, "delayed-date")]/text()')[0])[0][1].strip()
            amount = dom.xpath('//td[text()="Cancelled Warrants"]/ancestor::tr/td[position()=2]/text()')[0]
        except Exception as e:
            logger.error('%s 错误: %s' % (metal, e.args[0]))
            continue

        SpotWarehouseReceipt.objects.update_or_create_all_envs(
            logger,
            varieties=metal,
            date=datetime.strptime(date_string, '%d %B %Y'),
            source=source,
            is_cancelled=True,
            duration_unit='d',
            area='总计',
            symbol=mapping['symbol'],
            defaults={
                'amount': amount,
            }
        )


def crawl_shfe():
    """
    从 history spider 直接搬过来，和其他格式不一样
    :return:
    """
    source = 'shfe'
    current_date = date.today()
    mappings = {
        'Al': {
            '上海': 'USE00108',
            '保税商品总计': 'USE00109',
            '保税总计': 'USE00110',
            '天津': 'USE00111',
            '完税商品总计': 'USE00112',
            '完税总计': 'USE00113',
            '山东': 'USE00114',
            '广东': 'USE00115',
            '总计': 'USE00116',
            '江苏': 'USE00117',
            '河南': 'USE00118',
            '浙江': 'USE00119',
            '重庆': 'USE00120',
        },
        'Cu': {
            '上海': 'USE00121',
            '保税商品总计': 'USE00122',
            '保税总计': 'USE00123',
            '完税商品总计': 'USE00124',
            '完税总计': 'USE00125',
            '广东': 'USE00126',
            '总计': 'USE00127',
            '江苏': 'USE00128',
            '浙江': 'USE00129',
        },
        'Ni': {
            '上海': 'USE00130',
            '总计': 'USE00131',
            '江苏': 'USE00132',
            '浙江': 'USE00133',
        },
        'Pb': {
            '上海': 'USE00134',
            '天津': 'USE00135',
            '广东': 'USE00136',
            '总计': 'USE00137',
            '江苏': 'USE00138',
            '浙江': 'USE00139',
        },
        'Zn': {
            '上海': 'USE00140',
            '广东': 'USE00141',
            '总计': 'USE00142',
            '江苏': 'USE00143',
            '浙江': 'USE00144',
        },
    }

    if SpotWarehouseReceipt.objects.filter(date=current_date, source=source):
        logger.info(('%s 识别为已爬取' % current_date).center(80, '*'))
        return

    today_string = date.strftime(current_date, '%Y%m%d')
    url = 'http://www.shfe.com.cn/data/dailydata/%sdailystock.dat' % today_string

    logger.info('开始爬取 %s, url: %s' % (source, url))
    response = requests.get(url, timeout=5)

    if response.status_code == 200:
        json_response = json.loads(response.text)['o_cursor']

        receipt_list = []
        for row in filter(lambda i: '计' in i.get('WHABBRNAME', ''), json_response):
            varieties_cn = strip_eng(row['VARNAME'])
            varieties = METAL_MAPPINGS.get(varieties_cn, varieties_cn)
            area = strip_eng(row['REGNAME'] or row['WHABBRNAME'])
            warehouse_receipt = SpotWarehouseReceipt(
                varieties=varieties,
                area=area,
                date=current_date,
                source=source,
                duration_unit='d',
                amount=row['WRTWGHTS'],
                change=row['WRTCHANGE'],
                symbol=mappings.get(varieties, {}).get(area, None),
            )
            receipt_list.append(warehouse_receipt)

        try:
            if receipt_list:
                with transaction.atomic():
                    SpotWarehouseReceipt.objects.bulk_create_all_envs(
                        receipt_list,
                        logger=logger,
                        logger_params={'current_date': current_date}
                    )
        except Exception as e:
            logger.error(('%s 插入失败 %s %s' % (current_date, e, response.url)).center(80, '*'))
    else:
        logger.info('%s 请求返回 %s' % (current_date, response.status_code))
