from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from ..views import victor_percent

urlpatterns = [
    url(r'^$', victor_percent.VictorPercentView.as_view()),
    url(r'^list$', victor_percent.VictorPercentViewList.as_view()),
    # url(r'^(?P<pk>\S+)$', live.LiveView.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)