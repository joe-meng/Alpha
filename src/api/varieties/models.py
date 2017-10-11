# encoding: utf-8
from django.db import models

from enums import FeeTypes
from model_mixins import VarietiesMixin, DateMixin, PriceRangeMixin, CreatedAtMixin, SourceMixin, \
    AlphaBaseMixin, SymbolMixin


class VarietiesRecord(AlphaBaseMixin):
    """
    品类
    """
    code = models.CharField('代号', max_length=16)
    exchange = models.CharField('交易所', max_length=16, null=True)
    short_name = models.CharField('短名', max_length=16, null=True)
    long_name = models.CharField('长名', max_length=32, null=True)
    display_name = models.CharField('展示名', max_length=32, null=True)
    is_disabled = models.BooleanField('是否禁用', default=False)

    class Meta:
        db_table = 'varieties_record'
        ordering = ['-id']


class Source(AlphaBaseMixin):
    """
    资讯提供方和缩写的对应关系
    """
    code = models.CharField('代码', max_length=16)
    name = models.CharField('资讯方', max_length=64)

    class Meta:
        db_table = 'source'


class Fee(VarietiesMixin, SourceMixin, DateMixin, PriceRangeMixin, CreatedAtMixin, AlphaBaseMixin, SymbolMixin):
    type = models.IntegerField('费用类型', choices=FeeTypes.choices())

    class Meta:
        db_table = 'varieties_fee'


class Contracts(AlphaBaseMixin):
    contract = models.CharField(primary_key=True, max_length=10)
    contract_name = models.CharField(max_length=20, blank=True, null=True)
    exchange = models.CharField(max_length=10)
    open_date = models.DateField(blank=True, null=True)
    expire_date = models.DateField(blank=True, null=True)
    start_deliv_date = models.DateField(blank=True, null=True)
    end_deliv_date = models.DateField(blank=True, null=True)
    volume_multiple = models.IntegerField(blank=True, null=True)
    is_trading = models.IntegerField(blank=True, null=True)
    varieties = models.CharField(max_length=10, blank=True, null=True)
    price_tick = models.FloatField(blank=True, null=True)
    exchange_long_margin_ratio = models.FloatField(blank=True, null=True)
    exchange_short_margin_ratio = models.FloatField(blank=True, null=True)
    product_class = models.CharField(max_length=10, blank=True, null=True)
    underlying_instrument = models.CharField(max_length=10, blank=True, null=True)
    max_market_order_volume = models.IntegerField(blank=True, null=True)
    min_market_order_volume = models.IntegerField(blank=True, null=True)
    max_limit_order_volume = models.IntegerField(blank=True, null=True)
    min_limit_order_volume = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contracts'
        unique_together = (('contract', 'exchange'),)


class VarietiesSidebarTable(AlphaBaseMixin):
    """
    侧边栏对应的表格数据
    """
    chart_sidebar_id = models.IntegerField('chart_sidebar 表的 id, 对应到哪个 sidebar')
    data_code = models.CharField('代号', max_length=32)
    table = models.CharField('表名', max_length=16)
    extra = models.TextField('额外字段的展示名、获取方式', max_length=512, default='[]')

    class Meta:
        db_table = 'varieties_sidebar_table'
        ordering = ['-id']

