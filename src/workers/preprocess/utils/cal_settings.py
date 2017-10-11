


COMMON_RES_DAEL_LIST = [
    'update_capital_value',
]

COMMON_INIT_LIST = [
    'init_main_contract', #初始化主力合约
]

DAY_COMMON_INIT_LIST = [

]

MIN_COMMON_INIT_LIST = [

]



MIN_INIT_PATA_MAP = {
    'cu': ['init_serial_price', 'init_bwd', 'init_change', 'init_internal_bwd',
           'init_lme_3', 'init_exchange', 'init_exchange_1m', 'init_exchange_2m', 'init_exchange_3m',
           'init_exchange_6m', 'init_main_contract_price',
           'init_month_position', 'init_month_stock', 'init_smm_spot_price', 'init_month_warehouse_receipts',
           'init_position', 'init_smm_last_month_spot_price', 'init_smm_last_year_spot_price', 'init_last_year_stock_in',
           'init_delivery_month_inner_bwd',
           ],

    'al': ['init_serial_price', 'init_bwd', 'init_change', 'init_internal_bwd',
           'init_lme_3', 'init_exchange', 'init_exchange_1m', 'init_exchange_2m', 'init_exchange_3m',
           'init_exchange_6m'],

    'pb': ['init_serial_price', 'init_bwd', 'init_change', 'init_internal_bwd',
           'init_lme_3', 'init_exchange', 'init_exchange_1m', 'init_exchange_2m', 'init_exchange_3m',
           'init_exchange_6m'],

    'zn': ['init_serial_price', 'init_bwd', 'init_change', 'init_internal_bwd',
           'init_lme_3', 'init_exchange', 'init_exchange_1m', 'init_exchange_2m', 'init_exchange_3m',
           'init_exchange_6m', 'init_main_contract_price',
           'init_month_position', 'init_month_stock', 'init_shmet_spot_price', 'init_month_warehouse_receipts',
           'init_position', 'init_shmet_last_month_spot_price', 'init_shmet_last_year_spot_price', 'init_last_year_stock_in',
           'init_delivery_month_inner_bwd',

           ],

    'ni': ['init_serial_price_1_5_9', 'init_bwd', 'init_change', 'init_internal_bwd',
           'init_lme_3', 'init_exchange', 'init_exchange_1m', 'init_exchange_2m', 'init_exchange_3m',
           'init_exchange_6m'],

    "hc": ['init_serial_price_1_5_10'],  # 热卷
    "i": ['init_serial_price_1_5_9'],  # 铁矿
    "j": ['init_serial_price_1_5_9'],  # 焦炭
    "jd": ['init_serial_price'],  # 鸡蛋
    "jm": ['init_serial_price_1_5_9'],  # 焦煤
    "l": ['init_serial_price_1_5_9'],  # 塑料
    "m": ['init_serial_price_1_5_9'],  # 豆粕
    "ma": ['init_serial_price_1_5_9'],  # 郑醇
    "pp": ['init_serial_price_1_5_9'],  # PP
    "rb": ['init_serial_price_1_5_10'],  # 螺纹
    "rm": ['init_serial_price_1_5_9'],  # 菜粕
    "ru": ['init_serial_price_1_5_9'],  # 橡胶
    "ta": ['init_serial_price_1_5_9'],  # PTA
    "v": ['init_serial_price_1_5_9'],  # PVC
    "zc": ['init_serial_price_1_5_9'],  # 郑煤


}


MIN_RES_DEAL_MAP = {
    'cu': ['in_and_out', 'get_basic', 'get_hlun_price_diff', 'get_cross_star',
           'get_stock_ratio', 'get_position_chain', 'get_basic_rate', 'get_smm_spot_price_diff',
           'get_warehouse_receipts', 'get_position_deff',
           'get_smm_spot_month_deff', 'get_smm_spot_year_deff', 'get_shmet_spot_month_deff', 'get_shmet_spot_year_deff',
           'get_delivery_month_position_deff', 'get_month_warehouse_deff', 'get_delivery_month_bwd_deff',

           ],

    'al': ['in_and_out', 'get_basic'],

    'pb': ['in_and_out', 'get_basic'],

    'zn': ['in_and_out', 'get_basic', 'get_hlun_price_diff', 'get_cross_star',
           'get_stock_ratio', 'get_position_chain', 'get_basic_rate', 'get_shmet_spot_price_diff',
           'get_warehouse_receipts', 'get_position_deff',
           'get_smm_spot_month_deff', 'get_smm_spot_year_deff', 'get_shmet_spot_month_deff', 'get_shmet_spot_year_deff',
           'get_delivery_month_position_deff', 'get_month_warehouse_deff', 'get_delivery_month_bwd_deff'

           ],

    'ni': ['in_and_out', 'get_basic'],

    "hc": ['get_basic'], #热卷
    "i": ['get_basic'], #铁矿
    "j": ['get_basic'], #焦炭
    "jd": ['get_basic'], #鸡蛋
    "jm": ['get_basic'], #焦煤
    "l": ['get_basic'], #塑料
    "m": ['get_basic'], #豆粕
    "ma": ['get_basic'], #郑醇
    "pp": ['get_basic'], #PP
    "rb": ['get_basic'], #螺纹
    "rm": ['get_basic'], #菜粕
    "ru": ['get_basic'], #橡胶
    "ta": ['get_basic'], #PTA
    "v": ['get_basic'], #PVC
    "zc": ['get_basic'], #郑煤

}


