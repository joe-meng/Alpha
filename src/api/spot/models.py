# -- coding: utf-8 --
from model_mixins import *


class SpotPriceDetail(VarietiesMixin, SourceMixin, DateTimeMixin, PriceRangeMixin, CreatedAtMixin, AlphaBaseMixin, SymbolMixin):
    """
    现货报价分数据
    """

    class Meta:
        db_table = 'spot_price_detail'


class SpotPriceSummary(VarietiesMixin, SourceMixin, DateMixin, DurationUnitMixin, PriceRangeMixin, CreatedAtMixin, AlphaBaseMixin, SymbolMixin):
    """
    现货报价统计数据
    """

    class Meta:
        db_table = 'spot_price_summary'


class SpotExchangeRateDetail(CurrencyMixin, DateTimeMixin, CreatedAtMixin, SourceMixin, AlphaBaseMixin, SymbolMixin):
    """
    现汇/现钞汇率,分数据
    """
    price_buy = models.DecimalField('现汇买入', decimal_places=2, max_digits=10, null=True)
    price_sell = models.DecimalField('现汇卖出', decimal_places=2, max_digits=10, null=True)
    cash_buy = models.DecimalField('现钞买入', decimal_places=2, max_digits=10, null=True)
    cash_sell = models.DecimalField('现钞卖出', decimal_places=2, max_digits=10, null=True)
    administration_price = models.DecimalField('外汇局中间价', decimal_places=2, max_digits=10, null=True)
    price = models.DecimalField('报价', decimal_places=2, max_digits=10, null=True)

    class Meta:
        db_table = 'spot_exchange_detail'


class SpotExchangeRateSummary(CurrencyMixin, DateMixin, DurationUnitMixin, CreatedAtMixin, SourceMixin, AlphaBaseMixin, SymbolMixin):
    """
    现汇/现钞汇率,统计数据
    """
    price_buy = models.DecimalField('现汇买入', decimal_places=2, max_digits=10, null=True)
    price_sell = models.DecimalField('现汇卖出', decimal_places=2, max_digits=10, null=True)
    cash_buy = models.DecimalField('现钞买入', decimal_places=2, max_digits=10, null=True)
    cash_sell = models.DecimalField('现钞卖出', decimal_places=2, max_digits=10, null=True)
    administration_price = models.DecimalField('外汇局中间价', decimal_places=2, max_digits=10, null=True)
    price = models.DecimalField('报价', decimal_places=2, max_digits=10, null=True)

    class Meta:
        db_table = 'spot_exchange_summary'


class SpotHolding(VarietiesMixin, DateMixin, SourceMixin, DurationUnitMixin, AmountMixin, CreatedAtMixin, AlphaBaseMixin, SymbolMixin):
    """
    现货持仓日数据
    """

    class Meta:
        db_table = 'spot_holding'


class SpotWarehouseReceipt(VarietiesMixin, DateMixin, SourceMixin, DurationUnitMixin, AmountMixin, CreatedAtMixin, AreaMixin, AlphaBaseMixin, SymbolMixin):
    """
    现货仓单日数据
    """

    is_cancelled = models.BooleanField('是否为注销仓单', default=False)

    class Meta:
        db_table = 'spot_warehouse_receipt'


class SpotStock(VarietiesMixin, DateMixin, SourceMixin, DurationUnitMixin, AmountMixin, CreatedAtMixin, AreaMixin, AlphaBaseMixin, SymbolMixin):
    """
    现货库存日数据
    """

    class Meta:
        db_table = 'spot_stock'
