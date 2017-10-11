# coding: utf-8
import json
import datetime
import when
from django.db import connection

from common.utils import log_exception
from common.views import BackstageBaseAPIView, BackstageHTTPResponse
from share.data import ProxyData
from chart.models import Chart, ChartLine, Exchange, Variety, Sidebar, SidebarChart


class ChartVarietyView(BackstageBaseAPIView):

    @log_exception
    def get(self, request):
        u"""
        获取所有品种
        ---
        """
        exchanges = Exchange.objects.all()
        varieties = Variety.objects.all()
        varieties_dict = {}
        for variety in varieties:
            varieties_dict.setdefault(variety.exchange, []).append({'variety': variety.variety,
                                                                    'variety_name': variety.variety_name})
        data = [{'exchange': exchange.exchange,
                 'exchange_name': exchange.exchange_name,
                 'varieties': varieties_dict.get(exchange.exchange, [])} for exchange in exchanges]
        return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
                                     data=data, message='获取品目列表成功').to_response()


class ChartSidebarView(BackstageBaseAPIView):

    @log_exception
    def get(self, request):
        u"""
        获取品种侧边栏
        ---

        parameters:
            - name: variety
              description: 品种
              paramType: query
              required: True
        """
        params = request.query_params.dict()
        variety = params.get('variety')
        sidebars = Sidebar.objects.filter(variety=variety).order_by('-priority', 'id')
        data = [{'sidebar_id': sidebar.id, 'sidebar_name': sidebar.name} for sidebar in sidebars]
        return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
                                     data=data, message='获取侧边栏列表成功').to_response()

    @log_exception
    def post(self, request):
        u"""
        新增侧边栏
        ---

        parameters:
            - name: variety
              description: 品种
              paramType: form
              required: True
            - name: sidebar_name
              description: 侧边栏名称
              paramType: form
              required: True
        """
        data = self.request_data(request)
        variety = data['variety']
        name = data['sidebar_name']
        sidebar = Sidebar(variety=variety, name=name)
        sidebar.save()
        return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
                                     data=data, message='新增侧边栏成功').to_response()

    @log_exception
    def put(self, request):
        u"""
        修改侧边栏
        ---

        parameters:
            - name: id
              description: 侧边栏id
              paramType: form
              required: true
            - name: name
              description: 侧边栏名称
              paramType: form
              required: true
        """
        data = self.request_data(request)
        sidebar_id = data['id']
        sidebar_name = data['name']
        sidebar = Sidebar.objects.get(pk=sidebar_id)
        sidebar.name = sidebar_name
        sidebar.save()
        return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
                                     data=data, message='修改侧边栏成功').to_response()

    @log_exception
    def delete(self, request):
        u"""
        删除侧边栏
        ---

        parameters:
            - name: sidebar_id
              description: 侧边栏id
              paramType: form
              required: True
        """
        data = self.request_data(request)
        sidebar_id = data['sidebar_id']
        sidebar = Sidebar.objects.get(pk=sidebar_id)
        sidebar.delete()
        return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
                                     data=data, message='删除侧边栏成功').to_response()


class ChartSidebarOrderView(BackstageBaseAPIView):

    @log_exception
    def post(self, request):
        u"""
        侧边栏列表排序
        ---

        parameters:
            - name: id_list
              description: 侧边栏id list
              paramType: form
              required: True
        """
        data = self.request_data(request)
        id_list = json.loads(data['id_list'])
        for index, sidebar_id in enumerate(id_list):
            priority = -(index + 1)
            sidebar = Sidebar.objects.get(pk=sidebar_id)
            sidebar.priority = priority
            sidebar.save()
        return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
                                     data=data, message='侧边栏排序成功').to_response()


