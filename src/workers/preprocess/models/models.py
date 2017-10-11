
if __name__ == '__main__':
    import sys
    sys.path.append("../../..")

from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base, AbstractConcreteBase
from sqlalchemy import Column, Integer, String, ForeignKey, \
                        or_, BIGINT, Float, Date, DateTime, Enum, Boolean, TEXT
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
# sqlalchemy.engine.url.URL
from share.settings.defaults import get_env


cur_env = get_env()
db_url = URL('mysql+pymysql', host=cur_env['HOST'], database=cur_env['NAME'],
             username=cur_env['USER'], port=cur_env['PORT'], password=cur_env['PASSWORD'],
             query={'charset': 'utf8'})
Base = declarative_base()


# eng = create_engine(db_url, echo=True)
eng = create_engine(db_url, echo=False)
Session = sessionmaker(bind=eng)

class TempBase(AbstractConcreteBase):
    """基类"""
    __tablename__ = 'temp_users'

    # id = Column(BIGINT, primary_key=True, autoincrement=True)
    # created_at = Column(DateTime, default=datetime.now(), nullable=False)
    # updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)
    #
    FORBIDDEN_COLUMN_LIST = ['id', 'created_at', 'updated_at']
    SHOW_COLUMN_LIST = []

    def __init__(self, *args, **kwargs):
        """初始化"""
        super(TempBase, self).__init__(*args, **kwargs)
        forbidden = []
        for i in self.FORBIDDEN_COLUMN_LIST:
            forbidden.append(self.__tablename__+'.'+i)
        self.FORBIDDEN_COLUMN_LIST = forbidden
        show = []
        for k in self.SHOW_COLUMN_LIST:
            show.append(self.__tablename__+'.'+k)
        self.SHOW_COLUMN_LIST = show

    def to_dict(self):
        """序列化"""
        # return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
        # return {c.name: getattr(self, c.name, None) for c in self.show_lst}
        res = {}
        all_show_lst = self.SHOW_COLUMN_LIST  or self.__table__.columns
        for c in all_show_lst:
            if not c.name in self.FORBIDDEN_COLUMN_LIST:
                res[c.name] = getattr(self, c.name, None)
        return res


class DaySymbolBase(AbstractConcreteBase):
    """基类"""
    __tablename__ = 'day_symbol_base'

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)
    amount = Column(Float, nullable=True, doc=u'', )
    symbol = Column(String(length=64), nullable=True, doc=u'', )
    date = Column(Date, nullable=True, doc=u'', )


class MinSymbolBase(AbstractConcreteBase):
    """基类"""
    __tablename__ = 'min_symbol_base'

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)
    amount = Column(Float, nullable=True, doc=u'', )
    symbol = Column(String(length=64), nullable=True, doc=u'', )
    date = Column(DateTime, nullable=True, doc=u'', )


class MainContract(Base, TempBase):
    __tablename__ = 'main_contract'

    varieties = Column(String(length=10), primary_key=False, nullable=True, doc=u'品种')
    exchange = Column(String(length=10), nullable=False, doc=u'交易所', primary_key=True,)
    settlement_date = Column(Date, nullable=False, doc=u'日期', primary_key=True,)
    main_contract = Column(String(length=10), nullable=False, doc=u'主力合约')
    serial_contract1 = Column(String(length=10), nullable=True, doc=u'连一')
    serial_contract2 = Column(String(length=10), nullable=True, doc=u'连二')
    serial_contract3 = Column(String(length=10), nullable=True, doc=u'连三')
    serial_contract4 = Column(String(length=10), nullable=True, doc=u'连四')
    serial_contract5 = Column(String(length=10), nullable=True, doc=u'连五')
    serial_contract6 = Column(String(length=10), nullable=True, doc=u'连六')
    serial_contract7 = Column(String(length=10), nullable=True, doc=u'连七')
    serial_contract8 = Column(String(length=10), nullable=True, doc=u'连八')
    serial_contract9 = Column(String(length=10), nullable=True, doc=u'连九')
    serial_contract10 = Column(String(length=10), nullable=True, doc=u'连十')
    serial_contract11 = Column(String(length=10), nullable=True, doc=u'连十一')
    serial_contract12 = Column(String(length=10), nullable=True, doc=u'连十二')


