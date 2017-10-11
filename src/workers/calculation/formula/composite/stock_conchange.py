from lib.mathlib import *

e_variety = e.ch_variety
message = "%s总库存重大变动:连续3周改变2%%" % e_variety

e.result = REF(e, STOCK, 3)
stock_data = e.result
change, change_data = ISCONTCHANGE(stock_data, 0.02)

ALERT(e, message, change)
CHART(e, STOCK)

logger.info("%s总库存3周改变量为:%s,预警值为连续改变2%%",
            e_variety, change_data)