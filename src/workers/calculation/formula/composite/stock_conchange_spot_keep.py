from lib.mathlib import *

e_variety = e.ch_variety
message = "%s库存连续改变3周(2%%)而价格未动(一天内100元,一周500元)" % e_variety

stock_data = REF(e, STOCK, 3)
is_change, change_result = ISCONTCHANGE(stock_data, 0.02)


spot_week_data = REF(e, SPOT, 5, INDEX_CONTRACT)
week_change_result = spot_week_data[-1]-spot_week_data[-5]
week_change = ABS(week_change_result) <= 500

spot_day_data = REF(e, SPOT, 3, INDEX_CONTRACT)
day_change, day_change_result = ISCONTCHANGEABS(spot_day_data,100, isge=False)

if is_change and (week_change or day_change):
    ALERT(e, message)
    CHART(e, STOCK)

logger.info("%s库存3周改变量为:%s,预警值为大于等于2%%, 价格一天内改变量为%s元 , "
            "预警幅度为小于等于100元, 价格一周内改变是为%s元, 预警值为小于等于500元",
            e_variety, change_result, day_change_result, week_change_result)



