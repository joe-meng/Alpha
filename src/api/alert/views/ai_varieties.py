#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from datetime import datetime

from django.db.models import QuerySet
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import connection

from common.models import BackstageHTTPResponse, PageInfo
from common.views import BackstageBaseAPIView
from common.utils import gen_page_info
from common.utils import log_exception
from ..models import AiVarieties, AttentionList, PredictionRecord
# from ..serializers import AlertSerializer
from ..view_lib import get_description, get_res, get_quotes, user_check


logger = logging.getLogger("use_info_ms")


class AiVarietiesView(BackstageBaseAPIView):

    @log_exception
    @user_check
    def get(self, request):
        u"""
        获取预测品类列表
        ---

        parameters:
            - name: exchange
              description: 交易所
              paramType: query
              required: false
            - name: date
              description: 日期
              paramType: query
              required: false
            - name: is_attention
              description: 是否查询关注(0:不按照关注查询,1:按照关注查询)
              paramType: query
              required: false

        """
        query_dict = request.query_params.dict().copy()
        # class_display = query_dict.pop('class_display', '0')
        date = query_dict.pop('date', str(datetime.now())[:10])
        exchange = query_dict.pop('exchange', None)
        is_attention = query_dict.pop('is_attention', '0')
        logger.info('获取预测品类列表, exchange: %s, date: %s, is_attention: %s'%(exchange, date, is_attention))
        user_id = request.user.id
        if not date:
            return BackstageHTTPResponse(
                                BackstageHTTPResponse.API_HTTP_CODE_INVILID_PARAMS,
                                message=u'时间必填').to_response()
        sql_para = ["q.date = '%s'"%date]
        if exchange and is_attention=='0':
            sql_para = sql_para+["v.exchange = '%s'"%exchange]
        where = ' and '.join(sql_para)
        res = []
        with connection.cursor() as cr:
            sql = """
                 select v.varieties, v.count_user, v.id as varieties_id, q.price, q.trend, q.change_price,
                        q.change_percent, q.ai_prediction
                 from alert_ai_varieties as v left join alert_quotes_record as q on v.id=q.varieties_id
                 where %s
                 order by v.id
            """%(where)
            cr.execute(sql)
            vals_lst = cr.fetchall()
            head = get_description(cr.description)
            res = get_res(head, vals_lst)
        new_res = []
        for vals in res:
            att_objs = AttentionList.objects.filter(user_id=user_id, varieties_id=vals['varieties_id']).first()
            if is_attention == '1':
                if not att_objs:
                    continue
            vals['attention'] = False
            if att_objs:
                vals['attention'] = True

            pre_objs = PredictionRecord.objects.filter(user_id=user_id, varieties_id=vals['varieties_id'], date=date).all()
            vals['partical'] = False
            if pre_objs:
                vals['partical'] = True
            if not vals['price']:
                quo = get_quotes(varieties=vals['varieties'], date=date)
                vals.update(quo)
            new_res.append(vals)

            logger.info('正常返回预测品类列表, exchange: %s, date: %s, is_attention: %s' % (exchange, date, is_attention))
        return BackstageHTTPResponse(
            data=new_res,
            message=u'正常返回所有数据').to_response()
