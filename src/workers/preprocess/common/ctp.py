
from datetime import datetime, timedelta
import logging
import abc
import when
from sqlalchemy import desc

from models.models import MainContract, DayKline, SpotStock, SpotPriceSummary, SpotWarehouseReceipt, FutureExchange, \
    FutureBwdSummary, FuturePriceDetail, DataWind
from models.models import Session
from utils.enums import MIN_PARA_MODEL_MAP, MIN_VARIEYIES_DICT, \
                        DAY_VARIEYIES_DICT,  ALLOW_EXCHANGE, \
                        ALLOW_VARIETIES, PRE_SYMBOL, DAY_PARA_MODEL_MAP, PRE_SYMBOL, PRODUCT_CLASS_MAP

from utils.cal_settings import DAY_INIT_PATA_MAP, DAY_RES_DEAL_MAP
from utils.enums import METAL_RATE_DICT, CHANGE_DICT, EXTRA_PRICE, OUTPUT_SYMBOL_MAP, IMPORT_AMOUNT_MAP

# self.db = Session()
_logger = logging.getLogger(__name__)
# _logger = None
check_log = logging.getLogger('check')


class BasePreprocess(object):
    """计算公式基类"""
    def __init__(self, *args, **kwargs):
        super(BasePreprocess, self).__init__(*args, **kwargs)
        self.main_contract_price = 0.0
        self.lme_3 = 0
        self.exchange_3m = 0
        self.date = datetime.now().strftime('%Y-%m-%d')
        self.this_month_position = []
        self.last_month_position = []
        self.this_month_stock = []
        self.last_month_stock = []
        self.main_price_open = 0.0
        self.main_price_close = 0.0
        self.main_price_high = 0.0
        self.main_price_low = 0.0
        self.main_contract = {}
        self.today_smm_spot_price = 0.0
        self.last_week_smm_spot_price = 0.0
        self.today_shmet_spot_price = 0.0
        self.last_week_shmet_spot_price = 0.0
        self.this_month_warehouse_receipts = []
        self.last_month_warehouse_receipts = []
        # self.serial_contract1 = 0.0
        # self.serial_contract2 = 0.0
        # self.serial_contract3 = 0.0
        # self.serial_contract6 = 0.0

        self.contract1_price = 0.0
        self.contract2_price = 0.0
        self.contract3_price = 0.0
        self.contract6_price = 0.0

        self.today_position = 0.0 #今天持仓
        self.yesterday_position = 0.0 #昨天持仓

        self.last_month_smm_spot_price = 0.0 #上个月有色网的现货价格
        self.last_year_smm_spot_price = 0.0 #去年今天有色网的现货价格
        self.last_month_shmet_spot_price = 0.0 #上个月今天上海金属网现货价格
        self.last_year_shmet_spot_price = 0.0 #去年今天上海金属网现货价格
        self.last_delivery_month_position = 0.0 #上个交割月今天持仓

        self.today_stock_in = 0.0 #今天的库存
        self.last_year_stock_in = 0.0 #去年今天的库存
        self.this_delivery_month_inner_bwd = [] #此持仓月的升贴水
        self.last_delivery_month_inner_bwd = [] #上个交割月今天的升贴水

        self.output = 0.0 #产量
        self.import_amount = 0.0 #进口量

        self.import_cost = 0.0

    @property
    def cal_total_output(self):
        """计算总产量"""
        logging.info('计算(总产量), 品类: %s, 时间: %s' % (self.varieties, self.date))
        res = {}
        if self.output and self.import_amount:
            self.total_output = float(self.output)+float(self.import_amount)
            res = {'total_output': self.total_output}
        return res

    @property
    def cal_delivery_month_bwd_deff(self):
        """计算交割月升贴水差"""
        logging.info('计算(交割月升贴水差), 品类: %s, 时间: %s' % (self.varieties, self.date))
        res = {}
        this_len = len(self.this_delivery_month_inner_bwd)
        last_len = len(self.last_delivery_month_inner_bwd)
        if last_len == 0:
            return res
        if this_len > last_len:
            first_vals = self.last_delivery_month_inner_bwd[0]
            for i in range(this_len - last_len):
                self.last_delivery_month_inner_bwd = [first_vals] + self.last_delivery_month_inner_bwd
        for index in range(this_len):
            if str(self.this_delivery_month_inner_bwd[index]['date']) == self.date:
                self.delivery_month_bwd_deff = float(self.this_delivery_month_inner_bwd[index]['vals']) - \
                                            float(self.last_delivery_month_inner_bwd[index]['vals'])
                res.update({
                    'delivery_month_bwd_deff': self.delivery_month_bwd_deff,
                })
        return res

    @property
    def cal_year_stock_deff(self):
        """计算库存年差"""
        self.year_stock_deff = self.today_stock_in - self.last_year_stock_in
        return {'year_stock_deff': self.year_stock_deff}

    @property
    def cal_month_warehouse_deff(self):
        """计算月仓单差"""
        # self.month_warehouse_deff = self.today_warehouse_receipts - self.day_last_month_warehouse
        # return {'month_warehouse_deff': self.month_warehouse_deff}
        logging.info('计算(月仓单差), 品类: %s, 时间: %s' % (self.varieties, self.date))
        res = {}
        this_len = len(self.this_month_warehouse_receipts)
        last_len = len(self.last_month_warehouse_receipts)
        if last_len == 0:
            return res
        if this_len > last_len:
            first_vals = self.last_month_warehouse_receipts[0]
            for i in range(this_len - last_len):
                self.last_month_warehouse_receipts = [first_vals] + self.last_month_warehouse_receipts
        for index in range(this_len):
            if str(self.this_month_warehouse_receipts[index]['date']) == self.date:
                self.month_warehouse_deff = float(self.this_month_warehouse_receipts[index]['vals']) - \
                                                    float(self.last_month_warehouse_receipts[index]['vals'])
                res.update({
                    'month_warehouse_deff': self.month_warehouse_deff,
                })
        return res

    @property
    def cal_delivery_month_position_deff(self):
        """计算交割月持仓差"""
        # self.delivery_month_position_deff = self.today_position - self.last_delivery_month_position
        # return {'delivery_month_position_deff': self.delivery_month_position_deff}
        logging.info('计算(交割月持仓差), 品类: %s, 时间: %s' % (self.varieties, self.date))
        res = {}
        this_len = len(self.this_month_position)
        last_len = len(self.last_month_position)
        if last_len == 0:
            return res
        if this_len > last_len:
            first_vals = self.last_month_position[0]
            for i in range(this_len - last_len):
                self.last_month_position = [first_vals] + self.last_month_position
        for index in range(this_len):
            if str(self.this_month_position[index]['date']) == self.date:
                self.delivery_month_position_deff = float(self.this_month_position[index]['vals']) - \
                                                    float(self.last_month_position[index]['vals'])
                res.update({
                    'delivery_month_position_deff': self.delivery_month_position_deff,
                })
        return res


    @property
    def cal_smm_spot_month_deff(self):
        """计算有色网现货价格月差"""
        self.smm_spot_month_deff = float(self.today_smm_spot_price) - float(self.last_month_smm_spot_price)
        return {'smm_spot_month_deff': self.smm_spot_month_deff}\

    @property
    def cal_smm_spot_year_deff(self):
        """计算有色网现货价格年差"""
        self.smm_spot_year_deff = float(self.today_smm_spot_price) - float(self.last_year_smm_spot_price)
        return {'smm_spot_year_deff': self.smm_spot_year_deff}

    @property
    def cal_shmet_spot_month_deff(self):
        """计算上海金属网现货价格月差"""
        self.shmet_spot_month_deff = float(self.today_shmet_spot_price) - float(self.last_month_shmet_spot_price)
        return {'shmet_spot_month_deff': self.shmet_spot_month_deff}\

    @property
    def cal_shmet_spot_year_deff(self):
        """计算上海金属网现货价格年差"""
        self.shmet_spot_year_deff = float(self.today_shmet_spot_price) - float(self.last_year_shmet_spot_price)
        return {'shmet_spot_year_deff': self.shmet_spot_year_deff}


    @property
    def caculate_hlun_price_diff(self):
        """
        沪伦价格差计算公式
        :return:
        """
        logging.info('计算(沪伦价格差计算公式), 品类: %s, 时间: %s'%(self.varieties, self.date))
        # 上期所价格 - (伦敦3月价格 * 1.17 * 当日汇率)
        res = float(self.main_contract_price) - (float(self.lme_3)*1.17*float(self.exchange_3m))
        return {
            'hlun_price_diff': res,
        }


    @property
    def caculate_position_chain(self):
        """持仓环比计算公式"""
        # 作为技术管理人员, 我希望预计算能计算库存环比值(当月对应日库存 - 上月对应日库存 / 上月对应日库存)
        # 的比值(包括历史及每日更新的比值(包括历史及每日更新)
        logging.info('计算(持仓环比), 品类: %s, 时间: %s' % (self.varieties, self.date))
        res = []
        this_len = len(self.this_month_position)
        last_len = len(self.last_month_position)
        if last_len == 0:
            return res
        if this_len > last_len:
            first_vals = self.last_month_position[0]
            for i in range(this_len-last_len):
                self.last_month_position = [first_vals] + self.last_month_position
        for index in range(this_len):
            if float(self.last_month_position[index]['vals']) == 0:
                rate = 0.0
            else:
                rate = float(self.this_month_position[index]['vals']) / float(self.last_month_position[index]['vals'])
            res.append({
                'amount': rate,
                'date': self.this_month_position[index]['date'],
                'key': 'position_chain',
            })
        return res

    @property
    def caculate_stock_ratio(self):
        """计算库存环比"""
        # 作为技术管理人员, 我希望预计算能计算合约持仓环比值(当月对应日持仓 - 上月对应日持仓 / 上月对应日持仓)
        # 的比值(包括历史及每日更新)
        # 作为技术管理人员, 我希望预计算能计算主力合约(收盘价 - 开盘价 / 开盘价)的比值(包括历史及每日更新)
        logging.info('计算(库存环比), 品类: %s, 时间: %s' % (self.varieties, self.date))
        res = []
        this_len = len(self.this_month_stock)
        last_len = len(self.last_month_stock)
        if last_len == 0:
            return res
        if this_len > last_len:
            first_vals = self.last_month_stock[0]
            for i in range(this_len - last_len):
                self.last_month_stock = [first_vals] + self.last_month_stock
        for index in range(this_len):
            rate = float(self.this_month_stock[index]['vals']) / float(self.last_month_stock[index]['vals'])
            res.append({
                'amount': rate,
                'date': self.this_month_stock[index]['date'],
                'key': 'stock_ratio',
            })
        return res

    @property
    def caculate_cross_star(self):
        """计算十字星阈值"""
        # 作为技术管理人员, 我希望预计算能计算主力合约(收盘价 - 开盘价 / 开盘价)
        # 的比值(包括历史及每日更新)
        logging.info('计算(十字星阈值), 品类: %s, 时间: %s' % (self.varieties, self.date))
        res = 0.0
        if self.main_price_open != 0:
            res = (self.main_price_close - self.main_price_open) / self.main_price_open
        return {
            'cross_star': res,
        }


    @property
    def calculation_basic_rate(self):
        """计算基差比值"""
        logging.info('计算(基差比值), 品类: %s, 时间: %s' % (self.varieties, self.date))
        if not self.contract1_price:
            self.calculation_basic
        price_1 = self.contract1_price
        price_2 = self.contract2_price
        price_3 = self.contract3_price
        if not price_1:
            basic_1_2_rate = 0
            basic_1_3_rate = 0
        else:
            basic_1_2_rate = round((price_1 - price_2) / price_1, 4)
            basic_1_3_rate = round((price_1 - price_3) / price_1, 4)
        if not price_2:
            basic_2_3_rate = 0
        else:
            basic_2_3_rate = round((price_2 - price_3) / price_2, 4)
        res = {
            "basic_1_2_rate": basic_1_2_rate,
            "basic_1_3_rate": basic_1_3_rate,
            "basic_2_3_rate": basic_2_3_rate,
        }
        return res


    @property
    def calculation_basic(self):
        """计算基差"""
        logging.info('计算(基差), 品类: %s, 时间: %s' % (self.varieties, self.date))
        res = {}
        if self.contract1_price and self.contract2_price:
            self.basic_1_2 = self.contract1_price - self.contract2_price
            res['basic_1_2'] = self.basic_1_2
        if self.contract1_price and self.contract3_price:
            self.basic_1_3 = self.contract1_price - self.contract3_price
            res['basic_1_3'] = self.basic_1_3
        if self.contract2_price and self.contract3_price:
            self.basic_2_3 = self.contract2_price - self.contract3_price
            res['basic_2_3'] = self.basic_2_3
        return res

    @property
    def calculation_smm_spot_price_diff(self):
        """计算有色网现货周价差"""
        logging.info('计算(有色网现货周价差), 品类: %s, 时间: %s' % (self.varieties, self.date))
        return {
            'smm_spot_price_diff': float(self.today_smm_spot_price) - float(self.last_week_smm_spot_price),
        }

    @property
    def calculation_shmet_spot_price_diff(self):
        """计算上海金属网现货周价差"""
        logging.info('计算(上海金属网现货周价差), 品类: %s, 时间: %s' % (self.varieties, self.date))
        return {
            'shmet_spot_price_diff': float(self.today_shmet_spot_price) - float(self.last_week_shmet_spot_price)
        }

    @property
    def calculation_warehouse_receipts(self):
        """计算仓单环比"""
        # 作为技术管理人员, 我希望预计算能计算合约持仓环比值(当月对应日持仓 - 上月对应日持仓 / 上月对应日持仓)
        # 的比值(包括历史及每日更新)
        # 作为技术管理人员, 我希望预计算能计算主力合约(收盘价 - 开盘价 / 开盘价)的比值(包括历史及每日更新)
        logging.info('计算(仓单环比), 品类: %s, 时间: %s' % (self.varieties, self.date))
        res = []
        this_len = len(self.this_month_warehouse_receipts)
        last_len = len(self.last_month_warehouse_receipts)
        if last_len == 0:
            return res
        if this_len > last_len:
            first_vals = self.last_month_warehouse_receipts[0]
            for i in range(this_len - last_len):
                self.last_month_warehouse_receipts = [first_vals] + self.last_month_warehouse_receipts
        for index in range(this_len):
            if float(self.last_month_warehouse_receipts[index]['vals']) == 0:
                rate = 0.0
            else:
                rate = float(self.this_month_warehouse_receipts[index]['vals']) / float(self.last_month_warehouse_receipts[index]['vals'])
            res.append({
                'amount': rate,
                'date': self.this_month_warehouse_receipts[index]['date'],
                'key': 'warehouse_receipts',
            })
        return res

