# -- coding: utf-8 --
from datetime import date, timedelta, datetime

import json
import re

import logging

import requests
from django.db import transaction
from lxml import html

from spot.models import SpotStock


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


def crawl_shfe():
    """
    从 history spider 直接搬过来，和其他格式不一样
    :return:
    """
    source = 'shfe'
    mappings = {
        'Al': {
            '上海': 'USE00067',
            '保税商品总计': 'USE00068',
            '天津': 'USE00069',
            '完税商品总计': 'USE00070',
            '山东': 'USE00071',
            '广东': 'USE00072',
            '江苏': 'USE00073',
            '河南': 'USE00074',
            '浙江': 'USE00075',
            '重庆': 'USE00076',
            '总计': 'USE00151',
        },
        'Cu': {
            '上海': 'USE00077',
            '保税商品总计': 'USE00078',
            '完税商品总计': 'USE00079',
            '广东': 'USE00080',
            '总计': 'USE00081',
            '江苏': 'USE00082',
            '浙江': 'USE00083',
        },
        'Ni': {
            '上海': 'USE00084',
            '总计': 'USE00085',
            '江苏': 'USE00086',
            '浙江': 'USE00087',
        },
        'Pb': {
            '上海': 'USE00088',
            '天津': 'USE00089',
            '广东': 'USE00090',
            '总计': 'USE00091',
            '江苏': 'USE00092',
            '浙江': 'USE00093',
        },
        'Zn': {
            '上海': 'USE00094',
            '广东': 'USE00095',
            '总计': 'USE00096',
            '江苏': 'USE00097',
            '浙江': 'USE00098',
        },
    }

    def strip_eng(string):
        return re.findall(r'(.*)\$\$.*', string)[0]

    current_date = date.today()

    # 只爬未爬过的数据
    if SpotStock.objects.filter(date=current_date, source=source):
        logger.info(('%s 识别为已爬取' % current_date).center(80, '*'))
        return

    today_string = date.strftime(current_date, '%Y%m%d')
    url = 'http://www.shfe.com.cn/data/dailydata/%sweeklystock.dat' % today_string

    logger.info('开始爬取 %s, url: %s' % (source, url))
    response = requests.get(url, timeout=5)

    if response.status_code == 200:
        json_response = json.loads(response.text)['o_cursor']

        stock_list = []
        for row in filter(lambda i: '计' in i.get('WHABBRNAME', ''), json_response):
            varieties_cn = strip_eng(row['VARNAME'])
            varieties = METAL_MAPPINGS.get(varieties_cn, varieties_cn)
            area = strip_eng(row['REGNAME'] or row['WHABBRNAME'])
            stock = SpotStock(
                varieties=varieties,
                area=area,
                date=current_date,
                source=source,
                duration_unit='w',
                amount=row['SPOTWGHTS'] or None,
                change=row['SPOTCHANGE'] or None,
                symbol=mappings.get(varieties, {}).get(area, None),
            )
            stock_list.append(stock)

        try:
            if stock_list:
                with transaction.atomic():
                    SpotStock.objects.bulk_create_all_envs(
                        stock_list,
                        logger=logger,
                        logger_params={'current_date': current_date}
                    )
        except Exception as e:
            logger.error(('%s 插入失败 %s %s' % (current_date, e, response.url)).center(80, '*'))
    else:
        logger.info('%s 请求返回 %s' % (current_date, response.status_code))


def crawl_shmet():
    """
    LME 库存
    """
    source = 'shmet_lme'
    metal_mappings = {
        'Cu': {
            'match': '铜',
            'symbol': 'USE00099',
        },
        'Al': {
            'match': '铝',
            'symbol': 'USE00100',
        },
        'Pb': {
            'match': '铅',
            'symbol': 'USE00101',
        },
        'Zn': {
            'match': '锌',
            'symbol': 'USE00102',
        },
        'Ni': {
            'match': '镍',
            'symbol': 'USE00103',
        },
    }
    url = 'http://www.shmet.com/Template/_Template.html?viewName=_HomeLme&metalid=10191,10198,10199,10200,10201,10202'

    logger.info('开始爬取 %s, url: %s' % (source, url))
    response = requests.get(url, timeout=5)
    dom = html.fromstring(response.text)

    for metal, mapping in metal_mappings.items():
        line = dom.xpath('//td[position()=1][contains(.,"%s")]/ancestor::tr' % mapping['match'])[0].getchildren()
        date_string = '%s-%s' % (date.today().year, line[4].text)

        SpotStock.objects.update_or_create_all_envs(
            logger,
            varieties=metal,
            source=source,
            date=datetime.strptime(date_string, '%Y-%m-%d').date(),
            duration_unit='d',
            symbol=mapping['symbol'],
            defaults={
                'amount': line[1].text,
                'change': line[2].text,
            }
        )

