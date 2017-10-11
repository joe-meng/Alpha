from lib.mathlib import *

e_variety = e.ch_variety
message = "%s现货价格价格未动(日间100元,一周500元), 期货价格持续下跌3天" % e_variety

spot_week_data = REF(e, WEEK_SPOT_DIFF)[0]
week_change = ABS(spot_week_data) <= 500

spot_day_data = REF(e, SPOT, 3)
day_change, e.result = ISCONTCHANGEABS(spot_day_data,100, isge=False)

settle_data = REF(e, SETTLE, 3)

settle_change, change_data = ISCONTDOWNABS(settle_data,0)

if (week_change or day_change) and settle_change:
    ALERT(e, message)
    CHART(e, SETTLE)

logger.info("%s期货价格3天下跌幅度为:%s,预警值为连续下跌, 现货价格日间改变量为%s元 , "
            "预警幅度为小于等于100元, 现货价格一周内改变是为%s元, 预警值为小于等于500元",
            e_variety, change_data, e.result, spot_week_data)