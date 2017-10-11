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
from ..models import PredictionRecord
from ..serializers import PredictionRecordSerializer
from ..view_lib import user_check


logger = logging.getLogger("use_info_ms")


class ViewResView(BackstageBaseAPIView):

    @log_exception
    @user_check
    def get(self, request):
        u"""
        查看用户的预测结果
        ---
        parameters:
            - name: user_id
              description: 用户id
              paramType: query
              required: true
            - name: date
              description: 日期
              paramType: query
              required: true
            - name: varieties_id
              description: 品类id
              paramType: query
              required: true
        """
        query_dict = request.query_params.dict().copy()
        date = query_dict.get('date')
        varieties_id = query_dict.get('varieties_id')
        user_id = query_dict.get('user_id')
        pre_obj = PredictionRecord.objects.filter(user_id=user_id, varieties_id=varieties_id, date=date).first()
        if pre_obj:
            pre_obj.visit_number = pre_obj.visit_number + 1
            pre_obj.save()
        serializer = PredictionRecordSerializer(pre_obj)
        res = serializer.data
        logger.info('正常返回所有数据')
        return BackstageHTTPResponse(
            data=res,
            message=u'正常返回所有数据').to_response()

