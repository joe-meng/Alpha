import logging
import oss2
import uuid
from django.contrib.auth import login, logout
from django.core.paginator import Paginator
from django.db.models import Q, Exists, OuterRef, Subquery
from django.conf import settings

from formulas.models import Formula, FormulaVarieties
from formulas.serializers import FormulaSerializerWithSubscription
from user.models import User, FormulaSubscription, VarietiesSubscription, InvitationCode, \
    UserFeedback
from user.serializers import UserSerializer, FormulaSubscriptionSerializer, VarietiesSubscriptionSerializer, \
    InvitationCodeSerializer, UserFeedbackSerializer, InvitationCodeWithUserSerializer
from rest_framework.views import APIView

from common.models import BackstageHTTPResponse
from common.utils import log_exception
from varieties.models import VarietiesRecord
from varieties.serializers import VarietiesRecordSerializerWithSubscription


class UserCurrentAPI(APIView):

    @log_exception
    def get(self, request, *args, **kwargs):
        """
        获取当前用户信息
        ---
        """
        if not request.user.id:
            return BackstageHTTPResponse(code=BackstageHTTPResponse.API_HTTP_CODE_NOT_LOGIN_ERR).to_response()

        request.user.update_wechat_mobile()
        data = UserSerializer(request.user).data
        return BackstageHTTPResponse(
            code=BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
            data=data,
        ).to_response()

    @log_exception
    def patch(self, request, *args, **kwargs):
        """
        修改当前用户
        ---
        parameters:
            - name: head_img
              description: 图片
              type: file
              paramType: form
              required: false
            - name: display_name
              description: 昵称
              type: string
              paramType: form
              required: false
            - name: introduction
              description: 简介
              type: string
              paramType: form
              required: false
        """
        if not request.user.id:
            return BackstageHTTPResponse(code=BackstageHTTPResponse.API_HTTP_CODE_NOT_LOGIN_ERR).to_response()

        head_img = request.data.get('head_img', None)
        display_name = request.data.get('display_name', None)
        introduction = request.data.get('introduction', None)

        if head_img:
            auth = oss2.Auth(settings.ALI_OSS_ACCESS_KEY_ID, settings.ALI_OSS_ACCESS_KEY_SECRET)
            bucket = oss2.Bucket(auth, settings.ALI_OSS_ENDPOINT, settings.ALI_OSS_BUCKET_NAME)

            remote_file_name = '%s.%s' % (uuid.uuid4().hex, head_img.name.split('.')[-1])
            res = bucket.put_object(remote_file_name, head_img)
            logging.info('上传到阿里云, 文件名: %s, 请求id: %s, 返回状态: %s' % (remote_file_name, res.request_id, res.status))
            remote_url = ''.join([settings.FATHER_URL, remote_file_name])
            request.user.head_img = remote_url
        if display_name:
            request.user.display_name = display_name
        if introduction:
            request.user.introduction = introduction
        request.user.save()

        data = UserSerializer(request.user).data
        return BackstageHTTPResponse(
            code=BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
            data=data,
        ).to_response()


class UserLoginAPI(APIView):

    @log_exception
    def post(self, request, *args, **kwargs):
        """
        用户登录
        ---
        parameters:
            - name: username
              description: 用户名
              type: string
              paramType: form
              required: true
            - name: password
              description: 密码
              type: string
              paramType: form
              required: true
        """
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        if not username or not password:
            return BackstageHTTPResponse(code=BackstageHTTPResponse.API_HTTP_CODE_LOGIN_ERR).to_response()
        user = User.objects.filter(username=username).first()
        if not user:
            return BackstageHTTPResponse(code=BackstageHTTPResponse.API_HTTP_CODE_LOGIN_ERR).to_response()
        if not user.check_password(password):
            return BackstageHTTPResponse(code=BackstageHTTPResponse.API_HTTP_CODE_LOGIN_ERR).to_response()
        login(request, user)
        return BackstageHTTPResponse(
            code=BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
            data=UserSerializer(user).data
        ).to_response()


class UserUpdateAPI(APIView):

    @log_exception
    def post(self, request, *args, **kwargs):
        """
        和 qian.useonline.cn 同步手机信息
        ---
        """
        if not request.user.is_authenticated:
            return BackstageHTTPResponse(code=BackstageHTTPResponse.API_HTTP_CODE_NOT_LOGIN_ERR).to_response()
        request.user.update_wechat_mobile()
        serializer = UserSerializer(request.user)
        return BackstageHTTPResponse(
            code=BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
            data=serializer.data
        ).to_response()


