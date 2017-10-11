# -- coding: utf-8 --
from datetime import datetime
from django.db import models
from django.utils import timezone


from model_mixins import CreatedAtMixin, AlphaBaseMixin


class Alert(CreatedAtMixin, AlphaBaseMixin):
    title = models.TextField('标题', null=True, blank=True)
    body = models.TextField('正文', null=True, blank=True)
    user_id = models.IntegerField('用户编号', null=True)
    triggered_by = models.IntegerField('由哪条计算触发', null=True)
    is_pushed = models.BooleanField('是否已推送', default=False)
    variety = models.CharField('种类', max_length=10, default=False, null=False)
    price = models.CharField('是否已推送', default=False, max_length=30, null=False)
    # source = models.CharField('来源', default=False, max_length=30, null=False)
    # exchange = models.CharField('交易所', default=False, max_length=30, null=False)
    contract = models.CharField('合约', default=False, max_length=30, null=False)



class DayKline(models.Model):
    contract = models.CharField(primary_key=True, max_length=20)
    exchange = models.CharField(max_length=10)
    date_time = models.DateTimeField()
    price_open = models.FloatField(blank=True, null=True)
    price_high = models.FloatField(blank=True, null=True)
    price_low = models.FloatField(blank=True, null=True)
    price_close = models.FloatField(blank=True, null=True)
    volumn = models.FloatField(blank=True, null=True)
    turnover = models.FloatField(blank=True, null=True)
    openinterest = models.IntegerField(blank=True, null=True)
    pre_settlement_price = models.FloatField(blank=True, null=True)
    settlement_price = models.FloatField(blank=True, null=True)
    price_close2 = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'day_kline'
        unique_together = (('contract', 'exchange', 'date_time'),)


class MainContract(models.Model):
    varieties = models.CharField(primary_key=True, max_length=10)
    exchange = models.CharField(max_length=10)
    settlement_date = models.DateField()
    main_contract = models.CharField(max_length=10, blank=True, null=True)
    serial_contract1 = models.CharField(max_length=10, blank=True, null=True)
    serial_contract2 = models.CharField(max_length=10, blank=True, null=True)
    serial_contract3 = models.CharField(max_length=10, blank=True, null=True)
    serial_contract4 = models.CharField(max_length=10, blank=True, null=True)
    serial_contract5 = models.CharField(max_length=10, blank=True, null=True)
    serial_contract6 = models.CharField(max_length=10, blank=True, null=True)
    serial_contract7 = models.CharField(max_length=10, blank=True, null=True)
    serial_contract8 = models.CharField(max_length=10, blank=True, null=True)
    serial_contract9 = models.CharField(max_length=10, blank=True, null=True)
    serial_contract10 = models.CharField(max_length=10, blank=True, null=True)
    serial_contract11 = models.CharField(max_length=10, blank=True, null=True)
    serial_contract12 = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'main_contract'
        unique_together = (('varieties', 'exchange', 'settlement_date'),)


class AiVarieties(models.Model):
    """al比赛的品类"""

    varieties = models.CharField('品类', max_length=10)
    exchange = models.CharField('', max_length=10)
    # ai_prediction = models.BooleanField('AI是否预测', default=False)
    count_user = models.IntegerField('参与的用户数', default=0)
    created_at = models.DateTimeField('创建时间', default=timezone.now)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'alert_ai_varieties'



class PredictionRecord(models.Model):
    """预测记录"""

    pre_dict = [('up', '涨'),
                ('down', '跌')]

    varieties_id = models.IntegerField('品类id')
    user_id = models.IntegerField('用户id')
    prediction = models.CharField('预测涨跌', choices=pre_dict, max_length=10)
    date = models.DateField('预测时间', blank=False, null=False)
    if_visible = models.BooleanField('是否可见', default=True)
    is_true = models.CharField('预测是否正确', max_length=2,  blank=True, default='n')
    visit_number = models.IntegerField('查看次数', default=0)
    created_at = models.DateTimeField('创建时间', default=timezone.now)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'alert_prediction_record'


class QuotesRecords(models.Model):
    """行情记录"""

    trend_dict = (('up', '上升'),
                  ('down', '下降'),
                  ('c', '不变'),)

    date = models.DateField('时间', blank=False, null=False)
    price = models.FloatField('价格', default=0)
    trend = models.CharField('涨跌趋势', max_length=10, choices=trend_dict)
    change_price = models.FloatField('价差', default=0)
    change_percent = models.DecimalField('价格百分比', decimal_places=2, max_digits=10)
    ai_prediction = models.BooleanField('AI是否预测', default=False)
    created_at = models.DateTimeField('创建时间', default=timezone.now)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    varieties_id = models.IntegerField('品类id')

    class Meta:
        db_table = 'alert_quotes_record'


class AttentionList(models.Model):
    """关注列表"""

    user_id = models.IntegerField('用户id', null=False, blank=False)
    varieties_id = models.IntegerField('品类id')

    class Meta:
        db_table = 'alert_attention_list'











