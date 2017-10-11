data = REF(e, PD, 3)
alert, e.result = ISCONTUP(data, 0)

e_variety = e.ch_variety
message = "%s上海金属网升贴水连续上涨3天" % e_variety

ALERT(e, message, alert)
CHART(e, PD)

logger.info("%s上海金属网升贴水最近四天数据为:%s, 三天上涨比率为%s, 预警指数为3天连续上涨",
            e_variety, data, e.result)