#迁移min_hander方法
    @property
    def cal_import_cost(self):
        # 计算进口成本
        res = {}
        logging.info('计算(进口成本), 品类: %s, 时间: %s' % (self.varieties, self.date))
        rate = METAL_RATE_DICT.get(self.varieties, 1)
        if not self.exchange_now:
            return res
        if self.lme_3 and self.bwd:
            self.import_cost = round(
                (float(self.lme_3) + float(self.bwd) + float(self.change)) * 1.17 * float(self.exchange_now) * rate + EXTRA_PRICE.get(self.varieties, 150),
                4)
        else:
            self.import_cost = 0.0
            res = {'import_cost': self.import_cost}
        return res

    @property
    def cal_import_cost_1m(self):
        # 计算一月进口成本
        logging.info('计算(一月进口成本), 品类: %s, 时间: %s' % (self.varieties, self.date))
        if not hasattr(self, 'change_1m'):
            self.cal_change_1m
        rate = METAL_RATE_DICT.get(self.varieties, 1)
        self.import_cost_1m = round(
            (self.lme_3 + self.bwd + self.change_1m) * 1.17 * self.exchange_1m * rate + EXTRA_PRICE.get(self.varieties,
                                                                                                        150), 4)
        return {'import_cost_1m': self.import_cost_1m}

    @property
    def cal_import_cost_2m(self):
        # 计算二月进口成本
        logging.info('计算(二月进口成本), 品类: %s, 时间: %s' % (self.varieties, self.date))
        if not hasattr(self, 'exchange_2m'):
            self.cal_exchange_2m
        rate = METAL_RATE_DICT.get(self.varieties, 1)
        self.import_cost_2m = round(
            (self.lme_3 + self.bwd + self.change_2m) * 1.17 * self.exchange_2m * rate + EXTRA_PRICE.get(self.varieties,
                                                                                                        150), 4)
        return {'import_cost_2m': self.import_cost_2m}

    @property
    def cal_import_cost_3m(self):
        # 计算三月进口成本
        logging.info('计算(三月进口成本), 品类: %s, 时间: %s' % (self.varieties, self.date))
        rate = METAL_RATE_DICT.get(self.varieties, 1)
        if not hasattr(self, 'exchange_3m'):
            self.cal_exchange_3m
        self.import_cost_3m = round(
            (self.lme_3 + self.bwd + self.change_3m) * 1.17 * self.exchange_3m * rate + EXTRA_PRICE.get(self.varieties,
                                                                                                        150), 4)
        return {'import_cost_3m': self.import_cost_3m}

    @property
    def cal_import_cost_6m(self):
        # 计算六月进口成本
        logging.info('计算(六月进口成本), 品类: %s, 时间: %s' % (self.varieties, self.date))
        rate = METAL_RATE_DICT.get(self.varieties, 1)
        if not hasattr(self, 'exchange_6m'):
            self.cal_exchange_6m
        self.import_cost_6m = round(
            (self.lme_3 + self.bwd + self.change_6m) * 1.17 * self.exchange_6m * rate + EXTRA_PRICE.get(self.varieties,
                                                                                                        150), 4)
        return {'import_cost_6m': self.import_cost_6m}

    @property
    def cal_domestic_price(self):
        # 计算国内报价
        # 国内报价 = 连续合约 + 国内升贴水 除了现货外 其他合约 连续=国内报价
        self.domestic_price = float(self.contract1_price) + float(self.internal_bwd)
        return {'domestic_price': self.domestic_price}

    @property
    def cal_domestic_price_1m(self):
        # 计算1个月合约的国内报价
        self.domestic_price_1m = self.contract1_price
        return {'domestic_price_1m': self.domestic_price_1m}

    @property
    def cal_domestic_price_2m(self):
        # 计算2个月合约的国内报价
        self.domestic_price_2m = self.contract2_price
        return {'domestic_price_2m': self.domestic_price_2m}

    @property
    def cal_domestic_price_3m(self):
        # 计算3个月合约的国内报价
        self.domestic_price_3m = self.contract3_price
        return {'domestic_price_3m': self.domestic_price_3m}

    @property
    def cal_domestic_price_6m(self):
        # 计算6个月合约的国内报价
        self.domestic_price_6m = self.contract6_price
        return {'domestic_price_6m': self.domestic_price_6m}

    @property
    def cal_cur_rate(self):
        # 计算比值  进口平衡比值
        res = {}
        if not self.lme_3:
            return {}
        if not hasattr(self, 'import_cost'):
            self.cal_import_cost
        if not hasattr(self, 'domestic_price'):
            self.cal_domestic_price
        self.rate = round(self.import_cost / float(self.lme_3), 4)
        # 进口比值
        self.import_rate = round(self.domestic_price / (float(self.lme_3) + float(self.change)), 4)
        # 剔除汇率比值
        res['rate'] = self.rate
        res['import_rate'] = self.import_rate

        if float(self.exchange_now):
            self.no_exchange_rate = round(self.domestic_price / (float(self.lme_3) * float(self.exchange_now)), 4)
            res['no_exchange_rate'] = self.no_exchange_rate
        return res

    @property
    def cal_1m_rate(self):
        if not self.lme_3:
            return {}
        if not hasattr(self, 'import_cost_1m'):
            self.cal_import_cost_1m
        if not hasattr(self, 'domestic_price_1m'):
            self.cal_domestic_price_1m
        # 1月 进口平衡比值
        self.rate_1m = round(self.import_cost_1m / float(self.lme_3), 4)
        # 1月 进口比值
        self.import_rate_1m = round(float(self.domestic_price_1m) / (float(self.lme_3) + float(self.change_1m)), 4)
        # 1月 剔除汇率比值
        self.no_exchange_rate_1m = round(float(self.domestic_price_1m) / (float(self.lme_3) * float(self.exchange_1m)), 4)
        return {
            'rate_1m': self.rate_1m,
            'import_rate_1m': self.import_rate_1m,
            'no_exchange_rate_1m': self.no_exchange_rate_1m,
        }

    @property
    def cal_2m_rate(self):
        if not self.lme_3:
            return {}
        if not hasattr(self, 'import_cost_2m'):
            self.cal_import_cost_2m
        if not hasattr(self, 'domestic_price_2m'):
            self.cal_domestic_price_2m
        # 2月 进口平衡比值
        self.rate_2m = round(float(self.import_cost_2m) / float(self.lme_3), 4)
        # 2月 进口比值
        self.import_rate_2m = round(float(self.domestic_price_2m) / (float(self.lme_3) + float(self.change_2m)), 4)
        # 2月 剔除汇率比值
        self.no_exchange_rate_2m = round(float(self.domestic_price_2m) / (float(self.lme_3) * float(self.exchange_2m)), 4)
        return {
            'rate_2m': self.rate_2m,
            'import_rate_2m': self.import_rate_2m,
            'no_exchange_rate_2m': self.no_exchange_rate_2m,
        }

    @property
    def cal_3m_rate(self):
        if not self.lme_3:
            return {}
        if not hasattr(self, 'import_cost_3m'):
            self.cal_import_cost_3m
        if not hasattr(self, 'domestic_price_3m'):
            self.cal_domestic_price_3m
        # 3月 进口平衡比值
        self.rate_3m = round(float(self.import_cost_3m) / float(self.lme_3), 4)
        # 3月 进口比值
        self.import_rate_3m = round(float(self.domestic_price_3m) / (float(self.lme_3) + float(self.change_3m)), 4)
        # 3月 剔除汇率比值
        self.no_exchange_rate_3m = round(float(self.domestic_price_3m) / (float(self.lme_3) * float(self.exchange_3m)), 4)
        return {
            'rate_3m': self.rate_3m,
            'import_rate_3m': self.import_rate_3m,
            'no_exchange_rate_3m': self.no_exchange_rate_3m,
        }

    @property
    def cal_6m_rate(self):
        if not self.lme_3:
            return {}
        if not hasattr(self, 'import_cost_6m'):
            self.cal_import_cost_6m
        if not hasattr(self, 'domestic_price_6m'):
            self.cal_domestic_price_6m
        # 6月 进口平衡比值
        self.rate_6m = round(float(self.import_cost_6m) / float(self.lme_3), 4)
        # 6月 进口比值
        self.import_rate_6m = round(float(self.domestic_price_6m) / (float(self.lme_3) + float(self.change_6m)), 4)
        # 6月 剔除汇率比值
        self.no_exchange_rate_6m = round(float(self.domestic_price_6m) / (float(self.lme_3) * float(self.exchange_6m)), 4)
        return {
            'rate_6m': self.rate_6m,
            'import_rate_6m': self.import_rate_6m,
            'no_exchange_rate_6m': self.no_exchange_rate_6m,
        }

    @property
    def cal_profit(self):
        # 计算盈亏
        res = {}
        if not hasattr(self, 'domestic_price'):
            self.cal_domestic_price
        if self.domestic_price and self.internal_bwd and self.import_cost:
            self.profit = round(self.domestic_price + self.internal_bwd - self.import_cost, 4)
            res = {'profit': self.profit}
        return res

    @property
    def cal_profit_1m(self):
        """计算1月盈亏"""
        res = {}
        if not hasattr(self, 'domestic_price_1m'):
            self.cal_domestic_price_1m
        if self.domestic_price_1m and self.import_cost_1m:
            self.profit_1m = round(float(self.domestic_price_1m) - float(self.import_cost_1m), 4)
            res = {'profit_1m': self.profit_1m}
        return res

    @property
    def cal_profit_2m(self):
        """计算2月盈亏"""
        res = {}
        if not hasattr(self, 'domestic_price_2m'):
            self.cal_domestic_price_2m
        if self.domestic_price_2m and self.import_cost_2m:
            self.profit_2m = round(float(self.domestic_price_2m) - float(self.import_cost_2m), 4)
            res = {'profit_2m': self.profit_2m}
        return res

    @property
    def cal_profit_3m(self):
        """计算3月盈亏"""
        res = {}
        if not hasattr(self, 'domestic_price_3m'):
            self.cal_domestic_price_3m
        if self.domestic_price_3m and self.import_cost_3m:
            self.profit_3m = round(float(self.domestic_price_3m) - float(self.import_cost_3m), 4)
            res = {'profit_3m': self.profit_3m}
        return res

    @property
    def cal_profit_6m(self):
        """计算6月盈亏"""
        res = {}
        if not hasattr(self, 'domestic_price_6m'):
            self.cal_domestic_price_6m
        if self.domestic_price_6m and self.import_cost_6m:
            self.profit_6m = round(float(self.domestic_price_6m) - float(self.import_cost_6m), 4)
            res = {'profit_3m': self.profit_6m}
        return res

    @property
    def cal_change_1m(self):
        # 计算1月调水
        self.change_1m = round(float(self.change) * CHANGE_DICT["1"], 4)
        return {'change_1m': self.change_1m}

    @property
    def cal_change_2m(self):
        # 计算2月调水
        self.change_2m = round(float(self.change) * CHANGE_DICT["2"], 4)
        return {'change_2m': self.change_2m}

    @property
    def cal_change_3m(self):
        # 计算3月调水
        self.change_3m = round(float(self.change) * CHANGE_DICT["3"], 4)
        return {'change_3m': self.change_3m}

    @property
    def cal_change_6m(self):
        # 计算6月调水
        self.change_6m = round(float(self.change) * CHANGE_DICT["6"], 4)
        return {'change_6m': self.change_6m}

    @property
    def cal_1m_hulun(self):
        # 一月沪伦比计算
        if not self.lme_3 or not self.contract1_price:
            return {}
        self.hulun_1m = round(float(float(self.contract1_price) / float(self.lme_3)), 4)
        return {'hulun_1m': self.hulun_1m}

    @property
    def cal_3m_hulun(self):
        # 三月沪伦比计算
        if not self.lme_3 or not self.contract3_price:
            return {}
        self.hulun_3m = round(float(float(self.contract3_price) / float(self.lme_3)), 4)
        return {'hulun_3m': self.hulun_3m}

    @property
    def cal_position_deff(self):
        """计算持仓差值"""
        self.position_deff = self.today_position - self.yesterday_position
        return {'position_deff': self.position_deff}


