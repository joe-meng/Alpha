# coding: utf-8
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from capital.views import ExchangeCapitalView, ProductCapitalView,\
    VarietyCapitalView, TodayVarietyCapitalView

urlpatterns = [
    url(r'^exchange$', ExchangeCapitalView.as_view()),
    url(r'^product', ProductCapitalView.as_view()),
    url(r'^variety', VarietyCapitalView.as_view()),
    url(r'^today', TodayVarietyCapitalView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
