#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from django.db.models import QuerySet
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from common.models import BackstageHTTPResponse, PageInfo
from common.views import BackstageBaseAPIView
from common.utils import gen_page_info
from common.utils import log_exception
from user.models import User
from user.serializers import UserSerializer
from ..models import PredictionRecord, QuotesRecords
from ..serializers import PredictionRecordSerializer, QuotesRecordsSerializer
from ..view_lib import user_check


logger = logging.getLogger("use_info_ms")


class AiPredictionView(BackstageBaseAPIView):


    @log_exception
    # @user_check
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
        # user_id = request.user.id
        user_obj = User.objects.filter(username='ALPHA_AI').first()
        user_id = user_obj.id
        date = post_data.get('date', None)
        varieties_id = post_data.get('varieties_id', None)
        prediction = post_data.get('prediction', None)
        p_objs = PredictionRecord.objects.filter(date=date, varieties_id=varieties_id, user_id=user_id).all()
        if p_objs:
            logger.info('已经预测')
            res = PredictionRecordSerializer(p_objs[0]).data
            # res.update(get_predict_number(date))
            return BackstageHTTPResponse(
                data=res,
                message=u'已经预测').to_response()
        else:
            quo_obj = QuotesRecords.objects.filter(varieties_id=varieties_id, date=date).first()
            quo_obj.ai_prediction = True
            quo_obj.save()
            obj = PredictionRecord(date=date, varieties_id=varieties_id, user_id=user_id, prediction=prediction)
            obj.save()
            res = PredictionRecordSerializer(obj).data
            logger.info('提交预测成功')
            # res.update(get_predict_number(date))
            return BackstageHTTPResponse(
                data=res,
                message=u'提交预测成功').to_response()

