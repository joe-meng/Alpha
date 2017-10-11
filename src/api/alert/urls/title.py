from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from ..views import title

urlpatterns = [
    url(r'^$', title.AlertTitleView.as_view()),
    # url(r'^(?P<pk>\S+)$', live.LiveView.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)