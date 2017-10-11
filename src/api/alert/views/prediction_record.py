#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from django.db.models import QuerySet
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import connection

from common.models import BackstageHTTPResponse, PageInfo
from common.views import BackstageBaseAPIView
# from common.utils import gen_page_info
from common.utils import log_exception
from ..models import PredictionRecord, AiVarieties, QuotesRecords
from ..serializers import PredictionRecordSerializer, QuotesRecordsSerializer
from ..view_lib import user_check, get_quotes
from user.models import User


logger = logging.getLogger("use_info_ms")


class PredictionRecordViewList(BackstageBaseAPIView):

    @log_exception
    @user_check
    def get(self, request):
        u"""
        获取当前和历史的预测数据
        ---

        parameters:
            - name: user_id
              description: 用户id
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
        res = []
        query_dict = request.query_params.dict().copy()
        # date = query_dict.get('date', None)
        user_id = query_dict.get('user_id', None)
        # user_id = request.user.id
        index = query_dict.get('index', 1)
        # descent = query_dict.get('descent', None)
        number = query_dict.get('number', 10)
        offset = (int(index) - 1) * number
        if request.user.id != user_id:
            user_obj = User.objects.get(pk=user_id)
            user_obj.visit_time = user_obj.visit_time + 1
            user_obj.save()

        with connection.cursor() as cr:
            sql = """
                select date
                from alert_prediction_record
                where user_id = '%s'
                group by date
                order by date desc
                limit %s
                offset %s
            """ % (user_id, number, offset)
            cr.execute(sql)
            vals_lst = cr.fetchall()

            if vals_lst:
                end = str(vals_lst[0][0])
                start = str(vals_lst[-1][0])
                predict_objs = PredictionRecord.objects.filter(date__lte=end, date__gte=start, user_id=user_id).all()
                serializer = PredictionRecordSerializer(predict_objs, many=True)
                res = serializer.data
                for vals in res:
                    ai_obj = AiVarieties.objects.get(pk=vals['varieties_id'])
                    vals['varieties_name'] = ai_obj.varieties
                    if vals['is_true'] == 'n':
                        quo_vals = get_quotes(ai_obj.varieties, vals['date'])
                        vals.update(quo_vals)
                    else:
                        quo_obj = QuotesRecords.objects.filter(varieties_id=vals['varieties_id'], date=vals['date']).first()
                        quo_vals = QuotesRecordsSerializer(quo_obj).data
                        vals.update(quo_vals)

        logger.info('正常返回分页:%s:' % (index))
        return BackstageHTTPResponse(
                                     data=res,
                                     message=u'正常返回分页').to_response()

    @log_exception
    @user_check
    def post(self, request):
        u"""
        提交预测
        ---

        parameters:
            - name: date
              description: 时间
              paramType: form
              required: true
            - name: varieties_id
              description: 品类
              paramType: form
              required: true
            - name: prediction
              description: 预测涨跌(up:涨,down:跌,c:不变)
              paramType: form
              required: true
        """
        post_data = self.request_data(request)
        user_id = request.user.id
        date = post_data.get('date', None)
        varieties_id = post_data.get('varieties_id', None)
        prediction = post_data.get('prediction', None)
        p_objs = PredictionRecord.objects.filter(date=date, varieties_id=varieties_id, user_id=user_id).all()
        if p_objs:
            logger.info('已经预测')
            res = PredictionRecordSerializer(p_objs[0]).data
            res.update(get_predict_number(date))
            return BackstageHTTPResponse(
                data=res,
                message=u'已经预测').to_response()
        else:
            obj = PredictionRecord(date=date, varieties_id=varieties_id, user_id=user_id, prediction=prediction)
            obj.save()
            res = PredictionRecordSerializer(obj).data
            logger.info('提交预测成功')
            res.update(get_predict_number(date))
            return BackstageHTTPResponse(
                data=res,
                message=u'提交预测成功').to_response()

    @log_exception
    @user_check
    def put(self, request):
        u"""
        清空历史
        ---
        parameters:

        """
        user_id = request.user.id
        objs = PredictionRecord.objects.filter(if_visible=True, user_id=user_id).all()
        for obj in objs:
            obj.if_visible = False
            obj.save()
        logger.info('成功删除历史')
        return BackstageHTTPResponse(
            message=u'成功删除历史').to_response()


class PredictionRecordView(BackstageBaseAPIView):

    @log_exception
    @user_check
    def get(self, request):
        u"""
        获取当前用户的预测数据
        ---

        parameters:


        """
        res = {'up': 0.0, 'down': 0.0}
        query_dict = request.query_params.dict().copy()
        # date = query_dict.get('date', None)
        user_id = request.user.id
        predict = PredictionRecord.objects.order_by('-date').first()
        date = predict.date
        res['date'] = date
        # if not date:
        #     return BackstageHTTPResponse(
        #                         BackstageHTTPResponse.API_HTTP_CODE_INVILID_PARAMS,
        #                         message=u'时间必填').to_response()

        pre_obj =PredictionRecord.objects.filter(date=date, user_id=user_id).first()
        if pre_obj:
            res.update(PredictionRecordSerializer(pre_obj).data)
        with connection.cursor() as cr:
            sql = """
                select count(*), prediction
                from alert_prediction_record
                where date = '%s'
                group by prediction
            """ % date
            cr.execute(sql)
            vals_lst = cr.fetchall()
            for vals in vals_lst:
                if vals[1] == 'up':
                    res['up'] = vals[0]
                elif vals[1] == 'down':
                    res['down'] = vals[0]
        logger.info('返回用户的预测信息')
        return BackstageHTTPResponse(
                                     data=res,
                                     message=u'返回用户的预测信息').to_response()


def get_predict_number(date):
    """获取当然猜涨猜跌的人数"""
    res ={}
    with connection.cursor() as cr:
        sql = """
            select count(*), prediction
            from alert_prediction_record
            where date = '%s'
            group by prediction
        """ % date
        cr.execute(sql)
        vals_lst = cr.fetchall()
        for vals in vals_lst:
            if vals[1] == 'up':
                res['up'] = vals[0]
            elif vals[1] == 'down':
                res['down'] = vals[0]
    return res