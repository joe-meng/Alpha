
if __name__ == '__main__':
    import sys
    sys.path.append("../../..")

from datetime import datetime, timedelta
import when

from ctp_preprocess.day_handler import cal_day_info
from other_preprocess.output import update_output
from utils.enums import DAY_VARIEYIES_DICT
from models.models import Session



def month_re_cal():
    """每天重复计算一个月内的数据"""
    db = Session()
    var_obj = db.execute('select code, exchange from varieties ')
    var_vals = var_obj.fetchall()
    exchange_map = dict(var_vals)
    db.close()
    now = datetime.now()
    last_month = when.past(months=1)
    for i in range((now-last_month).days + 1):
        date = str(last_month + timedelta(days=i))[:10]
        # ctp日数据
        for varieties in DAY_VARIEYIES_DICT.keys():
            exchange = exchange_map.get(varieties.lower())
            if not exchange:
                exchange = exchange_map.get(varieties.upper())
            cal_day_info(varieties, date, exchange)
        # 总资产
        update_output(date)

if __name__ == '__main__':
    month_re_cal()