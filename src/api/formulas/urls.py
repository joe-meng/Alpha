# -- coding: utf-8 --

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from formulas.run import FormulaExecuteView
from formulas.views import FormulasListAPI, FormulaFunctionsListAPI, FormulasDetailAPI, FormulasTemplateAPI, \
    FormulaVarietiesDetailAPI

urlpatterns = [
    url(r'^$', FormulasListAPI.as_view()),
    url(r'^template/$', FormulasTemplateAPI.as_view()),
    url(r'^(?P<id>[0-9]+)/$', FormulasDetailAPI.as_view()),
    url(r'^(?P<id>[0-9]+)/varieties/(?P<varieties_id>[0-9]+)/$',     FormulaVarietiesDetailAPI.as_view()),
    url(r'^functions/', FormulaFunctionsListAPI.as_view()),
    url(r'^execute/', FormulaExecuteView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
