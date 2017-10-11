
# import logs
# import logging
# logger = logging.getLogger('shell')
import sys
from datetime import datetime, timedelta
sys.path.append("../..")
import multiprocessing
# import getopt
#
# opts, args = getopt.getopt(sys.argv[1:], "hi:o:")
# input_file=""
# output_file=""
# for op, value in opts:
#     if op == "-i":
#         input_file = value
#     elif op == "-o":
#         output_file = value
#     elif op == "-h":
#         usage()
#         sys.exit()

args_lst = sys.argv[1:]
arg = args_lst and args_lst[0] or 'all'




exchange_map = {
        'IC': 'CFFEX',
        'IF': 'CFFEX',
        'IH': 'CFFEX',
        'T': 'CFFEX',
        'TF': 'CFFEX',
        'CF': 'CZCE',
        'FG': 'CZCE',
        'JR': 'CZCE',
        'LR': 'CZCE',
        'MA': 'CZCE',
        'OI': 'CZCE',
        'PM': 'CZCE',
        'RI': 'CZCE',
        'RM': 'CZCE',
        'RS': 'CZCE',
        'SF': 'CZCE',
        'SM': 'CZCE',
        'SR': 'CZCE',
        'TA': 'CZCE',
        'WH': 'CZCE',
        'ZC': 'CZCE',
        'a': 'DCE',
        'b': 'DCE',
        'bb': 'DCE',
        'c': 'DCE',
        'cs': 'DCE',
        'fb': 'DCE',
        'i': 'DCE',
        'j': 'DCE',
        'jd': 'DCE',
        'jm': 'DCE',
        'l': 'DCE',
        'm': 'DCE',
        'p': 'DCE',
        'pp': 'DCE',
        'v': 'DCE',
        'y': 'DCE',
        'ag': 'SHFE',
        'al': 'SHFE',
        'au': 'SHFE',
        'bu': 'SHFE',
        'cu': 'SHFE',
        'fu': 'SHFE',
        'hc': 'SHFE',
        'ni': 'SHFE',
        'pb': 'SHFE',
        'rb': 'SHFE',
        'ru': 'SHFE',
        'sn': 'SHFE',
        'wr': 'SHFE',
        'zn': 'SHFE',
}


# def caculate_history_vals(date):
def caculate_history_vals(q, i, env):
    import os
    os.environ['ALPHA_ENV'] = env
    os.environ['init_check'] = '1'
    from utils.enums import DAY_VARIEYIES_DICT
    from ctp_preprocess.day_handler import cal_day_info

    end_day = datetime.today()
    # allow_v = ['cu', 'al', 'zn', 'pb', 'ni']
    # allow_v = ['pb']
    allow_v = DAY_VARIEYIES_DICT.keys()

    while True:
        if q.empty():
            break
        date = q.get()
        print('======date==%s=====process: %s====env : %s='%(date, i, env))
        if date > end_day:
            return
        for v in allow_v:
            varieties = v.lower()
            exchange = exchange_map.get(varieties)
            if not exchange:
                exchange = exchange_map.get(varieties.upper())
            if not exchange:
                continue
            cal_day_info(varieties, str(date)[:10], exchange)
            # print('*******************')
        # db = Session()
        # for i in range(7):
        #     cal_contract_vals(db, varieties, i, str(date)[:10], exchange)


def start_process(number, q, env):
    process_list = []
    for i in range(number):
        p = multiprocessing.Process(target=caculate_history_vals, args=(q, i, env))
        p.daemon = True
        p.start()
        process_list.append(p)
    return process_list


def muti_process_update():
    start_date = datetime.strptime('2017-09-10', '%Y-%m-%d')
    now = datetime.today()
    q = multiprocessing.Queue()
    online_q = multiprocessing.Queue()
    for i in range((now-start_date).days+1):
        date = start_date + timedelta(days=i)
        q.put(date)
        online_q.put(date)
    if arg == 'test':
        lst = start_process(8, q, 'test')
    elif arg == 'online':
        lst = start_process(8, q, 'online')
    else:
        lst2 = start_process(8, q, 'online')
        lst1 = start_process(8, q, 'test')
        lst = lst1 + lst2
    for pro in lst:
        if pro.is_alive():
            pro.join()
    print('=======end=======')


