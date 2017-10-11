# coding: utf-8

from common.utils import log_exception
from common.views import BackstageBaseAPIView, BackstageHTTPResponse
from share.data import TableData, DataChart, Ship


class TableDataView(BackstageBaseAPIView):

    @log_exception
    def get(self, request):
        u"""
        获取编号数据
        ---
        parameters:
            - name: data_code
              description: 数据编号
              paramType: query
              required: true
            - name: table_name
              description: 数据所在表
              paramType: query
              required: false
            - name: start
              description: 开始日期
              paramType: query
              required: false
            - name: end
              description: 结束日期
              paramType: query
              required: false
        """
        query = request.query_params.dict()
        data_code = query.get('data_code')
        table_name = query.get('table_name')
        start = query.get('start')
        end = query.get('end')
        data_obj = TableData(data_code, table_name, start, end)
        return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
                                     data=data_obj.get_all(timestamp=True)).to_response()


class TableDataListView(BackstageBaseAPIView):

    @log_exception
    def get(self, request):
        u"""
        批量获取编号数据
        ---
        parameters:
            - name: line[]
              description: 图表编号
              paramType: query
              required: true
        """
        lines = request.query_params.getlist('line[]')
        chart = DataChart()
        for line in lines:
            line_param = line.split('*')
            if len(line_param) != 4:
                continue
            data_code, table_name, start, end = line_param
            data_obj = TableData(data_code, table_name, start, end)
            chart.add_line(data_obj)
        return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
                                     data=chart.get_all()).to_response()


class ShipDataView(BackstageBaseAPIView):

    @log_exception
    def get(self, request):
        u"""
        获取ship数据
        ---
        parameters:
            - name: variety
              description: 品目
              paramType: query
              required: true
            - name: price_code
              description: 数据编号
              paramType: query
              required: true
            - name: contract
              description: 合约
              paramType: query
              required: false
            - name: start
              description: 开始日期
              paramType: query
              required: false
            - name: end
              description: 结束日期
              paramType: query
              required: false
        """
        query = request.query_params.dict()
        variety = query.get('variety')
        price_code = query.get('price_code')
        contract = query.get('contract') or 'main_contract'
        start = query.get('start')
        end = query.get('end')
        data_obj = Ship(variety, price_code, serial=contract, start=start, end=end)
        return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
                                     data=data_obj.get_all(timestamp=True)).to_response()


class ShipDataListView(BackstageBaseAPIView):
    @log_exception
    def get(self, request):
        u"""
        批量获取ship数据
        ---

        parameters:
            - name: line[]
              description: ship编号
              paramType: query
              required: true
        """
        lines = request.query_params.getlist('line[]')
        chart = DataChart()
        for line in lines:
            line_param = line.split('*')
            if len(line_param) != 5:
                continue
            variety, price_code, contract, start, end = line_param
            contract = contract or 'main_contract'
            data_obj = Ship(variety, price_code, serial=contract, start=start, end=end)
            chart.add_line(data_obj)
        return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
                                     data=chart.get_all()).to_response()


class LatestTableDataView(BackstageBaseAPIView):

    @log_exception
    def get(self, request):
        u"""
        获取编号数据
        ---
        parameters:
            - name: data_code
              description: 数据编号
              paramType: query
              required: true
            - name: table_name
              description: 数据所在表
              paramType: query
              required: false
        """
        query = request.query_params.dict()
        data_code = query.get('data_code')
        table_name = query.get('table_name')
        data_obj = TableData(data_code, table_name, limit=1, desc=True)
        data = data_obj.get_all(timestamp=True)
        data['time'] = data['line'][0][0] if len(data['line']) else None
        data['data'] = data['line'][0][1] if len(data['line']) else None
        return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
                                     data=data).to_response()


class LatestTableDataListView(BackstageBaseAPIView):

    @log_exception
    def get(self, request):
        u"""
        批量获取编号数据
        ---
        parameters:
            - name: line[]
              description: 图表编号
              paramType: query
              required: true
        """
        lines = request.query_params.getlist('line[]')
        chart = DataChart()
        for line in lines:
            line_param = line.split('*')
            if len(line_param) != 2:
                continue
            data_code, table_name = line_param
            data_obj = TableData(data_code, table_name, limit=1, desc=True)
            chart.add_line(data_obj)
        data = chart.get_all()
        for item in data:
            item['time'] = item['line'][0][0] if len(item['line']) else None
            item['data'] = item['line'][0][1] if len(item['line']) else None
        return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
                                     data=data).to_response()
