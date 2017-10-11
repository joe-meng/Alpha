# coding: utf-8
import click
import os
import sys

alert_path = os.path.dirname(os.path.abspath(__file__))
workers_path = os.path.dirname(alert_path)
src_path = os.path.dirname(workers_path)
if src_path not in sys.path:
    sys.path.append(src_path)

import conf
from viewer import AlertMessage
from share.contrib import import_string
from workers.share.handler import Handler
from workers.share.consumer import SyncConsumer, AsyncConsumer


consumer_cls_dict = {'sync': SyncConsumer, 'async': AsyncConsumer}


@click.group()
def cli():
    pass


@cli.command()
@click.option('--mode', '-m',
              default='sync', type=click.Choice(consumer_cls_dict.keys()),
              help='选择同步方式(sync)还是异步方式(async)启动服务')
def runserver(mode):
    handler = Handler()
    handler.set_msg_class(AlertMessage)
    for f in conf.ALERT_FILTERS:
        f_cls = import_string(f)
        handler.add_filter(f_cls())
    for v in conf.ALERT_VIEWERS:
        v_cls = import_string(v)
        handler.add_viewer(v_cls())
    consumer_cls = consumer_cls_dict[mode]
    consumer = consumer_cls(conf.consumer_conf)
    consumer.set_handler(handler)
    consumer.run()


if __name__ == '__main__':
    runserver()
