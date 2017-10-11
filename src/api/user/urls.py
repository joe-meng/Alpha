# coding: utf-8
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from user.views import UserCurrentAPI, UserLoginAPI, UserSubscriptionFormulaListAPI, UserSubscriptionFormulaDetailAPI, \
    UserSubscriptionVarietiesListAPI, UserSubscriptionVarietiesDetailAPI, UserWechatOpenidCheckAPI, \
    UserDefaultInvitationCodeAPI, UserFeedbackAPI, InvitationCodeDetailAPI, UserUpdateAPI, UserLogoutAPI

urlpatterns = [
    url(r'^current/$',  UserCurrentAPI.as_view()),
    url(r'^login/$',    UserLoginAPI.as_view()),
    url(r'^logout/$',   UserLogoutAPI.as_view()),
    url(r'^update/$',   UserUpdateAPI.as_view()),
    url(r'^subscription/formulas/$',                    UserSubscriptionFormulaListAPI.as_view()),
    url(r'^subscription/formulas/(?P<formula_id>[0-9]+)/varieties/(?P<varieties_id>[0-9]+)/$',     UserSubscriptionFormulaDetailAPI.as_view()),
    url(r'^subscription/varieties/$',                   UserSubscriptionVarietiesListAPI.as_view()),
    url(r'^subscription/varieties/(?P<id>[0-9]+)/$',    UserSubscriptionVarietiesDetailAPI.as_view()),
    url(r'^wechat-openid/(?P<openid>\S+)/$',    UserWechatOpenidCheckAPI.as_view()),
    url(r'^invitation-code/default/$',          UserDefaultInvitationCodeAPI.as_view()),
    url(r'^invitation-code/(?P<code>\S+)/$',    InvitationCodeDetailAPI.as_view()),
    url(r'^feedback/', UserFeedbackAPI.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
