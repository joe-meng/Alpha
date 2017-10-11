import sys
from datetime import datetime, timedelta
sys.path.append("../..")


args_lst = sys.argv[1:]
arg = args_lst and args_lst[0] or 'all'


# from models.models import Symbol, Session
# from utils.enums import PRE_SYMBOL, MIN_VARIEYIES_DICT, DAY_VARIEYIES_DICT


# db = Session()

def update_or_create_symbol(symbol, vals):
    from models.models import Symbol, Session
    """更新或删除symbol表"""
    db = Session()
    now = str(datetime.now())[:19]
    symbol_objs = db.query(Symbol).filter(Symbol.symbol == symbol).all()
    if symbol_objs:
        obj = symbol_objs[0]
        for key in vals:
            obj.updated_at = now
            setattr(obj, key, vals[key])
        if len(symbol_objs) > 1:
            for index in range(1, len(symbol_objs)):
                db.delete(symbol_objs[index])
    else:
        new_obj = Symbol(**vals)
        new_obj.updated_at = now
        db.add(new_obj)
    db.commit()
    db.close()


def update_base_symbol():
    """更新基差的symbol"""
    from utils.enums import PRE_SYMBOL, MIN_VARIEYIES_DICT, DAY_VARIEYIES_DICT
    # ('一月和二月的差值', 'PE000037', 'min_preprocess', '预计算-分钟数据', 'min', 'Cu'),
    # ('一月和三月的差值', 'PE000038', 'min_preprocess', '预计算-分钟数据', 'min', 'Cu'),
    # ('二月和三月的差值', 'PE000039', 'min_preprocess', '预计算-分钟数据', 'min', 'Cu'),
    # ('title', 'symbol', 'table_name', 'source', 'duration_unit', 'varieties')
    para_dict = {
        "basic_1_2": ["037", dict(zip(('title', 'symbol', 'table_name', 'source', 'duration_unit', 'varieties'),
                                      ('一月和二月的差值', '', '', '预计算-分钟数据', 'min', '')
                                      ))],

        "basic_1_3": ["038", dict(zip(('title', 'symbol', 'table_name', 'source', 'duration_unit', 'varieties'),
                                      ('一月和三月的差值', '', 'min_preprocess', '预计算-分钟数据', 'min', '')
                                      ))],

        "basic_2_3": ["039", dict(zip(('title', 'symbol', 'table_name', 'source', 'duration_unit', 'varieties'),
                                      ('二月和三月的差值', '', '', '预计算-分钟数据', 'min', '')
                                      ))],
        # #################################
        "basic_1_2_rate": ["044", dict(zip(('title', 'symbol', 'table_name', 'source', 'duration_unit', 'varieties'),
                                      ('(连一-连二)/连一的比值', '', '', '预计算-分钟数据', 'min', '')
                                      ))],

        "basic_1_3_rate": ["045", dict(zip(('title', 'symbol', 'table_name', 'source', 'duration_unit', 'varieties'),
                                      ('(连一-连三)/连一的比值', '', 'min_preprocess', '预计算-分钟数据', 'min', '')
                                      ))],

        "basic_2_3_rate": ["046", dict(zip(('title', 'symbol', 'table_name', 'source', 'duration_unit', 'varieties'),
                                      ('(连二 - 连三)/连二的比值', '', '', '预计算-分钟数据', 'min', '')
                                      ))],
    }
    # db = Session()
    for para in para_dict:
        para_code, vals = para_dict[para]

        for varieties in MIN_VARIEYIES_DICT:
            new_vals = vals.copy()
            symbol = MIN_VARIEYIES_DICT[varieties]+para_code
            new_vals['symbol'] = symbol
            new_vals['table_name'] = 'min_preprocess'
            new_vals['varieties'] = varieties
            new_vals['source'] = '预计算-分钟数据'
            print('=======%s=======' % new_vals)
            update_or_create_symbol(symbol, new_vals)

        for varieties in DAY_VARIEYIES_DICT:
            new_vals = vals.copy()
            symbol = DAY_VARIEYIES_DICT[varieties]+para_code
            new_vals['symbol'] = symbol
            new_vals['table_name'] = 'day_preprocess'
            new_vals['varieties'] = varieties
            new_vals['source'] = '预计算-日数据'
            new_vals['duration_unit'] = 'day'
            update_or_create_symbol(symbol, new_vals)
            print('=======%s=======' % new_vals)
    # db.commit()
    print('**==done===***')