class DayKline(Base, TempBase):
    __tablename__ = 'day_kline'

    contract = Column(String(length=10), primary_key=True, nullable=False, doc=u'合约')
    exchange = Column(String(length=10), nullable=False, doc=u'交易所', primary_key=True)
    date_time = Column(DateTime, nullable=False, doc=u'时间', primary_key=True)
    update_time = Column(DateTime, nullable=False, doc=u'更新时间')
    price_open = Column(Float, nullable=False, doc=u'开盘价')
    price_high = Column(Float, nullable=False, doc=u'最高价')
    price_low = Column(Float, nullable=False, doc=u'最低价')
    price_close = Column(Float, nullable=False, doc=u'收盘价')
    settlement_price = Column(Float, nullable=False, doc=u'结算价')
    volumn = Column(Float, nullable=False, doc=u'')
    turnover = Column(Float, nullable=False, doc=u'')
    openinterest = Column(Float, nullable=False, doc=u'')
    pre_settlement_price = Column(Float, nullable=False, doc=u'')
    price_close2 = Column(Float, nullable=False, doc=u'')
    ask_volumn = Column(Float, nullable=False, doc=u'')
    bid_volumn = Column(Float, nullable=False, doc=u'')
    flow_fund = Column(Float, nullable=False, doc=u'资金流入流出')
    sendimentary_money = Column(Float, nullable=False, doc=u'资金沉淀')


class FutureBwdSummary(Base, TempBase):
    __tablename__ = 'future_bwd_summary'

    id = Column(BIGINT, primary_key=True, doc='id', autoincrement=True)
    created_at = Column(DateTime, nullable=False, doc=u'')
    future = Column(String(length=16), nullable=True, doc=u'', )
    source = Column(String(length=32), nullable=True, doc=u'', )
    date = Column(Date, nullable=True, doc=u'', )
    varieties = Column(String(length=16), nullable=True, doc=u'', )
    price_high = Column(Float, nullable=True, doc=u'', )
    price_low = Column(Float, nullable=True, doc=u'', )
    price = Column(Float, nullable=True, doc=u'', )
    contract = Column(String(length=16), nullable=True, doc=u'', )
    duration_unit = Column(String(length=16), nullable=True, doc=u'', )
    change = Column(Float, nullable=True, doc=u'', )
    symbol = Column(String(length=16), nullable=True, doc=u'', )
    timestamp = Column(String(length=16), nullable=True, doc=u'', )


class FuturePriceDetail(Base, TempBase):
    __tablename__ = 'future_price_detail'

    id = Column(BIGINT, primary_key=True, doc='id', autoincrement=True)
    created_at = Column(DateTime, nullable=False, doc=u'')
    future = Column(String(length=16), nullable=True, doc=u'', )
    source = Column(String(length=32), nullable=True, doc=u'', )
    date_time = Column(DateTime, nullable=True, doc=u'', )
    varieties = Column(String(length=16), nullable=True, doc=u'', )
    price_high = Column(Float, nullable=True, doc=u'', )
    price_low = Column(Float, nullable=True, doc=u'', )
    price = Column(Float, nullable=True, doc=u'', )
    contract = Column(String(length=16), nullable=True, doc=u'', )
    # duration_unit = Column(String(length=16), nullable=True, doc=u'', )
    # change = Column(Float, nullable=True, doc=u'', )
    symbol = Column(String(length=16), nullable=True, doc=u'', )
    timestamp = Column(String(length=16), nullable=True, doc=u'', )




