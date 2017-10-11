# coding: utf-8
import datetime
from django.db import connection

from common.utils import log_exception
from common.views import BackstageBaseAPIView, BackstageHTTPResponse


class TodayVarietyCapitalView(BackstageBaseAPIView):

    @log_exception
    def get(self, request):
        u"""
        获取品种资金沉淀
        ---
        parameters:
            - name: in_limit
              description: 品种数量
              paramType: query
              required: false
            - name: out_limit
              description: 品种数量
              paramType: query
              required: false
            - name: pre_limit
              description: 品种数量
              paramType: query
              required: false
        """
        today = datetime.date.today()
        params = request.query_params.dict()
        # 资金沉淀
        pre_limit = int(params.get('pre_limit')) if params.get('pre_limit') else 7
        sql = ('select a.variety, b.sendimentary_money, a.variety_name from chart_variety as a '
               'left join day_kline as b on a.index_contract=b.contract where b.date_time=%s '
               'order by b.sendimentary_money desc limit %s')
        cursor = connection.cursor()
        cursor.execute(sql, (today, pre_limit))
        pre_data = cursor.fetchall()
        pre_data = [{'variety': variety, 'name': name, 'amount': amount}for variety, amount, name in pre_data]
        # 流出
        out_limit = int(params.get('out_limit')) if params.get('out_limit') else 5
        sql = ('select a.variety, b.flow_fund, a.variety_name from chart_variety as a '
               'left join day_kline as b on a.index_contract=b.contract where b.flow_fund<=0 '
               'and b.date_time=%s order by b.flow_fund asc limit %s')
        cursor = connection.cursor()
        cursor.execute(sql, (today, out_limit))
        flow_out_data = cursor.fetchall()
        flow_out_data = [{'variety': variety, 'name': name, 'amount': amount} for variety, amount, name in flow_out_data]
        # 流入
        in_limit = int(params.get('in_limit')) if params.get('in_limit') else 5
        sql = ('select a.variety, b.flow_fund, a.variety_name from chart_variety as a '
               'left join day_kline as b on a.index_contract=b.contract where b.flow_fund>=0 '
               'and b.date_time=%s order by b.flow_fund desc limit %s')
        cursor = connection.cursor()
        cursor.execute(sql, (today, in_limit))
        flow_in_data = cursor.fetchall()
        flow_in_data = [{'variety': variety, 'name': name, 'amount': amount} for variety, amount, name in flow_in_data]
        return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
                                     data={'pre': pre_data,
                                           'flow_in': flow_in_data,
                                           'flow_out': flow_out_data}, message='获取前几个品种的资金沉淀和流入流出').to_response()


class VarietyCapitalView(BackstageBaseAPIView):

    @log_exception
    def get(self, request):
        u"""
        获取今日资金流入流出量最大的几个品种的历史资金沉淀
        ---

        parameters:
            - name: in_limit
              description: 品种数量
              paramType: query
              required: false
            - name: out_limit
              description: 品种数量
              paramType: query
              required: false
        """
        today = datetime.date.today()
        params = request.query_params.dict()
        # 流出
        out_limit = int(params.get('out_limit')) if params.get('out_limit') else 5
        sql = ('select a.variety, a.index_contract, a.variety_name from chart_variety as a '
               'left join day_kline as b on a.index_contract=b.contract where b.flow_fund<=0 '
               'and b.date_time=%s order by b.flow_fund asc limit %s')
        cursor = connection.cursor()
        cursor.execute(sql, (today, out_limit))
        flow_out_data = cursor.fetchall()
        flow_out = []
        for variety, contract, name in flow_out_data:
            sql = ('select sendimentary_money, date_time from day_kline '
                   'where contract=%s order by date_time desc limit 10')
            cursor.execute(sql, (contract,))
            variety_data = cursor.fetchall()
            variety_data = [{'date': date, 'amount': amount} for amount, date in variety_data]
            variety_data.reverse()
            flow_out.append({'name': name, 'data': variety_data})
        # 流入
        in_limit = int(params.get('in_limit')) if params.get('in_limit') else 5
        sql = ('select a.variety, a.index_contract, a.variety_name from chart_variety as a '
               'left join day_kline as b on a.index_contract=b.contract where b.flow_fund>=0 '
               'and b.date_time=%s order by b.flow_fund desc limit %s')
        cursor = connection.cursor()
        cursor.execute(sql, (today, in_limit))
        flow_in_data = cursor.fetchall()
        flow_in = []
        for variety, contract, name in flow_in_data:
            sql = ('select sendimentary_money, date_time from day_kline '
                   'where contract=%s order by date_time desc limit 10')
            cursor.execute(sql, (contract,))
            variety_data = cursor.fetchall()
            variety_data = [{'date': date, 'amount': amount} for amount, date in variety_data]
            variety_data.reverse()
            flow_in.append({'name': name, 'data': variety_data})

        return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
                                     data={'flow_in': flow_in,
                                           'flow_out': flow_out}, message='获取历史资金流入流出成功').to_response()


class ExchangeCapitalView(BackstageBaseAPIView):

    @log_exception
    def get(self, request):
        u"""
        获取三大交易所历史资金流入流出
        ---
        """
        data = []
        exchanges = (('SHFE', '上期所'), ('DCE', '郑商所'), ('CZCE', '大商所'))
        cursor = connection.cursor()
        for exchange, name in exchanges:
            sql = ('SELECT sum(flow_fund) as amount, date_time FROM alpha.day_kline '
                   'where exchange=%s and contract like "%%8888" group by date_time '
                   'order by date_time desc limit 15;')
            cursor.execute(sql, (exchange,))
            result = cursor.fetchall()
            result = [{'date': date, 'amount': amount} for amount, date in result]
            result.reverse()
            data.append({'name': name, 'data': result})
        return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
                                     data=data, message='获取交易所资金变化成功').to_response()


class ProductCapitalView(BackstageBaseAPIView):

    @log_exception
    def get(self, request):
        u"""
        获取四大产品线资金流入流出
        ---
        """
        data = []
        categories = ((1, '有色'), (2, '黑色'), (3, '化工'), (4, '农产品'))
        cursor = connection.cursor()
        for category, name in categories:
            sql = ('select sum(a.flow_fund) as amount, a.date_time from alpha.day_kline as a '
                   'left join alpha.chart_variety as b on a.contract=b.index_contract '
                   'where b.category=%s group by a.date_time order by a.date_time desc limit 15')
            cursor.execute(sql, (category,))
            result = cursor.fetchall()
            result = [{'date': date, 'amount': amount} for amount, date in result]
            result.reverse()
            data.append({'name': name, 'data': result})
        return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
                                     data=data, message='获取产品线资金流入流出成功').to_response()
