main_con = REF(e, MAIN_CONTRACT)
threshold = REF(e, DOJI_STAR_THRESHOLD)
e.result = REF(e, DOJI_STAR_RATE)

message = "%s开盘价收盘价差值比率为%s, 十字星预警比率为%s" % (main_con[0], e.result[0], threshold[0])


if ABS(e.result[0]) <= threshold[0]:
    ALERT(e, message)
    CHART(e, DOJI_STAR_RATE)

logger.info(message)