def update_symbol(min_para_dict, day_para_dict, var_lst):
    from utils.enums import PRE_SYMBOL, MIN_VARIEYIES_DICT, DAY_VARIEYIES_DICT
    for varieties in var_lst:
        for para in min_para_dict:
            """分钟数据"""
            para_code, vals = min_para_dict[para]

            new_vals = vals.copy()
            symbol = MIN_VARIEYIES_DICT[varieties] + para_code
            new_vals['symbol'] = symbol
            # new_vals['table_name'] = 'min_preprocess'
            new_vals['varieties'] = varieties
            print('=======%s=======' % new_vals)
            update_or_create_symbol(symbol, new_vals)

        for day_para in day_para_dict:
            day_para_code, day_vals = day_para_dict[day_para]
            day_new_vals = day_vals.copy()
            day_symbol = DAY_VARIEYIES_DICT[varieties] + day_para_code
            day_new_vals['symbol'] = day_symbol
            day_new_vals['varieties'] = varieties
            print('=======%s=======' % day_new_vals)
            update_or_create_symbol(day_symbol, day_new_vals)



# ==================================
# 2017-08-18日修改symbol,增加:
    # 'cross_star': '040',
    # 'hlun_price_diff': '041',
    # 'position_chain': '042',
    # 'stock_ratio': '043',

min_para_dict_16_08_18 = {
    "cross_star": ["040", dict(zip(('title', 'symbol', 'table_name', 'source', 'duration_unit', 'varieties'),
                                   ('十字星比值', '', 'preprocess_min_cross_star', '预计算-分钟数据', 'min', '')
                                   ))],

    "hlun_price_diff": ["041", dict(zip(('title', 'symbol', 'table_name', 'source', 'duration_unit', 'varieties'),
                                        ('沪伦差价', '', 'preprocess_day_hlun_deff', '预计算-分钟数据', 'min', '')
                                        ))],
}

day_para_dict_16_08_18 = {
    "cross_star": ["040", dict(zip(('title', 'symbol', 'table_name', 'source', 'duration_unit', 'varieties'),
                                   ('十字星比值', '', 'preprocess_day_cross_star', '预计算-日数据', 'day', '')
                                   ))],

    "hlun_price_diff": ["041", dict(zip(('title', 'symbol', 'table_name', 'source', 'duration_unit', 'varieties'),
                                        ('沪伦差价', '', 'preprocess_day_hlun_deff', '预计算-日数据', 'day', '')
                                        ))],

    "position_chain": ["042", dict(zip(('title', 'symbol', 'table_name', 'source', 'duration_unit', 'varieties'),
                                        ('持仓环比', '', 'preprocess_day_position_chain', '预计算-日数据', 'day', '')
                                        ))],

    "stock_ratio": ["043", dict(zip(('title', 'symbol', 'table_name', 'source', 'duration_unit', 'varieties'),
                                        ('库存环比', '', 'preprocess_day_stock_ratio', '预计算-日数据', 'day', '')
                                        ))],

}

# ########################2017-8-22

min_para_dict_17_08_22 = {
    "smm_spot_price_diff": ["047", dict(zip(('title', 'symbol', 'table_name', 'source', 'duration_unit', 'varieties'),
                                   ('有色网今天现货价格与上周的当天的差值', '', 'preprocess_min_smm_price_deff', '预计算-分钟数据', 'min', '')
                                   ))],

    "shmet_spot_price_diff": ["048", dict(zip(('title', 'symbol', 'table_name', 'source', 'duration_unit', 'varieties'),
                                        ('上海金属网今天现货价格与上周的当天的差值', '', 'preprocess_min_shmet_price_deff', '预计算-分钟数据', 'min', '')
                                        ))],
}

day_para_dict_17_08_22 = {
    "smm_spot_price_diff": ["047", dict(zip(('title', 'symbol', 'table_name', 'source', 'duration_unit', 'varieties'),
                                   ('有色网今天现货价格与上周的当天的差值', '', 'preprocess_day_smm_price_deff', '预计算-日数据', 'day', '')
                                   ))],

    "shmet_spot_price_diff": ["048", dict(zip(('title', 'symbol', 'table_name', 'source', 'duration_unit', 'varieties'),
                                        ('上海金属网今天现货价格与上周的当天的差值', '', 'preprocess_day_shmet_price_deff', '预计算-日数据', 'day', '')
                                        ))],

    "warehouse_receipts": ["049", dict(zip(('title', 'symbol', 'table_name', 'source', 'duration_unit', 'varieties'),
                                              ('仓单环比', '', 'preprocess_day_warehouse_receipts', '预计算-日数据',
                                               'day', '')
                                              ))],

}

