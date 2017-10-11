# coding: utf-8
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from chart.views import ChartListView, ChartView, ChartLineView


urlpatterns = [
    url(r'^batch$', ChartListView.as_view()),
    url(r'^$', ChartView.as_view()),
    url(r'^line$', ChartLineView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
