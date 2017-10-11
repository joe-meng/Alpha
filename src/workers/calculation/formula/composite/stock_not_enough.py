from lib.mathlib import *
from lib.utils.date_utils import *

e_variety = e.ch_variety
message = "%s库存不足以维持剩余天数" % e_variety

year_sale = REF(e, YEAL_SALE, end_date=begin_year())[0]
e.result = REF(e, STOCK)
stock = e.result[0]
days = float(stock)/(float(year_sale)/365)

alert = days < 5

ALERT(e, message, alert)
CHART(e, STOCK)

logger.info("%s库存剩余量为:%s, 按去年平均消费量还可以维持%s天,预警天数:%s天",
            e_variety, stock, days, 5)