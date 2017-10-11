from django.core.paginator import Paginator
from django.db import transaction
from rest_framework.views import APIView

from common.models import BackstageHTTPResponse, KVObject
from common.utils import log_exception
from user.models import FormulaSubscription
from varieties.models import VarietiesRecord
from .serializers import FormulaSerializer, FormulaFunctionSerializer
from .models import FormulaFunction, Formula, FormulaVarieties


class FormulasListAPI(APIView):

    @log_exception
    def post(self, request, *args, **kwargs):
        """
        新建公式
        ---
        parameters:
            - name: title
              description: 标题
              type: string
              paramType: form
              required: false
            - name: description
              description: 描述
              type: string
              paramType: form
              required: false
            - name: formula
              description: 公式内容
              type: string
              paramType: form
              required: false
            - name: comment
              description: 备注
              type: string
              paramType: form
              required: false
            - name: varieties_id
              description: 品目 id
              type: integer
              paramType: form
              required: false
        """
        if not request.user.id:
            return BackstageHTTPResponse(code=BackstageHTTPResponse.API_HTTP_CODE_NOT_LOGIN_ERR).to_response()

        varieties_id = request.data.get('varieties_id', None)
        if varieties_id and not VarietiesRecord.objects.filter(id=varieties_id).first():
            return BackstageHTTPResponse(code=BackstageHTTPResponse.API_HTTP_CODE_INVILID_PARAMS, message='没有该品目').to_response()

        serializer = FormulaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        formula_serializer = serializer.save(user_id=self.request.user.id)

        if varieties_id:
            FormulaVarieties(
                formula_id=formula_serializer.id,
                varieties_id=varieties_id
            ).save()
            # 有品目的话自动订阅该 formula
            FormulaSubscription(
                user_id=request.user.id,
                formula_id=formula_serializer.id,
                varieties_id=varieties_id
            ).save()

        return BackstageHTTPResponse(code=BackstageHTTPResponse.API_HTTP_CODE_NORMAL, data=serializer.data).to_response()


class FormulasDetailAPI(APIView):

    @log_exception
    def get(self, request, id):
        """
        公式详情
        ---
        parameters:
            - name: id
              description: 公式id
              type: integer
              paramType: path
              required: true
        """
        formula = Formula.objects.filter(id=id).first()
        if not formula:
            return BackstageHTTPResponse(code=BackstageHTTPResponse.API_HTTP_CODE_NOT_FOUND).to_response()

        serializer = FormulaSerializer(formula)
        return BackstageHTTPResponse(code=BackstageHTTPResponse.API_HTTP_CODE_NORMAL, data=serializer.data).to_response()

    @log_exception
    def patch(self, request, id):
        """
        公式详情
        ---
        parameters:
            - name: id
              description: 公式id
              type: integer
              paramType: path
              required: true
            - name: formula
              description: 公式内容
              type: string
              paramType: form
              required: false
            - name: title
              description: 公式标题
              type: string
              paramType: form
              required: false
            - name: description
              description: 公式描述
              type: string
              paramType: form
              required: false
            - name: comment
              description: 公式备注
              type: string
              paramType: form
              required: false
        """
        if not request.user.id:
            return BackstageHTTPResponse(code=BackstageHTTPResponse.API_HTTP_CODE_NOT_LOGIN_ERR).to_response()

        formula = Formula.objects.filter(id=id).first()
        if not formula:
            return BackstageHTTPResponse(code=BackstageHTTPResponse.API_HTTP_CODE_NOT_FOUND).to_response()

        # 内置公式
        if formula.user_id is None:
            # 复制一份成为该用户的私有公式，并且复制原有公式和品目的对应关系
            with transaction.atomic():
                original_formula_id = formula.id
                formula.id = None
                formula.user_id = request.user.id
                serializer = FormulaSerializer(formula, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                new_formula = serializer.save(user_id=request.user.id)
                new_formula_varieties = []
                for formula_varieties in FormulaVarieties.objects.filter(formula_id=original_formula_id):
                    formula_varieties.id = None
                    formula_varieties.formula_id = new_formula.id
                    new_formula_varieties.append(formula_varieties)
                FormulaVarieties.objects.bulk_create(new_formula_varieties)
        elif formula.user_id == request.user.id:
            serializer = FormulaSerializer(formula, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            return BackstageHTTPResponse(code=BackstageHTTPResponse.API_HTTP_CODE_NO_PERMISSION, message='该公式不属于您').to_response()
        return BackstageHTTPResponse(code=BackstageHTTPResponse.API_HTTP_CODE_NORMAL, data=serializer.data).to_response()


class FormulaFunctionsListAPI(APIView):

    @log_exception
    def get(self, request, *args, **kwargs):
        """
        公式可用方法列表
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
        formula_functions = FormulaFunction.objects.all()
        paginator = Paginator(formula_functions, request.GET.get('number', 100))
        page = paginator.page(request.GET.get('index', 1))
        serializer = FormulaFunctionSerializer(page, many=True)
        return BackstageHTTPResponse(
            code=BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
            data=serializer.data,
            pageinfo=page
        ).to_response()


class FormulasTemplateAPI(APIView):

    @log_exception
    def get(self, request, *args, **kwargs):
        """
        默认公式模板
        ---
        """
        formula_template = KVObject.objects.filter(k='default_formula_template').first()
        formula = Formula(
            formula=formula_template.v,
            title='公式模板',
        )
        serializer = FormulaSerializer(formula)
        return BackstageHTTPResponse(
            code=BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
            data=serializer.data,
        ).to_response()


class FormulaVarietiesDetailAPI(APIView):

    @log_exception
    def delete(self, request, id, varieties_id):
        """
        删除公式和品目的对应关系
        ---
        parameters:
            - name: id
              description: 公式 id
              type: integer
              paramType: path
              required: true
            - name: varieties_id
              description: 品类 id
              type: integer
              paramType: path
              required: true
        """
        if not request.user.id:
            return BackstageHTTPResponse(code=BackstageHTTPResponse.API_HTTP_CODE_NOT_LOGIN_ERR).to_response()

        formula = Formula.objects.filter(id=id).first()
        if not formula:
            return BackstageHTTPResponse(code=BackstageHTTPResponse.API_HTTP_CODE_NOT_FOUND).to_response()
        if not formula.user_id:
            return BackstageHTTPResponse(code=BackstageHTTPResponse.API_HTTP_CODE_NO_PERMISSION, message='公有公式不允许删除').to_response()
        if formula.user_id != request.user.id:
            return BackstageHTTPResponse(code=BackstageHTTPResponse.API_HTTP_CODE_NO_PERMISSION, message='该公式不属于您').to_response()

        formula_varieties = FormulaVarieties.objects.filter(
            formula_id=id,
            varieties_id=varieties_id
        ).first()
        if formula_varieties:
            formula_varieties.delete()

        return BackstageHTTPResponse(
            code=BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
        ).to_response()

