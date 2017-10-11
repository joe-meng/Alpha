# -- coding: utf-8 --
import django_filters

from tables.models import Tables


class TablesFilter(django_filters.FilterSet):

    class Meta:
        model = Tables
        fields = ['name', 'type']