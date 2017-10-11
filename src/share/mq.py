# -- coding: utf-8 --
import os
import logging
import pika
import sys
from share.settings.defaults import get_env


cur_env = get_env()
connection = pika.BlockingConnection(pika.ConnectionParameters(cur_env["MQ_HOST"]))

channel = connection.channel()

# 声明所需所有队列
channel.queue_declare(queue='hello')
