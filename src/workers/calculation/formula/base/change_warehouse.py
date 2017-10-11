con1_opi = REF(e, OPI, contract=CON_CONTRACT_1)[0]
con1_vol = REF(e, VOL, contract=CON_CONTRACT_1)[0]
con1_con_name = REF(e, CON_CONTRACT_1)[0]

e_variety = e.ch_variety
for CON_CONTRACT in [CON_CONTRACT_2, CON_CONTRACT_3, CON_CONTRACT_4,
          CON_CONTRACT_5, CON_CONTRACT_6, CON_CONTRACT_7, CON_CONTRACT_8,
          CON_CONTRACT_9, CON_CONTRACT_10, CON_CONTRACT_11, CON_CONTRACT_12]:
    con_name = REF(e, CON_CONTRACT)[0]
    con_opi = REF(e, OPI, contract=CON_CONTRACT)[0]
    con_vol = REF(e, VOL, contract=CON_CONTRACT)[0]
    if con_opi < con1_opi and con_vol > con1_vol:
        message = "品目%s发生由合约%s移仓到远期合约%s的现象" % (e_variety, con1_con_name, con_name)
        ALERT(e, message)
        CHART(e, VOL, CON_CONTRACT)
        e.result=[con_vol-con1_vol]
        logger.info(message)
        break
    logger.info("品目%s主力合约无移仓合约%s情况发生", con_name)