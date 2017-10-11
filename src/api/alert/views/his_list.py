#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from math import ceil
import datetime

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from common.models import BackstageHTTPResponse, PageInfo
from common.views import BackstageBaseAPIView
from common.utils import gen_page_info
from common.utils import log_exception
from alert.models import Alert
from alert.serializers import AlertSerializer
from ..view_lib import get_history_data
from ..view_lib import para_name_map, varieties_name_map
from ..models import MainContract
from workers.calculation.lib.mathlib.mathfun import data_gap
from share.data import Ship


logger = logging.getLogger("use_info_ms")


class AlertHistoryTitleView(BackstageBaseAPIView):


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
        # limit = int(query_dict.get('limit', 3))
        index_number = int(query_dict.get('number', 10))
        # index_number = 10
        index = int(query_dict.get('index', 1))
        limit = (index_number*index)
        offset = (index-1)*index_number
        logger.info('查看预警历史数据, 预警id: %s, 查看数量: %s' % (alert_id, limit))
        if offset < 0:
            return BackstageHTTPResponse(
                code=BackstageHTTPResponse.API_HTTP_CODE_INVILID_PARAMS,
                message='分页页数错误, 分页不能小于1').to_response()
        if not alert_id:
            return BackstageHTTPResponse(
                                        code=BackstageHTTPResponse.API_HTTP_CODE_INVILID_PARAMS,
                                         message=u'预警id不存在').to_response()

        alert_obj = Alert.objects.get(pk=alert_id)
        variety = alert_obj.variety
        price = alert_obj.price
        contract = alert_obj.contract
        # source = alert_obj.source
        # exchange = alert_obj.exchange
        m_con_objs = MainContract.objects.filter(varieties=variety).order_by('-settlement_date').all()
        vals_len = len(m_con_objs)
        if vals_len <= offset:
            return BackstageHTTPResponse(
                code=BackstageHTTPResponse.API_HTTP_CODE_INVILID_PARAMS,
                message='分页页数错误, 分页超过最大值').to_response()
        head_vals = {'para_name': para_name_map.get(price), #'para_unit': para_unit_map.get(price),
                                 'varieties': varieties_name_map.get(variety), 'contract_unit': '元',
                                 'explan': '', 'para_type': price}
        body = []

        number, date_list = get_history_data(variety, 'CLOSE',
                                                           limit=limit, offset=offset, contract=contract)
        m_d1, m_d2, m_gd, m_rate = data_gap(number)
        # datetime.datetime.utcfromtimestamp(timeStamp)
        start = datetime.datetime.fromtimestamp(date_list[-1]/1000)
        end = datetime.datetime.fromtimestamp(date_list[0]/1000)
        para_number, para_date_list = get_history_data(variety, price, limit=limit,
                                                                 offset=offset, start=start, end=end)
        data = Ship(variety, price, start=None, end=None, limit=None, offset=None, desc=True)
        para_unit = data.unit or ''
        p_d1, p_d2, p_gd, p_rate = [], [], [], []
        if para_number:
            p_d1, p_d2, p_gd, p_rate = data_gap(para_number)

        head_vals['para_unit'] = para_unit
        m_gd = list(m_gd)[1:] + [0]
        m_rate = list(m_rate)[1:] + [0]
        p_gd = list(p_gd)[1:]+[0]
        p_rate = list(p_rate)[1:]+[0]

        len_main = len(number)
        if len_main > index_number:
            len_main = len_main-1
        for i in range(len_main):
            # main_date = str(date_list[i])[:10]
            main_date = str(datetime.datetime.fromtimestamp(date_list[i]/1000))
            vals = {'date': main_date, 'contract_price': number[i]}
            vals['contract_chage_number'] = round(abs(m_gd[i]), 4)
            vals['contract_change'] = round(abs(m_rate[i]), 4)
            if m_gd[i] > 0:
                vals['contract_trend'] = 'down'
            elif m_gd[i] == 0:
                vals['contract_trend'] = 'constant'
            else:
                vals['contract_trend'] = 'up'

            vals['para_type'] = price
            len_para = len(para_number)
            if len_para > index_number:
                len_para = len_para-1

            vals['if_para'] = False
            vals['para_chage_number'] = 0.0
            vals['para_change'] = 0.0
            vals['para_number'] = 0.0
            vals['para_trend'] = 0.0

            for para_i in range(len_para):
                if para_date_list[para_i] == date_list[i]:
                    vals['if_para'] = True
                    vals['para_chage_number'] = round(abs(p_gd[para_i]), 4)
                    if str(p_rate[para_i]) == 'nan':
                        vals['para_change'] = 0
                    else:
                        vals['para_change'] = round(abs(p_rate[para_i]), 4)
                    if str(price).lower() == 'pd':
                        vals['para_number'] = abs(round(para_number[para_i], 4))
                    else:
                        vals['para_number'] = round(para_number[para_i], 4)
                    if p_gd[para_i] > 0:
                        vals['para_trend'] = 'down'
                    elif p_gd[para_i] == 0:
                        vals['para_trend'] = 'constant'
                    else:
                        vals['para_trend'] = 'up'
                    if para_number[para_i] > 0:
                        vals['attr'] = True
                    else:
                        vals['attr'] = False
                    break
                # else:

            body.append(vals)

        res ={'head': head_vals, 'body': body}
        serializer = AlertSerializer(alert_obj)
        res['alert'] = serializer.data
        logger.info('正常返回预警详细数据')
        return BackstageHTTPResponse(
                data=res,
                message=u'正常返回预警详细数据',
                pageinfo=PageInfo(index, index_number,
                              ceil(float(vals_len)/index_number),
                              vals_len,
                              '')).to_response()


