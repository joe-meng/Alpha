# coding: utf-8
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from varieties.views import SidebarTableDataHandler, VarietiesDetailHandler

urlpatterns = [
    url(r'^(?P<chart_variety>\S+)/sidebar/(?P<sidebar>\S+)/table/', SidebarTableDataHandler.as_view()),
    url(r'^(?P<id>\d+)/', VarietiesDetailHandler.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)



