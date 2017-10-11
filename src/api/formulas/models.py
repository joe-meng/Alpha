# -- coding: utf-8 --
from django.db import models

from model_mixins import AlphaBaseMixin, CreatedAtMixin, UpdatedAtMixin


class Formula(AlphaBaseMixin, CreatedAtMixin, UpdatedAtMixin):
    """
    公式本身属性, user_id null 表示这是公有公式
    """
    user_id = models.IntegerField('用户 id', null=True)
    title = models.CharField('公式标题', max_length=64, null=True)
    description = models.TextField('描述', max_length=2048, null=True)
    formula = models.TextField('公式内容', max_length=4096, null=True)
    comment = models.TextField('备注', max_length=512, null=True)

    class Meta:
        db_table = 'formula'
        ordering = ['-id']


class FormulaVarieties(AlphaBaseMixin, CreatedAtMixin):
    """
    公式适用于哪些品类
    """
    formula_id = models.IntegerField('公式 id')
    varieties_id = models.IntegerField('品类 id')

    class Meta:
        db_table = 'formula_varieties'
        ordering = ['-id']


class FormulaFunction(AlphaBaseMixin, CreatedAtMixin, UpdatedAtMixin):
    """
    公式可用的方法
    """
    function_name = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=64, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'formula_function'
        ordering = ['-id']
