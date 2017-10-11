#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

__author__ = 'daixf'

urlpatterns = [
    url(r'^codes/$', views.HTTPCodeListView.as_view()),
    url(r'^choices/$', views.ModelChoiceListView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

