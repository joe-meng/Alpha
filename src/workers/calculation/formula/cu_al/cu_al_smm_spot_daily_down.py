data = REF(e, SPOT, 1)
alert, e.result = ISCONTDOWNABS(data, 100)

e_variety = e.ch_variety
e.introduction = "%sSMM现货平均价格下跌大于等于100元" % e_variety

ALERT(e, message, alert)
CHART(e, SPOT)

logger.info("%sSMM现货平均价格日间数据为:%s, 下降幅度%s , 预警幅度为%s",
            e_variety, data, e.result, 100)
