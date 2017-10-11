from lib.mathlib import *

e_variety = e.ch_variety
message = "%s现货价格上涨(一天内100元,一周500元), 期货价格持续上升3天" % e_variety

spot_week_data = REF(e, WEEK_SPOT_DIFF)[0]
week_change = ABS(spot_week_data) >= 500

spot_day_data = REF(e, SPOT, 3)
day_change, day_change_result = ISCONTCHANGEABS(spot_day_data,100)

settle_data = REF(e, SETTLE, 3)

settle_change, e.result = ISCONTUPABS(settle_data,0)

if (week_change or day_change) and settle_change:
    ALERT(e, message)
    CHART(e, SPOT)

logger.info("%s期货价格3天上涨幅度为:%s,预警值为连续上涨, 现货价格一天内改变量为%s元 , "
            "预警幅度为大于等于100元, 现货价格一周内改变是为%s元, 预警值为大于等于500元",
            e_variety, e.result, day_change_result, spot_week_data)