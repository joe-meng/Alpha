#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@date: 2016-06-13

@author: Devin
"""
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from backstage.views import manual_tags

urlpatterns = [
    url(r'^$', manual_tags.TagListView.as_view()),
    url(r'^(?P<pk>\S+)$', manual_tags.TagView.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