class BaseInitPreprocess(object):
    """初始化基类"""

    def __init__(self, varieties, date, exchange, *args, **kwargs):
        super(BaseInitPreprocess, self).__init__(*args, **kwargs)
        if not hasattr(self, 'pre_obj'):
            self.pre_obj = BasePreprocess()
        # self.pre_obj.varieties = varieties
        # self.pre_obj.name = varieties
        # self.pre_obj.date = date
        self.varieties = varieties
        self.date = date
        self.exchange = exchange

        # self.init_main_contract_price()

    def init_main_contract(self):
        """初始化主力合约数据"""
        _logger.info('初始化主力合约数据, 品类: %s, 时间: %s' % (self.varieties, self.date))
        contract_objs = self.db.query(MainContract).filter(MainContract.settlement_date == self.date[:10],
                                                      MainContract.varieties == self.varieties,
                                                      MainContract.exchange == self.exchange).all()
        if contract_objs:
            obj = contract_objs and contract_objs[0]
            self.pre_obj.main_contract = obj.to_dict()
            # pre_obj.handler = handler
            # self.pre_obj.varieties = varieties
            # self.pre_obj.date = self.date
        else:
            # check_log.error('主力合约信息不存在--品目: %s, 日期: %s'%(self.varieties, self.date))
            _logger.info('主力合约信息不存在')
            return 'exit'


    def init_main_contract_price(self):
        """初始化主力合约价格"""
        new_date = self.date+' 00:00:00'
        dk_objs = self.db.query(DayKline).filter(DayKline.contract == self.pre_obj.main_contract['main_contract'],
                                            DayKline.date_time == new_date).all()
        if dk_objs:
            dk_obj = dk_objs[0]
            self.pre_obj.main_price_close = dk_obj.price_close or 0.0
            self.pre_obj.main_price_open = dk_obj.price_open or 0.0
            self.pre_obj.main_price_high = dk_obj.price_high or 0.0
            self.pre_obj.main_price_low = dk_obj.price_low or 0.0
            self.pre_obj.main_contract_price = dk_obj.settlement_price or dk_obj.price_close or 0.0
        return


    def init_month_position(self):
        """初始化月度持仓"""
        this_serial_contract1 = self.pre_obj.main_contract['serial_contract1']
        self.pre_obj.this_month_position = self.get_month_position(this_serial_contract1)
        if self.pre_obj.this_month_position:
            this_month_first_day = self.pre_obj.this_month_position[-1]['date']
            contract_objs = self.db.query(MainContract).filter(MainContract.settlement_date < this_month_first_day,
                                                          MainContract.varieties == self.varieties,
                                                          MainContract.exchange == self.exchange).\
                                                          order_by(desc(MainContract.settlement_date)).all()
            contract_obj = contract_objs[0]
            last_serial_contract1 = contract_obj.serial_contract1
            self.pre_obj.last_month_position = self.get_month_position(last_serial_contract1)


    def get_month_position(self, serial_contract1):
        """获取月度持仓"""
        contract_objs = self.db.query(MainContract).\
                        filter(MainContract.serial_contract1 == serial_contract1).\
                        order_by(desc(MainContract.settlement_date)).all()
        res = []
        for contract_obj in contract_objs:
            date_time = str(contract_obj.settlement_date) + ' 00:00:00'
            dk_objs = self.db.query(DayKline).filter(DayKline.date_time == date_time,
                                                DayKline.contract == contract_obj.serial_contract1).all()
            if not dk_objs:
                continue
            dk_obj = dk_objs[0]
            res.append({
                'date': str(contract_obj.settlement_date),
                'vals': dk_obj.openinterest,
            })
        return res

    def init_position(self):
        """获取主力合约今天和昨天的持仓"""
        contract_objs = self.db.query(MainContract).filter(MainContract.settlement_date <= self.date,
                                                           MainContract.varieties == self.varieties)\
                                                        .order_by(desc(MainContract.settlement_date)).all()
        if len(contract_objs) < 2:
            return
        yes_contract = self.varieties+'9999'
        yesterday = str(contract_objs[1].settlement_date)
        dk_objs = self.db.query(DayKline).filter(DayKline.date_time == self.date+' 00:00:00',
                                                 DayKline.contract == self.pre_obj.main_contract['main_contract']).all()
        if dk_objs:
            self.pre_obj.today_position = dk_objs[0].openinterest
        yes_dk_objs = self.db.query(DayKline).filter(DayKline.date_time == yesterday+' 00:00:00',
                                                     DayKline.contract == yes_contract).all()
        if yes_dk_objs:
            self.pre_obj.yesterday_position = yes_dk_objs[0].openinterest

    def init_month_stock(self):
        """初始化月度库存"""
        this_month = self.date
        last_month = str(when._add_time(datetime.strptime(self.date, '%Y-%m-%d'), months=-1))
        self.pre_obj.this_month_stock = self.get_month_stock(this_month)
        self.pre_obj.last_month_stock = self.get_month_stock(last_month)

    def get_month_stock(self, date):
        """获取月度库存"""
        res = []
        this_month = date[:7]
        stock_objs = self.db.query(SpotStock).filter(SpotStock.area == '总计',
                                                SpotStock.date.like(this_month+'%'),
                                                SpotStock.varieties == self.varieties).\
                                                order_by(desc(SpotStock.date)).all()
        for obj in stock_objs:
            res.append(
                {
                    'date': obj.date,
                    'vals': obj.amount,
                }
            )
        return res

    def init_last_year_stock_in(self):
        """初始化今天和去年今天库存"""

        stock_objs = self.db.query(SpotStock).filter(SpotStock.area == '总计',
                                                     SpotStock.date.like(self.date + '%'),
                                                     SpotStock.varieties == self.varieties). \
                                                order_by(desc(SpotStock.date)).all()
        if stock_objs:
            self.pre_obj.today_stock_in = stock_objs[0].amount
        last_year = str(when._add_time(datetime.strptime(self.date, '%Y-%m-%d'), years=-1))
        new_stock_objs = self.db.query(SpotStock).filter(SpotStock.area == '总计',
                                                        SpotStock.date <= last_year,
                                                        SpotStock.varieties == self.varieties).\
                                                order_by(desc(SpotStock.date)).all()
        if new_stock_objs:
            last_year_date = new_stock_objs[0].date
            if str(last_year_date)[:4] != last_year[:4]:
                new_stock_objs2 = self.db.query(SpotStock).filter(SpotStock.area == '总计',
                                                                 SpotStock.date <= last_year,
                                                                 SpotStock.varieties == self.varieties). \
                                                            order_by(desc(SpotStock.date)).all()
                if new_stock_objs2:
                    self.pre_obj.last_year_stock_in = new_stock_objs2[0].amount
            else:
                self.pre_obj.last_year_stock_in = new_stock_objs[0].amount

    def init_month_warehouse_receipts(self):
        """初始化月度仓单"""
        this_month = self.date
        last_month = str(when._add_time(datetime.strptime(self.date, '%Y-%m-%d'), months=-1))
        self.pre_obj.this_month_warehouse_receipts = self.get_month_warehouse_receipts(this_month)
        self.pre_obj.last_month_warehouse_receipts = self.get_month_warehouse_receipts(last_month)

    def get_month_warehouse_receipts(self, date):
        """获取月度仓单"""
        res = []
        this_month = date[:7]
        ware_objs = self.db.query(SpotWarehouseReceipt).filter(SpotWarehouseReceipt.area == '总计',
                                                                SpotWarehouseReceipt.source == 'shfe',
                                                                SpotWarehouseReceipt.date.like(this_month + '%'),
                                                                SpotWarehouseReceipt.varieties == self.varieties).\
                                                        order_by(desc(SpotWarehouseReceipt.date)).all()
        for obj in ware_objs:
            res.append(
                {
                    'date': obj.date,
                    'vals': obj.amount,
                }
            )
        return res

    def get_spot_price(self, date, source):
        """获取现货价格"""
        res = 0.0
        date = str(date)[:10]
        spot_objs = self.db.query(SpotPriceSummary).filter(SpotPriceSummary.date == date,
                                                           SpotPriceSummary.varieties == self.pre_obj.varieties,
                                                           SpotPriceSummary.source == source).all()
        if spot_objs:
            res = spot_objs[0].price
        return res

    def get_last_time_spot_price(self, date, source, tp='month'):
        """获取现货价格"""
        res = 0.0
        date = str(date)[:10]
        spot_objs = self.db.query(SpotPriceSummary).filter(SpotPriceSummary.date <= date,
                                                           SpotPriceSummary.varieties == self.pre_obj.varieties,
                                                           SpotPriceSummary.source == source).\
                                                    order_by(desc(SpotPriceSummary.date)).all()
        if not spot_objs:
            return res
        obj = spot_objs[0]
        if tp == 'month':
            check1 = str(obj.date)[5:7]
            check2 = date[5:7]
        else:
            check1 = str(obj.date)[:4]
            check2 = date[:4]
        if check1 != check2:
            new_spot_objs = self.db.query(SpotPriceSummary).filter(SpotPriceSummary.date > date,
                                                               SpotPriceSummary.varieties == self.pre_obj.varieties,
                                                               SpotPriceSummary.source == source).\
                                                        order_by(SpotPriceSummary.date).all()
            if new_spot_objs:
                res = new_spot_objs[0].price
        else:
            res = obj.price

        return res

    def init_smm_spot_price(self):
        """初始化上海有色网现货价格"""
        self.pre_obj.today_smm_spot_price = self.get_spot_price(self.pre_obj.date, 'smm')
        date = datetime.strptime(self.pre_obj.date, '%Y-%m-%d')
        last_week_day = date - timedelta(days=7)
        self.pre_obj.last_week_smm_spot_price = self.get_spot_price(last_week_day, 'smm')

    def init_shmet_spot_price(self):
        """初始化上海金属网现货价格"""
        self.pre_obj.today_shmet_spot_price = self.get_spot_price(self.pre_obj.date, 'shmet')
        date = datetime.strptime(self.pre_obj.date, '%Y-%m-%d')
        last_week_day = date - timedelta(days=7)
        self.pre_obj.last_week_shmet_spot_price = self.get_spot_price(last_week_day, 'shmet')

    def init_smm_last_month_spot_price(self):
        """初始化上个月今天的现货价格"""
        if not self.pre_obj.today_smm_spot_price:
            self.pre_obj.today_smm_spot_price = self.get_spot_price(self.pre_obj.date, 'smm')
        last_month = str(when._add_time(datetime.strptime(self.date, '%Y-%m-%d'), months=-1))
        self.pre_obj.last_month_smm_spot_price = self.get_last_time_spot_price(last_month, 'smm')

    def init_smm_last_year_spot_price(self):
        """初始化去年今天的现货价格"""
        if not self.pre_obj.today_smm_spot_price:
            self.pre_obj.today_smm_spot_price = self.get_spot_price(self.pre_obj.date, 'smm')
        last_month = str(when._add_time(datetime.strptime(self.date, '%Y-%m-%d'), years=-1))
        self.pre_obj.last_year_smm_spot_price = self.get_last_time_spot_price(last_month, 'smm', tp='year')

    def init_shmet_last_month_spot_price(self):
        """初始化上个月今天的现货价格"""
        if not self.pre_obj.today_shmet_spot_price:
            self.pre_obj.today_shmet_spot_price = self.get_spot_price(self.pre_obj.date, 'shmet')
        last_month = str(when._add_time(datetime.strptime(self.date, '%Y-%m-%d'), months=-1))
        self.pre_obj.last_month_shmet_spot_price = self.get_last_time_spot_price(last_month, 'shmet')

    def init_shmet_last_year_spot_price(self):
        """初始化去年今天的现货价格"""
        if not self.pre_obj.today_shmet_spot_price:
            self.pre_obj.today_shmet_spot_price = self.get_spot_price(self.pre_obj.date, 'shmet')
        last_month = str(when._add_time(datetime.strptime(self.date, '%Y-%m-%d'), years=-1))
        self.pre_obj.last_year_shmet_spot_price = self.get_last_time_spot_price(last_month, 'shmet', tp='year')

    def init_delivery_month_inner_bwd(self):
        """初始化月度(持仓月)国内升贴水"""
        this_serial_contract1 = self.pre_obj.main_contract['serial_contract1']
        self.pre_obj.this_delivery_month_inner_bwd = self.get_delivery_month_inner_bwd(this_serial_contract1)
        if self.pre_obj.this_month_position:
            this_month_first_day = self.pre_obj.this_month_position[-1]['date']
            contract_objs = self.db.query(MainContract).filter(MainContract.settlement_date < this_month_first_day,
                                                               MainContract.varieties == self.varieties,
                                                               MainContract.exchange == self.exchange). \
                order_by(desc(MainContract.settlement_date)).all()
            contract_obj = contract_objs[0]
            last_serial_contract1 = contract_obj.serial_contract1
            self.pre_obj.last_delivery_month_inner_bwd = self.get_delivery_month_inner_bwd(last_serial_contract1)

    def get_delivery_month_inner_bwd(self, serial_contract1):
        """获取月度持仓"""
        contract_objs = self.db.query(MainContract). \
            filter(MainContract.serial_contract1 == serial_contract1). \
            order_by(desc(MainContract.settlement_date)).all()
        res = []
        for contract_obj in contract_objs:
            date_time = str(contract_obj.settlement_date)
            bwd_objs = self.db.query(FutureBwdSummary).filter(FutureBwdSummary.date == date_time,
                                                             FutureBwdSummary.varieties == self.varieties,
                                                             FutureBwdSummary.source == 'shmet').all()
            if not bwd_objs:
                continue
            bwd_obj = bwd_objs[0]
            res.append({
                'date': str(contract_obj.settlement_date),
                'vals': bwd_obj.price,
            })
        return res


    def init_bwd(self):
        """初始化升贴水的价格"""
        # 获取升贴水的价格
        self.pre_obj.bwd = 0
        bwd_objs = self.db.query(FutureBwdSummary).filter(FutureBwdSummary.source == 'shmet_bonded',
                                                         FutureBwdSummary.varieties == self.varieties,
                                                          FutureBwdSummary.date == self.date[:10]).all()
        if bwd_objs:
            bwd_obj = bwd_objs[0]
            self.pre_obj.bwd = float(bwd_obj.price or 0)
        else:
            self.pre_obj.bwd = 0

    def init_change(self):
        """初始化调水"""
        # 获取调水
        self.pre_obj.change = 0
        bwd_objs = self.db.query(FutureBwdSummary).filter(FutureBwdSummary.source == 'shmet_lme',
                                                          FutureBwdSummary.varieties == self.varieties,
                                                          FutureBwdSummary.date == self.date[:10]).all()
        if bwd_objs:
            bwd_obj = bwd_objs[0]
            price_high = float(bwd_obj.price_high or 0)
            price_low = float(bwd_obj.price_low or 0)
            self.pre_obj.change = (price_high + price_low) / 2
        else:
            self.pre_obj.change = 0

    def init_internal_bwd(self):
        """初始化国内升贴水"""
        self.pre_obj.internal_bwd = 0
        bwd_objs = self.db.query(FutureBwdSummary).filter(FutureBwdSummary.source == 'shmet',
                                                          FutureBwdSummary.varieties == self.varieties,
                                                          FutureBwdSummary.date == self.date[:10]).all()
        if bwd_objs:
            bwd_obj = bwd_objs[0]
            self.pre_obj.internal_bwd = float(bwd_obj.price or 0)
        else:
            self.pre_obj.internal_bwd = 0

    def init_lme_3(self):
        """初始化lme_3的价格"""
        lme_price = {
            'al': 'LALS',
            'cu': 'LCPS',
            'ni': 'LNKS',
            'pb': 'LLDS',
            # 'SND': '',
            'zn': 'LZNS',
        }

        self.pre_obj.lme_3 = 0

        # detail_objs = self.db.query(FuturePriceDetail).filter(FuturePriceDetail.source == 'sina_lme',
        #                                                    FuturePriceDetail.varieties == self.varieties,
        #                                                  FuturePriceDetail.date_time.like('%'+self.date[:10]+'%')).\
        #                                                     order_by(desc(FuturePriceDetail.date_time)).all()
        detail_objs = self.db.query(DayKline).filter(DayKline.contract == lme_price.get(self.varieties, '0000000'),
                                                     DayKline.date_time == self.date[:10]+' 00:00:00').all()

        if detail_objs:
            detail_obj = detail_objs[0]
            if detail_obj.settlement_price:
                self.pre_obj.lme_3 = float(detail_obj.settlement_price)
            elif detail_obj.price_close:
                self.pre_obj.lme_3 = float(detail_obj.price_close or 0)
            else:
                self.pre_obj.lme_3 = 0.0
            # self.pre_obj.lme_3 = float(detail_obj.price or 0)
        else:
            self.pre_obj.lme_3 = 0


    def init_exchange(self):
        """初始化周汇率"""
        self.pre_obj.exchange_now = 0
        exchange_objs = self.db.query(FutureExchange).filter(FutureExchange.future == '1w',
                                                             FutureExchange.date == self.date).\
                                                    order_by(desc(FutureExchange.date)).all()

        if exchange_objs:
            exchange_obj = exchange_objs[0]
            self.pre_obj.exchange_now = float(exchange_obj.price or 0)
        else:
            self.pre_obj.exchange_now = 0


    def init_exchange_1m(self):
        """ 一月期汇率"""
        self.pre_obj.exchange_1m = 0
        exchange_objs = self.db.query(FutureExchange).filter(FutureExchange.future == '1m').order_by(desc(FutureExchange.date)).all()

        if exchange_objs:
            exchange_obj = exchange_objs[0]
            self.pre_obj.exchange_1m = float(exchange_obj.price or 0)
        else:
            self.pre_obj.exchange_1m = 0



    def init_exchange_2m(self):
        """初始化  二月期汇率 """
        self.pre_obj.exchange_2m = 0
        exchange_objs = self.db.query(FutureExchange).filter(FutureExchange.future == '2m').order_by(desc(FutureExchange.date)).all()

        if exchange_objs:
            exchange_obj = exchange_objs[0]
            self.pre_obj.exchange_2m = float(exchange_obj.price or 0)
        else:
            self.pre_obj.exchange_2m = 0


    def init_exchange_3m(self):
        """初始化周汇率  三月期汇率"""
        self.pre_obj.exchange_3m = 0
        exchange_objs = self.db.query(FutureExchange).filter(FutureExchange.future == '3m').order_by(desc(FutureExchange.date)).all()

        if exchange_objs:
            exchange_obj = exchange_objs[0]
            self.pre_obj.exchange_3m = float(exchange_obj.price or 0)
        else:
            self.pre_obj.exchange_3m = 0


    def init_exchange_6m(self):
        """初始化周汇率  六月期汇率"""
        self.pre_obj.exchange_6m = 0
        exchange_objs = self.db.query(FutureExchange).filter(FutureExchange.future == '6m').order_by(desc(FutureExchange.date)).all()

        if exchange_objs:
            exchange_obj = exchange_objs[0]
            self.pre_obj.exchange_6m = float(exchange_obj.price or 0)
        else:
            self.pre_obj.exchange_6m = 0

    def init_output_import(self):
        """初始化产量和进口量"""
        output_symbol = OUTPUT_SYMBOL_MAP.get(self.varieties.lower())
        import_symbol = IMPORT_AMOUNT_MAP.get(self.varieties.lower())
        if output_symbol and import_symbol:
            # out_rate_objs = self.db.query(Symbol)
            out_rate_objs = self.db.execute("select benchmark from symbol where symbol = '%s'"%output_symbol).fetchone()
            out_rate = out_rate_objs and out_rate_objs[0] or 1
            out_objs = self.db.query(DataWind).filter(DataWind.symbol == output_symbol,
                                                      DataWind.date == self.date).\
                                                order_by(desc(DataWind.date)).all()
            if out_objs:
                self.pre_obj.output = float(out_objs[0].amount) * float(out_rate)

            import_objs = self.db.query(DataWind).filter(DataWind.symbol == import_symbol,
                                                      DataWind.date == self.date).\
                                                order_by(desc(DataWind.date)).all()

            import_rate_objs = self.db.execute(
                "select benchmark from symbol where symbol = '%s'" % import_symbol).fetchone()
            import_rate = import_rate_objs and import_rate_objs[0] or 1
            if import_objs:
                self.pre_obj.import_amount = float(import_objs[0].amount) * float(import_rate)


