con1 = REF(e, CON_CONTRACT_1)
warrant_list = REF(e, WARRANT, 30, start_date=begin_month())
month_rate = REF(e, WARRANT_MONTH_RATE, 30, start_date=begin_month())

gt_days = COUNTGT(month_rate)
e_variety = e.ch_variety

alert = gt_days >= 3
logger.info("当月%s数据为:%s,环比为:%s, 连续上涨天数%s,预警最小上涨天数:3天",
              e_variety, warrant_list, month_rate, gt_days)

e.result = REF(e, WARRANT_MONTH_DIFF, gt_days)
message = "沪%s交割月%s合约持仓：仓单环比连续上涨%s天" % (e_variety, con1, gt_days)

ALERT(e, message, alert)
CHART(e, WARRANT_MONTH_RATE)

logger.info("环比上升天数:%s, 上升率:%s, 上升数量:%s", gt_days, month_rate[-gt_days:],
            gt_days)