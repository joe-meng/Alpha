data = REF(e, SPOT, 1)
alert, e.result = ISCONTUPABS(data, 100)

e_variety = e.ch_variety
e.introduction = "%sSMM现货平均价格上升大于等于100元" % e_variety

ALERT(e, message, alert)
CHART(e, SPOT)

logger.info("%sSMM现货平均价格日间数据为:%s, 上升幅度%s , 预警幅度为%s",
            e_variety, data, e.result, 100)
