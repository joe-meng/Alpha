#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import traceback

import pika

from settings import mq, logger
from handler import CalcMessageHandler
from lib.datalib.dbdata import prehandle_data
from lib.vo import PreProcessMessage


class CalcServer(object):
    _connection = None
    _channel = None
    _conf = mq.get("sub")

    def __init__(self):
        self.handler = CalcMessageHandler()

    def on_message(self, channel, method_frame, header_frame, body):
        logger.info('message arrive: %s' % body)
        try:
            msg = PreProcessMessage(body)
            with prehandle_data(msg.varieties) as pre_data:
                self.handler.do_handle(pre_data)
        except Exception as e:
            logger.error("处理消息获得异常:%s", traceback.format_exc())
        finally:
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)


class SyncCalcServer(CalcServer):
    @property
    def channel(self):
        if not self._channel:
            self._channel = self.connection.channel()
            self._channel.exchange_declare(self._conf.get('exchange'),
                                           type=self._conf.get(
                                               'exchange_type'))
            self._channel.queue_declare(self._conf.get('queue'), exclusive=True)
            self._channel.queue_bind(exchange=self._conf.get('exchange'),
                                     routing_key=self._conf.get('routing_key'),
                                     queue=self._conf.get('queue'))
        return self._channel

    @property
    def connection(self):
        if not self._connection:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(self._conf.get('host')))
            self._connection = connection
        return self._connection

    def run(self):
        logger.debug('sync consumer...')
        while True:
            try:
                logger.info('start consuming...')
                self.channel.basic_consume(self.on_message,
                                           self._conf.get('queue'))
                self.channel.start_consuming()
            except pika.exceptions.ConnectionClosed:
                logger.error('lost connection...')
                logger.error('reconnect 5 seconds later...')
                self._channel = None
                self._connection = None
                time.sleep(5)
            except KeyboardInterrupt:
                logger.error('stop consuming...')
                self.channel.stop_consuming()
                self.channel.close()
                self.connection.close()
                break
            except Exception as e:
                logger.error(str(e))
                time.sleep(1)
            finally:
                pass


class AsyncCalcServer(CalcServer):
    _consumer_tag = None
    _closing = False

    @property
    def connection(self):
        if not self._connection:
            connection = pika.SelectConnection(
                pika.ConnectionParameters(self._conf.get('host')),
                self.on_connection_open,
                stop_ioloop_on_close=False)
            self._connection = connection
        return self._connection

    def on_connection_open(self, unused_connection):
        self.connection.add_on_close_callback(self.on_connection_closed)
        self.connection.channel(on_open_callback=self.on_channel_open)

    def on_connection_closed(self, connection, reply_code, reply_text):
        self._channel = None
        if self._closing:
            self.connection.ioloop.stop()
        else:
            logger.error('lost connection...')
            logger.error('reconnect 5 seconds later...')
            self.connection.add_timeout(5, self.reconnect)

    def reconnect(self):
        self.connection.ioloop.stop()
        if not self._closing:
            self._connection = None
            self.connection.ioloop.start()

    def on_channel_open(self, channel):
        self._channel = channel
        self._channel.add_on_close_callback(self.on_channel_closed)
        self._channel.exchange_declare(self.on_exchange_declare_ok,
                                       self._conf.get('exchange'),
                                       self._conf.get('exchange_type'))

    def on_channel_closed(self, channel, reply_code, reply_text):
        self.connection.close()

    def on_exchange_declare_ok(self, unused_frame):
        self._channel.queue_declare(self.on_queue_declare_ok,
                                    self._conf.get('queue'))

    def on_queue_declare_ok(self, method_frame):
        self._channel.queue_bind(self.on_bind_ok,
                                 self._conf.get('queue'),
                                 self._conf.get('exchange'),
                                 self._conf.get('routing_key'))

    def on_bind_ok(self, unused_frame):
        self.start_consuming()

    def start_consuming(self):
        self._channel.add_on_cancel_callback(self.on_consumer_cancelled)
        logger.info('start consuming...')
        self._consumer_tag = self._channel.basic_consume(self.on_message,
                                                         self._conf.get(
                                                             'queue'))

    def on_consumer_cancelled(self, method_frame):
        if self._channel:
            self._channel.close()

    def stop_consuming(self):
        logger.info('stop consuming...')
        self._closing = True
        self._channel.basic_cancel(self.on_cancel_ok, self._consumer_tag)
        self.connection.ioloop.stop()

    def on_cancel_ok(self, unused_frame):
        self._channel.close()

    def run(self):
        logger.info('async consumer...')
        try:
            self.connection.ioloop.start()
        except KeyboardInterrupt:
            self.stop_consuming()
        finally:
            pass
