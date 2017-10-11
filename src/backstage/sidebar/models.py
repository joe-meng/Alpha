# -- coding: utf-8 --
from django.db import models


class Exchange(models.Model):

    exchange = models.CharField(max_length=45)
    exchange_name = models.CharField(max_length=45)

    class Meta:
        db_table = 'chart_exchange'


class Variety(models.Model):

    exchange = models.CharField(max_length=45)
    variety = models.CharField(max_length=45)
    variety_name = models.CharField(max_length=45)

    class Meta:
        db_table = 'chart_variety'


class Sidebar(models.Model):

    variety = models.CharField(max_length=45)
    name = models.CharField(max_length=45)
    priority = models.IntegerField(null=True)

    class Meta:
        db_table = 'chart_sidebar_copy'


class SidebarChart(models.Model):

    SIZE_ONE = 1
    SIZE_TWO = 2
    SIZE_CHOICES = ((SIZE_ONE, '跨一栏'), (SIZE_TWO, '跨两栏'))
    sidebar_id = models.IntegerField()
    chart_id = models.IntegerField()
    size = models.IntegerField(choices=SIZE_CHOICES)
    priority = models.IntegerField(null=True)
