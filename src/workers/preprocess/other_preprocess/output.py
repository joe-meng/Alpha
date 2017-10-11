
if __name__ == '__main__':
    import sys
    sys.path.append("../../..")

import logs
import logging
from datetime import datetime, timedelta
from sqlalchemy import desc

from models.models import DataWind, Session, PreprocessDayDataArtificial
from utils.enums import OUTPUT_SYMBOL_MAP, IMPORT_AMOUNT_MAP, DAY_VARIEYIES_DICT
from common.common import save_symbol_data, get_symbol
# init_check = os.environ.get('init_check', None)
_logger = logging.getLogger(__name__)


def cal_total_output(varieties, date, output=0.0, import_amount=0.0):
    """计算总产量"""
    logging.info('计算(总产量), 品类: %s, 时间: %s' % (varieties, date))
    res = {}
    if output and import_amount:
        total_output = float(output) +float(import_amount)
        res = {'vals': total_output}
    return res


def init_output_import(db, varieties, date):
    """初始化产量和进口量"""
    res = {}
    output_symbol = OUTPUT_SYMBOL_MAP.get(varieties.lower())
    import_symbol = IMPORT_AMOUNT_MAP.get(varieties.lower())
    if output_symbol and import_symbol:
        # out_rate_objs = db.query(Symbol)
        out_rate_objs = db.execute("select benchmark from symbol where symbol = '%s'" % output_symbol).fetchone()
        out_rate = out_rate_objs and out_rate_objs[0] or 1
        out_objs = db.query(DataWind).filter(DataWind.symbol == output_symbol,
                                                  DataWind.date == date). \
            order_by(desc(DataWind.date)).all()
        if out_objs:
            output = float(out_objs[0].amount) * float(out_rate)
            res['output'] = output

        import_objs = db.query(DataWind).filter(DataWind.symbol == import_symbol,
                                                     DataWind.date == date). \
            order_by(desc(DataWind.date)).all()

        import_rate_objs = db.execute(
            "select benchmark from symbol where symbol = '%s'" % import_symbol).fetchone()
        import_rate = import_rate_objs and import_rate_objs[0] or 1
        if import_objs:
            import_amount = float(import_objs[0].amount) * float(import_rate)
            res['import_amount'] = import_amount
    return res


def update_output(date):
    """计算总产量"""
    db = Session()
    obj = PreprocessDayDataArtificial
    # for varieties in DAY_VARIEYIES_DICT.keys():
    for varieties in ['cu', 'al', 'pb', 'zn']:
        symbol = get_symbol(varieties, key='total_output')
        init_vals = init_output_import(db, varieties, date)
        res = cal_total_output(varieties, date, **init_vals)
        if res:
            logging.debug('保存(总产量), 品类: %s, 时间: %s, 值: %s '% (varieties, date, res))
            save_symbol_data(db, res, date, symbol=symbol, obj=obj)
            db.commit()
    db.close()


def update_today_output():
    today = str(datetime.now())[:10]
    update_output(today)


if __name__ == '__main__':
    now = datetime.now()
    start_date = datetime.strptime('2010-01-01', '%Y-%m-%d')
    for i in range((now-start_date).days):
        date = str(start_date + timedelta(days=i))[:10]
        update_output(date)

