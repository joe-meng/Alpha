# -- coding: utf-8 --
from datetime import date, timedelta, datetime

import json
import re

from django.db import transaction
from scrapy import Spider, Request

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
    '沥青(仓库)': 'Bu_warehouse',
    '沥青仓库': 'Bu_warehouse',
    '沥青(厂库)': 'Bu_factory',
    '沥青厂库': 'Bu_factory',
    '沥青': 'Bu',
    '热轧卷板': 'Hc',
}

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


class StockSpider(Spider):
    name = 'stock'
    handle_httpstatus_list = [404]
    custom_settings = {
        'START_DATE': date(2017, 5, 23),
        'END_DATE': date.today(),
    }

    def start_requests(self):
        self.current_date = self.settings['START_DATE']
        while self.current_date <= self.settings['END_DATE']:
            # 只爬未爬过的数据
            if SpotStock.objects.filter(date=self.current_date, source='shfe'):
                self.logger.info(('%s 识别为已爬取' % self.current_date).center(80, '*'))
                self.current_date = self.current_date + timedelta(days=1)
            else:
                today_string = date.strftime(self.current_date, '%Y%m%d')
                url = 'http://www.shfe.com.cn/data/dailydata/%sweeklystock.dat' % today_string
                yield Request(url, callback=self.parse_json)
                self.current_date = self.current_date + timedelta(days=1)

    def parse_json(self, response):
        if response.status == 200:
            json_response = json.loads(response.text)['o_cursor']

            stock_list = []
            date = datetime.strptime(re.findall(r'\d+', response.url)[0], '%Y%m%d').date()
            for row in filter(lambda i: '计' in i.get('WHABBRNAME', ''), json_response):
                varieties_cn = strip_eng(row['VARNAME'])
                varieties = METAL_MAPPINGS.get(varieties_cn, varieties_cn)
                area = strip_eng(row['REGNAME'] or row['WHABBRNAME'])
                stock = SpotStock(
                    varieties=varieties,
                    area=area,
                    date=date,
                    source='shfe',
                    duration_unit='w',
                    amount=row['SPOTWGHTS'] or None,
                    change=row['SPOTCHANGE'] or None,
                    symbol=mappings.get(varieties, {}).get(area, None),
                )
                stock_list.append(stock)

            try:
                if stock_list:
                    with transaction.atomic():
                        SpotStock.objects.bulk_create(stock_list)
                        self.logger.info(('%s 插入成功' % date).center(80, '*'))
            except Exception as e:
                self.logger.error(('%s 插入失败 %s %s' % (date, e, response.url)).center(80, '*'))
