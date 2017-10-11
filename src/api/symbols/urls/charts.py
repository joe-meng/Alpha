# coding: utf-8
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from symbols.views.charts import TableDataListView


urlpatterns = [
    url(r'^$', TableDataListView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
