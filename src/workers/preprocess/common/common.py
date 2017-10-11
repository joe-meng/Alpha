
from utils.enums import DAY_VARIEYIES_DICT, PRE_SYMBOL

def save_symbol_data(db, res, date, symbol=None, obj=None):
    """更新或插入symbol"""
    if symbol:
        if obj:
            pre_objs = db.query(obj).filter(obj.date == date, obj.symbol == symbol).all()
            if pre_objs:
                pre_obj = pre_objs[0]
                pre_obj.amount = res['vals']
            else:
                new_pre_obj = obj(date=date, symbol=symbol, amount=res['vals'])
                db.add(new_pre_obj)


def get_symbol(varieties, key):
    """获取symbol"""
    if varieties.lower() not in DAY_VARIEYIES_DICT or key not in PRE_SYMBOL:
        return None
    return DAY_VARIEYIES_DICT[varieties.lower()] + PRE_SYMBOL[key]