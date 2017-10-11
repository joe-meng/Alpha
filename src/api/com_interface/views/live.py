#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@date: 2016-06-13

@author: Devin
"""
import logging
import json


from common.models import BackstageHTTPResponse, PageInfo
from common.views import BackstageBaseAPIView
from backstage.views import live
from common.utils import gen_like_filter_mongo
from common.utils import gen_page_info_mongo
from common.utils import get_mongo_id
from common.utils import log_exception


logger = logging.getLogger("use_info_ms")


class LiveViewList(BackstageBaseAPIView):

    @log_exception
    def get(self, request):
        u"""
        获取所有的文章
        ---


        parameters:
            - name: machine_class
              description: 品目
              type: string
              paramType: query
              required: false
            - name: look_state
              description: 查看状态
              type: string
              paramType: query
              required: false
            - name: pub_state
              description: 发布状态
              type: string
              paramType: query
              required: false
            - name: push_state
              description: 推送状态
              type: string
              paramType: query
              required: false
            - name: pub_time
              description: 发布时间
              type: string
              paramType: query
              required: false
            - name: content_text
              description: 全文
              type: string
              paramType: query
              required: false
            - name: manual_tags
              description: 标签
              type: string
              paramType: query
              required: false
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
        :param request:
        :return:
        """
        return live.LiveViewList().get(request)


class LiveView(BackstageBaseAPIView):

    @log_exception
    def get(self, request, pk):
        """
        通过主键获取新闻数据
        ---

        parameters:
            - name: pk
              description: 数据id
              type: string
              paramType: path
              required: true
        responseMessages:
            - code: 401
              message: Not authenticated
            - code: 403
              message: Insufficient rights to call this procedure
        """

        return live.LiveView.get(request, pk)

