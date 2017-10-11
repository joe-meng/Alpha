# encoding: utf-8
import uuid
from secrets import token_hex
from urllib.parse import urlencode, unquote, urlparse, urlunparse

import logging

import re
import requests
import time
from django.conf import settings
from django.contrib.auth import login
from django.contrib.sessions.models import Session
from django.http import QueryDict
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.status import HTTP_302_FOUND
from rest_framework.views import APIView
from wechatpy import WeChatClient, WeChatOAuth
from wechatpy import parse_message
from wechatpy.client.api import WeChatJSAPI

from common.models import BackstageHTTPResponse
from common.utils import log_exception
from enums import WechatQRScanResultCode
from user.models import User, InvitationCode
from wechat.models import WechatQR, WechatUser
from wechat.serializers import WechatQRSerializer


logger = logging.getLogger("wechat")


def generate_temp_scene_str():
    return str(uuid.uuid4()).replace('-', '')


class AlphaWeChatClient(WeChatClient):
    @property
    def access_token(self):
        return self.fetch_access_token()

    def fetch_access_token(self):
        resp = requests.get(settings.WECHAT_GET_ACCESS_TOKEN_URL, {'appId': settings.WECHAT_APPID, 'secret': settings.WECHAT_APPSECRET})
        if resp.json()['code'] != '000000':
            logger.error('%s access_token 返回错误: %s' % (settings.WECHAT_GET_ACCESS_TOKEN_URL, resp.json()))
            return ''
        else:
            return resp.json()['data']


class WechatPushHandler(APIView):
    """
    接收微信服务号的事件推送
    """

    @log_exception
    def post(self, request, *args, **kwargs):
        """
        处理微信事件推送
        ---
        """
        msg = parse_message(request.body)
        logger.info('收到微信事件推送: %s' % msg)
        openid = msg.source

        client = AlphaWeChatClient(settings.WECHAT_APPID, settings.WECHAT_APPSECRET)
        wechat_user = client.user.get(openid)
        WechatUser.objects.update_or_create(openid=openid, defaults=wechat_user)

        if msg.event == 'unsubscribe':
            user = User.objects.filter(openid=openid).first()
            if user:
                session_list = []
                for session in Session.objects.all():
                    try:
                        if session.get_decoded()['_auth_user_id'] == str(user.id):
                            session_list.append(session.pk)
                    except Exception:
                        pass
                logger.info('logging out user %s' % user.id)
                if session_list:
                    Session.objects.filter(pk__in=session_list).delete()
            return Response('')

        if msg.event not in ('subscribe_scan', 'scan'):
            # subscribe_scan 未关注用户扫描带参数二维码事件
            # scan 已关注用户扫描带参数二维码事件
            logger.info('不是扫描二维码事件,返回: event:%s' % msg.event)
            return Response('')

        qr = WechatQR.objects.filter(scene_str=msg.scene_id, openid=None, expire_at__gte=timezone.now()).first()
        if not qr:
            logger.error('未找到 scene_str: %s' % msg.scene_id)
            return Response('')

        logger.info('找到 scene_str: %s, 更新其 openid 为: %s' % (msg.scene_id, openid))
        qr.openid = openid

        if len(msg.scene_id) != 32:
            # 已经弃用，现在只有 scene_id 是 uuid 的情况
            # scene_id 是手机号的话是注册新用户请求
            user = User.objects.filter(openid=openid).first()
            if user:
                # 如果微信已绑定其他手机号，不允许重复绑定，返回失败
                if user.mobile != msg.scene_id:
                    logger.info('该 openid: %s 已绑定其他手机号: %s，不允许重复绑定，返回失败' % (openid, user.mobile))
                    qr.scan_result = WechatQRScanResultCode.ALREADY_BOUND.value
                else:
                    # 如果微信已绑定该手机号，不允许重复绑定，返回失败
                    logger.info('该 openid: %s 已绑定该手机: %s，无需重复绑定，返回成功' % (openid, user.mobile))
                    qr.scan_result = WechatQRScanResultCode.SUCCESS.value
            else:
                # 注册新用户
                logger.info('为 openid: %s 生成新用户，并绑定到手机号 %s，返回成功' % (openid, msg.scene_id))
                user = User(
                    openid=openid,
                    username=msg.scene_id,
                    mobile=msg.scene_id,
                )
                if qr.invitation_code:
                    user.invitation_code = qr.invitation_code
                user.save()
                qr.scan_result = WechatQRScanResultCode.SUCCESS.value

        elif len(msg.scene_id) == 32:
            # scene_id 是 uuid 的话是登录请求
            user = User.objects.filter(openid=openid).first()
            if not user:
                # 未注册自动生成新用户
                user = User(
                    openid=openid,
                    username=openid,
                )
                user.save()
                user.create_default_subscriptions(logger)

            user.update_wechat_mobile(logger=logger)
            if not user.mobile:
                # 未绑定手机号
                qr.scan_result = WechatQRScanResultCode.NOT_REAL_NAMED.value
                user.send_wechat_template_bind_mobile(client)
            else:
                # 已绑定手机号，返回成功
                qr.scan_result = WechatQRScanResultCode.SUCCESS.value

            # 如果没有邀请码，更新其邀请码
            if not user.invitation_code:
                user.invitation_code = qr.invitation_code
                user.save()

        qr.save()

        # 给新用户发送 绑定手机号 模板信息
        return Response('')


