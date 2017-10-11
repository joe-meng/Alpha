# coding: utf-8
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from symbols.views import SymbolListAPI, TableListAPI, SymbolClassificationListAPI

urlpatterns = [
    url(r'^$', SymbolListAPI.as_view()),
    url(r'^tables$', TableListAPI.as_view()),
    url(r'^classifications/(?P<classification>\d+)/$', SymbolClassificationListAPI.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
