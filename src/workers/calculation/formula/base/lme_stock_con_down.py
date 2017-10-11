data = REF(e, STOCK_LME, 3)
alert, e.result = ISCONTDOWN(data, 0)

e_variety = e.ch_variety
message = "%sLME库存已连续下降3周" % e_variety

ALERT(e, message, alert)
CHART(e, STOCK_LME)

logger.info("%sLME库存最近四天库存数据为:%s, 三天下降比率为%s,  预警指数为3周连续下跌",
            e_variety, data, e.result)