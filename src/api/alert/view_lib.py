
import datetime
# import time

# from workers.calculation.lib.vo import FormulaEnv, DBPreProcess
# from workers.calculation.lib import mathlib
from workers.calculation.lib.mathlib import *

# from .models import Alert
from django.db import connection
from share.data import ref_ship
from functools import wraps
from common.models import BackstageHTTPResponse

para_name_map = {}
# with connection.cursor() as cursor:
#     cursor.execute('select `price_code`, `desc` from ref_ship')
#     ref_ship_list = cursor.fetchall()
#     para_name_map = dict(ref_ship_list)




varieties_name_map = {
    'cu': '铜',
    'zn': '锌',
    'al': '铝',
    'pb': '铅',
    'ni': '镍',
    'pvc': 'pvc',
}


def get_cross_star(varieties, res_type='his', limit=3, offset=0):
    """获取十字星数据"""
    m_con_objs = MainContract.objects.filter(varieties=varieties).order_by('-settlement_date').all()
    vals_len = len(m_con_objs)
    res = []
    data = []
    lmt = limit + 1
    if vals_len >= limit:
        m_con_objs = m_con_objs[offset:lmt]
    else:
        m_con_objs = m_con_objs[offset:]
    for obj in m_con_objs:
        daykline_obj = DayKline.objects.filter(contract=obj.main_contract,
                                                date_time=obj.settlement_date).order_by('-date_time')[0]
        # daykline_obj = DayKline.objects.filter(contract=obj.main_contract).order_by('-date_time')[0]
        price_open = daykline_obj.price_open
        price_high = daykline_obj.price_high
        price_low = daykline_obj.price_low
        pric_close = daykline_obj.price_close
        price_date = str(daykline_obj.date_time)[:10]
        if res_type == 'his':
            data.append((price_open-pric_close) / price_open)
        elif res_type == 'chart':
            res.append([price_open, price_high, price_low, pric_close, price_date])

    if res_type == 'his':
        d1, d2, gd, rate = data_gap(data)
        return gd[1:], rate[1:], data
    else:
        return res[:-1]


def get_history_data(varieties, price, contract=None, limit=3, offset=0, start=None, end=None):
    """获取各个参数历史数据列表"""

    limit = limit + 1
    data = ref_ship(varieties, price, limit=limit, timestamp=True, start=start, offset=offset, end=end)

    number = []
    date_list = []
    for vals in data:
        if vals[1]:
            number.append(float(vals[1]))
        else:
            number.append(0.0)
        date_list.append(vals[0])
    return number, date_list


def get_description(descrip):
    res = []
    for line in descrip:
        res.append(line[0])
    return res

def get_res(des, vals):
    res = []
    for i in vals:
        res.append(dict(zip(des, i)))
    return res

def get_quotes(varieties, date):
    """获取行情数据"""
    # price = ''
    res = {}
    price = 'SETTLE'
    day = datetime.datetime.strptime(date, '%Y-%m-%d')
    data = ref_ship(varieties, price, limit=2, start=day, end=day)
    if data:
        data = ref_ship(varieties, price, limit=2, end=day)
        d1, d2, gd, rate = data_gap(data)
        res['price'] = data[0]
        if gd[0] < 0:
            res['trend'] = 'up'
        elif gd[0] > 0:
            res['trend'] = 'down'
        else:
            res['trend'] = 'c'
        res['change_price'] = abs(round(gd[0], 4))
        res['change_percent'] = abs(round(rate[0], 4))
        res['yes_price'] = data[1]

    return res


def user_check(func):
    @wraps(func)
    def wrapper(self, request):
        if not request.user.id:
            return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_NO_PERMISSION).to_response()
        else:
            return func(self, request)



    return wrapper



if __name__ == '__main__':
    vals = get_history_data('cu', 'WARRANT')
    # vals = get_history_data('cu', 'MAIN_CONTRACT')
    # print(vals)