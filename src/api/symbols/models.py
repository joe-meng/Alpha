# -- coding: utf-8 --
from django.db import models

# Create your models here.
from model_mixins import AlphaBaseMixin, UpdatedAtMixin, SymbolMixin, DurationUnitMixin, SourceMixin, UnitMixin, \
    VarietiesMixin


class Symbol(SymbolMixin, AlphaBaseMixin, UpdatedAtMixin, DurationUnitMixin, SourceMixin, UnitMixin, VarietiesMixin):
    title = models.CharField('指标名称', max_length=256)
    table_name = models.CharField('表名', max_length=64, null=True)
    match = models.TextField('JSON 形式 匹配字段名和对应匹配值', max_length=512, null=True)
    column = models.CharField('支持的 column 名', max_length=64, null=True)
    is_disabled = models.BooleanField('是否禁用', default=False)
    wind_account = models.CharField('使用哪个万德账号', max_length=16, null=True)

    classification_1 = models.CharField(max_length=64, blank=True, null=True)
    classification_2 = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        db_table = 'symbol'
        ordering = ['-id']
