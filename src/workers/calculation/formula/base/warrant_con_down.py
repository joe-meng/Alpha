data = REF(e, WARRANT, 3)
alert, e.result = ISCONTDOWN(data, 0)

e_variety = e.ch_variety
message = "上期所%s仓单已连续下降3天" % e_variety

ALERT(e, message, alert)
CHART(e, WARRANT)

logger.info("上期所%s仓单四天数据为:%s,三天连续下降比率为:%s, 预警为3天连续下降",
            e_variety, data, e.result)
