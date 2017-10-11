# coding: utf-8
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from symbols.views.charts import LatestTableDataView, LatestTableDataListView


urlpatterns = [
    url(r'^latest$', LatestTableDataView.as_view()),
    url(r'^latest_list$', LatestTableDataListView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
