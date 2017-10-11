# -- coding: utf-8 --

from src.share.mq import channel


def calculation(ch, method, properties, body):
    ch.basic_ack(delivery_tag=method.delivery_tag)


while 1:
    channel.basic_consume(calculation, queue='hello')

