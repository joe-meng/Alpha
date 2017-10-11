#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from django.db.models import QuerySet
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import connection

from common.models import BackstageHTTPResponse, PageInfo
from common.views import BackstageBaseAPIView
from common.utils import gen_page_info
from common.utils import log_exception
from ..models import PredictionRecord
# from ..serializers import AlertSerializer
from ..view_lib import get_description, get_res, user_check
from user.models import User
from user.serializers import UserSerializer


logger = logging.getLogger("use_info_ms")


class PredictionView(BackstageBaseAPIView):

    @log_exception
    @user_check
    def get(self, request):
        u"""
        获取用户列表
        ---

        parameters:
            - name: varieties_id
              description: 品类
              paramType: query
              required: True
            - name: date
              description: 日期
              paramType: query
              required: True
            - name: index
              description: 分页显示第几页
              paramType: query
              required: false
            - name: number
              description: 每页显示几条数据
              paramType: query
              required: false
            - name: descent
              description: 需要倒序的字段,用逗号分开,默认通过ID 正序
              paramType: query
              required: false

        """
        query_dict = request.query_params.dict().copy()
        date = query_dict.get('date', None)
        varieties_id = query_dict.get('varieties_id', '')
        user_id = request.user.id
        index = query_dict.get('index', 1)
        descent = query_dict.get('descent', None)
        number = query_dict.get('number', 10)
        # is_page = query_dict.get('is_page', '1')
        offset = (int(index) - 1) * int(number)
        order_by = 'u.id'
        ai_vals = get_ai_prediction(date, varieties_id)
        me_vals = get_user_prediction(user_id, date, varieties_id)
        res = []
        if ai_vals:
            res.append(ai_vals)
        if me_vals:
            res.append(me_vals)
        if descent:
            order_by = ''
            for i in descent.split(','):
                order_by = order_by + ', %s desc'%i
        with connection.cursor() as cr:
            sql = """
                select u.username, u.id as user_id, u.visit_time, u.victor_number, u.fail_number, u.win_percent,
                    p.prediction, u.head_img, p.date
                from user as u left join alert_prediction_record as p on u.id=p.user_id
                where p.date = '%s' and p.varieties_id = %s and u.id != '%s'
                order by %s
                limit %s
                offset %s
            """ % (date, varieties_id, user_id, order_by, number, offset)
            cr.execute(sql)
            vals_lst = cr.fetchall()
            head = get_description(cr.description)
            vals = get_res(head, vals_lst) or []
            res = res + vals

        for key in res:
            if key:
                key['recent_predict'] = get_recent_prediction(date, key['user_id'], 4)
                obj = User.objects.get(pk=key['user_id'])
                user_vals = UserSerializer(obj).data
                key.update(user_vals)
            if key.get('visible', None) == None:
                key['visible'] = False

        logger.info('正常返回分页:%s:' % (index))
        return BackstageHTTPResponse(
                                     data=res,
                                     message=u'正常返回分页').to_response()


def get_user_prediction(user_id, date, varieties_id):
    """获取单个用户的预测信息"""
    res = {'visible': True, 'user_id': user_id, 'date': date, 'varieties_id': varieties_id}
    with connection.cursor() as cr:
        sql = """
            select u.username, u.id as user_id, u.visit_time, u.victor_number, u.fail_number, u.win_percent,
                    p.prediction
            from user as u left join alert_prediction_record as p on u.id=p.user_id
            where u.id = %s and p.date = %s and p.varieties_id = '%s'
        """ % (user_id, date, varieties_id)
        cr.execute(sql)
        vals_lst = cr.fetchall()
        if vals_lst:
            head = get_description(cr.description)
            res = get_res(head, vals_lst)

    return res


def get_ai_prediction(date, varieties_id):
    """获取AI用户的预测信息"""

    with connection.cursor() as cr:
        sql = """
            select u.username, u.id as user_id, u.visit_time, u.victor_number, u.fail_number, u.win_percent,
                    p.prediction
            from user as u left join alert_prediction_record as p on u.id=p.user_id
            where u.username = 'ALPHA_AI' and p.date = '%s' and p.varieties_id = '%s'
        """ % (date, varieties_id)
        cr.execute(sql)
        vals_lst = cr.fetchall()
        head = get_description(cr.description)
        res = get_res(head, vals_lst) or {}
        if res:
            res['visible'] = True
    return res

def get_recent_prediction(date, user_id, limit):
    """获取最近的预测结果"""
    res = []
    predict_objs = PredictionRecord.objects.filter(date__lt=date, user_id=user_id).all()[:limit]
    for obj in predict_objs:
        res.append({'prediction':obj.prediction,
                    'is_true': obj.is_true})
    return res