class BaseResPreprocess(object):
    """获取数据"""

    # persis_obj_map = {}
    # varieties_map = {}

    def __init__(self, *args, **kwargs):
        super(BaseResPreprocess, self).__init__(*args, **kwargs)
        persis_obj_map = {}
        varieties_map = {}
        self.res = {}
        # if not hasattr(self, 'persis_obj_map'):
        #     self.persis_obj_map = {}
        # if not hasattr(self, 'varieties_map'):
        #     self.varieties_map = {}


    def get_hlun_price_diff(self):
        """沪伦差价"""
        self.res.update(self.pre_obj.caculate_hlun_price_diff)


    def get_cross_star(self):
        """获取十字星比值"""
        self.res.update(self.pre_obj.caculate_cross_star)

    def get_stock_ratio(self):
        """获取库存环比"""
        self.update_ring_rate(self.pre_obj.caculate_stock_ratio)

    def get_position_chain(self):
        self.update_ring_rate(self.pre_obj.caculate_position_chain)

    def get_warehouse_receipts(self):
        self.update_ring_rate(self.pre_obj.calculation_warehouse_receipts)

    def update_ring_rate(self, data):
        """更新或者插入环比"""
        for vals in data:
            date = vals['date']
            key = vals['key']
            amount = vals['amount']
            obj = DAY_PARA_MODEL_MAP.get(key)
            if not obj:
                continue
            symbol = self.get_day_symbol(key)
            pre_objs = self.db.query(obj).filter(obj.date == date, obj.symbol == symbol).all()
            if not symbol:
                continue
            # today = str(datetime.now())[:10]
            if pre_objs:
                pre_obj = pre_objs[0]
                pre_obj.amount = amount
            else:
                new_pre_obj = obj(date=date, symbol=symbol, amount=amount)
                self.db.add(new_pre_obj)
            self.db.commit()


    def get_day_symbol(self, key):
        """获取日symbol"""
        varieties = self.pre_obj.varieties
        if varieties.lower() not in DAY_VARIEYIES_DICT or key not in PRE_SYMBOL:
            return None
        return DAY_VARIEYIES_DICT[varieties.lower()] + PRE_SYMBOL[key]


    def get_symbol(self, key):
        """获取symbol"""
        varieties = self.pre_obj.varieties
        if varieties.lower() not in self.varieties_map or key not in PRE_SYMBOL:
            return None
        return self.varieties_map[varieties.lower()] + PRE_SYMBOL[key]


    def save_symbol_data(self, res, date):
        """更新或插入symbol"""
        for key in res:
            symbol = self.get_symbol(key)
            if symbol:
                obj = self.persis_obj_map.get(key)
                if obj:
                    pre_objs = self.db.query(obj).filter(obj.date == date, obj.symbol == symbol).all()
                    if pre_objs:
                        pre_obj = pre_objs[0]
                        pre_obj.amount = res[key]
                    else:
                        new_pre_obj = obj(date=date, symbol=symbol, amount=res[key])
                        self.db.add(new_pre_obj)
        self.db.commit()


    def get_smm_spot_price_diff(self):
        self.res.update(self.pre_obj.calculation_smm_spot_price_diff)


    def get_shmet_spot_price_diff(self):
        self.res.update(self.pre_obj.calculation_shmet_spot_price_diff)


    def get_basic_rate(self):
        """获取基差比值"""
        self.res.update(self.pre_obj.calculation_basic_rate)


    def get_basic(self):
        self.res.update(self.pre_obj.calculation_basic)


    def common_update_capital_value(self, date, obj):
        """从day_kline中生成日线和分钟线"""
        product_class = PRODUCT_CLASS_MAP.get(self.pre_obj.varieties.lower())
        if not product_class:
            return
        contract = self.pre_obj.varieties.lower()+'8888'
        date_time = self.pre_obj.date + " 00:00:00"
        dk_objs = self.db.query(DayKline).filter(DayKline.contract == contract,
                                                 DayKline.date_time == date_time).all()
        if not dk_objs:
            return
        dk_obj = dk_objs[0]
        vals_objs = self.db.query(obj).filter(obj.date == date,
                                              obj.varieties == self.pre_obj.varieties,
                                              obj.exchange == self.pre_obj.exchange).all()
        flow = dk_obj.flow_fund or 0.0
        precipitation = dk_obj.sendimentary_money or 0.0
        if vals_objs:
            vals_obj = vals_objs[0]
            vals_obj.flow = flow
            vals_obj.precipitation = precipitation
            if len(vals_objs) > 1:
                for i in range(1, len(vals_objs)):
                    self.db.delete(vals_objs[i])
        else:
            new_vals = {
                'date': date,
                'exchange': self.pre_obj.exchange,
                'product_class': product_class,
                'flow': flow or 0,
                'precipitation': precipitation,
                'varieties': self.pre_obj.varieties,
            }
            new_obj = obj(**new_vals)
            self.db.add(new_obj)


    def get_hulun_rate(self):
        self.res.update(self.pre_obj.cal_1m_hulun)
        self.res.update(self.pre_obj.cal_3m_hulun)


    def get_position_deff(self):
        """获取主力合约的持仓差(今天 - 昨天)"""
        self.res.update(self.pre_obj.cal_position_deff)

    def get_smm_spot_month_deff(self):
        """有色网现货价格月差"""
        self.res.update(self.pre_obj.cal_smm_spot_month_deff)

    def get_smm_spot_year_deff(self):
        """有色网现货价格年差"""
        self.res.update(self.pre_obj.cal_smm_spot_year_deff)

    def get_shmet_spot_month_deff(self):
        """上海金属网现货价格月差"""
        self.res.update(self.pre_obj.cal_shmet_spot_month_deff)

    def get_shmet_spot_year_deff(self):
        """上海金属网现货价格年差"""
        self.res.update(self.pre_obj.cal_shmet_spot_year_deff)

    def get_delivery_month_position_deff(self):
        """持仓月差"""
        self.res.update(self.pre_obj.cal_delivery_month_position_deff)

    def get_month_warehouse_deff(self):
        """仓单月差"""
        self.res.update(self.pre_obj.cal_month_warehouse_deff)

    def get_delivery_month_bwd_deff(self):
        """持仓月升贴水差"""
        self.res.update(self.pre_obj.cal_delivery_month_bwd_deff)

    def get_total_output(self):
        self.res.update(self.pre_obj.cal_total_output)