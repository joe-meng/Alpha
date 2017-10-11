# coding: utf-8
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from tables.views import TableListAPI, TableDetailAPI

urlpatterns = [
    url(r'^$',                 TableListAPI.as_view()),
    url(r'^(?P<id>[0-9]+)/$',    TableDetailAPI.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
