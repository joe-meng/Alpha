alert_rate = 0.005
e_variety = e.ch_variety

e.result = REF(e, CON1_CON2_DIFF_RATE)
message = "沪%s连1-连2变化比率为%s, 预警指数%s" % (e_variety, round(e.result[0], 4), alert_rate)

if abs(e.result[0]) >= alert_rate:
    ALERT(e, message)
    CHART(e, CON1_CON2_DIFF_RATE)
logger.info(message)
