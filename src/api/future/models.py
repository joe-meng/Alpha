# -- coding: utf-8 --
from model_mixins import *


class FuturePriceDetail(VarietiesMixin, ContractMixin, FutureMixin, SourceMixin, DateTimeMixin, PriceRangeMixin, CreatedAtMixin, SymbolMixin, AlphaBaseMixin):
    """
    期货报价,分数据
    """

    class Meta:
        db_table = 'future_price_detail'
        ordering = ('-date_time',)


class FuturePriceSummary(VarietiesMixin, ContractMixin, FutureMixin, SourceMixin, DateMixin, DurationUnitMixin, PriceRangeMixin, CreatedAtMixin, SymbolMixin, AlphaBaseMixin):
    """
    期货报价,统计数据
    """

    class Meta:
        db_table = 'future_price_summary'


class FutureExchangeRate(CurrencyMixin, FutureMixin, DateMixin, SourceMixin, BuySellPriceMixin, CreatedAtMixin, SymbolMixin, AlphaBaseMixin):
    """
    期汇率,日数据
    """

    class Meta:
        db_table = 'future_exchange'


class FutureHolding(VarietiesMixin, DateMixin, FutureMixin, SourceMixin, AmountMixin, CreatedAtMixin, SymbolMixin, AlphaBaseMixin):
    """
    期货持仓,日数据
    """

    class Meta:
        db_table = 'future_holding'


class FutureWarehouseReceipt(VarietiesMixin, DateMixin, FutureMixin, SourceMixin, AmountMixin, CreatedAtMixin, SymbolMixin, AlphaBaseMixin):
    """
    期货仓单,日数据
    """
    is_cancelled = models.BooleanField('是否为注销仓单', default=False)

    class Meta:
        db_table = 'future_warehouse_receipt'


class FutureBWDDetail(VarietiesMixin, ContractMixin, FutureMixin, DateTimeMixin, SourceMixin, PriceRangeMixin, CreatedAtMixin, SymbolMixin, AlphaBaseMixin):
    """
    现货对比期货的升贴水, 分数据
    """
    change = models.DecimalField('调水', decimal_places=2, max_digits=10, null=True)

    class Meta:
        db_table = 'future_bwd_detail'


class FutureBWDSummary(VarietiesMixin, ContractMixin, FutureMixin, DateMixin, DurationUnitMixin, SourceMixin, PriceRangeMixin, CreatedAtMixin, SymbolMixin, AlphaBaseMixin):
    """
    现货对比期货的升贴水,统计数据
    """
    change = models.DecimalField('调水', decimal_places=2, max_digits=10, null=True)

    class Meta:
        db_table = 'future_bwd_summary'


class FutureContract(VarietiesMixin, FutureMixin, ContractMixin, UpdatedAtMixin, AlphaBaseMixin, SymbolMixin):
    """
    当前所用到的期货合约、主力合约
    future = null 表示主力合约
    future = 1m 表示1月后的合约
    """

    class Meta:
        db_table = 'future_contract'
        unique_together = (('varieties', 'future'),)