class FutureExchange(Base, TempBase):
    __tablename__ = 'future_exchange'

    id = Column(BIGINT, primary_key=True, doc='id', autoincrement=True)
    created_at = Column(DateTime, nullable=False, doc=u'')
    future = Column(String(length=16), nullable=True, doc=u'', )
    source = Column(String(length=32), nullable=True, doc=u'', )
    date = Column(Date, nullable=True, doc=u'', )
    # varieties = Column(String(length=16), nullable=True, doc=u'', )
    price_buy = Column(Float, nullable=True, doc=u'', )
    price_sell = Column(Float, nullable=True, doc=u'', )
    price = Column(Float, nullable=True, doc=u'', )
    # contract = Column(String(length=16), nullable=True, doc=u'', )
    currency = Column(String(length=16), nullable=True, doc=u'', )
    # change = Column(Float, nullable=True, doc=u'', )
    symbol = Column(String(length=16), nullable=True, doc=u'', )
    timestamp = Column(String(length=16), nullable=True, doc=u'', )


class PreprocessData(Base):
    __tablename__ = 'preprocess_data'

    id = Column(BIGINT, primary_key=True, doc='id', autoincrement=True)
    varieties = Column(String(length=16), nullable=True, doc=u'', )
    change = Column(Float, nullable=True, doc=u'', )
    change_1m = Column(Float, nullable=True, doc=u'', )
    change_2m = Column(Float, nullable=True, doc=u'', )
    change_3m = Column(Float, nullable=True, doc=u'', )
    change_6m = Column(Float, nullable=True, doc=u'', )
    profit = Column(Float, nullable=True, doc=u'', )
    profit_1m = Column(Float, nullable=True, doc=u'', )
    profit_2m = Column(Float, nullable=True, doc=u'', )
    profit_3m = Column(Float, nullable=True, doc=u'', )
    profit_6m = Column(Float, nullable=True, doc=u'', )
    import_cost = Column(Float, nullable=True, doc=u'', )
    import_cost_1m = Column(Float, nullable=True, doc=u'', )
    import_cost_2m = Column(Float, nullable=True, doc=u'', )
    import_cost_3m = Column(Float, nullable=True, doc=u'', )
    import_cost_6m = Column(Float, nullable=True, doc=u'', )
    domestic_price = Column(Float, nullable=True, doc=u'', )
    domestic_price_1m = Column(Float, nullable=True, doc=u'', )
    domestic_price_2m = Column(Float, nullable=True, doc=u'', )
    domestic_price_3m = Column(Float, nullable=True, doc=u'', )
    domestic_price_6m = Column(Float, nullable=True, doc=u'', )
    rate = Column(Float, nullable=True, doc=u'', )
    rate_1m = Column(Float, nullable=True, doc=u'', )
    rate_2m = Column(Float, nullable=True, doc=u'', )
    rate_3m = Column(Float, nullable=True, doc=u'', )
    rate_6m = Column(Float, nullable=True, doc=u'', )
    no_exchange_rate = Column(Float, nullable=True, doc=u'', )
    no_exchange_rate_1m = Column(Float, nullable=True, doc=u'', )
    no_exchange_rate_2m = Column(Float, nullable=True, doc=u'', )
    no_exchange_rate_3m = Column(Float, nullable=True, doc=u'', )
    no_exchange_rate_6m = Column(Float, nullable=True, doc=u'', )
    import_rate = Column(Float, nullable=True, doc=u'', )
    import_rate_1m = Column(Float, nullable=True, doc=u'', )
    import_rate_2m = Column(Float, nullable=True, doc=u'', )
    import_rate_3m = Column(Float, nullable=True, doc=u'', )
    import_rate_6m = Column(Float, nullable=True, doc=u'', )
    hulun_1m = Column(Float, nullable=True, doc=u'', )
    hulun_3m = Column(Float, nullable=True, doc=u'', )
    basic_1_2 = Column(Float, nullable=True, doc=u'', )
    basic_1_3 = Column(Float, nullable=True, doc=u'', )
    basic_2_3 = Column(Float, nullable=True, doc=u'', )
    date = Column(DateTime, nullable=True, doc=u'', )


