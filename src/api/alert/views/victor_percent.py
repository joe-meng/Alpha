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
# from ..models import PredictionRecord
# from ..serializers import PredictionRecordSerializer
from ..view_lib import user_check


logger = logging.getLogger("use_info_ms")


class VictorPercentView(BackstageBaseAPIView):

    @log_exception
    @user_check
    def get(self, request):
        u"""
        获取用户胜率信息
        ---
        parameters:

        """

        user_id = request.user.id
        pre_obj = User.objects.get(pk=user_id)
        serializer = UserSerializer(pre_obj)
        res = serializer.data
        logger.info('正常返回所有数据')
        return BackstageHTTPResponse(
            data=res,
            message=u'正常返回所有数据').to_response()


class VictorPercentViewList(BackstageBaseAPIView):

    @log_exception
    @user_check
    def get(self, request):
        u"""
        获取用户列表
        ---

        parameters:
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
            - name: is_page
              description: 是否需要分页，default=1 ('0', '不需要分页')，('1', '需要分页')
              paramType: query
              required: false

        """
        query_dict = request.query_params.dict().copy()
        index, number, sort_tuple, descent = gen_page_info(query_dict)
        is_page = query_dict.pop('is_page', '1')

        user_objs = User.objects.order_by(*sort_tuple).all()

        if is_page == '1':

            paginator = Paginator(user_objs, number)

            try:
                pg = paginator.page(index)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                index = 1
                pg = paginator.page(index)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                index = paginator.num_pages
                pg = paginator.page(index)
            serializer = UserSerializer(pg, many=True)
            res = serializer.data
            logger.info('正常返回分页:%s:' % (index))
            return BackstageHTTPResponse(
                data=res,
                message=u'正常返回分页').to_response()

        else:
            serializer = UserSerializer(user_objs, many=True)
            res = serializer.data
            logger.info('正常返回所有数据')
            return BackstageHTTPResponse(
                data=res,
                message=u'正常返回所有数据').to_response()