class SidebarChartsView(BackstageBaseAPIView):

    @log_exception
    def get(self, request):
        u"""
        获取侧边栏所有图
        ---

        parameters:
            - name: sidebar_id
              description: 侧边栏id
              paramType: query
              required: True
        """
        params = request.query_params.dict()
        sidebar_id = params['sidebar_id']
        sql = ('select a.id, a.chart_id, a.size, b.graph, b.compare, b.p_axis, b.s_axis '
               'from chart_sidebar_chart as a left join chart_chart as b on a.chart_id=b.id '
               'where a.sidebar_id=%s order by a.priority desc, a.id asc;')
        cursor = connection.cursor()
        cursor.execute(sql, sidebar_id)
        result = cursor.fetchall()
        charts = []
        for row in result:
            chart = {'id': row[0],
                     'chart_id': row[1],
                     'size': row[2],
                     'graph': row[3],
                     'compare': row[4],
                     'p_axis': row[5],
                     's_axis': row[6]}
            charts.append(chart)
        return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
                                     data={'charts': charts}, message='获取侧边栏图列表成功').to_response()

    @log_exception
    def post(self, request):
        u"""
        增加一个侧边栏图
        ---

        parameters:
            - name: sidebar_id
              description: 侧边栏id
              paramType: form
              required: True
            - name: chart_id
              description: 图id
              paramType: form
              required: True
            - name: size
              description: 是否跨两栏（1， 跨一栏）（2， 跨两栏）
              paramType: form
              required: True
        """
        pass

    @log_exception
    def put(self, request):
        u"""
        修改一个侧边栏图
        ---

        parameters:
            - name: id
              description: 侧边栏图id
              paramType: form
              required: True
            - name: size
              description: 侧边栏图大小(1, 跨一栏)(2, 跨两栏)
              paramType: form
              required: false
            - name: chart_id
              description: 图id
              paramType: form
              required: false
        """
        pass

    @log_exception
    def delete(self, request):
        u"""
        删除一个侧边栏图
        ---

        parameters:
            - name: id
              description: 侧边栏图id
              paramType: form
              required: True
        """
        pass


class SidebarChartsOrderView(BackstageBaseAPIView):

    @log_exception
    def post(self, request):
        u"""
        侧边栏图列表排序
        ---

        parameters:
            - name: id_list
              description: 侧边栏图id list
              paramType: form
              required: True
        """
        pass


class ChartListView(BackstageBaseAPIView):

    @log_exception
    def get(self, request):
        u"""
        获取alpha系统所有图
        ---
        parameters:
            - name: title
              description: 图标题
              paramType: query
              required: false
            - name: graph
              description: 图形状(1, 线型)(2, 柱状)
              paramType: query
              required: false
            - name: compare
              description: 图对比(1, 非对比)(2, 年对比)(3, 月对比)
              paramType: query
              required: false
        """
        pass


