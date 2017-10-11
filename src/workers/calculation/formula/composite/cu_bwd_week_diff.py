from lib.mathlib import *
from lib.utils.date_utils import *

e_variety = e.ch_variety
message = "%s升贴水与上月同期对比差距较大" % e_variety

e.result = REF(e, PD_MONTH_DIFF)

diff = e.result[0]

ni_alert = e.content_variety == Ni and diff >= 300
other_alert = e.content_variety != Ni and diff >= 100

alert =  ni_alert or other_alert

CHART(e, PD)
ALERT(e, message, alert)

logger.info("%s升贴水与上月同期对比差距:%s, 预警为镍:300, 其它100", e_variety, diff)