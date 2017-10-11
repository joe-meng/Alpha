#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@date: 2017-07-06

@author: Devin
"""
import logging.config
import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOGGER_DIR = os.path.normpath(
    os.path.join(BASE_DIR, "../../../logs/workers/calculation"))
if not os.path.exists(LOGGER_DIR):
    os.makedirs(LOGGER_DIR)



LOGGING_DICT = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '[%(lineno)d]: %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGGER_DIR, 'calculation_info.log'),
            'backupCount': 5,
            'maxBytes': 50 * 1024 * 1024,
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGGER_DIR, 'calculation_error.log'),
            'backupCount': 5,
            'maxBytes': 50 * 1024 * 1024,
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'calculationlog': {
            'handlers': ['file', 'error_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
    'root': {'handlers': ['console'],
             'level': 'INFO',
             'propagate': True}
}

logging.config.dictConfig(LOGGING_DICT)
logger = logging.getLogger("calculationlog")


SHARE_LIB = os.path.normpath(os.path.join(BASE_DIR, "../../"))
sys.path.append(SHARE_LIB)
from share import conf as share_conf
from share.data import ref_ship
from share.formula.executor import WorkerFormulaExecutor, ShareFormula

mysql = {'host': share_conf.mysql["host"],
         'port': share_conf.mysql["port"],
         'user': share_conf.mysql["user"],
         'password': share_conf.mysql["password"],
         'db': share_conf.mysql["db"],
         'charset': share_conf.mysql["charset"],
         'timeout': share_conf.mysql["timeout"],}


mq = {"sub": {'host': share_conf.mq["host"],
              'exchange': 'useonline.alpha.analysis',
              'exchange_type': 'topic',
              'routing_key': 'preprocess',
              'queue': 'queue.preprocess_done'},

      "pub": {'host': share_conf.mq["host"],
              'exchange': 'useonline.alpha.analysis',
              'exchange_type': 'topic',
              'routing_key': 'calculation'}
      }
