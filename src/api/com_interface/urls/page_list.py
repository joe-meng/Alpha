#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@date: 2016-06-13

@author: Devin
"""
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from com_interface.views import page_list

urlpatterns = [
    url(r'^$', page_list.PageListView.as_view()),
    # url(r'^(?P<pk>\S+)$', page_list.NewsView.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
