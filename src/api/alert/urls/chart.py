from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from ..views import chart

urlpatterns = [
    url(r'^$', chart.AlertHistoryChartView.as_view()),
    # url(r'^(?P<pk>\S+)$', live.LiveView.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)