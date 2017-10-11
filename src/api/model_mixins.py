# -- coding: utf-8 --
from pprint import pformat

import logging
from django.conf import settings
from django.db import models
from django.forms import model_to_dict
from django.utils import timezone


default_logger = logging.getLogger(__name__)


class CreatedAtMixin(models.Model):
    created_at = models.DateTimeField('创建于', default=timezone.now)

    class Meta:
        abstract = True


class UpdatedAtMixin(models.Model):
    updated_at = models.DateTimeField('更新于', auto_now=True)

    class Meta:
        abstract = True


class FutureMixin(models.Model):
    """
    future = 1m 表示连一、本月合约
    """
    future = models.CharField('多久以后的期货合约', max_length=16, null=True, db_index=True)

    class Meta:
        abstract = True


class SourceMixin(models.Model):
    source = models.CharField('来源', max_length=32, null=True, db_index=True)

    class Meta:
        abstract = True


class DateTimeMixin(models.Model):
    date_time = models.DateTimeField('时间', null=True, db_index=True)
    timestamp = models.CharField('unix timestamp 格式时间', max_length=16, null=True, db_index=True)

    class Meta:
        abstract = True


class DateMixin(models.Model):
    date = models.DateField('日期', null=True, db_index=True)
    timestamp = models.CharField('unix timestamp 格式时间', max_length=16, null=True, db_index=True)

    class Meta:
        abstract = True


class VarietiesMixin(models.Model):
    varieties = models.CharField('品类', max_length=16, null=True, db_index=True)

    class Meta:
        abstract = True


class PriceRangeMixin(models.Model):
    """
    单方报价
    """
    price_high = models.DecimalField('最高价', null=True, decimal_places=2, max_digits=10)
    price_low = models.DecimalField('最低价', null=True, decimal_places=2, max_digits=10)
    price = models.DecimalField('中间价', null=True, decimal_places=2, max_digits=10)

    class Meta:
        abstract = True


class BuySellPriceMixin(models.Model):
    """
    买卖方报价
    """
    price_buy = models.DecimalField('买入价', decimal_places=2, max_digits=10, null=True)
    price_sell = models.DecimalField('卖出价', decimal_places=2, max_digits=10, null=True)
    price = models.DecimalField('中间价', decimal_places=2, max_digits=10, null=True)

    class Meta:
        abstract = True


class CurrencyMixin(models.Model):
    """
    汇率
    """
    currency = models.CharField('货币代码', max_length=16, null=True)

    class Meta:
        abstract = True


class ContractMixin(models.Model):
    contract = models.CharField('合约', max_length=16, null=True)

    class Meta:
        abstract = True


class AmountMixin(models.Model):
    amount = models.DecimalField('量', decimal_places=2, max_digits=15, null=True)
    change = models.DecimalField('量变化', decimal_places=2, max_digits=10, null=True)

    class Meta:
        abstract = True


class DurationUnitMixin(models.Model):
    duration_unit = models.CharField('时间单位', max_length=16, null=True)

    class Meta:
        abstract = True


class UnitMixin(models.Model):
    unit = models.CharField('数字的计量单位', max_length=16, null=True)

    class Meta:
        abstract = True


class AreaMixin(models.Model):
    area = models.CharField('区域', max_length=32, null=True, db_index=True)

    class Meta:
        abstract = True


class SymbolMixin(models.Model):
    symbol = models.CharField('指标 ID', max_length=64, null=True, db_index=True)

    class Meta:
        abstract = True


class AlphaBaseManager(models.Manager):

    def update_or_create_all_envs(self, logger=default_logger, *args, **kwargs):
        logger_params = kwargs.pop('logger_params', {})
        for db in settings.SPIDER_WRITING_DB_NAMES:
            obj, created = super(AlphaBaseManager, self).using(db).update_or_create(*args, **kwargs)
            logger.info('[%s] 环境 %s: %s, 日志参数: %s' % (db, '插入' if created else '更新', obj, logger_params))

    def bulk_create_all_envs(self, obj_list, logger=default_logger, *args, **kwargs):
        logger_params = kwargs.pop('logger_params', {})
        for db in settings.SPIDER_WRITING_DB_NAMES:
            super(AlphaBaseManager, self).using(db).bulk_create(obj_list, *args, **kwargs)
            logger.info('[%s] 环境 插入成功 %s条, 日志参数: %s' % (db, len(obj_list), logger_params))


class AlphaBaseMixin(models.Model):
    objects = AlphaBaseManager()

    def __str__(self):
        return '\n' + pformat(model_to_dict(self))

    class Meta:
        abstract = True
