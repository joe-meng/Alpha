#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@date: 2016-06-13

@author: Devin
"""
import logging


from django.contrib.auth import authenticate,login,logout
# from django.contrib import auth

from common.models import BackstageHTTPResponse, PageInfo
from common.views import BackstageBaseAPIView
from common.utils import gen_like_filter_mongo
from common.utils import gen_page_info_mongo
from common.utils import get_mongo_id
from common.utils import log_exception
from backstage.serializers import MSUserSerializer


logger = logging.getLogger("use_info_ms")


class LoginView(BackstageBaseAPIView):

    @log_exception
    def post(self, request):
        u"""
        登录
        ---

        parameters:
            - name: username
              description: 用户名
              type: string
              paramType: form
              required: true
            - name: password
              description: 密码
              type: string
              paramType: form
              required: true
        :param request:
        :return:
        """
        post_data = self.request_data(request)
        username = post_data.get('username', '')
        password = post_data.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            # return render_to_response('index.html', RequestContext(request))
            logger.info('登录成功')
            serializer = MSUserSerializer(user)
            return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
                                        data=serializer.data).to_response()
        else:
            logger.info('用户名或密码错误')
            return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_LOGIN_ERR,
                                         message=u'用户名或密码错误').to_response()

