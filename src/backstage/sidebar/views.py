# coding: utf-8
from common.views import BackstageBaseAPIView, BackstageHTTPResponse


class VarietyView(BackstageBaseAPIView):

    def get(self, request):
        u"""
        获取所有品种
        ---
        """
        pass


class SidebarView(BackstageBaseAPIView):

    def get(self, request):
        u"""
        获取某品种侧边栏
        ---

        parameters:
            - name: variety
              description: 品种
              paramType: query
              required: True
        """
        pass

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
        pass

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
        pass

    def delete(self, request):
        u"""
        删除侧边栏
        ---

        parameters:
            - name: id
              description: 侧边栏id
              paramType: form
              required: True
        """
        pass


class SidebarOrderView(BackstageBaseAPIView):

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
        pass


class SidebarChartsView(BackstageBaseAPIView):

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
        pass

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
