main_con = REF(e, MAIN_CONTRACT)
e.result = REF(e, SHFE_LME_DIFF)
e_variety = e.ch_variety

message = "沪%s主力合约%s结算价比LME价格（剔除影响）超-300元" % (e_variety, main_con[0])

if e.result and e.result[0] >= -300:
    ALERT(e, message)
    CHART(e, SHFE_LME_DIFF)

logger.info("%s主力合约为%s, 差值为%s, 预警值:%s",
            e_variety, main_con[0], e.result, -300)
