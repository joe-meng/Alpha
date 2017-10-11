# -*- coding: utf-8 -*-
# from djangoMiddleware.settings import EXCLUDE_URL
from django.shortcuts import HttpResponseRedirect
import re

# exclued_path = [re.compile(item) for item in EXCLUDE_URL]
from common.models import BackstageHTTPResponse
from django.utils.deprecation import MiddlewareMixin


class PubAuthMiddleWare(MiddlewareMixin):

    def process_request(self, request):
        url_path = request.path
        path_list = url_path.split('/')

        if re.match('/api/1/', url_path):
            if re.match('/api/1/login/', url_path):
                return
            if not request.user.is_authenticated():
                return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_NOT_LOGIN_ERR,
                                        message=u'您无权限访问此api, 请先登录',).to_response()
        else:
            return


class DisableCSRFCheckMiddleWare(MiddlewareMixin):

    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)
        return