DAY_INIT_PATA_MAP = MIN_INIT_PATA_MAP.copy()

DAY_INIT_PATA_MAP.update(
    {
#
        'cu': ['init_serial_price', 'init_bwd', 'init_change', 'init_internal_bwd',
               'init_lme_3', 'init_exchange', 'init_exchange_1m', 'init_exchange_2m', 'init_exchange_3m',
               'init_exchange_6m', 'init_main_contract_price',
               'init_month_position', 'init_month_stock', 'init_smm_spot_price', 'init_month_warehouse_receipts',
               'init_position', 'init_smm_last_month_spot_price', 'init_smm_last_year_spot_price',
               'init_last_year_stock_in', 'init_output_import',
               'init_delivery_month_inner_bwd',
               ],

        'al': ['init_serial_price', 'init_bwd', 'init_change', 'init_internal_bwd',
               'init_lme_3', 'init_exchange', 'init_exchange_1m', 'init_exchange_2m', 'init_exchange_3m',
               'init_exchange_6m', 'init_output_import',
               ],

        'pb': ['init_serial_price', 'init_bwd', 'init_change', 'init_internal_bwd',
               'init_lme_3', 'init_exchange', 'init_exchange_1m', 'init_exchange_2m', 'init_exchange_3m',
               'init_exchange_6m', 'init_output_import',],

        'zn': ['init_serial_price', 'init_bwd', 'init_change', 'init_internal_bwd',
               'init_lme_3', 'init_exchange', 'init_exchange_1m', 'init_exchange_2m', 'init_exchange_3m',
               'init_exchange_6m', 'init_main_contract_price',
               'init_month_position', 'init_month_stock', 'init_shmet_spot_price', 'init_month_warehouse_receipts',
               'init_position', 'init_shmet_last_month_spot_price', 'init_shmet_last_year_spot_price',
               'init_last_year_stock_in', 'init_output_import',
               'init_delivery_month_inner_bwd',

               ],
    }
)



DAY_RES_DEAL_MAP = MIN_RES_DEAL_MAP.copy()
DAY_RES_DEAL_MAP.update(
    {
        'cu': ['in_and_out', 'get_basic', 'get_hlun_price_diff', 'get_cross_star',
               'get_stock_ratio', 'get_position_chain', 'get_basic_rate', 'get_smm_spot_price_diff',
               'get_warehouse_receipts', 'get_position_deff',
               'get_smm_spot_month_deff', 'get_smm_spot_year_deff', 'get_shmet_spot_month_deff', 'get_shmet_spot_year_deff',
               'get_delivery_month_position_deff', 'get_month_warehouse_deff', 'get_delivery_month_bwd_deff',
               'get_total_output',

           ],

        'al': ['in_and_out', 'get_basic', 'get_total_output',],

        'pb': ['in_and_out', 'get_basic', 'get_total_output',],

        'zn': ['in_and_out', 'get_basic', 'get_hlun_price_diff', 'get_cross_star',
               'get_stock_ratio', 'get_position_chain', 'get_basic_rate', 'get_shmet_spot_price_diff',
               'get_warehouse_receipts', 'get_position_deff',
               'get_smm_spot_month_deff', 'get_smm_spot_year_deff', 'get_shmet_spot_month_deff', 'get_shmet_spot_year_deff',
               'get_delivery_month_position_deff', 'get_month_warehouse_deff', 'get_delivery_month_bwd_deff',
               'get_total_output',

               ],

        'ni': ['get_in_and_out_other', 'get_basic'],


})

for var in MIN_INIT_PATA_MAP:
    MIN_INIT_PATA_MAP[var] = COMMON_INIT_LIST + MIN_INIT_PATA_MAP[var]

for var in DAY_INIT_PATA_MAP:
    DAY_INIT_PATA_MAP[var] = COMMON_INIT_LIST + DAY_INIT_PATA_MAP[var]