class MinPreprocess(Base, TempBase):
    __tablename__ = 'min_preprocess'

    id = Column(BIGINT, primary_key=True, doc='id', autoincrement=True)
    amount = Column(Float, nullable=True, doc=u'', )
    symbol = Column(String(length=64), nullable=True, doc=u'', )
    date = Column(DateTime, nullable=True, doc=u'', )


class DayPreprocess(Base, TempBase):
    __tablename__ = 'day_preprocess'

    id = Column(BIGINT, primary_key=True, doc='id', autoincrement=True)
    amount = Column(Float, nullable=True, doc=u'', )
    symbol = Column(String(length=64), nullable=True, doc=u'', )
    date = Column(Date, nullable=True, doc=u'', )


class Symbol(Base, TempBase):
    __tablename__ = 'symbol'

    id = Column(BIGINT, primary_key=True, doc='id', autoincrement=True)
    updated_at = Column(DateTime, nullable=False, doc=u'', default=datetime.now())
    title = Column(String(length=256), nullable=False, doc=u'', )
    symbol = Column(String(length=64), nullable=True, doc=u'', )
    table_name = Column(String(length=64), nullable=True, doc=u'', )
    match = Column(TEXT, nullable=True, doc=u'', )
    unit = Column(String(length=16), nullable=True, doc=u'', )
    source = Column(String(length=32), nullable=True, doc=u'', )
    duration_unit = Column(String(length=16), nullable=True, doc=u'', )
    varieties = Column(String(length=16), nullable=True, doc=u'', )
    column = Column(String(length=64), nullable=True, doc=u'', )
    is_disabled = Column(Integer, nullable=True, default=1)

class SpotStock(Base, TempBase):
    __tablename__ = 'spot_stock'

    id = Column(BIGINT, primary_key=True, doc='id', autoincrement=True)
    created_at = Column(DateTime, nullable=False, doc=u'', default=datetime.now())
    source = Column(String(length=32), nullable=True, doc=u'', )
    date = Column(Date, nullable=False, doc=u'', default=datetime.now())
    varieties = Column(String(length=16), nullable=True, doc=u'', )
    amount = Column(Float, nullable=True, doc=u'', )
    change = Column(Float, nullable=True, doc=u'', )
    duration_unit = Column(String(length=16), nullable=True, doc=u'', )
    area = Column(String(length=32), nullable=True, doc=u'', )
    symbol = Column(String(length=64), nullable=True, doc=u'', )
    timestamp = Column(String(length=16), nullable=True, doc=u'', )

#####################
class PreprocessDayPositionChain(Base, TempBase, DaySymbolBase):
    # """日持仓环比对象"""
    __tablename__ = 'preprocess_day_position_chain'

class PreprocessDayStockRadio(Base, TempBase, DaySymbolBase):
    """日库存环比对象"""
    __tablename__ = 'preprocess_day_stock_radio'


class PreprocessDayHlunDeff(Base, TempBase, DaySymbolBase):
    """日沪伦差价对象"""
    __tablename__ = 'preprocess_day_hlun_deff'


class PreprocessDayCrossStar(Base, TempBase, DaySymbolBase):
    """日十字星比值对象"""
    __tablename__ = 'preprocess_day_cross_star'


class PreprocessMinHlunDeff(Base, TempBase, MinSymbolBase):
    """分钟沪伦差价对象"""
    __tablename__ = 'preprocess_min_hlun_deff'


class PreprocessMinCrossStar(Base, TempBase, MinSymbolBase):
    """分钟十字星比值对象"""
    __tablename__ = 'preprocess_min_cross_star'


