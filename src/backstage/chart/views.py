# coding: utf-8

from common.views import BackstageBaseAPIView, BackstageHTTPResponse


class ChartListView(BackstageBaseAPIView):

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

    def get(self, request):
        u"""
        获取图信息（不包括曲线历史数据）
        ---

        parameters:
            - name: id
              description: 图id
              paramType: query
              required: true
        """
        pass

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
