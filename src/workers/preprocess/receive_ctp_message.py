# -- coding: utf-8 --

import sys
sys.path.append("../..")


from share.mq import channel
# from calculation import start_cal
from ctp_preprocess.day_handler import cal_day
from ctp_preprocess.min_handler import cal_min

def get_info_from_ctp_queue():
    channel.exchange_declare(exchange='useonline.alpha.analysis',
                             exchange_type='topic')

    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue

    binding_key = "ctp"
    channel.queue_bind(exchange='useonline.alpha.analysis',
                       queue=queue_name,
                       routing_key=binding_key)

    # binding_key = "spider"
    # channel.queue_bind(exchange='useonline.alpha.analysis',
    #                    queue=queue_name,
    #                    routing_key=binding_key)

    # channel.basic_consume(start_cal,
    #                       queue=queue_name,
    #                       no_ack=True)
    channel.basic_consume(cal_min,
                          queue=queue_name,
                          no_ack=True)

    # ========================
    day_q = channel.queue_declare(exclusive=True)
    day_binding_key = "ctp_day"
    day_q_name = day_q.method.queue
    channel.queue_bind(exchange='useonline.alpha.analysis',
                       queue=day_q_name,
                       routing_key=day_binding_key)

    channel.basic_consume(cal_day,
                          queue=day_q_name,
                          no_ack=True)
    channel.start_consuming()


if __name__ == '__main__':
    get_info_from_ctp_queue()
