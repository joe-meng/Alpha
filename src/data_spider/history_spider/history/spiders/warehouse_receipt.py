# -- coding: utf-8 --
from datetime import date, timedelta, datetime

import json
import pandas
import re

from django.db import transaction
from scrapy import Spider, Request

from spot.models import SpotWarehouseReceipt

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


def strip_eng(string):
    return re.findall(r'(.*)\$\$.*', string)[0]


class WarehouseReceiptSpider(Spider):
    name = 'warehouse'
    handle_httpstatus_list = [404]
    custom_settings = {
        'START_DATE': date(2017, 7, 1),
        'END_DATE': date.today(),
    }

    def start_requests(self):
        self.current_date = self.settings['START_DATE']
        while self.current_date <= self.settings['END_DATE']:
            # 只爬未爬过的数据
            if SpotWarehouseReceipt.objects.filter(date=self.current_date, source='shfe'):
                self.logger.info(('%s 识别为已爬取' % self.current_date).center(80, '*'))
                self.current_date = self.current_date + timedelta(days=1)
            else:
                today_string = date.strftime(self.current_date, '%Y%m%d')
                url = 'http://www.shfe.com.cn/data/dailydata/%sdailystock.html' % today_string
                yield Request(url, callback=self.parse_html)
                self.current_date = self.current_date + timedelta(days=1)

    def parse_html(self, response):
        if response.status == 404:
            url = response.url[:-4] + 'dat'
            yield Request(url, callback=self.parse_json)
            return
        else:
            df = pandas.read_html(response.text)[0]

            try:
                df = df.dropna(how='all')[2:-1]  # 取表正文内容
                df.loc[df[3].isnull()] = df[df[3].isnull()].shift(axis=1)  # 平移错列
                df = df[
                    ~df[0].isnull() & ~df[0].str.contains('地区').fillna(True) |
                    df[1].str.contains('计') |
                    df[1].str.contains('交割金库')
                ].reset_index()  # 过滤表内容、重新 index
                df[1] = df[1].apply(
                    lambda x: str(x).replace(' ', '')
                ).apply(
                    lambda x: str(x).replace('交割金库', '上期所指定交割金库')
                )  # 修正表内容
                df_合计 = df[df[1] == '合计'][[1, 2, 3]]  # 找出合计行
                df.update(df_合计.set_index(df_合计.index.values - 1))  # 把合计行上移到地区行
                df = df[~(df[0].isnull() & (df[1] == '合计'))][[0, 1, 2, 3]]  # 去除仓库明细，只留合计
            except Exception as e:
                self.logger.error(('%s pandas 解析失败' % response.url).center(80, '*'))

            variety = None
            receipt_list = []
            date = datetime.strptime(re.findall(r'\d+', response.url)[0], '%Y%m%d').date()
            for row in df.values:
                if row[0] in METAL_TYPES:
                    variety = row[0]
                    continue

                varieties = METAL_MAPPINGS.get(variety, variety)
                area = row[1] if (pandas.isnull(row[0]) or row[0]=='nan') else row[0]
                warehouse_receipt = SpotWarehouseReceipt(
                    varieties=varieties,
                    area=area,
                    date=date,
                    source='shfe',
                    duration_unit='d',
                    amount=row[2],
                    change=row[3],
                    symbol=mappings.get(varieties, {}).get(area, None),
                )
                receipt_list.append(warehouse_receipt)

            try:
                with transaction.atomic():
                    SpotWarehouseReceipt.objects.bulk_create(receipt_list)
                    self.logger.info(('%s 插入成功' % date).center(80, '*'))
            except Exception as e:
                self.logger.error(('%s 插入失败 %s %s' % (date, e, response.url)).center(80, '*'))

    def parse_json(self, response):
        if response.status == 200:
            json_response = json.loads(response.text)['o_cursor']

            receipt_list = []
            date = datetime.strptime(re.findall(r'\d+', response.url)[0], '%Y%m%d').date()
            for row in filter(lambda i: '计' in i.get('WHABBRNAME', ''), json_response):
                variety = strip_eng(row['VARNAME'])
                area = strip_eng(row['REGNAME'] or row['WHABBRNAME'])
                varieties = METAL_MAPPINGS.get(variety, variety)
                warehouse_receipt = SpotWarehouseReceipt(
                    varieties=varieties,
                    area=area,
                    date=date,
                    source='shfe',
                    duration_unit='d',
                    amount=row['WRTWGHTS'],
                    change=row['WRTCHANGE'],
                    symbol=mappings.get(varieties, {}).get(area, None),
                )
                receipt_list.append(warehouse_receipt)

            try:
                if receipt_list:
                    with transaction.atomic():
                        SpotWarehouseReceipt.objects.bulk_create(receipt_list)
                        self.logger.info(('%s 插入成功' % date).center(80, '*'))
            except Exception as e:
                self.logger.error(('%s 插入失败 %s %s' % (date, e, response.url)).center(80, '*'))
