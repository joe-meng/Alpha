# -- coding: utf-8 --
import sys
sys.path.append("../..")


from share.mq import channel, connection, cur_env

def send_message_to_ready_queue(message):
    channel.exchange_declare(exchange='useonline.alpha.analysis',
                             exchange_type='topic')

    channel.basic_publish(exchange='useonline.alpha.analysis',
                          routing_key='preprocess',
                          body=message)
    print(" [x] Sent %r:%r" % ('preprocess', message))
    # connection.close()



def send_tcp_info():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=cur_env["MQ_HOST"]))
    channel = connection.channel()

    channel.exchange_declare(exchange='useonline.alpha.analysis',
                             exchange_type='topic')

    message = "sn1705,SHFE,Min1,2017-07-03 00:00:00,6365,6401,6303,6369,341954,2179956750,586488,6379,6405"
    channel.basic_publish(exchange='useonline.alpha.analysis',
                          routing_key='ctp',
                          body=message)
    print(" [x] Sent %r:%r" % ('ctp', message))
    connection.close()
