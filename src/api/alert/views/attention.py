#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from django.db.models import QuerySet
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


from common.models import BackstageHTTPResponse, PageInfo
from common.views import BackstageBaseAPIView
from common.utils import gen_page_info
from common.utils import log_exception
from ..models import AttentionList, AiVarieties
from ..serializers import AttentionListSerializer
from ..view_lib import user_check


logger = logging.getLogger("use_info_ms")


class AttendtionView(BackstageBaseAPIView):

    @log_exception
    @user_check
    def post(self, request):
        u"""
        关注或者取消关注
        ---

        parameters:
            - name: type
              description: 类型(0:关注, 1:取消关注)
              paramType: form
              required: True
            - name: varieties_id
              description: 品类id
              paramType: form
              required: True

        """
        post_data = self.request_data(request)
        tp = post_data.get('type', None)
        varieties_id = post_data.get('varieties_id', None)
        logger.info('添加或者取消关注, type: %s, varieties_id: %s,(0:关注, 1:取消关注)' %(tp, varieties_id))
        user_id = request.user.id
        att_objs = AttentionList.objects.filter(user_id=user_id, varieties_id=varieties_id).all()
        len_att = len(att_objs)
        if tp == '0':
            if len_att == 0:
                new_att = AttentionList(user_id=user_id, varieties_id=varieties_id)
                new_att.save()
            elif len_att > 1:
                for i in range(len_att-1):
                    att_objs[i].delete()
        elif tp == '1':
            for i in range(len_att):
                att_objs[i].delete()
        else:
            # return BackstageHTTPResponse(
            #     message=u'正常返回所有数据').to_response()
            return

        logger.info('成功添加或者取消关注')
        return BackstageHTTPResponse(
            message=u'成功添加或者取消关注').to_response()

