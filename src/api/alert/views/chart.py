#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
# from datetime import datetime
import datetime
import time
import math
import when

# from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from common.models import BackstageHTTPResponse, PageInfo
from common.views import BackstageBaseAPIView
# from common.utils import gen_page_info
from common.utils import log_exception
from alert.models import Alert
# from alert.serializers import AlertSerializer
# from workers.calculation.lib.vo import FormulaEnv, DBPreProcess
# from workers.calculation.lib import mathlib
# from workers.calculation.lib.mathlib import *
from ..view_lib import para_name_map, get_history_data
from ..models import MainContract, DayKline
from share.data import Ship



logger = logging.getLogger("use_info_ms")


def get_cross_star(varieties, past_day, limit=3, offset=0):
    """获取十字星数据"""
    m_con_objs = MainContract.objects.filter(varieties=varieties, settlement_date__gte=str(past_day)[:10]).order_by('-settlement_date').all()
    vals_len = len(m_con_objs)
    res = []
    data = []
    lmt = limit + 1
    if vals_len >= limit:
        m_con_objs = m_con_objs[offset:lmt]
    else:
        m_con_objs = m_con_objs[offset:]
    for obj in m_con_objs:
        daykline_obj_lst = DayKline.objects.filter(contract=obj.main_contract,
                                                date_time=obj.settlement_date).order_by('-date_time').all()
        # daykline_obj = DayKline.objects.filter(contract=obj.main_contract).order_by('-date_time')[0]
        daykline_obj = daykline_obj_lst and daykline_obj_lst[0] or None
        if not daykline_obj:
            continue
        price_open = daykline_obj.price_open
        price_high = daykline_obj.price_high
        price_low = daykline_obj.price_low
        pric_close = daykline_obj.price_close
        price_date = str(daykline_obj.date_time)[:10]
        dt = datetime.datetime.strptime(str(price_date)[:10] + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
        res.append([int(time.mktime(dt.timetuple())) * 1000, price_open, price_high, price_low, pric_close])
    # res.reverse()
    return res[1:]


class AlertHistoryChartView(BackstageBaseAPIView):


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
            - name: limit
              description: 数据条数
              paramType: query
              required: false

        """
        query_dict = request.query_params.dict().copy()
        alert_id = query_dict.get('alert_id', None)
        limit = int(query_dict.get('limit', 3))
        logger.info('查看预警历史数据, 预警id: %s, 查看数量: %s'%(alert_id, limit))
        leta = math.floor(limit / 30)
        if leta <1:
            leta = 1
        # now = datetime.datetime.strptime(str(datetime.datetime.now())[10] + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
        past_day = datetime.datetime.strptime(str(when.past(months=leta))[:10] + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
        today = datetime.datetime.today()
        if not alert_id:
            return BackstageHTTPResponse(
                                        code=BackstageHTTPResponse.API_HTTP_CODE_INVILID_PARAMS,
                                         message=u'预警id不存在').to_response()
        alert_obj = Alert.objects.get(pk=alert_id)
        variety = alert_obj.variety
        price = alert_obj.price
        # source = alert_obj.source
        # exchange = alert_obj.exchange
        contract = alert_obj.contract

        _y = []

        data, date_time = get_history_data(variety, 'CLOSE', limit=limit,
                                           contract=contract, start=past_day, end=today)
        y = list(zip(date_time, data))
        # for i in range(len(data)):
        #     if datetime.datetime.fromtimestamp(date_time[i]/1000) < past_day:
        #         break
        #     y.append([date_time[i], data[i]])
        new_vals = Ship(variety, price, start=None, end=None, limit=None, offset=None, desc=True)
        para_unit = new_vals.unit or ''
        y.reverse()
        res = {
            'y': y,
            'y_max': max(data),
            'y_min': min(data),
            'y_name': '主力合约',
            'y_unit': '元',
            '_y_name': para_name_map[price],
            '_y_unit': para_unit,
            'para_type': price,
            'date_end': str(datetime.datetime.now())[:10],
            'date_start': str(past_day)[:10],
        }

        if price == 'CROSS_STAR':
            para_vals = get_cross_star(variety, past_day, limit)
            res.update({
                '_y': para_vals,
                '_y_max': None,
                '_y_min': None,
            })
        else:
            para_data, para_date_time = get_history_data(variety, price, limit=limit, start=past_day, end=today)
            # for i in range(len(para_data)-1):
            #     # print(datetime.datetime.fromtimestamp(para_date_time[i] / 1000))
            #     if datetime.datetime.fromtimestamp(para_date_time[i] / 1000) < past_day:
            #         break
            #     _y.append([para_date_time[i], para_data[i]])
            _y = list(zip(para_date_time, para_data))

            _y.reverse()
            res.update({
                '_y': _y,
                '_y_max': max(para_data),
                '_y_min': min(para_data),
                   })


        logger.info('正常返回预警详细数据')
        return BackstageHTTPResponse(
                data=res,
                message=u'正常返回预警详细数据').to_response()



