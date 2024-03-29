#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@date: 2016-06-13

@author: Devin
"""
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from com_interface.views import stalist

urlpatterns = [
    url(r'^$', stalist.StalistView.as_view()),
    # url(r'^(?P<pk>\S+)$', page_list.NewsView.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