class WechatQRListAPI(APIView):

    @log_exception
    def post(self, request, *args, **kwargs):
        """
        向微信请求带参数二维码，用于用户扫码登录
        ---
        parameters:
            - name: scene_str
              description: 注册时填用户手机号，登录时不用传
              type: string
              paramType: form
              required: false
            - name: invitation_code
              description: 邀请码
              type: string
              paramType: form
              required: false
        """
        scene_str = request.data.get('scene_str', '')
        invitaion_code_str = request.data.get('invitation_code', None)
        invitaion_code = InvitationCode.objects.filter(code=invitaion_code_str).first()
        logger.info('invitation_code: %s' % invitaion_code_str)

        # 传手机号表示注册
        if len(scene_str) == 11 and scene_str.isdigit():
            mobile = scene_str
            # 注册必须要 invitation_code
            if not invitaion_code:
                return BackstageHTTPResponse(
                    code=BackstageHTTPResponse.API_HTTP_CODE_INVILID_PARAMS,
                    message='邀请码错误',
                ).to_response()

            user = User.objects.filter(mobile=mobile).first()
            if user:
                # 已经是注册用户的话
                # 如果没有邀请码，为其保存邀请码
                # 如果有邀请码，不修改其邀请码
                logger.info('用户表中检测到手机号: %s 存在' % mobile)
                if user.invitation_code is None:
                    logger.info('手机号为 %s 的用户没有邀请码，更新其邀请码为 %s' % (mobile, invitaion_code.code))
                    user.invitation_code = invitaion_code.code
                    user.save()
                else:
                    logger.info('手机号为 %s 的用户已有邀请码，不为其更新邀请码' % mobile)
                # 随机生成新的 scene_str，表示登录
                scene_str = generate_temp_scene_str()

        # 没有传 scene_str 或者没有找到用户的话，随机生成一个新的表示登录
        if not scene_str:
            scene_str = generate_temp_scene_str()

        client = AlphaWeChatClient(settings.WECHAT_APPID, settings.WECHAT_APPSECRET)
        expire_seconds = settings.WECHAT_QR_EXPIRE_SECONDS
        action_name = 'QR_STR_SCENE'

        qr = WechatQR.objects.filter(scene_str=scene_str, expire_at__gte=timezone.now()).first()
        if not qr:
            logger.info('向微信请求生成二维码，参数: %s' % scene_str)
            res = client.qrcode.create({
                'expire_seconds': expire_seconds,
                'action_name': action_name,
                'action_info': {
                    'scene': {
                        'scene_str': scene_str,
                    },
                }
            })
            logger.info('向微信请求生成二维码, 返回: %s' % res)
            image_url = 'https://mp.weixin.qq.com/cgi-bin/showqrcode?%s' % urlencode({'ticket': res['ticket']})
            qr = WechatQR(
                expire_seconds=expire_seconds,
                action_name=action_name,
                ticket=res['ticket'],
                url=res['url'],
                image_url=image_url,
                scene_str=scene_str,
            )
            if invitaion_code:
                qr.invitation_code = invitaion_code.code
            qr.save()

        return BackstageHTTPResponse(
            code=BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
            data=WechatQRSerializer(qr).data
        ).to_response()


class WechatQRDetailAPI(APIView):

    @log_exception
    def get(self, request, scene_str):
        """
        向微信请求带参数二维码，用于用户扫码登录
        ---
        parameters:
            - name: scene_str
              description: 注册时填用户手机号，登录时不用传
              type: string
              paramType: path
              required: true
        """
        qr = WechatQR.objects.filter(scene_str=scene_str).first()
        if not qr:
            return BackstageHTTPResponse(
                code=BackstageHTTPResponse.API_HTTP_CODE_NOT_FOUND,
            ).to_response()

        serializer = WechatQRSerializer(qr)
        if qr.openid:
            user = User.objects.filter(openid=qr.openid, is_active=True).first()
            if user:
                user.update_wechat_mobile(logger=logger)
                login(request, user)
        return BackstageHTTPResponse(
            code=BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
            data=serializer.data
        ).to_response()