class UserSubscriptionFormulaListAPI(APIView):

    @log_exception
    def get(self, request, *args, **kwargs):
        """
        用户的公式订阅情况
        ---
        parameters:
            - name: varieties_id
              description: 品类 id
              type: integer
              paramType: query
              required: false
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
        if not request.user.id:
            return BackstageHTTPResponse(code=BackstageHTTPResponse.API_HTTP_CODE_NOT_LOGIN_ERR).to_response()

        varieties_id = request.GET.get('varieties_id', None)
        formulas = Formula.objects.filter(Q(user_id=None) | Q(user_id=request.user.id))
        if varieties_id:
            formulas = formulas.filter(
                id__in=FormulaVarieties.objects.filter(varieties_id=varieties_id).values_list('formula_id', flat=True))

        formulas = formulas.annotate(
            subscribed=Exists(
                FormulaSubscription.objects.filter(
                    user_id=self.request.user.id,
                    formula_id=OuterRef('id'),
                    varieties_id=varieties_id
                )
            ),
            subscription_id=Subquery(
                FormulaSubscription.objects.filter(
                    user_id=self.request.user.id,
                    formula_id=OuterRef('id'),
                    varieties_id=varieties_id
                ).values('id')[:1]
            ),
        ).order_by('-created_at')

        paginator = Paginator(formulas, request.GET.get('number', 100))
        page = paginator.page(request.GET.get('index', 1))
        serializer = FormulaSerializerWithSubscription(page, many=True)

        return BackstageHTTPResponse(
            code=BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
            data=serializer.data,
            pageinfo=page
        ).to_response()

    @log_exception
    def post(self, request, *args, **kwargs):
        """
        订阅公式
        ---
        parameters:
            - name: formula_id
              description: 公式 id
              type: string
              paramType: form
              required: true
            - name: varieties_id
              description: 品目 id
              type: string
              paramType: form
              required: true
        """
        if not request.user.id:
            return BackstageHTTPResponse(code=BackstageHTTPResponse.API_HTTP_CODE_NOT_LOGIN_ERR).to_response()

        formula_id = request.data.get('formula_id', None)
        varieties_id = request.data.get('varieties_id', None)
        if not formula_id or not varieties_id:
            return BackstageHTTPResponse(code=BackstageHTTPResponse.API_HTTP_CODE_INVILID_PARAMS).to_response()

        formula = Formula.objects.filter(id=formula_id).first()
        varieties = VarietiesRecord.objects.filter(id=varieties_id).first()
        if not formula or not varieties:
            return BackstageHTTPResponse(code=BackstageHTTPResponse.API_HTTP_CODE_NOT_FOUND).to_response()

        formula = Formula.objects.filter(Q(user_id=request.user.id)|Q(user_id=None), id=formula_id).first()
        if not formula:
            return BackstageHTTPResponse(code=BackstageHTTPResponse.API_HTTP_CODE_NO_PERMISSION).to_response()

        if not FormulaVarieties.objects.filter(varieties_id=varieties_id, formula_id=formula_id):
            return BackstageHTTPResponse(
                code=BackstageHTTPResponse.API_HTTP_CODE_INVILID_PARAMS,
                message='公式和品类不匹配',
            ).to_response()

        subscription = FormulaSubscription.objects.filter(user_id=request.user.id, formula_id=formula_id, varieties_id=varieties_id).first()
        if not subscription:
            subscription = FormulaSubscription(
                user_id=request.user.id,
                formula_id=formula_id,
                varieties_id=varieties_id,
            )
            subscription.save()

        serializer = FormulaSubscriptionSerializer(subscription)
        return BackstageHTTPResponse(
            code=BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
            data=serializer.data,
        ).to_response()


class UserSubscriptionFormulaDetailAPI(APIView):

    @log_exception
    def delete(self, request, formula_id, varieties_id):
        """
        取消订阅公式
        ---
        parameters:
            - name: formula_id
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

        subscription = FormulaSubscription.objects.filter(
            user_id=request.user.id,
            formula_id=formula_id,
            varieties_id=varieties_id
        ).first()
        if subscription:
            subscription.delete()

        return BackstageHTTPResponse(
            code=BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
        ).to_response()


class UserSubscriptionVarietiesListAPI(APIView):

    @log_exception
    def get(self, request):
        """
        用户的品类订阅情况
        ---
        """
        if not request.user.id:
            return BackstageHTTPResponse(code=BackstageHTTPResponse.API_HTTP_CODE_NOT_LOGIN_ERR).to_response()

        varieties = VarietiesRecord.objects.all()
        varieties = varieties.annotate(
            subscribed=Exists(
                VarietiesSubscription.objects.filter(
                    user_id=self.request.user.id,
                    varieties_id=OuterRef('id')
                )
            ),
            subscription_id=Subquery(
                VarietiesSubscription.objects.filter(
                    user_id=self.request.user.id,
                    varieties_id=OuterRef('id')
                ).values('id')[:1]
            ),
        ).order_by('-subscribed', 'short_name')
        for variety in varieties:
            variety.count = FormulaSubscription.objects.filter(user_id=request.user.id, varieties_id=variety.id).count()

        paginator = Paginator(varieties, request.GET.get('number', 100))
        page = paginator.page(request.GET.get('index', 1))
        serializer = VarietiesRecordSerializerWithSubscription(page, many=True)

        return BackstageHTTPResponse(
            code=BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
            data=serializer.data,
            pageinfo=page
        ).to_response()

    @log_exception
    def post(self, request, *args, **kwargs):
        """
        订阅品类
        ---
        parameters:
            - name: varieties_id
              description: 品目 id
              type: string
              paramType: form
              required: true
        """
        if not request.user.id:
            return BackstageHTTPResponse(code=BackstageHTTPResponse.API_HTTP_CODE_NOT_LOGIN_ERR).to_response()

        varieties_id = request.data.get('varieties_id', None)
        if not varieties_id:
            return BackstageHTTPResponse(code=BackstageHTTPResponse.API_HTTP_CODE_INVILID_PARAMS).to_response()

        varieties = VarietiesRecord.objects.filter(id=varieties_id).first()
        if not varieties:
            return BackstageHTTPResponse(code=BackstageHTTPResponse.API_HTTP_CODE_NOT_FOUND).to_response()

        subscription = VarietiesSubscription.objects.filter(user_id=request.user.id, varieties_id=varieties_id).first()
        if not subscription:
            subscription = VarietiesSubscription(
                user_id=request.user.id,
                varieties_id=varieties_id,
            )
            subscription.save()

        serializer = VarietiesSubscriptionSerializer(subscription)
        return BackstageHTTPResponse(
            code=BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
            data=serializer.data,
        ).to_response()


