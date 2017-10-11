from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework.views import APIView

from common.models import BackstageHTTPResponse
from common.utils import log_exception
from symbols.filters import SymbolFilter
from symbols.models import Symbol
from symbols.serializers import SymbolSerializer


class SymbolListAPI(APIView):
    @log_exception
    def get(self, request, *args, **kwargs):
        """
        公式可用数据点列表
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
            - name: table_name
              description: 表名
              type: string
              paramType: query
              required: false
            - name: classification_1
              description: 第一维度
              type: string
              paramType: query
              required: false
            - name: classification_2
              description: 第二维度
              type: string
              paramType: query
              required: false
        """
        symbols = Symbol.objects.all()
        symbols = SymbolFilter(request.GET, queryset=symbols).qs
        paginator = Paginator(symbols, request.GET.get('number', 100))
        page = paginator.page(request.GET.get('index', 1))
        serializer = SymbolSerializer(page, many=True)
        return BackstageHTTPResponse(
            code=BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
            data=serializer.data,
            pageinfo=page
        ).to_response()


class TableListAPI(APIView):

    @log_exception
    def get(self, request, *args, **kwargs):
        """
        公式可用表
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
        """
        table_names = list(Symbol.objects.exclude(
            Q(table_name__isnull=True)|(Q(table_name=''))
        ).values_list('table_name', flat=True).order_by('table_name').distinct())
        return BackstageHTTPResponse(
            code=BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
            data=table_names,
        ).to_response()


class SymbolClassificationListAPI(APIView):

    @log_exception
    def get(self, request, classification, *args, **kwargs):
        """
        公式可用区分维度
        ---
        parameters:
            - name: classification
              description: 第几个区分维度
              type: integer
              paramType: path
              required: true
        """
        column_name = 'classification_%s' % classification
        if column_name not in [i.attname for i in Symbol._meta.fields]:
            return BackstageHTTPResponse(
                code=BackstageHTTPResponse.API_HTTP_CODE_NOT_FOUND,
                message='未找到数据'
            ).to_response()
        query_dict_1 = {'%s__isnull' % column_name: True}
        query_dict_2 = {column_name: ''}
        column_values = list(Symbol.objects.exclude(
            Q(**query_dict_1)|(Q(**query_dict_2))
        ).values_list(column_name, flat=True).order_by(column_name).distinct())
        return BackstageHTTPResponse(
            code=BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
            data=column_values,
        ).to_response()