#++========================2017-08-29

day_para_dict_17_08_29 = {
    "position_deff": ["050", dict(zip(('title', 'symbol', 'table_name', 'source', 'duration_unit', 'varieties'),
                                   ('今天的持仓减上个交易日持仓', '', 'preprocess_day_position_deff', '预计算-日数据', 'day', '')
                                   ))],
}

min_para_dict_17_08_29 = {
    "position_deff": ["050", dict(zip(('title', 'symbol', 'table_name', 'source', 'duration_unit', 'varieties'),
                                   ('今天的持仓减上个交易日持仓', '', 'preprocess_min_position_deff', '预计算-分钟数据', 'min', '')
                                   ))],

}

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#     =======================2017-08-31
day_para_dict_17_08_31 = {

    "smm_spot_month_deff": ["051", dict(zip(('title', 'symbol', 'table_name', 'source', 'duration_unit', 'varieties'),
                                   ('有色网现货价格月差', '', 'preprocess_day_smm_spot_month_deff', '预计算-日数据', 'day', '')
                                   ))],
    "smm_spot_year_deff": ["052", dict(zip(('title', 'symbol', 'table_name', 'source', 'duration_unit', 'varieties'),
                                   ('有色网现货价格年差', '', 'preprocess_day_smm_spot_year_deff', '预计算-日数据', 'day', '')
                                   ))],
    "shmet_spot_month_deff": ["053", dict(zip(('title', 'symbol', 'table_name', 'source', 'duration_unit', 'varieties'),
                                   ('上海金属网现货价格月差', '', 'preprocess_day_shmet_spot_month_deff', '预计算-日数据', 'day', '')
                                   ))],
    "shmet_spot_year_deff": ["054", dict(zip(('title', 'symbol', 'table_name', 'source', 'duration_unit', 'varieties'),
                                   ('上海金属网现货价格年差', '', 'preprocess_day_shmet_spot_year_deff', '预计算-日数据', 'day', '')
                                   ))],
    "delivery_month_position_deff": ["055", dict(zip(('title', 'symbol', 'table_name', 'source', 'duration_unit', 'varieties'),
                                   ('持仓月差', '', 'preprocess_day_delivery_month_position_deff', '预计算-日数据', 'day', '')
                                   ))],
    "month_warehouse_deff": ["056", dict(zip(('title', 'symbol', 'table_name', 'source', 'duration_unit', 'varieties'),
                                   ('仓单月差', '', 'preprocess_day_month_warehouse_deff', '预计算-日数据', 'day', '')
                                   ))],
}

# +++++++++++++++++++++++++++++++++++++++++++++++++++++
# =====================================2017-09-04
day_para_dict_17_09_04 = {

    "delivery_month_bwd_deff": ["057", dict(zip(('title', 'symbol', 'table_name', 'source', 'duration_unit', 'varieties'),
                                   ('升贴水持仓月差', '', 'preprocess_day_delivery_month_bwd_deff', '预计算-日数据', 'day', '')
                                   ))],

}

day_para_dict_17_09_04_02 = {
    'total_output': ["058", dict(zip(('title', 'symbol', 'table_name', 'source', 'duration_unit', 'varieties'),
                                   ('总产量', '', 'data_artificial', '预计算-日数据', 'day', '')
                                   ))],
}


def total_update():
    # update_base_symbol()
    update_symbol(min_para_dict_16_08_18, day_para_dict_16_08_18, ['cu', 'zn'])
    update_symbol(min_para_dict_17_08_22, day_para_dict_17_08_22, ['cu', 'zn'])
    update_symbol(min_para_dict_17_08_29, day_para_dict_17_08_29, ['cu', 'zn'])
    update_symbol({}, day_para_dict_17_08_31, ['cu', 'zn'])
    update_symbol({}, day_para_dict_17_09_04, ['cu', 'zn'])
    update_symbol({}, day_para_dict_17_09_04_02, ['cu', 'zn', 'al', 'pb'])




if __name__ == '__main__':

    total_update()