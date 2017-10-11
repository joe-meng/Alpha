# encoding: utf-8
from django.db import models

from model_mixins import AlphaBaseMixin, SymbolMixin, AmountMixin, DateMixin, PriceRangeMixin, CreatedAtMixin


class WindData(SymbolMixin, AmountMixin, DateMixin, AlphaBaseMixin):
    """
    万德数据
    """

    class Meta:
        db_table = 'data_wind'


class LingtongData(SymbolMixin, PriceRangeMixin, DateMixin, AlphaBaseMixin):
    """
    灵通报价
    """

    change = models.DecimalField('量变化', decimal_places=2, max_digits=10, null=True)

    class Meta:
        db_table = 'data_lingtong'


class EnanchuData(SymbolMixin, AmountMixin, DateMixin, AlphaBaseMixin):
    """
    南储数据
    """

    class Meta:
        db_table = 'data_enanchu'


class LGMIData(SymbolMixin, AmountMixin, DateMixin, AlphaBaseMixin):
    """
    兰格钢铁数据
    """

    class Meta:
        db_table = 'data_lgmi'


class DataWorkingTimePercentage(SymbolMixin, AmountMixin, DateMixin, AlphaBaseMixin):

    class Meta:
        managed = False
        db_table = 'data_working_time_percentage'


class DataSinaDayKLine(SymbolMixin, DateMixin, CreatedAtMixin, AlphaBaseMixin):
    exchange = models.CharField(max_length=10)
    varieties = models.CharField(max_length=10)
    price_open = models.FloatField(blank=True, null=True)
    price_high = models.FloatField(blank=True, null=True)
    price_low = models.FloatField(blank=True, null=True)
    price_close = models.FloatField(blank=True, null=True)
    volume = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'data_sina_day_kline'
        ordering = ('-date', )


class DataShfeDayKLine(SymbolMixin, DateMixin, CreatedAtMixin, AlphaBaseMixin):
    volume = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'data_shfe_day_kline'
        ordering = ('-date', )
