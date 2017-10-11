# coding: utf-8
from django.shortcuts import get_object_or_404

from common.utils import log_exception
from common.views import BackstageBaseAPIView, BackstageHTTPResponse
from formulas.models import Formula
from workers.calculation.lib.vo import FormulaEnv, DBPreProcess
from share.formula import ApiFormulaExecutor, ShareFormula
from varieties.models import VarietiesRecord


class FormulaExecuteView(BackstageBaseAPIView):

    @log_exception
    def post(self, request):
        u"""
        公式测试执行
        ---
        parameters:
            - name: formula_id
              description: 交易所
              paramType: form
              required: True
            - name: variety_id
              description: 品种
              paramType: form
              required: True
        """
        params = self.request_data(request)
        formula_id = params['formula_id']
        variety_id = int(params['variety_id'])
        variety = get_object_or_404(VarietiesRecord, pk=variety_id)
        variety = variety.code
        formula = get_object_or_404(Formula, pk=formula_id)
        f = ShareFormula(id=formula.id, title=formula.title, formula=formula.formula,
                         description=formula.description, user_id=formula.user_id)
        env = FormulaEnv(id=formula_id, pre_data=DBPreProcess(varieties=variety))
        if variety_id not in f.varieties:
            log = "编号%s的公式适用品目%s, 不适用当前上下文中品目%s" % (f.id, f.varieties, env.content_variety)
            data = {'success': False, 'log': log}
            return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
                                         data=data, message='公式执行失败').to_response()
        else:
            executor = ApiFormulaExecutor(f, env)
            log = executor.run()
            data = {'success': executor.success,
                    'log': log,
                    'chart': executor.chart_data}
            return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
                                         data=data, message='公式执行成功').to_response()