class CapitalFlowsMin(Base, TempBase):
    """资金流动分钟表"""
    __tablename__ = 'capital_flows_min'

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)

    flow = Column(Float, nullable=True, doc=u'资金流入流出', )
    precipitation = Column(Float, nullable=True, doc=u'资金沉淀', )
    varieties = Column(String(length=16), nullable=True, doc=u'品类', )
    date = Column(DateTime, nullable=True, doc=u'时间', )
    exchange = Column(String(length=16), nullable=True, doc=u'交易所', )
    product_class = Column(String(length=16), nullable=True, doc=u'产品分类', )


class CapitalFlowsDay(Base, TempBase):
    """资金流动日表"""
    __tablename__ = 'capital_flows_day'

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)

    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)
    flow = Column(Float, nullable=True, doc=u'资金流入流出', )
    precipitation = Column(Float, nullable=True, doc=u'资金沉淀', )
    varieties = Column(String(length=16), nullable=True, doc=u'品类', )
    date = Column(Date, nullable=True, doc=u'时间', )
    exchange = Column(String(length=16), nullable=True, doc=u'交易所', )
    product_class = Column(String(length=16), nullable=True, doc=u'产品分类', )


class SpotPriceSummary(Base, TempBase):
    __tablename__ = 'spot_price_summary'

    id = Column(BIGINT, primary_key=True, doc='id', autoincrement=True)

    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    source = Column(String(length=32), nullable=True, doc=u'来源', )
    date = Column(Date, nullable=True, doc=u'时间', )
    varieties = Column(String(length=16), nullable=True, doc=u'品类', )
    price_high = Column(Float, nullable=True, doc=u'', )
    price_low =Column(Float, nullable=True, doc=u'', )
    price = Column(Float, nullable=True, doc=u'', )
    duration_unit = Column(String(length=16), nullable=True, doc=u'', )
    symbol = Column(String(length=64), nullable=True, doc=u'', )
    timestamp = Column(String(length=16), nullable=True, doc=u'', )


class PreprocessMinSmmPriceDeff(Base, TempBase, MinSymbolBase):
    """分钟有色网现货价格与上周差值对象"""
    __tablename__ = 'preprocess_min_smm_price_deff'


class PreprocessDaySmmPriceDeff(Base, TempBase, DaySymbolBase):
    """日数据有色网现货价格与上周差值对象"""
    __tablename__ = 'preprocess_day_smm_price_deff'


class PreprocessMinShmetPriceDeff(Base, TempBase, MinSymbolBase):
    """分钟上海金属网现货价格与上周差值对象"""
    __tablename__ = 'preprocess_min_shmet_price_deff'


class PreprocessDayShmetPriceDeff(Base, TempBase, DaySymbolBase):
    """日数据上海金属网现货价格与上周差值对象"""
    __tablename__ = 'preprocess_day_shmet_price_deff'


class PreprocessDayWarehouseReceipts(Base, TempBase, DaySymbolBase):
    """日数据上海金属网现货价格与上周差值对象"""
    __tablename__ = 'preprocess_day_warehouse_receipts'


class SpotWarehouseReceipt(Base, TempBase):
    __tablename__ = 'spot_warehouse_receipt'

    id = Column(BIGINT, primary_key=True, doc='id', autoincrement=True)

    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    source = Column(String(length=32), nullable=True, doc=u'', )
    date = Column(Date, nullable=False)
    varieties = Column(String(length=16), nullable=True, doc=u'', )
    amount = Column(Float, nullable=True, doc=u'', )
    change = Column(Float, nullable=True, doc=u'', )
    duration_unit = Column(String(length=16), nullable=True, doc=u'', )
    area = Column(String(length=32), nullable=True, doc=u'', )
    is_cancelled = Column(Integer, doc='')
    symbol = Column(String(length=64), nullable=True, doc=u'', )
    timestamp = Column(String(length=16), nullable=True, doc=u'', )


class PreprocessMinPositionDeff(Base, TempBase, MinSymbolBase):
    """分钟上海金属网现货价格与上周差值对象"""
    __tablename__ = 'preprocess_min_position_deff'


