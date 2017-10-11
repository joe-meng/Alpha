"""alpha URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import os
import logging
from django.conf.urls import include, url
from django.contrib import admin

from common.views import AlphaSwaggerSchemaView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
]


urlpatterns += [
    url(r'^api/1/news/', include('backstage.urls.news', namespace="news")),

    url(r'^api/1/live/', include('backstage.urls.live', namespace="live")),

    url(r'^api/1/top_tag/', include('backstage.urls.manual_tags', namespace="top_tag")),
    url(r'^api/1/taglist/', include('backstage.urls.tags', namespace="tags")),

    url(r'^api/1/file_upload/', include('backstage.urls.file_upload', namespace="file_upload")),

    url(r'^api/1/login/', include('backstage.urls.login', namespace="login")),

    url(r'^api/1/keys/', include('common.urls', namespace="keys")),


    url(r'^news/news/', include('com_interface.urls.news', namespace="out_news")),

    url(r'^news/live/', include('com_interface.urls.live', namespace="out_live")),

    url(r'^news/pagelist', include('com_interface.urls.page_list', namespace="pagelist")),

    url(r'^news/daylist', include('com_interface.urls.day_list', namespace="daylist")),

    url(r'^news/list', include('com_interface.urls.page_list', namespace="list")),

    url(r'^news/stalist', include('com_interface.urls.stalist', namespace="stalist")),

    url(r'^news/detail/', include('com_interface.urls.detail', namespace="detail")),

    url(r'^news/types', include('com_interface.urls.types', namespace="types")),

    url(r'^news/tags', include('com_interface.urls.tags', namespace="tags")),

    url(r'^alert/alert', include('alert.urls.alert', namespace="alert")),

    url(r'^alert/title', include('alert.urls.title', namespace="title")),

    url(r'^alert/chart', include('alert.urls.chart', namespace="title")),

    url(r'^alert/history', include('alert.urls.his_list', namespace="history")),

    url(r'^alert/variety', include('alert.urls.variety_map', namespace="variety")),

    url(r'^alert/recent_day', include('alert.urls.recent_day', namespace="recent_day")),

    url(r'^alert/ai_varieties', include('alert.urls.ai_varieties', namespace="ai_varieties")),

    url(r'^alert/attention', include('alert.urls.attention', namespace="attention")),

    url(r'^alert/prediction', include('alert.urls.prediction', namespace="prediction")),

    url(r'^alert/prediction_record', include('alert.urls.prediction_record', namespace="prediction_record")),

    url(r'^alert/quotes', include('alert.urls.quotes', namespace="quotes")),

    url(r'^alert/victor_percent', include('alert.urls.victor_percent', namespace="victor_percent")),

    url(r'^alert/view_res', include('alert.urls.view_res', namespace="view_res")),

    url(r'^alert/ai_prediction', include('alert.urls.ai_prediction', namespace="ai_prediction")),

    url(r'^symbol/chart', include('symbols.urls.chart', namespace="symbol")),
    url(r'^symbol/charts', include('symbols.urls.charts', namespace="symbol")),
    url(r'^chart/variety', include('chart.urls.variety', namespace="chart")),
    url(r'^chart/sidebar', include('chart.urls.sidebar', namespace="chart")),
    url(r'^chart/sidebar_order', include('chart.urls.sidebar_order', namespace="chart")),
    url(r'^chart/sidebar_charts', include('chart.urls.sidebar_charts', namespace="chart")),
    url(r'^chart/sidebar_charts_order', include('chart.urls.sidebar_charts_order', namespace="chart")),
    url(r'^chart/chart', include('chart.urls.chart', namespace="chart")),
    url(r'^chart/chart_list', include('chart.urls.chart_list', namespace="chart")),
    url(r'^chart/lines', include('chart.urls.line', namespace="chart")),
    url(r'^capital/', include('capital.urls', namespace="capital")),
    url(r'^data/', include('symbols.urls.latest', namespace="data")),
    # url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^docs/', AlphaSwaggerSchemaView.as_view()),
]

urlpatterns += [
    url(r'^formula/',   include('formulas.urls', namespace="formula")),
    url(r'^symbol/',    include('symbols.urls', namespace="symbol")),
    url(r'^user/',      include('user.urls', namespace="user")),
    url(r'^wechat/',    include('wechat.urls', namespace="wechat")),
    # 表格数据
    url(r'^varieties/', include('varieties.urls', namespace='varieties')),
    url(r'^tables/',    include('tables.urls', namespace='tables')),
]


