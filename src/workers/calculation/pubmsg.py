#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@date: 2017-07-07

@author: Devin
"""
import json

import pika

from settings import mq, logger


def pub(msg):
    _conf = mq.get("pub")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=_conf.get("host")))
    channel = connection.channel()

    channel.exchange_declare(exchange=_conf.get("exchange"),
                             type=_conf.get("exchange_type"))

    channel.basic_publish(exchange=_conf.get("exchange"),
                          routing_key=_conf.get("routing_key"),
                          body=msg)

    connection.close()
