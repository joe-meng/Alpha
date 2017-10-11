# coding: utf-8
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from sidebar.views import VarietyView, SidebarView, SidebarOrderView, SidebarChartsView, SidebarChartsOrderView


urlpatterns = [
    url(r'^variety$', VarietyView.as_view()),
    url(r'^$', SidebarView.as_view()),
    url(r'^order$', SidebarOrderView.as_view()),
    url(r'^chart$', SidebarChartsView.as_view()),
    url(r'^chart_order$', SidebarChartsOrderView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
