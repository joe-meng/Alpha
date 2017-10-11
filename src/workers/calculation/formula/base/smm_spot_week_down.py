data = REF(e, WEEK_SPOT_DIFF, 1)
alert, e.result = ISCONTDOWNABS(data, 500)

e_variety = e.ch_variety
message = "%s上海金属网现货平均价格周比下跌大于等于500元" % e_variety

ALERT(e, message, alert)
CHART(e, WEEK_SPOT_DIFF)

logger.info("%s上海金属网现货平均价格周比数据为:%s, 周比下跌幅度%s元 , 预警幅度为%s元",
            e_variety, data, e.result, 500)