class UserSubscriptionVarietiesDetailAPI(APIView):

    @log_exception
    def delete(self, request, id):
        """
        取消订阅品类
        ---
        parameters:
            - name: id
              description: 品类 id
              type: integer
              paramType: path
              required: true
        """
        if not request.user.id:
            return BackstageHTTPResponse(code=BackstageHTTPResponse.API_HTTP_CODE_NOT_LOGIN_ERR).to_response()

        subscription = VarietiesSubscription.objects.filter(user_id=request.user.id, varieties_id=id).first()
        if subscription:
            subscription.delete()

        return BackstageHTTPResponse(
            code=BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
        ).to_response()


class UserWechatOpenidCheckAPI(APIView):

    @log_exception
    def get(self, request, openid):
        """
        检查微信 openid 是否已注册
        ---
        parameters:
            - name: openid
              description: 微信 openid
              type: string
              paramType: path
              required: true
        responseMessages:
            - code: 200
              message: 已注册
            - code: 404
              message: 未注册
        """
        user = User.objects.filter(openid=openid).first()
        if not user:
            return BackstageHTTPResponse(
                code=BackstageHTTPResponse.API_HTTP_CODE_NOT_FOUND,
                message='用户未注册'
            ).to_response()
        return BackstageHTTPResponse(
            code=BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
            message='用户已注册'
        ).to_response()


class UserDefaultInvitationCodeAPI(APIView):

    @log_exception
    def get(self, request):
        """
        获取用户默认邀请码
        ---
        """
        if not request.user.id:
            return BackstageHTTPResponse(code=BackstageHTTPResponse.API_HTTP_CODE_NOT_LOGIN_ERR).to_response()

        ic = InvitationCode.objects.filter(user_id=request.user.id, default=True).first()
        if not ic:
            return BackstageHTTPResponse(
                code=BackstageHTTPResponse.API_HTTP_CODE_NOT_FOUND,
                message='用户没有默认邀请码'
            ).to_response()

        serializer = InvitationCodeSerializer(ic)
        return BackstageHTTPResponse(
            code=BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
            data=serializer.data
        ).to_response()


class UserFeedbackAPI(APIView):

    @log_exception
    def post(self, request, *args, **kwargs):
        """
        提交意见反馈
        ---
        parameters:
            - name: content
              description: 反馈内容
              type: string
              paramType: form
              required: true
            - name: contact
              description: 联系方式
              type: string
              paramType: form
              required: false
        """
        content = request.data.get('content', None)
        contact = request.data.get('contact', None)
        if not content:
            return BackstageHTTPResponse(code=BackstageHTTPResponse.API_HTTP_CODE_FEEDBACK_CONTENT_NOT_EMPTY).to_response()

        feedback = UserFeedback(content=content, contact=contact)
        feedback.save()

        return BackstageHTTPResponse(
            code=BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
            data=UserFeedbackSerializer(feedback).data
        ).to_response()


class InvitationCodeDetailAPI(APIView):

    @log_exception
    def get(self, request, code, *args, **kwargs):
        """
        邀请码信息
        ---
        parameters:
            - name: code
              description: 邀请码
              type: string
              paramType: path
              required: true
        """
        invitation_code = InvitationCode.objects.filter(code=code).first()
        if not invitation_code:
            return BackstageHTTPResponse(code=BackstageHTTPResponse.API_HTTP_CODE_NOT_FOUND).to_response()

        serializer = InvitationCodeWithUserSerializer(invitation_code)
        return BackstageHTTPResponse(
            code=BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
            data=serializer.data
        ).to_response()


class UserLogoutAPI(APIView):

    @log_exception
    def get(self, request, *args, **kwargs):
        """
        用户登出
        ---
        """
        logout(request)
        return BackstageHTTPResponse(
            code=BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
        ).to_response()
