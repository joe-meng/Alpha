# coding: utf-8
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from wechat.views import WechatPushHandler, WechatQRListAPI, WechatQRDetailAPI, WechatJSParams, WechatOAuth2_CodeHandler

urlpatterns = [
    url(r'^qr/$',                       WechatQRListAPI.as_view()),
    url(r'^qr/(?P<scene_str>\S+)/$',    WechatQRDetailAPI.as_view()),
    url(r'^push-handler/',              WechatPushHandler.as_view()),
    url(r'^js-params/',                 WechatJSParams.as_view()),
    url(r'^oauth2/code/',               WechatOAuth2_CodeHandler.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