class WechatJSParams(APIView):

    @log_exception
    def post(self, request):
        """
        对接微信 JS SDK 需要的数据
        ---
        parameters:
            - name: url
              description: 请求页面 url
              type: string
              paramType: form
              required: true
        """
        url = request.data.get('url', '')
        if not url:
            return BackstageHTTPResponse(
                code=BackstageHTTPResponse.API_HTTP_CODE_INVILID_PARAMS,
                message='url 错误',
            ).to_response()
        url = unquote(url)
        timestamp = int(time.time())
        client = AlphaWeChatClient(settings.WECHAT_APPID, settings.WECHAT_APPSECRET)
        js_api = WeChatJSAPI(client)
        nonceStr = token_hex(12)
        ticket = js_api.get_ticket()['ticket']
        data = {
            'appId': settings.WECHAT_APPID,
            'timestamp': timestamp,
            'nonceStr': nonceStr,
            'signature': js_api.get_jsapi_signature(nonceStr, ticket, timestamp, url),
        }
        return BackstageHTTPResponse(
            code=BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
            data=data
        ).to_response()


class WechatOAuth2_CodeHandler(APIView):
    """
    处理网页 oauth2 带 code 授权
    """

    @log_exception
    def get(self, request):
        """
        处理微信事件推送
        ---
        parameters:
            - name: code
              description: 授权码
              type: string
              paramType: query
              required: true
            - name: invitation_code
              description: 邀请码
              type: string
              paramType: query
              required: false
            - name: url
              description: 跳转前端 url
              type: string
              paramType: query
              required: true
        """
        invitation_code = request.GET.get('invitation_code', '')
        invitation_code = InvitationCode.objects.filter(code=invitation_code).first()
        redirect_url = request.GET.get('url', '')
        oauth_code = request.GET.get('code', '')
        redirect_url_parts = list(urlparse(redirect_url))

        if not redirect_url:
            return BackstageHTTPResponse(
                code=BackstageHTTPResponse.API_HTTP_CODE_INVILID_PARAMS,
                message='缺少跳转url',
            ).to_response()
        if not oauth_code:
            return BackstageHTTPResponse(
                code=BackstageHTTPResponse.API_HTTP_CODE_INVILID_PARAMS,
                message='缺少授权码',
            ).to_response()
        oauth = WeChatOAuth(settings.WECHAT_APPID, settings.WECHAT_APPSECRET, redirect_url)
        oauth.fetch_access_token(oauth_code)
        wechat_user = oauth.get_user_info()
        WechatUser.objects.update_or_create(
            openid=oauth.open_id,
            defaults=wechat_user
        )
        user = User.objects.filter(openid=oauth.open_id, is_active=True).first()
        if not user:
            url = settings.A3_FE_REGISTER_URL
            url += '?invitation_code=%s&openid=%s' % (getattr(invitation_code, 'code', ''), oauth.open_id)
            return Response(status=HTTP_302_FOUND, headers={'Location': url})

        logger.info('redirect_url_parts: %s' % redirect_url_parts)
        new_query_dict = QueryDict('', mutable=True)
        original_url_path = re.findall(r'([^?]*)(?:\?.*)?', redirect_url_parts[5])[0]
        if '?' in redirect_url_parts[5]:
            original_url_query = re.findall(r'\?(.*)', redirect_url_parts[5])[0]
            new_query_dict.update(QueryDict(original_url_query, mutable=True))
        if user:
            user.update_wechat_mobile(logger=logger)
            login(request, user)
            # 微信不允许跨域携带 cookie，通过 header 来传 session_key
            new_query_dict.update({'session_id': request.session.session_key})
        if invitation_code:
            new_query_dict.update({'invitation_code': invitation_code.code,})
        new_query_dict.update({'openid': oauth.open_id})
        if redirect_url_parts[2].strip('/'):
            redirect_url_parts[2] = redirect_url_parts[2] + '#%s' % original_url_path
        else:
            redirect_url_parts[2] = '/#%s' % original_url_path
        redirect_url_parts[4] = new_query_dict.urlencode()
        redirect_url_parts[5] = ''
        redirect_url = urlunparse(redirect_url_parts)
        return Response(status=HTTP_302_FOUND, headers={'Location': redirect_url})