class ChartView(BackstageBaseAPIView):

    @log_exception
    def get(self, request):
        u"""
        获取图信息（包括曲线历史数据）
        ---
        parameters:
            - name: id
              description: 图id
              paramType: query
              required: True
        """
        data = request.query_params.dict()
        chart_id = data['id']
        chart = Chart.objects.get(pk=chart_id)
        chart_lines = ChartLine.objects.filter(chart_id=chart_id)
        data = []
        if chart.compare == Chart.COMPARE_YEAR:
            date, start, end = [], None, None
            for i in range(3):
                year = when.future(years=-i).strftime('%Y-01-01')
                if start:
                    end = start - datetime.timedelta(days=1)
                else:
                    end = None
                start = datetime.datetime.strptime(year, '%Y-%m-%d').date()
                date.insert(0, (start, end))
            for chart_line in chart_lines:
                line_data = ProxyData(chart_line.data_code, chart_line.table_name)
                year_data = []
                for start, end in date:
                    line_data.start = start
                    line_data.end = end
                    year_data.append({'year': start.strftime('%Y'),
                                      'data': line_data.get_list(timestamp=True)})
                data.append({'title': line_data.title,
                             'unit': line_data.unit,
                             'line': year_data,
                             'line_type': line_data.table,
                             'count': line_data.count(),
                             'data_code': line_data.data_code})
        elif chart.compare == Chart.COMPARE_MONTH:
            date, start, end = [], None, None
            for i in range(3):
                month = when.future(months=-i).strftime('%Y-%m-01')
                if start:
                    end = start - datetime.timedelta(days=1)
                else:
                    end = None
                start = datetime.datetime.strptime(month, '%Y-%m-%d').date()
                date.insert(0, (start, end))
            for chart_line in chart_lines:
                line_data = ProxyData(chart_line.data_code, chart_line.table_name)
                month_data = []
                for start, end in date:
                    line_data.start = start
                    line_data.end = end
                    month_data.append({'month': start.strftime('%Y-%m'),
                                       'data': line_data.get_list(timestamp=True)})
                data.append({'title': line_data.title,
                             'unit': line_data.unit,
                             'line': month_data,
                             'line_type': line_data.table,
                             'count': line_data.count(),
                             'data_code': line_data.data_code})
        else:
            six_month_ago = when.future(months=-6).date()
            for chart_line in chart_lines:
                line_data = ProxyData(chart_line.data_code, chart_line.table_name, start=six_month_ago)
                line_data = line_data.get_all(timestamp=True)
                line_data['title'] = chart_line.line_name
                data.append(line_data)
        return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
                                     data=data,
                                     message='获取图数据成功').to_response()

    @log_exception
    def post(self, request):
        u"""
        增加一个图
        ---

        parameters:
            - name: title
              description: 图标题
              paramType: form
              required: True
            - name: graph
              description: 图形状(1, 线形)(2, 柱状)
              paramType: form
              required: True
            - name: compare
              description: 图对比（1， 非对比）（2， 年对比）(3, 月对比)
              paramType: form
              required: True
            - name: p_axis
              description: 主轴显示
              paramType: form
              required: false
            - name: s_axis
              description: 次轴显示
              paramType: form
              required: false
        """
        pass

    @log_exception
    def put(self, request):
        u"""
        修改一个图
        ---

        parameters:
            - name: id
              description: 图id
              paramType: form
              required: True
            - name: title
              description: 图标题
              paramType: form
              required: false
            - name: graph
              description: 图形状(1, 线形)(2, 柱状)
              paramType: form
              required: false
            - name: compare
              description: 图对比（1， 非对比）（2， 年对比）(3, 月对比)
              paramType: form
              required: false
            - name: p_axis
              description: 主轴显示
              paramType: form
              required: false
            - name: s_axis
              description: 次轴显示
              paramType: form
              required: false
        """
        pass

    @log_exception
    def delete(self, request):
        u"""
        删除一个图
        ---

        parameters:
            - name: id
              description: 图id
              paramType: form
              required: True
        """
        pass


class ChartLineView(BackstageBaseAPIView):

    @log_exception
    def post(self, request):
        u"""
        增加一条曲线
        ---

        parameters:
            - name: chart_id
              description: 所属的图id
              paramType: form
              required: True
            - name: data_code
              description: 数据编码
              paramType: form
              required: True
            - name: table_name
              description: 数据类型
              paramType: form
              required: True
            - name: line_name
              description: 曲线名称
              paramType: form
              required: false
            - name: axis
              description: 主次轴(1, 主轴)(2, 次轴)
              paramType: form
              required: false
        """
        pass

    @log_exception
    def put(self, request):
        u"""
        修改一条曲线
        ---

        parameters:
            - name: id
              description: 曲线id
              paramType: form
              required: true
            - name: chart_id
              description: 所属的图id
              paramType: form
              required: false
            - name: data_code
              description: 数据编码
              paramType: form
              required: false
            - name: table_name
              description: 数据类型
              paramType: form
              required: false
            - name: line_name
              description: 曲线名称
              paramType: form
              required: false
            - name: axis
              description: 主次轴(1, 主轴)(2, 次轴)
              paramType: form
              required: false
        """
        pass

    @log_exception
    def delete(self, request):
        u"""
        删除一条曲线
        ---

        parameters:
            - name: id
              description: 曲线id
              paramType: form
              required: True
        """
        pass
