# coding: utf-8
import logging


class AlphaLoggerHandler(logging.Handler):

    def emit(self, record):
        # send record to ELK system
        pass


logging.root.name = 'alpha'
logger = logging.getLogger()
logger.addHandler(AlphaLoggerHandler())
