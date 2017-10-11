con1 = REF(e, CON_CONTRACT_1)

pre_con1 = CONTRACTN(e, con1[0], -1)
pre_con1_expire_dt = EXPIREDATE(e, pre_con1)[0]

# 获取当前交割月环比比率数据
rate_list = REF(e, OPI_MONTH_RATE, 30,
                 start_date=next_day(pre_con1_expire_dt))

gt_days = COUNTGT(rate_list)
e_variety = e.ch_variety

alert = gt_days >= 3
logger.info("当前环比上升天数为%s天,预警天数为大于等于3天", gt_days)

e.result = REF(e, OPI_MONTH_DIFF, gt_days)

message = "沪%s交割月%s合约持仓：总持仓环比连续上涨%s天" % (e_variety, con1[0], gt_days)

ALERT(e, message, alert)
CHART(e, OPI_MONTH_RATE)

logger.info("环比上升天数:%s, 上升率:%s, 上升数量:%s", gt_days, rate_list[-gt_days:],
            gt_days)