class PreprocessDayPositionDeff(Base, TempBase, DaySymbolBase):
    """日数据上海金属网现货价格与上周差值对象"""
    __tablename__ = 'preprocess_day_position_deff'


# class PreprocessMinSmmSpotMonthDeff(Base, TempBase, MinSymbolBase):
#     """分钟有色网现货价格月差"""
#     __tablename__ = 'preprocess_min_smm_spot_month_deff'


class PreprocessDaySmmSpotMonthDeff(Base, TempBase, DaySymbolBase):
    """日数据有色网现货价格月差"""
    __tablename__ = 'preprocess_day_smm_spot_month_deff'


# class PreprocessMinSmmSpotYearDeff(Base, TempBase, MinSymbolBase):
#     """分钟有色网现货价格年差"""
#     __tablename__ = 'preprocess_min_smm_spot_year_deff'


class PreprocessDaySmmSpotYearDeff(Base, TempBase, DaySymbolBase):
    """日数据有色网现货价格年差"""
    __tablename__ = 'preprocess_day_smm_spot_year_deff'



# class PreprocessMinShmetSpotMonthDeff(Base, TempBase, MinSymbolBase):
#     """分钟上海金属网现货价格月差"""
#     __tablename__ = 'preprocess_min_shmet_spot_month_deff'


class PreprocessDayShmetSpotMonthDeff(Base, TempBase, DaySymbolBase):
    """日数据上海金属网现货价格月差"""
    __tablename__ = 'preprocess_day_shmet_spot_month_deff'


# class PreprocessMinShmetSpotYearDeff(Base, TempBase, MinSymbolBase):
#     """分钟上海金属网现货价格年差"""
#     __tablename__ = 'preprocess_min_shmet_spot_year_deff'


class PreprocessDayShmetSpotYearDeff(Base, TempBase, DaySymbolBase):
    """日数据上海金属网现货价格年差"""
    __tablename__ = 'preprocess_day_shmet_spot_year_deff'


# class PreprocessMinDeliveryMonthPositionDeff(Base, TempBase, MinSymbolBase):
#     """分钟持仓月差（按持仓月计算）"""
#     __tablename__ = 'preprocess_min_delivery_month_position_deff'


class PreprocessDayDeliveryMonthPositionDeff(Base, TempBase, DaySymbolBase):
    """日数据持仓月差（按持仓月计算）"""
    __tablename__ = 'preprocess_day_delivery_month_position_deff'

# class PreprocessMinMonthWarehouseDeff(Base, TempBase, MinSymbolBase):
#     """分钟仓单月差"""
#     __tablename__ = 'preprocess_min_month_warehouse_deff'

class PreprocessDayMonthWarehouseDeff(Base, TempBase, DaySymbolBase):
    """日数据仓单月差"""
    __tablename__ = 'preprocess_day_month_warehouse_deff'

class PreprocessDayDeliveryMonthBwdDeff(Base, TempBase, DaySymbolBase):
    """日数据升贴水持仓月差"""
    __tablename__ = 'preprocess_day_delivery_month_bwd_deff'

class PreprocessDayDataArtificial(Base, TempBase):
    """总产量"""
    __tablename__ = 'data_artificial'

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    amount = Column(Float, nullable=True, doc=u'', )
    symbol = Column(String(length=64), nullable=True, doc=u'', )
    date = Column(DateTime, nullable=True, doc=u'', )

class DataWind(Base, TempBase):
    __tablename__ = 'data_wind'

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    amount = Column(Float, nullable=True, doc=u'', )
    symbol = Column(String(length=64), nullable=True, doc=u'', )
    change = Column(Float, nullable=True, doc=u'', )
    date = Column(Date, nullable=True, doc=u'', )
    timestamp = Column(String(length=16), nullable=True, doc=u'', )


if __name__ == '__main__':
    # import sys
    # sys.path.append("../..")
    Base.metadata.create_all(eng)