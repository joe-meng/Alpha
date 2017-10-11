data = REF(e, PD, 3)
alert, e.result = ISCONTDOWN(data, 0)

e_variety = e.ch_variety
message = "%sSMM升贴水连续下跌3天" % e_variety

ALERT(e, message, alert)
CHART(e, PD)

logger.info("%sSMM升贴水最近四天数据为:%s, 三天下跌比率为%s, 预警指数为3天连续下跌",
            e_variety, data, e.result)
