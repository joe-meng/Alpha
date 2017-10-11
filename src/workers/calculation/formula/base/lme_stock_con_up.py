data = REF(e, STOCK_LME, 3)
alert, e.result = ISCONTUP(data, 0)

e_variety = e.ch_variety
message = "%sLME库存连续上升3周" % e_variety

ALERT(e, message, alert)
CHART(e, STOCK_LME)

logger.info("%sLME库存最近四周库存数据为:%s, 三周上升比率为%s, 预警指数为3周连续上升",
            e_variety, data, e.result)
