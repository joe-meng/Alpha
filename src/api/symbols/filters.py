# -- coding: utf-8 --
import django_filters

from symbols.models import Symbol


class SymbolFilter(django_filters.FilterSet):

    class Meta:
        model = Symbol
        fields = ['table_name', 'symbol', 'classification_1', 'classification_2']