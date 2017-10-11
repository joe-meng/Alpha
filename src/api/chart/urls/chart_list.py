# coding: utf-8
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from chart.views import ChartListView


urlpatterns = [
    url(r'^$', ChartListView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