def get_serial_price(date, varieties, exchange, env):
    import os
    os.environ['ALPHA_ENV'] = env
    from ctp_preprocess.day_handler import _logger, Session, DayInitPreProcess, COMMON_INIT_LIST, DAY_INIT_PATA_MAP

    db = Session()
    init_obj = DayInitPreProcess(db, varieties, date, exchange)
    init_list = COMMON_INIT_LIST + DAY_INIT_PATA_MAP.get(varieties, [])
    for para in init_list:
        init_res = getattr(init_obj, para)()
        if init_res == "exit":
            # db.roll_back()
            db.close()
            return
    _logger.info("""
                    获取价格:
                    日期: %s,
                    品类: %s,
                    连一价格:%s,
                    连二价格:%s,
                    连三价格:%s,
                    连六价格:%s"""
                 % (date, varieties, init_obj.pre_obj.contract1_price,
                    init_obj.pre_obj.contract2_price, init_obj.pre_obj.contract3_price,
                    init_obj.pre_obj.contract6_price))

    db.commit()
    db.close()

def get_output_price(date, varieties, exchange, env):
    import os
    os.environ['ALPHA_ENV'] = env
    from ctp_preprocess.day_handler import _logger, Session, DayInitPreProcess, COMMON_INIT_LIST, DAY_INIT_PATA_MAP

    db = Session()
    init_obj = DayInitPreProcess(db, varieties, date, exchange)
    init_list = COMMON_INIT_LIST + DAY_INIT_PATA_MAP.get(varieties, [])
    for para in init_list:
        init_res = getattr(init_obj, para)()
        if init_res == "exit":
            # db.roll_back()
            db.close()
            return
    _logger.info("""
                    获取价格:
                    日期: %s,
                    品类: %s,
                    国内产量:%s,
                    进口产量:%s,
                    比值:%s,"""
                 % (date, varieties, init_obj.pre_obj.output,
                    init_obj.pre_obj.import_amount, init_obj.pre_obj.contract3_price
                    ))

    db.commit()
    db.close()


def run_single_by_one(i, q, varieties, exchange, env, res_name):
    import os
    os.environ['ALPHA_ENV'] = env
    from ctp_preprocess.day_handler import _logger, Session, DayInitPreProcess, COMMON_INIT_LIST, DAY_INIT_PATA_MAP, \
        DayResPreProcess

    while True:
        if q.empty():
            break
        date = str(q.get())
        # date = q
        print('======date==%s=====process: %s====env : %s=' % (date, i, env))
        db = Session()
        init_obj = DayInitPreProcess(db, varieties, date[:10], exchange)
        init_list = COMMON_INIT_LIST + DAY_INIT_PATA_MAP.get(varieties, [])
        for para in init_list:
            init_res = getattr(init_obj, para)()
            if init_res == "exit":
                # db.roll_back()
                db.close()
                break
        res_obj = DayResPreProcess(db, init_obj.pre_obj)
        # deal_list = ['get_total_output']
        deal_list = [res_name]
        for deal in deal_list:
            getattr(res_obj, deal)()
        res = res_obj.res
        res_obj.save_symbol_data(res, date)
        _logger.info('完成计算 res: %s, 日期: %s, 品类: %s' % (res_obj.res, date, res_obj.varieties))
        db.commit()
        db.close()

def single_start_process(number, q, varieties, exchange, env, res_name):
    process_list = []
    for i in range(number):
        p = multiprocessing.Process(target=run_single_by_one, args=(i, q, varieties, exchange, env, res_name))
        p.daemon = True
        p.start()
        process_list.append(p)
    return process_list

def run_single(varieties, exchange, res_name):
    start_date = datetime.strptime('2017-04-07', '%Y-%m-%d')
    now = datetime.today()
    q = multiprocessing.Queue()
    online_q = multiprocessing.Queue()
    for i in range((now - start_date).days + 1):
        date = start_date + timedelta(days=i)
        q.put(date)
        online_q.put(date)
    if arg == 'test':
        lst = single_start_process(8, q, varieties, exchange, 'test', res_name)
    elif arg == 'online':
        lst = single_start_process(8, online_q, varieties, exchange, 'online', res_name )
    else:
        lst2 = single_start_process(8, online_q, varieties, exchange, 'online', res_name )
        lst1 = single_start_process(8, q, varieties, exchange, 'test', res_name)
        lst = lst1 + lst2
    for pro in lst:
        if pro.is_alive():
            pro.join()


if __name__ == '__main__':
    arg = 'online'
    muti_process_update()
    # get_serial_price('2017-08-23', 'i', 'dce', 'test')
    # get_output_price('2016-12-31', 'cu', 'shfe', 'test')
    # run_single('cu', 'shfe', 'get_total_output')
    # run_single('al', 'shfe', 'get_total_output')
    # run_single('pb', 'shfe', 'get_total_output')
    # run_single('zn', 'shfe', 'get_total_output')
    # run_single('cu', 'shfe', 'cal_profit')
