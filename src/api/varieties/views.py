# coding: utf-8
import json

from rest_framework.views import APIView

from chart.models import Sidebar
from common.models import BackstageHTTPResponse
from common.utils import log_exception
from share.data import ref_table
from symbols.models import Symbol
from varieties.models import VarietiesSidebarTable, VarietiesRecord
from varieties.serializers import VarietiesRecordSerializer


class SidebarTableDataHandler(APIView):

    @log_exception
    def get(self, request, chart_variety, sidebar):
        """
        主页图表下方数据表格接口，支持所有 chart_sidebar 表中的 variety-sidebar 组合
        ---
        parameters:
            - name: chart_variety
              description: 品类
              type: string
              paramType: path
              required: true
            - name: sidebar
              description: 侧边栏参数
              type: string
              paramType: path
              required: true
        """
        chart_sidebar = ChartSidebar.objects.filter(variety=chart_variety, sidebar=sidebar).first()
        if not chart_sidebar:
            return BackstageHTTPResponse(
                code=BackstageHTTPResponse.API_HTTP_CODE_NOT_FOUND,
                message='未找到对应数据'
            ).to_response()
        sidebar_tables = VarietiesSidebarTable.objects.filter(chart_sidebar_id=chart_sidebar.id)
        fields = ['timestamp', 'number']
        # 定义最终生成的 shape/column
        for sidebar_table in sidebar_tables:
            # extra 格式 {"field": "source", "name": "来源", "fetch_code": "xxx"}
            # fetch_code 是获取数据的方式, 比如获取 symbol 表的 title, 那么就是 title
            extras = json.loads(sidebar_table.extra)
            for extra in extras:
                if extra['field'] not in fields:
                    fields.append(extra['field'])
        data_list = [fields]
        for i, sidebar_table in enumerate(sidebar_tables):
            data = [None] * len(fields)
            table_data = ref_table(sidebar_table.data_code, sidebar_table.table, limit=1, timestamp=True)
            data[:2] = table_data[0] if table_data else [None]*2

            if sidebar_table.table.lower() == 'symbol':
                symbol = Symbol.objects.filter(symbol=sidebar_table.data_code.split('.')[0]).first()
                extras = json.loads(sidebar_table.extra)
                for extra in extras:
                    data[fields.index(extra['field'])] = getattr(symbol, extra['fetch_code'], '') if not extra.get('text', '') else extra['text']
            data_list.append(data)
        return BackstageHTTPResponse(
            code=BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
            data={'data': data_list},
        ).to_response()


class VarietiesDetailHandler(APIView):
    def get(self, request, id):
        """
        品类详情
        ---
        parameters:
            - name: id
              description: 品类id
              type: string
              paramType: path
              required: true
        """
        varieties = VarietiesRecord.objects.filter(id=id).first()
        if not varieties:
            return BackstageHTTPResponse(
                code=BackstageHTTPResponse.API_HTTP_CODE_NOT_FOUND,
            ).to_response()
        serializer = VarietiesRecordSerializer(varieties)
        return BackstageHTTPResponse(
            code=BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
            data=serializer.data
        ).to_response()
