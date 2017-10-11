# /usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from django.http import QueryDict
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from pymongo import MongoClient

from common.utils import log_exception
from .models import BackstageHTTPResponse
from django.conf import settings

MONGO_DB_NAME = settings.MONGO_DB_NAME
MONGO_DB_SETTINGS = settings.MONGO_DB_SETTINGS

# from backstage.models import (WorkOrder, Message, MessageText, RuleAPIActuator,
#                           RuleRabitMQActuator)

logger = logging.getLogger("usecloudlog")

class BackstageBaseAPIView(APIView):

    news_model_list = [('source', ''), ('machine_tags', ''), ('machine_summary', ''), ('push_state', '0'),
                       ('pub_time', ''), ('title', ''), ('craw_time', ''), ('pub_state', '0'), ('look_state', '0'),
                       ('_id', ''), ('content_html', ''), ('top_tag', '0'), ('manual_tags', []), ('machine_class', ''),
                       ('url', ''), ('content_text', ''), ('is_rmd', '0'), ('pdf_url', '')]

    def __init__(self, *args, **kwargs):
        client = MongoClient(**MONGO_DB_SETTINGS)
        self.db = getattr(client, MONGO_DB_NAME)
        super(BackstageBaseAPIView, self).__init__(*args, **kwargs)

    def request_data(self, request):
        if request.method in ['PUT', 'POST', 'DELETE']:
            if isinstance(request.data, QueryDict):
                return request.data.dict()
            return request.data

    def get_serializers_mongo(self, mongo_objs):
        """序列化mongo查询对象"""
        # if self.model_type == 'news':
        res = []
        for vals in mongo_objs:
            key = {}
            for i in self.news_model_list:
                k, d = i
                key[k] = vals.get(k, d)

            res.append(key)
        return res



class HTTPCodeListView(APIView):
    """

    """

    def get(self, request):
        """
        获取所有的RESPONSE中code对应的信息
        ---

        type:
            code:
                required: true
                type: string
            value:
                required: true
                type: string

        parameters:
            - name: code
              description: 回复中的code
              type: string
              paramType: query
              required: false
        """
        data = BackstageHTTPResponse.CODE_DESCRIPTION
        query_dict = request.query_params.dict().copy()
        code = query_dict.get("code", None)
        if code:
            data = {code: data.get(code)}

        return BackstageHTTPResponse(
            BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
            data=data).to_response()


class ModelChoiceListView(APIView):
    def get(self, request):
        """
        获取所有的对像可选项的key-value
        ---

        type:
            code:
                required: true
                type: string
            value:
                required: true
                type: string

        parameters:

            - name: key
              description: >
                            要查询的可选项的类名,全小写,有效值: camera, eventlog,
                            rfidcard,rfidcontent,rfidreader
              type: string
              paramType: query
              required: false
        """
        # from django.contrib.auth.models import User
        res_dict = dict()
        # res_dict.update(User.get_choice_dict())
        # res_dict.update(WorkOrder.get_choice_dict())
        # res_dict.update(Message.get_choice_dict())
        # res_dict.update(MessageText.get_choice_dict())
        # res_dict.update(RuleAPIActuator.get_choice_dict())
        # res_dict.update(RuleRabitMQActuator.get_choice_dict())
        news_type_dict = {u'news': {u'pub_state': {u'0': u'未发布', u'1': u'发布'},
                                   u'look_state': {u'0': u'未查看', u'1': u'已查看'},
                                   u'push_state': {u'0': u'已推送', u'1': u'未推送'},
                                   }}
        res_dict.update(news_type_dict)
        query_dict = request.query_params.dict().copy()
        key = query_dict.get("key", None)
        if not key:
            return BackstageHTTPResponse(
                BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
                data=res_dict).to_response()
        #
        if key in res_dict:
            res_dict = res_dict.get(key)
            return BackstageHTTPResponse(
                BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
                data=res_dict).to_response()

        else:
            return BackstageHTTPResponse(
                BackstageHTTPResponse.API_HTTP_CODE_INVILID_PARAMS,
                data=res_dict).to_response()


from .utils import AlphaSchemaGenerator
from rest_framework.renderers import CoreJSONRenderer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework_swagger import renderers


class AlphaSwaggerSchemaView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [
        CoreJSONRenderer,
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer
    ]

    def get(self, request):
        generator = AlphaSchemaGenerator()
        schema = generator.get_schema(request=request)

        return Response(schema)


