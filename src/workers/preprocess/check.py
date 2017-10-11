
# from utils.cal_settings import
import logging
import os

check_logger = logging.getLogger('check')


def check(init_obj, init_lst):
    obj = init_obj.pre_obj
    for method in init_lst:
        if method in check_map:
            check_map[method](obj)


def check_serial_price(obj):
    """检查连1,2,3,6合约价格是否存在"""
    # obj = init_obj.pre_obj
    for i in [1, 2, 3, 6]:
        name = 'contract' + str(i) + '_price'
        if not hasattr(obj, name):
            check_logger.info('env: %s :price_check: 连(%s)合约价格不存在, 品类: %s, 日期(或时间): %s'%(os.environ['ALPHA_ENV'], i, obj.varieties, obj.date))
        elif getattr(obj, name) == 0:
            check_logger.info('env: %s :price_check: 连(%s)合约价格等于零, 品类: %s, 日期(或时间): %s'%(os.environ['ALPHA_ENV'], i, obj.varieties, obj.date))


def check_serial_price_other(obj):
    """检查连1,2,3合约价格是否存在"""
    # obj = init_obj.pre_obj
    for i in [1, 2, 3]:
        name = 'contract' + str(i) + '_price'
        if not hasattr(obj, name):
            check_logger.info('price_check: 连(%s)合约价格不存在, 品类: %s, 日期(或时间): %s'%(i, obj.varieties, obj.date))
        elif getattr(obj, name) == 0:
            check_logger.info('price_check: 连(%s)合约价格等于零, 品类: %s, 日期(或时间): %s' % (i, obj.varieties, obj.date))


check_map = {
    'init_serial_price': check_serial_price,
    'init_serial_price_1_5_9': check_serial_price_other,
    'init_serial_price_1_5_10': check_serial_price_other,
    # 'init_bwd', 'init_change', 'init_internal_bwd',
    # 'init_lme_3', 'init_exchange', 'init_exchange_1m', 'init_exchange_2m', 'init_exchange_3m',
    # 'init_exchange_6m', 'init_main_contract_price',
    # 'init_month_position', 'init_month_stock', 'init_smm_spot_price', 'init_month_warehouse_receipts',
    # 'init_position',
 }