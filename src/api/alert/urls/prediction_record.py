from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from ..views import prediction_record

urlpatterns = [
    url(r'^$', prediction_record.PredictionRecordView.as_view()),
    url(r'^list$', prediction_record.PredictionRecordViewList.as_view()),
    # url(r'^(?P<pk>\S+)$', live.LiveView.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)