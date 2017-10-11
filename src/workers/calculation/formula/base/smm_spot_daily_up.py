data = REF(e, SPOT, 1)
alert, e.result = ISCONTUPABS(data, 100)

e_variety = e.ch_variety
message = "%s上海金属网现货平均价格上涨大于等于100元" % e_variety

ALERT(e, message, alert)
CHART(e, SPOT)

logger.info("%s上海金属网现货平均价格日间数据为:%s, 上涨幅度%s , 预警幅度为%s",
            e_variety, data, e.result, 100)