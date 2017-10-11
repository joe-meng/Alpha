#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@date: 2016-06-13

@author: Devin
"""
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from ..views import news

urlpatterns = [
    url(r'^$', news.NewsViewList.as_view()),
    url(r'^(?P<pk>\S+)$', news.NewsView.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
