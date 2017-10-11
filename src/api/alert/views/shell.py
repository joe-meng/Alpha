#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from math import ceil

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from common.models import BackstageHTTPResponse, PageInfo
from common.views import BackstageBaseAPIView
from common.utils import gen_page_info
from common.utils import log_exception
from alert.models import Alert
from alert.serializers import AlertSerializer
from ..view_lib import get_main_contract, get_history_data
from ..view_lib import para_name_map, varieties_name_map
from ..models import MainContract, DayKline


logger = logging.getLogger("use_info_ms")


class shellView(BackstageBaseAPIView):


    @log_exception
    def get(self, request):
        u"""
        获取预警提示,主力合约,预警类别信息
        ---

        parameters:
            - name: alert_id
              description: 预警的id
              paramType: query
              required: true
            - name: index
              description: 分页显示第几页
              paramType: query
              required: false
            - name: number
              description: 每页显示几条数据
              paramType: query
              required: false

        """
        query_dict = request.query_params.dict().copy()
        alert_id = query_dict.get('alert_id', None)

        obj = DayKline.objects.filter(date_time, )

        return BackstageHTTPResponse(
                data=res,
                message=u'正常返回预警详细数据',).to_response()

import datetime
import requests
# from ..models import MainContract, DayKline


cu_contract = [
    # 'cu1601',
    # 'cu1602',
    # 'cu1603',
    # 'cu1604',
    # 'cu1605',
    # 'cu1606',
    # 'cu1607',
    # 'cu1608',
    # 'cu1609',
    # 'cu1610',
    # 'cu1611',
    # 'cu1612',
    # 'cu1701',
    # 'cu1702',
    # 'cu1703',
    # 'cu1704',
    # 'cu1705',
    'cu1706',
    'cu1707',
    'cu1708',
    'cu1709',
    'cu1710',
    'cu1711',
    'cu1712',
    'cu1801',
    'cu1802',
    'cu1803',
    'cu1804',
    'cu1805',
    'cu1806',
]

zn_contract = [
    # 'zn1601',
    # 'zn1602',
    # 'zn1603',
    # 'zn1604',
    # 'zn1605',
    # 'zn1606',
    # 'zn1607',
    # 'zn1608',
    # 'zn1609',
    # 'zn1610',
    # 'zn1611',
    # 'zn1612',
    # 'zn1701',
    # 'zn1702',
    # 'zn1703',
    # 'zn1704',
    # 'zn1705',
    # 'zn1706',
    'zn1707',
    'zn1708',
    'zn1709',
    'zn1710',
    'zn1711',
    'zn1712',
    'zn1801',
    'zn1802',
    'zn1803',
    'zn1804',
    'zn1805',
    'zn1806',
]


def add_shfe_day_k_line():
    """补充day_k_line的数据"""
    url = "http://stock2.finance.sina.com.cn/futures/api/jsonp.php/var%20_CU17072017_7_26=/InnerFuturesNewService.getDailyKLine?symbol=CU1707&_=2017_7_26"

    today = str(datetime.datetime.now().date()).replace('-', '_')
    for contract in cu_contract:
        # url = "http://stock2.finance.sina.com.cn/futures/api/jsonp.php/var%20_CU17072017_7_26=/InnerFuturesNewService.getDailyKLine?symbol=CU1707&_=2017_7_26"
        new_url = url.replace('2017_07_26', today).replace('CU1707', contract.upper())
        r = requests.get(new_url)
        # d = 'date_time'
        # o = 'open'
        # h = 'high'
        # l ='low'
        # c = 'close'
        # v = 'v'
        data = r.content
        str_vals_lst = data.decode().split('=')[1].strip().replace(';', '').replace('([', '').split('}')[:-1]
        res = []
        for vals in str_vals_lst:
            day_vals = {}
            new_vals = vals.replace(',{', '').replace('{', '').replace('"', '').strip().split(',')
            for i in new_vals:
                new_data = i.strip().split(':')
                # try:
                k = new_data[0]
                v = new_data[1]
                # except Exception as e:
                #     print(i, new_data)
                day_vals[k] = v
            # res.append(day_vals)
        # eval('vals = '+str_vals)
            date_time = day_vals['d']+ ' 00:00:00'
            objs = DayKline.objects.filter(contract=contract, date_time=date_time).all()
            if objs:
                obj = obj[0]
                obj.price_open = day_vals['o']
                obj.price_close = day_vals['c']
                obj.price_high = day_vals['h']
                obj.price_low = day_vals['l']
                obj.volumn = day_vals['v']
            else:
                d_k_l_vals = {
                    'contract': contract,
                    'date_time': date_time,
                    'price_open': day_vals['o'],
                    'price_close': day_vals['c'],
                    'price_high': day_vals['h'],
                    'price_lo': day_vals['l'],
                    'exchange': 'SHFE',
                    'volumn': day_vals['v'],
                    'settlement_price': day_vals['c'],
                    'pre_settlement_price': day_vals['c'],
                        }
        print(res)
        # print(r.content)


if __name__ == '__main__':
    add_shfe_day_k_line()