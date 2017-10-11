from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from ..views import his_list

urlpatterns = [
    url(r'^$', his_list.AlertHistoryTitleView.as_view()),
    # url(r'^(?P<pk>\S+)$', live.LiveView.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)