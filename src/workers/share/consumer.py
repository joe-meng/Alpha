# coding: utf-8
import time
import pika
import logging

from .handler import Handler


class ConsumerConf(object):
    """消费者配置类"""
    host = None
    exchange = None
    exchange_type = None
    routing_key = None
    queue = None

    def __init__(self, host=None, exchange=None, exchange_type=None, routing_key=None, queue=None):
        self.host = host
        self.exchange = exchange
        self.exchange_type = exchange_type
        self.routing_key = routing_key
        self.queue = queue


class ABCConsumer(object):
    """消费者抽象类，子类实现run方法"""
    handler = Handler()
    conf = ConsumerConf()

    def __init__(self, conf):
        self.conf = conf

    def on_message(self, channel, method_frame, header_frame, body):
        logging.info('message arrive: %s' % body)
        try:
            self.handler.do_handle(body)
        except Exception as e:
            logging.error(str(e))
        finally:
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)

    def set_handler(self, handler):
        self.handler = handler

    def set_conf(self, conf):
        self.conf = conf

    def run(self):
        raise NotImplemented


class SyncConsumer(ABCConsumer):
    """同步消费者"""

    def __init__(self, conf):
        super(SyncConsumer, self).__init__(conf)
        self._channel = None
        self._connection = None

    @property
    def channel(self):
        if not self._channel:
            self._channel = self.connection.channel()
            self._channel.exchange_declare(self.conf.exchange, type=self.conf.exchange_type)
            self._channel.queue_declare(self.conf.queue)
            self._channel.queue_bind(exchange=self.conf.exchange,
                                     routing_key=self.conf.routing_key,
                                     queue=self.conf.queue)
        return self._channel

    @property
    def connection(self):
        if not self._connection:
            connection = pika.BlockingConnection(pika.ConnectionParameters(self.conf.host))
            self._connection = connection
        return self._connection

    def run(self):
        logging.info('sync consumer...')
        while True:
            try:
                logging.info('start consuming...')
                self.channel.basic_consume(self.on_message, self.conf.queue)
                self.channel.start_consuming()
            except pika.exceptions.ConnectionClosed:
                logging.info('lost connection...')
                logging.info('reconnect 5 seconds later...')
                self._channel = None
                self._connection = None
                time.sleep(5)
            except KeyboardInterrupt:
                logging.info('stop consuming...')
                self.channel.stop_consuming()
                self.channel.close()
                self.connection.close()
                break
            except Exception as e:
                logging.error(str(e))
                time.sleep(1)
            finally:
                pass


class AsyncConsumer(ABCConsumer):
    """异步消费者"""

    def __init__(self, conf):
        super(AsyncConsumer, self).__init__(conf)
        self._consumer_tag = None
        self._closing = False
        self._channel = None
        self._connection = None

    @property
    def connection(self):
        if not self._connection:
            connection = pika.SelectConnection(pika.ConnectionParameters(self.conf.host),
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
            logging.info('lost connection...')
            logging.info('reconnect 5 seconds later...')
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
                                       self.conf.exchange,
                                       self.conf.exchange_type)

    def on_channel_closed(self, channel, reply_code, reply_text):
        self.connection.close()

    def on_exchange_declare_ok(self, unused_frame):
        self._channel.queue_declare(self.on_queue_declare_ok,
                                    self.conf.queue)

    def on_queue_declare_ok(self, method_frame):
        self._channel.queue_bind(self.on_bind_ok,
                                 self.conf.queue,
                                 self.conf.exchange,
                                 self.conf.routing_key)

    def on_bind_ok(self, unused_frame):
        self.start_consuming()

    def start_consuming(self):
        self._channel.add_on_cancel_callback(self.on_consumer_cancelled)
        logging.info('start consuming...')
        self._consumer_tag = self._channel.basic_consume(self.on_message,
                                                         self.conf.queue)

    def on_consumer_cancelled(self, method_frame):
        if self._channel:
            self._channel.close()

    def stop_consuming(self):
        logging.info('stop consuming...')
        self._closing = True
        self._channel.basic_cancel(self.on_cancel_ok, self._consumer_tag)
        self.connection.ioloop.stop()

    def on_cancel_ok(self, unused_frame):
        self._channel.close()

    def run(self):
        logging.info('async consumer...')
        while True:
            try:
                self.connection.ioloop.start()
            except pika.exceptions.AMQPConnectionError:
                logging.info('connection error...')
                logging.info('reconnect 30 seconds later...')
                self._connection = None
                time.sleep(30)
            except KeyboardInterrupt:
                self.stop_consuming()
                break
            except Exception as e:
                logging.error('handle message error:%s', str(e))
                time.sleep(1)
            finally:
                pass
