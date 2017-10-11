#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@date: 2016-06-13

@author: Devin
"""
import logging
import uuid

import oss2


from common.models import BackstageHTTPResponse
from common.views import BackstageBaseAPIView
from common.utils import log_exception
from backstage.serializers import MSUserSerializer
from django.conf import settings

logger = logging.getLogger("use_info_ms")


class FileUploadView(BackstageBaseAPIView):

    @log_exception
    def post(self, request):
        u"""
        上传文件
        ---

        parameters:
            - name: up_file
              description: 用户名
              type: file
              paramType: form
              required: true
        :param request:
        :return:
        """
        post_data = self.request_data(request)
        up_f = post_data.get('up_file', None)
        # f_name = post_data.get('file_name', '')
        f_name = up_f.name
        logger.info(u'上传文件, 文件名:%s'%f_name)
        if not up_f:
            msg = u"文件不存在"
            logger.info(msg)
            return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_INVILID_PARAMS,
                                         message=msg).to_response()
        if not f_name:
            msg = u"文件名为必填"
            logger.info(msg)
            return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_INVILID_PARAMS,
                                         message=msg).to_response()
        new_name = str(uuid.uuid1())[:8] + f_name
        auth = oss2.Auth(settings.ALI_OSS_ACCESS_KEY_ID, settings.ALI_OSS_ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, settings.ALI_OSS_ENDPOINT, settings.ALI_OSS_BUCKET_NAME)
        res = bucket.put_object(new_name, up_f.read())
        logger.info(u'上传文件, 文件名:%s, 请求id: %s, 返回状态: %s'% (new_name, res.request_id, res.status))
        url = ''.join([settings.FATHER_URL, new_name])
        return BackstageHTTPResponse(message=u'上传成功',
                                     data=dict(url=url)).to_response()


