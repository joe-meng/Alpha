# encoding: utf-8

import logging

from django.core.paginator import Paginator
from rest_framework.views import APIView

from common.models import BackstageHTTPResponse
from common.utils import log_exception
from tables.filters import TablesFilter
from tables.models import Tables
from tables.serializers import TableSerializer

logger = logging.getLogger(__name__)


class TableListAPI(APIView):

    @log_exception
    def get(self, request, *args, **kwargs):
        """
        数据表列表
        ---
        parameters:
            - name: index
              description: 页数
              type: integer
              paramType: query
              required: false
            - name: number
              description: 每页条数
              type: integer
              paramType: query
              required: false
            - name: name
              description: 名字
              type: string
              paramType: query
              required: false
            - name: type
              description: 类型
              type: integer
              paramType: query
              required: false
        """
        tables = Tables.objects.all()
        tables = TablesFilter(request.GET, queryset=tables).qs
        paginator = Paginator(tables, request.GET.get('number', 100))
        page = paginator.page(request.GET.get('index', 1))
        serializer = TableSerializer(page, many=True)
        return BackstageHTTPResponse(
            code=BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
            data=serializer.data,
            pageinfo=page
        ).to_response()


class TableDetailAPI(APIView):

    @log_exception
    def get(self, request, id, *args, **kwargs):
        """
        数据表
        ---
        parameters:
            - name: id
              description: id
              type: integer
              paramType: path
              required: true
        """
        table = Tables.objects.filter(id=id).first()
        if id and not table:
            return BackstageHTTPResponse(code=BackstageHTTPResponse.API_HTTP_CODE_INVILID_PARAMS, message='没有该表').to_response()

        serializer = TableSerializer(table)
        return BackstageHTTPResponse(
            code=BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
            data=serializer.data,
        ).to_response()
