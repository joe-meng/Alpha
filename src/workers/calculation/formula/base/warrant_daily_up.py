data = REF(e, WARRANT, 1)
alert, e.result = ISCONTUP(data, 0.02)

e_variety = e.ch_variety
message = "上期所%s仓单对比昨天上涨2%%" % e_variety

ALERT(e, message, alert)
CHART(e, WARRANT)

logger.info("上期所%s仓单二天数据为:%s,对比上涨比率为:%s, 预警为上涨2%%",
            e_variety, data, e.result)
