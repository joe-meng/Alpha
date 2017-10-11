from lib.mathlib import *

e_variety = e.ch_variety
message = "%s合约持仓量和交易量增大, 价格持续下降100元" % e_variety

opi_data = REF(e, OPI, 3)
vol_data = REF(e, VOL, 3)
settle_data = REF(e, SETTLE, 3)

opi_is_up, opi_up_data = ISCONTUP(opi_data, 0)
vol_is_up, vol_up_data = ISCONTUP(vol_data, 0)
settle_is_down, e.result = ISCONTDOWNABS(settle_data, 100)

if opi_is_up and vol_is_up and settle_is_down:
    ALERT(e, message)
    CHART(e, SETTLE)

logger.info("%s合约持仓量增量为:%s,预警值为连续增加, 交易量增量为%s , 预警值为连续增加"
            "结算价下降为%s, 预警幅度为连续下降大于等于100元",
            e_variety, opi_up_data, vol_up_data, e.result)