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


class Chart(models.Model):

    GRAPH_ONE = 1
    GRAPH_TWO = 2
    GRAPH_CHOICES = ((GRAPH_ONE, '线状图'), (GRAPH_TWO, '柱状图'))
    COMPARE_NORMAL = 1
    COMPARE_YEAR = 2
    COMPARE_MONTH = 3
    COMPARE_CHOICES = ((COMPARE_NORMAL, '不对比'), (COMPARE_YEAR, '年对比'), (COMPARE_MONTH, '月对比'))
    title = models.CharField(max_length=100)
    graph = models.IntegerField(choices=GRAPH_CHOICES)
    compare = models.IntegerField(choices=COMPARE_CHOICES)
    # 主轴显示
    p_axis = models.CharField(max_length=45)
    # 次轴显示
    s_axis = models.CharField(max_length=45)


class ChartLine(models.Model):

    AXIS_PRIMARY = 1
    AXIS_SECONDARY = 2
    AXIS_CHOICES = ((AXIS_PRIMARY, '主轴'), (AXIS_SECONDARY, '次轴'))
    chart_id = models.IntegerField()
    data_code = models.CharField(max_length=200)
    table_name = models.CharField(max_length=45)
    line_name = models.CharField(max_length=45)
    axis = models.IntegerField(choices=AXIS_CHOICES)

    class Meta:
        db_table = 'chart_line'
